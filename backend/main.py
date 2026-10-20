import os
import sys
import time

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Đảm bảo thư mục backend luôn nằm trong sys.path để import database thành công từ mọi nơi
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
import pymysql
import uvicorn
import uuid
import re
import httpx
from typing import Optional, List, Union

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- BỘ GHI LOG CHI TIẾT LỖI 422 (HỖ TRỢ DEBUG CỰC NHANH) ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("\n" + "="*50)
    print(">>> [LỖI ĐỊNH DẠNG 422 - UNPROCESSABLE CONTENT] <<<")
    print("Dữ liệu gửi từ Flutter lên không khớp với cấu trúc Schema của Backend!")
    for error in exc.errors():
        # Lấy tên trường bị lỗi
        field_path = " -> ".join([str(loc) for loc in error['loc']])
        print(f"❌ Lỗi tại trường: '{field_path}'")
        print(f"   - Chi tiết: {error['msg']}")
        print(f"   - Kiểu lỗi: {error['type']}")
    print("Payload thực tế nhận được:")
    print(exc.body)
    print("="*50 + "\n")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

# --- CẤU HÌNH LƯU TRỮ FILE TĨNH ---
UPLOAD_DIR = os.path.join(CURRENT_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Cấu hình mở cổng truy cập các file tĩnh (bao gồm ảnh bìa sách, pdf, mp3, avatar, và ảnh bài đăng...)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


from database import get_connection, init_db

# --- MODEL DATA (PYDANTIC) ---
class UserAuth(BaseModel):
    username: str
    password: str

class UserRegisterInput(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

# Model hỗ trợ toggle bookmark (Hỗ trợ cả trang PDF/EPUB và mốc thời gian Audio)
class BookmarkInput(BaseModel):
    username: str
    book_id: int
    page_number: Optional[int] = 0
    audio_position_ms: Optional[int] = 0
    note: Optional[str] = ""  # Nhận nội dung ghi chú từ Flutter gửi lên

# Model hỗ trợ quên/đặt lại mật khẩu
class ForgotPasswordInput(BaseModel):
    username: str
    new_password: str


# --- [TỐI ƯU HÓA] MODEL CHO HỆ THỐNG ĐƠN HÀNG (TRÁNH LỖI 422) ---
class OrderItemInput(BaseModel):
    book_id: int
    quantity: int
    price: float

    # Tự động chuyển đổi nếu Flutter gửi nhầm dạng chuỗi (String)
    @field_validator('book_id', mode='before')
    def parse_book_id(cls, v):
        if isinstance(v, (str, float)):
            return int(float(v))
        return v

    @field_validator('quantity', mode='before')
    def parse_quantity(cls, v):
        if isinstance(v, (str, float)):
            return int(float(v))
        return v

    @field_validator('price', mode='before')
    def parse_price(cls, v):
        if isinstance(v, str):
            return float(v.replace(',', '').strip())
        return v

class CheckoutInput(BaseModel):
    username: str
    full_name: str
    phone: str
    address: str
    total_amount: float
    items: List[OrderItemInput]

    # Tự động ép kiểu total_amount về float nếu Flutter gửi sang dạng String
    @field_validator('total_amount', mode='before')
    def parse_total_amount(cls, v):
        if isinstance(v, str):
            return float(v.replace(',', '').strip())
        return v

class UpdateOrderStatusInput(BaseModel):
    order_id: int
    status: str  # pending, shipping, completed, cancelled

class ReadingProgressInput(BaseModel):
    username: str
    book_id: int
    last_page: Optional[int] = 0
    last_epub_cfi: Optional[str] = ""
    last_audio_position_ms: Optional[int] = 0
    progress_percent: Optional[float] = 0.0

class ReviewInput(BaseModel):
    book_id: int
    username: str
    rating: int
    comment: Optional[str] = ""

class OnlineBookImportInput(BaseModel):
    username: str
    title: str
    author: Optional[str] = "Nhiều tác giả"
    content: Optional[str] = ""
    description: Optional[str] = ""
    category: Optional[str] = "Văn học & Tiểu thuyết"
    image_url: Optional[str] = ""
    pdf_url: Optional[str] = ""
    audio_url: Optional[str] = ""
    source: Optional[str] = "Project Gutenberg & LibriVox"
    external_id: Optional[str] = ""
    rating_avg: Optional[float] = 4.8
    review_count: Optional[int] = 25

# --- 1. KHỞI TẠO & TỰ ĐỘNG CẬP NHẬT DATABASE ---
# init_db is handled by database.py
init_db()


# --- 2. CÁC API HỆ THỐNG ---

# API Kiểm tra trạng thái máy chủ (Healthcheck / Ping)
@app.get("/api/ping")
def ping():
    return {
        "status": "ok",
        "message": "BookHub Backend is online",
        "timestamp": int(time.time())
    }

# API Proxy tải file tránh lỗi CORS trên Web Browser (hỗ trợ EPUB từ Gutenberg & Audiobook MP3 từ LibriVox)
@app.get("/api/proxy-file")
async def proxy_file(url: str, request: Request):
    if not url or not url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL không hợp lệ!")
    
    # 0. Chuẩn hóa URL (bỏ www. khỏi archive.org để tránh lỗi timeout mạng)
    clean_url = url.replace("www.archive.org", "archive.org")

    is_audio = any(ext in clean_url.lower() for ext in [".mp3", ".m4a", ".wav", ".ogg", "librivox"]) or "audio" in clean_url.lower()
    is_pdf = clean_url.lower().endswith(".pdf") or "pdf" in clean_url.lower()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BookHub/2026 Media-Proxy",
        "Accept": "audio/*, application/epub+zip, application/octet-stream, */*",
    }

    # Chuyển tiếp Range header từ trình duyệt/client nếu có (cần thiết cho audio stream và seek)
    client_range = request.headers.get("range")
    if client_range:
        headers["Range"] = client_range

    candidate_urls = [clean_url]
    gutenberg_match = re.search(r"gutenberg\.org/(?:ebooks/|cache/epub/)?(\d+)", clean_url)
    if gutenberg_match:
        g_id = gutenberg_match.group(1)
        candidate_urls.insert(0, f"https://www.gutenberg.org/cache/epub/{g_id}/pg{g_id}.epub")
        candidate_urls.append(f"https://www.gutenberg.org/ebooks/{g_id}.epub3.images")
        candidate_urls.append(f"https://www.gutenberg.org/ebooks/{g_id}.epub.noimages")

    seen = set()
    unique_candidates = []
    for c in candidate_urls:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)

    # Thử tải từ xa (timeout ngắn 8s cho audio để tránh làm đơ ứng dụng)
    fetch_timeout = 8.0 if is_audio else 20.0
    for target in unique_candidates:
        try:
            async with httpx.AsyncClient(
                timeout=fetch_timeout,
                follow_redirects=True,
                headers=headers,
                verify=False
            ) as client:
                resp = await client.get(target)
                if resp.status_code in [200, 206] and len(resp.content) > 500:
                    c_type = "audio/mpeg" if is_audio else resp.headers.get("content-type", "application/epub+zip")
                    resp_headers = {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Accept-Ranges": "bytes",
                        "Content-Disposition": "inline",
                    }
                    if "content-range" in resp.headers:
                        resp_headers["Content-Range"] = resp.headers["content-range"]
                    return Response(
                        content=resp.content,
                        status_code=resp.status_code,
                        media_type=c_type,
                        headers=resp_headers
                    )
        except Exception as err:
            print(f">>> Thử tải {target} không thành công: {err}")
            continue

    # 3. Fallback: Nếu không tải được từ xa, phục vụ tệp fallback nội bộ tương ứng
    try:
        if is_audio:
            # Fallback audio: audio_sample_1.mp3
            fallback_filename = "audio_sample_1.mp3"
            fallback_path = os.path.join(UPLOAD_DIR, fallback_filename)
            if os.path.exists(fallback_path):
                file_size = os.path.getsize(fallback_path)
                with open(fallback_path, "rb") as f:
                    if client_range and client_range.startswith("bytes="):
                        range_val = client_range.replace("bytes=", "").split("-")
                        start = int(range_val[0]) if range_val[0] else 0
                        end = int(range_val[1]) if len(range_val) > 1 and range_val[1] else file_size - 1
                        if end >= file_size:
                            end = file_size - 1
                        length = end - start + 1
                        f.seek(start)
                        chunk = f.read(length)
                        return Response(
                            content=chunk,
                            status_code=206,
                            media_type="audio/mpeg",
                            headers={
                                "Content-Range": f"bytes {start}-{end}/{file_size}",
                                "Accept-Ranges": "bytes",
                                "Content-Length": str(length),
                                "Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Methods": "*",
                                "Access-Control-Allow-Headers": "*",
                            }
                        )
                    else:
                        audio_data = f.read()
                        return Response(
                            content=audio_data,
                            media_type="audio/mpeg",
                            headers={
                                "Accept-Ranges": "bytes",
                                "Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Methods": "*",
                                "Access-Control-Allow-Headers": "*",
                            }
                        )
        else:
            fallback_filename = "dac_nhan_tam.pdf" if is_pdf else "nha_gia_kim.epub"
            fallback_path = os.path.join(UPLOAD_DIR, fallback_filename)
            if os.path.exists(fallback_path):
                with open(fallback_path, "rb") as f:
                    fallback_data = f.read()
                c_type = "application/pdf" if is_pdf else "application/epub+zip"
                return Response(
                    content=fallback_data,
                    media_type=c_type,
                    headers={
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Content-Disposition": "inline",
                    }
                )
    except Exception as e:
        print(f">>> Lỗi khi đọc file fallback: {e}")

    raise HTTPException(status_code=404, detail="Không thể tải tệp sách sau khi thử tất cả các nguồn.")

# API Đăng ký tài khoản người dùng chi tiết
@app.post("/api/register")
def register(user: UserRegisterInput):
    username = user.username.strip()
    password = user.password.strip()
    full_name = (user.full_name or "").strip()
    email = (user.email or "").strip().lower()
    phone = (user.phone or "").strip()

    if not username or not password:
        raise HTTPException(status_code=400, detail="Vui lòng điền đầy đủ tên đăng nhập và mật khẩu!")
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Tên đăng nhập phải chứa ít nhất 3 ký tự!")
    if " " in username:
        raise HTTPException(status_code=400, detail="Tên đăng nhập không được chứa khoảng trắng!")
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Mật khẩu phải chứa ít nhất 6 ký tự để đảm bảo bảo mật!")

    # Kiểm tra định dạng email nếu người dùng cung cấp
    if email:
        email_regex = r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$"
        if not re.match(email_regex, email):
            raise HTTPException(status_code=400, detail="Địa chỉ email không đúng định dạng hợp lệ!")

    # Kiểm tra số điện thoại nếu người dùng cung cấp
    if phone:
        phone_cleaned = re.sub(r"\D", "", phone)
        if len(phone_cleaned) < 9 or len(phone_cleaned) > 11:
            raise HTTPException(status_code=400, detail="Số điện thoại phải từ 9 đến 11 chữ số!")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Kiểm tra username đã tồn tại chưa
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail=f"Tên tài khoản '{username}' đã tồn tại! Vui lòng chọn tên khác.")

        # Kiểm tra email đã được đăng ký chưa nếu có email
        if email:
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail=f"Địa chỉ email '{email}' đã được liên kết với một tài khoản khác!")

        display_name = full_name if full_name else username
        cursor.execute(
            "INSERT INTO users (username, password, is_admin, full_name, email, phone) VALUES (%s, %s, 0, %s, %s, %s)",
            (username, password, display_name, email if email else None, phone if phone else None)
        )
        return {
            "status": "success",
            "message": f"Đăng ký tài khoản thành công! Chào mừng {display_name}.",
            "username": username,
            "full_name": display_name
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Lỗi đăng ký: {e}")
        raise HTTPException(status_code=400, detail=f"Lỗi đăng ký: {str(e)}")
    finally:
        conn.close()

# API Đăng nhập
@app.post("/api/login")
def login(user: UserAuth):
    username = user.username.strip()
    password = user.password.strip()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, is_admin, full_name, avatar_url FROM users WHERE username = %s AND password = %s",
        (username, password)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        is_admin_bool = True if row['is_admin'] == 1 else False
        return {
            "status": "success",
            "message": "Đăng nhập thành công",
            "username": row['username'],
            "is_admin": is_admin_bool,
            "full_name": row['full_name'] if row['full_name'] else row['username'],
            "avatar_url": row['avatar_url'] if row['avatar_url'] else ""
        }
    else:
        raise HTTPException(status_code=401, detail="Sai tài khoản hoặc mật khẩu")


# --- API QUÊN / ĐẶT LẠI MẬT KHẨU (MODULE 1) ---
@app.post("/api/auth/forgot-password")
def forgot_password(data: ForgotPasswordInput):
    username = data.username.strip()
    new_password = data.new_password.strip()

    if not username or not new_password:
        raise HTTPException(status_code=400, detail="Tên đăng nhập và mật khẩu mới không được để trống!")
    if len(new_password) < 3:
        raise HTTPException(status_code=400, detail="Mật khẩu mới phải có ít nhất 3 ký tự!")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản với tên đăng nhập này!")

        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
        return {"status": "success", "message": "Đặt lại mật khẩu thành công! Bạn có thể đăng nhập ngay."}
    finally:
        conn.close()


# --- API CẬP NHẬT THÔNG TIN CÁ NHÂN (HỌ TÊN & AVATAR VẬT LÝ) ---
@app.post("/api/user/update_profile")
async def update_profile(
    username: str = Form(...),
    full_name: str = Form(...),
    avatar_file: UploadFile = File(None)
):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, avatar_url FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            conn.close()
            raise HTTPException(status_code=404, detail="Không tìm thấy người dùng này!")

        new_avatar_url = user['avatar_url']
        if avatar_file and avatar_file.filename:
            ext = os.path.splitext(avatar_file.filename)[1].lower()
            safe_filename = f"avatar_{user['id']}_{int(time.time())}{ext}"
            file_path = os.path.join(UPLOAD_DIR, safe_filename)

            with open(file_path, "wb") as buffer:
                buffer.write(avatar_file.file.read())

            new_avatar_url = f"http://10.0.2.2:8000/uploads/{safe_filename}"

            if user['avatar_url'] and "/uploads/avatar_" in user['avatar_url']:
                try:
                    old_filename = user['avatar_url'].split("/uploads/")[-1]
                    old_file_path = os.path.join(UPLOAD_DIR, old_filename)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                except Exception as file_err:
                    print(f">>> Cảnh báo lỗi xóa avatar cũ: {file_err}")

        cursor.execute(
            "UPDATE users SET full_name = %s, avatar_url = %s WHERE username = %s",
            (full_name, new_avatar_url, username)
        )
        conn.close()

        return {
            "status": "success",
            "message": "Cập nhật hồ sơ cá nhân thành công!",
            "full_name": full_name,
            "avatar_url": new_avatar_url
        }

    except Exception as e:
        if conn:
            conn.close()
        print(">>> LỖI CẬP NHẬT PROFILE:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


# API Lấy danh sách tất cả các sách (Để đọc/nghe, hỗ trợ lọc theo thể loại và từ khóa)
@app.get("/api/books")
def get_all_books(category: Optional[str] = None, search: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM books"
    params = []
    conditions = []
    if category and category.strip() and category != "Tất cả":
        conditions.append("category = %s")
        params.append(category.strip())
    if search and search.strip():
        conditions.append("(title LIKE %s OR author LIKE %s)")
        q = f"%{search.strip()}%"
        params.extend([q, q])
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY CASE WHEN source = N'Kho Sách Việt Nam Tinh Hoa' OR pdf_url LIKE 'uploads/vn_book_%' OR audio_url LIKE 'uploads/vn_book_%' OR id IN (1,2,3,4) THEN 0 ELSE 1 END, id DESC"
    cursor.execute(sql, tuple(params) if params else None)
    books = cursor.fetchall()
    for b in books:
        if 'rating_avg' in b and b['rating_avg'] is not None:
            b['rating_avg'] = float(b['rating_avg'])
    conn.close()
    return books


# API Lấy chi tiết cuốn sách kèm nội dung và danh sách chương
@app.get("/api/books/{book_id}")
def get_book_detail(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    conn.close()
    if not book:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuốn sách này!")
    if 'rating_avg' in book and book['rating_avg'] is not None:
        book['rating_avg'] = float(book['rating_avg'])
    
    # Phân tích danh sách chương từ content nếu có cấu trúc === Chương X ===
    raw_content = book.get('content') or ''
    chapters = []
    if "===" in raw_content:
        matches = re.findall(r'===\s*([^=]+)\s*===\n(.*?)(?====\s*[^=]+\s*===|$)', raw_content, re.DOTALL)
        for idx, (ch_title, ch_text) in enumerate(matches, 1):
            clean_text = re.sub(r'<[^>]+>', '', ch_text).strip()
            chapters.append({
                "id": idx,
                "title": ch_title.strip(),
                "content": clean_text,
                "order": idx
            })
    if not chapters and raw_content:
        clean_text = re.sub(r'<[^>]+>', '', raw_content).strip()
        chapters.append({
            "id": 1,
            "title": "Chương 1: Toàn văn tác phẩm",
            "content": clean_text,
            "order": 1
        })
    book['chapters'] = chapters
    return book


# API Text-To-Speech (Phát âm tiếng Việt trực tiếp sử dụng neural TTS)
@app.get("/api/tts/speak")
async def tts_speak(text: str, voice: Optional[str] = "vi-VN-HoaiMyNeural"):
    clean_text = text.strip()
    if not clean_text:
        raise HTTPException(status_code=400, detail="Văn bản không được để trống!")
    if len(clean_text) > 3000:
        clean_text = clean_text[:3000]
    
    import edge_tts
    import io
    try:
        communicate = edge_tts.Communicate(clean_text, voice=voice)
        audio_stream = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])
        audio_bytes = audio_stream.getvalue()
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Disposition": "inline; filename=speech.mp3",
                "Cache-Control": "public, max-age=86400"
            }
        )
    except Exception as e:
        print(f">>> Lỗi TTS: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi tạo giọng đọc TTS: {str(e)}")


# API Lấy hoặc sinh tự động file Audio thuyết minh đọc nội dung cho từng chương sách
@app.get("/api/books/{book_id}/chapters/{chapter_index}/audio")
async def get_chapter_audio(book_id: int, chapter_index: int, request: Request, voice: Optional[str] = "vi-VN-HoaiMyNeural"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, content FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    conn.close()

    if not book:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuốn sách này!")

    raw_content = book.get('content') or ''
    chapters = []
    if "===" in raw_content:
        matches = re.findall(r'===\s*([^=]+)\s*===\n(.*?)(?====\s*[^=]+\s*===|$)', raw_content, re.DOTALL)
        for idx, (ch_title, ch_text) in enumerate(matches, 1):
            clean_text = re.sub(r'<[^>]+>', '', ch_text).strip()
            chapters.append({
                "id": idx,
                "title": ch_title.strip(),
                "content": clean_text
            })
    if not chapters and raw_content:
        chapters.append({
            "id": 1,
            "title": "Toàn văn tác phẩm",
            "content": re.sub(r'<[^>]+>', '', raw_content).strip()
        })

    if chapter_index < 1 or chapter_index > len(chapters):
        raise HTTPException(status_code=404, detail="Không tìm thấy chương yêu cầu!")

    target_chapter = chapters[chapter_index - 1]
    ch_text = target_chapter['content']
    ch_title = target_chapter['title']

    safe_voice = "hoaimy" if "HoaiMy" in (voice or "") else "namminh"
    cache_filename = f"audio_book_{book_id}_chap_{chapter_index}_{safe_voice}.mp3"
    cache_path = os.path.join(UPLOAD_DIR, cache_filename)

    if not os.path.exists(cache_path) or os.path.getsize(cache_path) < 2000:
        import edge_tts
        chosen_voice = voice or "vi-VN-HoaiMyNeural"
        speech_text = f"Tác phẩm {book['title']}. {ch_title}. {ch_text}"
        if len(speech_text) > 4500:
            speech_text = speech_text[:4500]
        try:
            communicate = edge_tts.Communicate(speech_text, voice=chosen_voice)
            await communicate.save(cache_path)
        except Exception as e:
            print(f">>> Lỗi tạo audio chương {chapter_index}: {e}")
            fallback_sample = os.path.join(UPLOAD_DIR, "audio_sample_1.mp3")
            if os.path.exists(fallback_sample):
                cache_path = fallback_sample

    file_size = os.path.getsize(cache_path)
    client_range = request.headers.get("range")
    if client_range and client_range.startswith("bytes="):
        range_val = client_range.replace("bytes=", "").split("-")
        start = int(range_val[0]) if range_val[0] else 0
        end = int(range_val[1]) if len(range_val) > 1 and range_val[1] else file_size - 1
        if end >= file_size:
            end = file_size - 1
        length = end - start + 1
        with open(cache_path, "rb") as f:
            f.seek(start)
            chunk = f.read(length)
        return Response(
            content=chunk,
            status_code=206,
            media_type="audio/mpeg",
            headers={
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Accept-Ranges": "bytes",
                "Content-Length": str(length),
                "Access-Control-Allow-Origin": "*",
            }
        )
    else:
        with open(cache_path, "rb") as f:
            audio_bytes = f.read()
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Accept-Ranges": "bytes",
                "Content-Length": str(file_size),
                "Access-Control-Allow-Origin": "*",
                "Content-Disposition": f"inline; filename={cache_filename}",
            }
        )


# API Lấy danh mục thể loại và số lượng sách tương ứng
@app.get("/api/categories")
def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, COUNT(*) as count FROM books GROUP BY category ORDER BY count DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


# API TÌM KIẾM SÁCH ONLINE TỪ GUTENDEX, LIBRIVOX & OPEN LIBRARY
@app.get("/api/admin/online-books/search")
async def search_online_books_api(query: str = "", source: str = "all", page: int = 1):
    from online_books import search_all_sources
    results = await search_all_sources(query=query, source=source, page=page)
    return results


# API ADMIN: TẢI / NHẬP SÁCH TRỰC TIẾP TỪ NGUỒN ONLINE VÀO KHO HỆ THỐNG
@app.post("/api/admin/online-books/import")
def import_online_book_api(data: OnlineBookImportInput):
    from online_books import import_single_book
    try:
        res = import_single_book(data.dict(), admin_username=data.username)
        return res
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi nhập sách: {str(e)}")



# API ADMIN: Thêm sách và Tải tệp tin vật lý (Đọc/Nghe)
@app.post("/api/admin/add_book")
async def add_book(
    username: str = Form(...),
    title: str = Form(...),
    author: str = Form(...),
    image_file: UploadFile = File(...),
    pdf_file: UploadFile = File(None),
    audio_file: UploadFile = File(None)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (username,))
    admin = cursor.fetchone()

    if not admin or not admin['is_admin']:
        conn.close()
        raise HTTPException(status_code=403, detail="Không có quyền Admin!")

    def save_uploaded_file(upload_file: UploadFile) -> str:
        if not upload_file or not upload_file.filename:
            return ""
        ext = os.path.splitext(upload_file.filename)[1].lower()
        safe_filename = f"file_{int(time.time() * 1000)}{ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        with open(file_path, "wb") as buffer:
            buffer.write(upload_file.file.read())
        return f"http://10.0.2.2:8000/uploads/{safe_filename}"

    try:
        image_url = save_uploaded_file(image_file)
        pdf_url = save_uploaded_file(pdf_file) if pdf_file else ""
        audio_url = save_uploaded_file(audio_file) if audio_file else ""

        sql = """
            INSERT INTO books (title, author, image_url, pdf_url, audio_url)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (title, author, image_url, pdf_url, audio_url))
        conn.close()
        return {"status": "success", "message": "Tải tệp tin và lưu cơ sở dữ liệu thành công!"}

    except Exception as e:
        if conn:
            conn.close()
        print(">>> LỖI THỰC THI TRÊN SERVER:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


# API ADMIN XÓA SÁCH VÀ FILE VẬT LÝ (Đọc/Nghe)
@app.delete("/api/books/{book_id}")
def delete_book(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT image_url, pdf_url, audio_url FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()

        if not book:
            conn.close()
            raise HTTPException(status_code=404, detail="Không tìm thấy sách yêu cầu xóa trên hệ thống!")

        def delete_physical_file(file_url: str):
            if not file_url:
                return
            try:
                filename = file_url.split("/uploads/")[-1]
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as file_err:
                print(f">>> Lỗi dọn dẹp file vật lý: {file_err}")

        delete_physical_file(book.get('image_url', ''))
        delete_physical_file(book.get('pdf_url', ''))
        delete_physical_file(book.get('audio_url', ''))

        cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
        conn.close()
        return {"status": "success", "message": "Đã xóa sách thành công!"}

    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


# ===================================================================
# --- 2.5 CÁC API CHO KỆ SÁCH BÁN (SHOPPING SHOP) ĐỘC LẬP ---
# ===================================================================

# A. LẤY TOÀN BỘ SÁCH BÁN Ở KỆ SÁCH (GET /api/shop-books)
@app.get("/api/shop-books")
def get_shop_books():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM shop_books ORDER BY id DESC")
        books = cursor.fetchall()
        for book in books:
            book['price'] = float(book['price'])
        return books
    except Exception as e:
        print(">>> LỖI LẤY KỆ SÁCH BÁN:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()

# B. ĐĂNG BÁN SÁCH MỚI (POST /api/shop-books)
@app.post("/api/shop-books")
async def add_shop_book(
    title: str = Form(...),
    author: str = Form(...),
    price: float = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...)
):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        ext = os.path.splitext(file.filename)[1].lower()
        safe_filename = f"shop_book_{int(time.time() * 1000)}{ext}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        image_url = f"http://10.0.2.2:8000/uploads/{safe_filename}"

        sql = """
            INSERT INTO shop_books (title, author, price, image_path, description)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (title.strip(), author.strip(), price, image_url, description.strip()))
        conn.close()

        return {"status": "success", "message": "Đăng bán sách thành công!", "image_path": image_url}
    except Exception as e:
        if conn:
            conn.close()
        print(">>> LỖI ĐĂNG BÁN SÁCH GIAN HÀNG:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi máy chủ: {str(e)}")

# C. XÓA SÁCH KHỎI KỆ BÁN (DELETE /api/shop-books/{book_id})
@app.delete("/api/shop-books/{book_id}")
def delete_shop_book(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT image_path FROM shop_books WHERE id = %s", (book_id,))
        book = cursor.fetchone()

        if not book:
            conn.close()
            raise HTTPException(status_code=404, detail="Không tìm thấy sách bán để xóa!")

        image_path = book.get('image_path')
        if image_path:
            try:
                filename = image_path.split("/uploads/")[-1]
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as file_err:
                print(f">>> Lỗi dọn dẹp file ảnh bìa sách bán cũ: {file_err}")

        cursor.execute("DELETE FROM shop_books WHERE id = %s", (book_id,))
        conn.close()
        return {"status": "success", "message": "Đã xóa sách khỏi kệ bán thành công!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        if conn:
            conn.close()
        print(">>> LỖI XÓA SÁCH GIAN HÀNG:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi máy chủ: {str(e)}")


# ===================================================================
# --- HỆ THỐNG API QUẢN LÝ ĐƠN HÀNG (CHECKOUT) ---
# ===================================================================

# 1. API Đặt Hàng (POST /api/orders/checkout)
@app.post("/api/orders/checkout")
def checkout_order(data: CheckoutInput):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Lưu thông tin đơn hàng tổng quát
        order_sql = """
            INSERT INTO orders (username, full_name, phone, address, total_amount, status)
            VALUES (%s, %s, %s, %s, %s, 'pending')
        """
        cursor.execute(order_sql, (data.username, data.full_name, data.phone, data.address, data.total_amount))
        order_id = cursor.lastrowid

        # Lưu chi tiết từng cuốn sách được mua trong giỏ hàng
        for item in data.items:
            item_sql = """
                INSERT INTO order_items (order_id, book_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(item_sql, (order_id, item.book_id, item.quantity, item.price))

        return {
            "status": "success",
            "message": "Đặt hàng thành công!",
            "order_id": order_id
        }
    except Exception as e:
        print(">>> LỖI XỬ LÝ ĐẶT HÀNG:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()


# 2. API Lấy lịch sử đơn hàng của User (GET /api/orders/history/{username})
@app.get("/api/orders/history/{username}")
def get_user_order_history(username: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM orders WHERE username = %s ORDER BY id DESC", (username,))
        orders = cursor.fetchall()

        for order in orders:
            order['total_amount'] = float(order['total_amount'])

            # Kết bảng để lấy chi tiết sách đã mua trong đơn hàng này
            items_sql = """
                SELECT oi.*, sb.title, sb.image_path, sb.author
                FROM order_items oi
                JOIN shop_books sb ON oi.book_id = sb.id
                WHERE oi.order_id = %s
            """
            cursor.execute(items_sql, (order['id'],))
            items = cursor.fetchall()
            for item in items:
                item['price'] = float(item['price'])

            order['items'] = items

        return orders
    except Exception as e:
        print(">>> LỖI LẤY LỊCH SỬ ĐƠN HÀNG:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# 3. API Lấy toàn bộ đơn hàng (Dành cho Admin - GET /api/orders/admin/all)
@app.get("/api/orders/admin/all")
def get_all_orders_for_admin(current_user: str):
    if current_user.strip().lower() != "admin":
        raise HTTPException(status_code=403, detail="Chỉ có quản trị viên mới có quyền xem danh sách đơn hàng!")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM orders ORDER BY id DESC")
        orders = cursor.fetchall()

        for order in orders:
            order['total_amount'] = float(order['total_amount'])

            items_sql = """
                SELECT oi.*, sb.title, sb.image_path, sb.author
                FROM order_items oi
                JOIN shop_books sb ON oi.book_id = sb.id
                WHERE oi.order_id = %s
            """
            cursor.execute(items_sql, (order['id'],))
            items = cursor.fetchall()
            for item in items:
                item['price'] = float(item['price'])
            order['items'] = items

        return orders
    except Exception as e:
        print(">>> LỖI LẤY ĐƠN HÀNG ADMIN:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# 4. API Cập nhật trạng thái đơn hàng (Dành cho Admin - PUT /api/orders/admin/status)
@app.put("/api/orders/admin/status")
def update_order_status(data: UpdateOrderStatusInput, current_user: str):
    if current_user.strip().lower() != "admin":
        raise HTTPException(status_code=403, detail="Chỉ có quản trị viên mới có quyền cập nhật trạng thái đơn hàng!")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE orders SET status = %s WHERE id = %s",
            (data.status, data.order_id)
        )
        return {"status": "success", "message": f"Cập nhật trạng thái đơn sang '{data.status}' thành công!"}
    except Exception as e:
        print(">>> LỖI CẬP NHẬT TRẠNG THÁI ĐƠN HÀNG:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# ===================================================================
# --- CÁC API HỆ THỐNG KHÁC (ADMIN USERS, BOOKMARKS...) ---
# ===================================================================

@app.get("/api/admin/users")
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, username, is_admin, full_name, avatar_url FROM users ORDER BY id DESC")
        users = cursor.fetchall()
        for user in users:
            user['is_admin'] = True if user['is_admin'] == 1 else False
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()

@app.delete("/api/admin/users/{user_id}")
def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username, is_admin FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="Không tìm thấy người dùng này!")

        if user['username'] == 'admin':
            raise HTTPException(status_code=400, detail="Không thể xóa tài khoản Admin mặc định!")

        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        return {"status": "success", "message": f"Đã xóa tài khoản '{user['username']}' thành công!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()

@app.post("/api/bookmarks/toggle")
def toggle_bookmark(data: BookmarkInput):
    user_raw = data.username.strip()
    user_lower = user_raw.lower()

    if not user_lower or user_lower in ["guest", "anonymous", "null", "undefined"] or "khách" in user_lower or "khach" in user_lower:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản khách không có quyền sử dụng tính năng đánh dấu trang!"
        )

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (user_raw,))
        db_user = cursor.fetchone()
        if not db_user:
            raise HTTPException(
                status_code=403,
                detail="Tài khoản này không tồn tại trong hệ thống. Vui lòng đăng nhập!"
            )

        page_num = data.page_number or 0
        audio_pos = data.audio_position_ms or 0

        if audio_pos > 0:
            cursor.execute(
                "SELECT id FROM bookmarks WHERE username = %s AND book_id = %s AND ABS(ISNULL(audio_position_ms, 0) - %s) <= 2000",
                (user_raw, data.book_id, audio_pos)
            )
        else:
            cursor.execute(
                "SELECT id FROM bookmarks WHERE username = %s AND book_id = %s AND page_number = %s",
                (user_raw, data.book_id, page_num)
            )
        existing = cursor.fetchone()

        if existing:
            cursor.execute("DELETE FROM bookmarks WHERE id = %s", (existing['id'],))
            mins = audio_pos // 60000
            secs = (audio_pos % 60000) // 1000
            label = f"mốc audio {mins:02d}:{secs:02d}" if audio_pos > 0 else f"trang {page_num}"
            return {"status": "removed", "message": f"Đã hủy đánh dấu {label}"}
        else:
            cursor.execute(
                "INSERT INTO bookmarks (username, book_id, page_number, audio_position_ms, note) VALUES (%s, %s, %s, %s, %s)",
                (user_raw, data.book_id, page_num, audio_pos, data.note)
            )
            mins = audio_pos // 60000
            secs = (audio_pos % 60000) // 1000
            label = f"mốc audio {mins:02d}:{secs:02d}" if audio_pos > 0 else f"trang {page_num}"
            return {"status": "added", "message": f"Đã đánh dấu {label} thành công!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        print(">>> LỖI TOGGLE BOOKMARK:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()

@app.get("/api/bookmarks/{username}")
def get_user_bookmarks(username: str):
    user_raw = username.strip()
    user_lower = user_raw.lower()

    if not user_lower or user_lower in ["guest", "anonymous", "null", "undefined"] or "khách" in user_lower or "khach" in user_lower:
        raise HTTPException(
            status_code=403,
            detail="Tài khoản khách không thể xem dữ liệu đánh dấu trang!"
        )

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (user_raw,))
        db_user = cursor.fetchone()
        if not db_user:
            raise HTTPException(
                status_code=403,
                detail="Tài khoản này không hợp lệ hoặc không tồn tại!"
            )

        sql = """
            SELECT b.id as bookmark_id, b.book_id, b.page_number, ISNULL(b.audio_position_ms, 0) as audio_position_ms, b.note, b.created_at,
                   s.title as book_title, s.author as book_author, s.image_url, s.pdf_url, s.audio_url
            FROM bookmarks b
            JOIN books s ON b.book_id = s.id
            WHERE b.username = %s
            ORDER BY b.created_at DESC
        """
        cursor.execute(sql, (user_raw,))
        bookmarks = cursor.fetchall()
        return bookmarks
    except HTTPException as he:
        raise he
    except Exception as e:
        print(">>> LỖI LẤY DANH SÁCH BOOKMARK:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()

@app.get("/api/bookmarks/{username}/{book_id}")
def get_book_bookmarks(username: str, book_id: int):
    user_raw = username.strip()
    user_lower = user_raw.lower()

    if not user_lower or user_lower in ["guest", "anonymous", "null", "undefined"] or "khách" in user_lower or "khach" in user_lower:
        return []

    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT b.id as bookmark_id, b.book_id, b.page_number, ISNULL(b.audio_position_ms, 0) as audio_position_ms, b.note, b.created_at
            FROM bookmarks b
            WHERE b.username = %s AND b.book_id = %s
            ORDER BY b.created_at DESC
        """
        cursor.execute(sql, (user_raw, book_id))
        return cursor.fetchall()
    except Exception as e:
        print(">>> LỖI LẤY BOOKMARK CỦA SÁCH:", str(e))
        return []
    finally:
        conn.close()


# ===================================================================
# --- CÁC API TÍNH NĂNG KHÁM PHÁ (NEWS FEED) ---
# ===================================================================

@app.post("/api/feed/posts")
async def create_feed_post(
    username: str = Form(...),
    content: str = Form(...),
    file: UploadFile = File(None)
):
    conn = get_connection()
    cursor = conn.cursor()
    image_url = ""
    initial_status = "approved" if username.strip().lower() == "admin" else "pending"

    try:
        if file and file.filename:
            ext = os.path.splitext(file.filename)[1].lower()
            unique_filename = f"post_{uuid.uuid4().hex}_{int(time.time())}{ext}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)

            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())

            image_url = f"http://10.0.2.2:8000/uploads/{unique_filename}"

        cursor.execute(
            "INSERT INTO posts (username, content, image_url, status) VALUES (%s, %s, %s, %s)",
            (username.strip(), content.strip(), image_url if image_url else None, initial_status)
        )
        conn.close()

        msg = "Đăng bài viết thành công!" if initial_status == "approved" else "Đăng bài viết thành công! Vui lòng chờ Admin duyệt."
        return {"status": "success", "message": msg}
    except Exception as e:
        if conn:
            conn.close()
        print(">>> LỖI ĐĂNG BÀI VIẾT KHÁM PHÁ:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


@app.get("/api/feed/posts")
def get_feed_posts(current_user: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM posts WHERE status = 'approved' ORDER BY created_at DESC")
        posts = cursor.fetchall()

        result = []
        for post in posts:
            post_id = post['id']

            cursor.execute("SELECT COUNT(*) as cnt FROM likes WHERE post_id = %s", (post_id,))
            likes_count = cursor.fetchone()['cnt']

            cursor.execute(
                "SELECT id FROM likes WHERE post_id = %s AND username = %s",
                (post_id, current_user.strip())
            )
            is_liked = cursor.fetchone() is not None

            cursor.execute(
                "SELECT id, username, content, created_at FROM comments WHERE post_id = %s ORDER BY created_at ASC",
                (post_id,)
            )
            comments = cursor.fetchall()

            formatted_comments = []
            for comment in comments:
                formatted_comments.append({
                    "id": comment['id'],
                    "username": comment['username'],
                    "content": comment['content'],
                    "created_at": comment['created_at'].strftime("%Y-%m-%d %H:%M:%S")
                })

            result.append({
                "id": post['id'],
                "username": post['username'],
                "content": post['content'],
                "image_url": post['image_url'],
                "status": post['status'],
                "created_at": post['created_at'].strftime("%Y-%m-%d %H:%M:%S"),
                "likes_count": likes_count,
                "is_liked": is_liked,
                "comments": formatted_comments
            })

        return result
    except Exception as e:
        print(">>> LỖI LẤY BẢN TIN KHÁM PHÁ:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()


@app.get("/api/feed/pending")
def get_pending_posts(current_user: str):
    if current_user.strip().lower() != "admin":
        raise HTTPException(status_code=403, detail="Chỉ tài khoản Admin mới có quyền truy cập hộp thư chờ duyệt!")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM posts WHERE status = 'pending' ORDER BY created_at DESC")
        posts = cursor.fetchall()

        result = []
        for post in posts:
            post_id = post['id']

            cursor.execute("SELECT COUNT(*) as cnt FROM likes WHERE post_id = %s", (post_id,))
            likes_count = cursor.fetchone()['cnt']

            cursor.execute("SELECT id FROM likes WHERE post_id = %s AND username = %s", (post_id, current_user.strip()))
            is_liked = cursor.fetchone() is not None

            cursor.execute("SELECT id, username, content, created_at FROM comments WHERE post_id = %s ORDER BY created_at ASC", (post_id,))
            comments = cursor.fetchall()
            formatted_comments = [{
                "id": c['id'],
                "username": c['username'],
                "content": c['content'],
                "created_at": c['created_at'].strftime("%Y-%m-%d %H:%M:%S")
            } for c in comments]

            result.append({
                "id": post['id'],
                "username": post['username'],
                "content": post['content'],
                "image_url": post['image_url'],
                "status": post['status'],
                "created_at": post['created_at'].strftime("%Y-%m-%d %H:%M:%S"),
                "likes_count": likes_count,
                "is_liked": is_liked,
                "comments": formatted_comments
            })

        return result
    except Exception as e:
        print(">>> LỖI LẤY DANH SÁCH CHỜ DUYỆT:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()


@app.put("/api/feed/posts/{post_id}/approve")
def approve_feed_post(post_id: int, username: str):
    if username.strip().lower() != "admin":
        raise HTTPException(status_code=403, detail="Bạn không có quyền duyệt bài viết này!")

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        if not post:
            raise HTTPException(status_code=404, detail="Không tìm thấy bài viết yêu cầu duyệt!")

        cursor.execute("UPDATE posts SET status = 'approved' WHERE id = %s", (post_id,))
        conn.close()
        return {"status": "success", "message": "Bài viết đã được duyệt công khai!"}
    except Exception as e:
        if conn:
            conn.close()
        print(">>> LỖI DUYỆT BÀI VIẾT:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


@app.delete("/api/feed/posts/{post_id}")
def delete_feed_post(post_id: int, username: str):
    conn = get_connection()
    cursor = conn.cursor()
    user_strip = username.strip()

    try:
        cursor.execute("SELECT username, image_url FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        if not post:
            conn.close()
            raise HTTPException(status_code=404, detail="Không tìm thấy bài viết cần xóa!")

        if user_strip.lower() != "admin" and post['username'] != user_strip:
            conn.close()
            raise HTTPException(status_code=403, detail="Bạn không có quyền xóa bài đăng của người khác!")

        image_url = post.get('image_url')
        if image_url:
            try:
                filename = image_url.split("/uploads/")[-1]
                file_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as file_err:
                print(f">>> Lỗi dọn dẹp ảnh bài đăng: {file_err}")

        cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
        conn.close()
        return {"status": "success", "message": "Đã xóa bài đăng thành công!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        if conn:
            conn.close()
        print(">>> LỖI XÓA BÀI VIẾT:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


@app.post("/api/feed/posts/{post_id}/like")
def toggle_feed_like(post_id: int, username: str):
    conn = get_connection()
    cursor = conn.cursor()
    user_strip = username.strip()

    try:
        cursor.execute(
            "SELECT id FROM likes WHERE post_id = %s AND username = %s",
            (post_id, user_strip)
        )
        like_record = cursor.fetchone()

        if like_record:
            cursor.execute("DELETE FROM likes WHERE id = %s", (like_record['id'],))
            conn.close()
            return {"status": "unliked", "message": "Đã bỏ thích bài viết thành công!"}
        else:
            cursor.execute(
                "INSERT INTO likes (post_id, username) VALUES (%s, %s)",
                (post_id, user_strip)
            )
            conn.close()
            return {"status": "liked", "message": "Đã thích bài viết thành công!"}
    except Exception as e:
        if conn:
            conn.close()
        print(">>> LỖI TOGGLE LIKE BÀI VIẾT:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


@app.post("/api/feed/posts/{post_id}/comment")
def add_feed_comment(post_id: int, username: str, content: str = Form(...)):
    if not content.strip():
        raise HTTPException(status_code=400, detail="Bình luận không được phép để trống!")

    conn = get_connection()
    cursor = conn.cursor()
    user_strip = username.strip()

    try:
        cursor.execute(
            "INSERT INTO comments (post_id, username, content) VALUES (%s, %s, %s)",
            (post_id, user_strip, content.strip())
        )

        last_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, username, content, created_at FROM comments WHERE id = %s",
            (last_id,)
        )
        new_comment = cursor.fetchone()
        conn.close()

        return {
            "id": new_comment['id'],
            "username": new_comment['username'],
            "content": new_comment['content'],
            "created_at": new_comment['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        if conn:
            conn.close()
        print(">>> LỖI GỬI BÌNH LUẬN KHÁM PHÁ:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")


# ===================================================================
# --- CÁC API TIẾN ĐỘ ĐỌC & BOOKMARK SYNC (MODULE 5) ---
# ===================================================================

@app.post("/api/progress/update")
def update_reading_progress(data: ReadingProgressInput):
    user_raw = data.username.strip()
    if not user_raw or user_raw.lower() in ["guest", "anonymous", "null", "undefined"]:
        return {"status": "ignored", "message": "Guest progress not persisted on server"}
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM books WHERE id = %s", (data.book_id,))
        if not cursor.fetchone():
            return {"status": "ignored", "message": f"Sách #{data.book_id} không tồn tại trên hệ thống"}

        cursor.execute("SELECT id FROM reading_progress WHERE username = %s AND book_id = %s", (user_raw, data.book_id))
        existing = cursor.fetchone()
        if existing:
            cursor.execute(
                """
                UPDATE reading_progress 
                SET last_page = %s, last_epub_cfi = %s, last_audio_position_ms = %s, progress_percent = %s, updated_at = GETDATE()
                WHERE id = %s
                """,
                (data.last_page or 0, data.last_epub_cfi or "", data.last_audio_position_ms or 0, data.progress_percent or 0.0, existing['id'])
            )
        else:
            cursor.execute(
                """
                INSERT INTO reading_progress (username, book_id, last_page, last_epub_cfi, last_audio_position_ms, progress_percent, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, GETDATE())
                """,
                (user_raw, data.book_id, data.last_page or 0, data.last_epub_cfi or "", data.last_audio_position_ms or 0, data.progress_percent or 0.0)
            )
        return {"status": "success", "message": "Đã lưu tiến độ thành công!"}
    except Exception as e:
        print(">>> LỖI CẬP NHẬT TIẾN ĐỘ:", repr(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()

@app.get("/api/progress/{username}")
def get_user_progress(username: str):
    user_raw = username.strip()
    if not user_raw or user_raw.lower() in ["guest", "anonymous", "null", "undefined"]:
        return []
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT p.id, p.book_id, p.last_page, p.last_epub_cfi, p.last_audio_position_ms, 
                   p.progress_percent, p.updated_at,
                   b.title, b.author, b.image_url, b.pdf_url, b.audio_url
            FROM reading_progress p
            JOIN books b ON p.book_id = b.id
            WHERE p.username = %s
            ORDER BY p.updated_at DESC
        """
        cursor.execute(sql, (user_raw,))
        records = cursor.fetchall()
        for r in records:
            r['progress_percent'] = float(r.get('progress_percent') or 0.0)
            if 'updated_at' in r and r['updated_at']:
                r['updated_at'] = r['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        return records
    except Exception as e:
        print(">>> LỖI LẤY TIẾN ĐỘ:", repr(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()

@app.get("/api/progress/{username}/{book_id}")
def get_book_progress(username: str, book_id: int):
    user_raw = username.strip()
    if not user_raw or user_raw.lower() in ["guest", "anonymous", "null", "undefined"]:
        return None
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM reading_progress WHERE username = %s AND book_id = %s",
            (user_raw, book_id)
        )
        row = cursor.fetchone()
        if row:
            row['progress_percent'] = float(row.get('progress_percent') or 0.0)
            if 'updated_at' in row and row['updated_at']:
                row['updated_at'] = row['updated_at'].strftime("%Y-%m-%d %H:%M:%S")
        return row
    except Exception as e:
        print(">>> LỖI LẤY TIẾN ĐỘ SÁCH:", repr(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()


# ===================================================================
# --- CÁC API ĐÁNH GIÁ & BÌNH LUẬN SÁCH (MODULE 7) ---
# ===================================================================

@app.post("/api/books/{book_id}/reviews")
def add_book_review(book_id: int, data: ReviewInput):
    user_raw = data.username.strip()
    if not user_raw or user_raw.lower() in ["guest", "anonymous", "null", "undefined"]:
        raise HTTPException(status_code=403, detail="Vui lòng đăng nhập để đánh giá sách!")
    if data.rating < 1 or data.rating > 5:
        raise HTTPException(status_code=400, detail="Điểm đánh giá phải từ 1 đến 5 sao!")
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM books WHERE id = %s", (book_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy cuốn sách này để đánh giá!")

        cursor.execute("SELECT id FROM book_reviews WHERE book_id = %s AND username = %s", (book_id, user_raw))
        existing = cursor.fetchone()
        if existing:
            cursor.execute(
                "UPDATE book_reviews SET rating = %s, comment = %s, created_at = GETDATE() WHERE id = %s",
                (data.rating, data.comment.strip() if data.comment else "", existing['id'])
            )
            review_id = existing['id']
        else:
            cursor.execute(
                "INSERT INTO book_reviews (book_id, username, rating, comment, created_at) VALUES (%s, %s, %s, %s, GETDATE())",
                (book_id, user_raw, data.rating, data.comment.strip() if data.comment else "")
            )
            review_id = cursor.lastrowid
        return {"status": "success", "message": "Đánh giá sách thành công!", "review_id": review_id}
    except Exception as e:
        print(">>> LỖI ĐÁNH GIÁ SÁCH:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()

@app.get("/api/books/{book_id}/reviews")
def get_book_reviews(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT r.id, r.book_id, r.username, r.rating, r.comment, r.created_at,
                   u.avatar_url, u.full_name
            FROM book_reviews r
            LEFT JOIN users u ON r.username = u.username
            WHERE r.book_id = %s
            ORDER BY r.created_at DESC
            """,
            (book_id,)
        )
        reviews = cursor.fetchall()
        total_rating = 0
        for r in reviews:
            total_rating += r['rating']
            if 'created_at' in r and r['created_at']:
                r['created_at'] = r['created_at'].strftime("%Y-%m-%d %H:%M:%S")
        avg_rating = round(total_rating / len(reviews), 1) if reviews else 0.0
        return {
            "reviews": reviews,
            "average_rating": avg_rating,
            "total_reviews": len(reviews)
        }
    except Exception as e:
        print(">>> LỖI LẤY ĐÁNH GIÁ SÁCH:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()

@app.delete("/api/reviews/{review_id}")
def delete_book_review(review_id: int, username: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username FROM book_reviews WHERE id = %s", (review_id,))
        review = cursor.fetchone()
        if not review:
            raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá này!")
        if username.strip().lower() != "admin" and review['username'] != username.strip():
            raise HTTPException(status_code=403, detail="Bạn không có quyền xóa đánh giá của người khác!")
        cursor.execute("DELETE FROM book_reviews WHERE id = %s", (review_id,))
        return {"status": "success", "message": "Đã xóa đánh giá thành công!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        print(">>> LỖI XÓA ĐÁNH GIÁ:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()


# ===================================================================
# --- CÁC API BỔ TRỢ ĐƠN HÀNG (MODULE 8) ---
# ===================================================================

@app.post("/api/orders/{order_id}/cancel")
def cancel_order(order_id: int, username: str):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username, status FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng!")
        if username.strip().lower() != "admin" and order['username'] != username.strip():
            raise HTTPException(status_code=403, detail="Bạn không có quyền hủy đơn hàng này!")
        if order['status'] != 'pending':
            raise HTTPException(status_code=400, detail="Chỉ có thể hủy đơn hàng khi trạng thái là Đang xử lý (pending)!")
        cursor.execute("UPDATE orders SET status = 'cancelled' WHERE id = %s", (order_id,))
        return {"status": "success", "message": "Đã hủy đơn hàng thành công!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        print(">>> LỖI HỦY ĐƠN HÀNG:", str(e))
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")
    finally:
        conn.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)