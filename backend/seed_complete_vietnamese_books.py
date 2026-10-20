# -*- coding: utf-8 -*-
"""
Script gieo hạt toàn diện kho sách tiếng Việt:
1. Xóa bỏ hoàn toàn sách nước ngoài Gutenberg / LibriVox khỏi database.
2. Sinh file PDF chuẩn in ấn nhiều trang (có Header, Footer số trang, Mục lục) và file EPUB chuẩn.
3. Sinh giọng đọc thuyết minh sách nói tiếng Việt truyền cảm bằng Edge-TTS AI (tuyệt đối không dùng nhạc/bài hát).
4. Cập nhật cơ sở dữ liệu với đầy đủ nội dung hoàn chỉnh nhiều chương cho từng cuốn.
"""
import os
import sys
import asyncio
import edge_tts

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from database import get_connection
from epub_builder import create_valid_epub
from pdf_builder import create_valid_pdf
from data_vietnamese_30_books import BOOKS_DATA

UPLOAD_DIR = os.path.join(CURRENT_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def generate_narration_audio(text: str, filename: str, voice: str = "vi-VN-HoaiMyNeural", force: bool = False) -> str:
    """Tạo audio thuyết minh tiếng Việt chuẩn bằng Azure Neural Voice qua edge-tts"""
    output_path = os.path.join(UPLOAD_DIR, filename)
    if not force and os.path.exists(output_path) and os.path.getsize(output_path) > 30000:
        return filename
        
    try:
        communicate = edge_tts.Communicate(text, voice=voice, rate="+0%", volume="+0%")
        await communicate.save(output_path)
        print(f"   [Audio] Đã tạo giọng đọc {voice}: {filename} ({os.path.getsize(output_path)} bytes)")
        return filename
    except Exception as e:
        print(f"   [Audio Lỗi] Không thể tạo {filename}: {e}")
        return "audio_sample_1.mp3"

async def main():
    print("=" * 70)
    print("BẮT ĐẦU CẬP NHẬT KHO SÁCH VIỆT NAM TINH HOA & XÓA SÁCH NƯỚC NGOÀI")
    print("=" * 70)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # ---------------- 1. XÓA BỎ HOÀN TOÀN SÁCH NƯỚC NGOÀI ----------------
    print("\n1. Đang dọn dẹp và xóa toàn bộ sách nước ngoài cũ...")
    cursor.execute("""
        SELECT id FROM books 
        WHERE source NOT LIKE N'%Việt Nam%'
    """)
    foreign_books = cursor.fetchall()
    foreign_ids = [b["id"] for b in foreign_books]
    print(f"-> Tìm thấy {len(foreign_ids)} cuốn sách nước ngoài cần loại bỏ.")
    
    if foreign_ids:
        # Xóa các ràng buộc ngoại khóa nếu có
        cursor.execute("DELETE FROM reading_progress WHERE book_id IN (SELECT id FROM books WHERE source NOT LIKE N'%Việt Nam%')")
        cursor.execute("DELETE FROM bookmarks WHERE book_id IN (SELECT id FROM books WHERE source NOT LIKE N'%Việt Nam%')")
        cursor.execute("DELETE FROM book_reviews WHERE book_id IN (SELECT id FROM books WHERE source NOT LIKE N'%Việt Nam%')")
        cursor.execute("DELETE FROM books WHERE source NOT LIKE N'%Việt Nam%'")
        conn.commit()
        print(f"-> Đã xóa thành công {len(foreign_ids)} cuốn sách nước ngoài khỏi database!")
    
    # ---------------- 2. ĐẢM BẢO TỆP FALLBACK AUDIO KHÔNG CHỨA BÀI HÁT ----------------
    print("\n2. Cập nhật các tệp audio mẫu cơ bản thành giọng đọc sách nói thuần túy...")
    sample_text_1 = (
        "Chào mừng bạn đến với ứng dụng đọc sách và sách nói BookHub. "
        "Mỗi cuốn sách là một thế giới kỳ diệu mở ra chân trời tri thức, nuôi dưỡng tâm hồn và thắp sáng ước mơ. "
        "Chúc bạn có những phút giây lắng nghe thật thư thái và tràn đầy cảm hứng."
    )
    sample_text_2 = (
        "Sách nói là người bạn đồng hành tuyệt vời trên mọi chặng đường. "
        "Dù bạn đang nghỉ ngơi, làm việc hay di chuyển, tri thức vẫn luôn bên bạn qua từng thanh âm truyền cảm. "
        "Hãy cùng BookHub khám phá kho tàng văn học và kiến thức vô tận."
    )
    await generate_narration_audio(sample_text_1, "audio_sample_1.mp3", "vi-VN-HoaiMyNeural")
    await generate_narration_audio(sample_text_2, "audio_sample_2.mp3", "vi-VN-NamMinhNeural")
    
    # ---------------- 3. TẠO FILE VÀ NẠP 33 CUỐN SÁCH HOÀN CHỈNH ----------------
    print(f"\n3. Bắt đầu tạo dữ liệu cho {len(BOOKS_DATA)} cuốn sách tiếng Việt hoàn chỉnh...")
    
    for idx, b in enumerate(BOOKS_DATA, 1):
        slug = b["slug"]
        title = b["title"]
        author = b["author"]
        category = b["category"]
        fmt = b.get("format", "pdf")
        
        # Chọn giọng đọc xen kẽ: Nữ Hoài My hoặc Nam Nam Minh
        voice = "vi-VN-NamMinhNeural" if idx % 2 == 0 else "vi-VN-HoaiMyNeural"
        audio_filename = f"{slug}.mp3"
        
        print(f"\n[{idx}/{len(BOOKS_DATA)}] Đang xử lý: '{title}' ({author}) - Thể loại: {category}")
        
        # 3.1 Tạo file Audio thuyết minh đọc trực tiếp nội dung tác phẩm (không chỉ đọc tóm tắt)
        first_chap = b["chapters"][0]
        read_aloud_text = f"Chào mừng bạn lắng nghe tác phẩm {title} của tác giả {author}. {first_chap['title']}. {first_chap['content']}"
        if len(read_aloud_text) > 3500:
            read_aloud_text = read_aloud_text[:3500]
        await generate_narration_audio(read_aloud_text, audio_filename, voice, force=True)
        audio_url = f"uploads/{audio_filename}"
        
        # 3.2 Luôn tạo cả file EPUB chuẩn hóa và file PDF in ấn nhiều trang
        epub_filename = f"{slug}.epub"
        epub_path = os.path.join(UPLOAD_DIR, epub_filename)
        create_valid_epub(epub_path, title, author, b["chapters"])
        print(f"   [EPUB] Đã tạo file EPUB chuẩn: {epub_filename} ({os.path.getsize(epub_path)} bytes)")

        pdf_filename = f"{slug}.pdf"
        pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)
        create_valid_pdf(pdf_path, title, author, b["chapters"], category)
        print(f"   [PDF] Đã tạo file PDF chuẩn nhiều trang: {pdf_filename} ({os.path.getsize(pdf_path)} bytes)")

        # Gán đường dẫn đọc mặc định theo định dạng sách
        book_url = f"uploads/{epub_filename}" if fmt == "epub" else f"uploads/{pdf_filename}"
            
        # 3.3 Chuẩn bị nội dung văn bản đầy đủ cho cột content
        full_text_list = []
        for c in b["chapters"]:
            full_text_list.append(f"=== {c['title']} ===\n{c['content']}")
        full_content = "\n\n".join(full_text_list)
        
        # 3.4 Cập nhật vào CSDL
        cursor.execute("SELECT id FROM books WHERE title = %s", (title,))
        existing = cursor.fetchone()
        if existing:
            book_id = existing["id"]
            cursor.execute("""
                UPDATE books
                SET author = %s,
                    content = %s,
                    audio_url = %s,
                    image_url = %s,
                    pdf_url = %s,
                    category = %s,
                    rating_avg = %s,
                    review_count = %s,
                    source = N'Kho Sách Việt Nam Tinh Hoa'
                WHERE id = %s
            """, (
                author,
                full_content,
                audio_url,
                b["image_url"],
                book_url,
                category,
                b["rating_avg"],
                b["review_count"],
                book_id
            ))
            print(f"   [DB] Đã cập nhật sách ID {book_id}: {title}")
        else:
            cursor.execute("""
                INSERT INTO books (title, author, content, audio_url, image_url, pdf_url, category, rating_avg, review_count, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, N'Kho Sách Việt Nam Tinh Hoa')
            """, (
                title,
                author,
                full_content,
                audio_url,
                b["image_url"],
                book_url,
                category,
                b["rating_avg"],
                b["review_count"]
            ))
            print(f"   [DB] Đã thêm mới sách: {title}")
            
    conn.commit()
    
    # ---------------- 4. KIỂM TRA TỔNG KẾT ----------------
    cursor.execute("SELECT COUNT(*) as cnt FROM books")
    total_books = cursor.fetchone()["cnt"]
    
    cursor.execute("SELECT category, COUNT(*) as cnt FROM books GROUP BY category")
    cat_stats = cursor.fetchall()
    
    conn.close()
    
    print("\n" + "=" * 70)
    print("HOÀN TẤT THÀNH CÔNG RỰC RỠ!")
    print(f"Tổng số sách trong hệ thống hiện tại: {total_books} cuốn.")
    print("Phân bố theo thể loại:")
    for c in cat_stats:
        print(f"  - {c['category']}: {c['cnt']} cuốn")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
