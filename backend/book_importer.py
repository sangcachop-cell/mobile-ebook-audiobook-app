import sys
import os
import json
import time
import re
import httpx
from typing import List, Dict, Any, Optional

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

SEEDS_DIR = os.path.join(CURRENT_DIR, "seeds")
os.makedirs(SEEDS_DIR, exist_ok=True)
SEEDS_FILE = os.path.join(SEEDS_DIR, "books_500.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BookHub/1.0"
}

def clean_author_name(raw_name: str) -> str:
    if not raw_name:
        return "Nhiều tác giả"
    name = raw_name.strip()
    # "Austen, Jane" -> "Jane Austen"
    if "," in name:
        parts = [p.strip() for p in name.split(",", 1)]
        if len(parts) == 2 and parts[1]:
            name = f"{parts[1]} {parts[0]}"
    # Remove birth/death years if present (e.g. "Jane Austen (1775-1817)")
    name = re.sub(r"\s*\(\d{3,4}\s*[-–]\s*\d{0,4}\)", "", name)
    name = re.sub(r"\s*\d{3,4}\s*[-–]\s*\d{0,4}", "", name)
    return name.strip() or "Khuyết danh"

def map_subjects_to_category(subjects: List[str], bookshelves: List[str]) -> str:
    text = " ".join((subjects or []) + (bookshelves or [])).lower()
    
    if any(k in text for k in ["detective", "mystery", "crime", "sherlock", "gothic", "horror", "murder", "dracula", "frankenstein"]):
        return "Trinh thám"
    elif any(k in text for k in ["philosophy", "ethics", "political science", "plato", "nietzsche", "kant", "aristotle", "stoic", "morals"]):
        return "Triết học"
    elif any(k in text for k in ["science fiction", "physics", "astronomy", "biology", "evolution", "nature", "chemistry", "mathematics", "scientific"]):
        return "Khoa học"
    elif any(k in text for k in ["history", "war", "ancient", "rome", "america", "military", "revolution", "historical", "civil war"]):
        return "Lịch sử"
    elif any(k in text for k in ["adventure", "fantasy", "sea stories", "pirate", "travel", "voyage", "wilderness", "treasure"]):
        return "Phiêu lưu"
    elif any(k in text for k in ["poetry", "poems", "sonnet", "plays", "drama", "verse", "theatre", "shakespeare"]):
        return "Thơ ca"
    elif any(k in text for k in ["children", "fairy", "juvenile", "fables", "nursery", "wonderland", "tales"]):
        return "Thiếu nhi"
    elif any(k in text for k in ["psychology", "self-help", "society", "sociology", "behavior", "mind", "human"]):
        return "Tâm lý"
    else:
        return "Tiểu thuyết"

def get_audio_for_title(title: str, librivox_map: Dict[str, str]) -> str:
    cleaned = re.sub(r"[^\w\s]", "", title.lower()).strip()
    for key, url in librivox_map.items():
        if key in cleaned or cleaned in key:
            return url
    return ""

def fetch_librivox_audiobooks(limit: int = 30) -> Dict[str, str]:
    print(f">>> Đang tải danh sách Audiobooks từ LibriVox API (limit={limit})...", flush=True)
    audio_map: Dict[str, str] = {}
    try:
        url = f"https://librivox.org/api/feed/audiobooks/?format=json&extended=1&limit={limit}"
        with httpx.Client(timeout=8.0, headers=HEADERS) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                for b in data.get("books", []):
                    title = b.get("title", "")
                    cleaned_title = re.sub(r"[^\w\s]", "", title.lower()).strip()
                    sections = b.get("sections", [])
                    if sections and isinstance(sections, list):
                        audio_url = sections[0].get("listen_url", "")
                        if audio_url:
                            audio_map[cleaned_title] = audio_url
                print(f"✅ Đã tải {len(audio_map)} liên kết Audiobook từ LibriVox thành công!", flush=True)
    except Exception as e:
        print(f"⚠️ Không thể tải danh sách LibriVox (dùng fallback audio): {e}", flush=True)
    return audio_map

def fetch_gutendex_page(client: httpx.Client, page: int) -> List[Dict[str, Any]]:
    url = f"https://gutendex.com/books/?languages=en&page={page}"
    resp = client.get(url)
    if resp.status_code != 200:
        print(f"⚠️ Trang {page} trả về mã lỗi: {resp.status_code}")
        return []
    data = resp.json()
    return data.get("results", [])

def build_500_books_dataset(target_count: int = 510) -> List[Dict[str, Any]]:
    print(f">>> Bắt đầu thu thập dữ liệu ~{target_count} sách từ Gutendex & LibriVox...", flush=True)
    
    # 1. Tải bản đồ LibriVox Audiobooks để gắn file MP3 trực tiếp
    librivox_audio_map = fetch_librivox_audiobooks(limit=30)
    
    # Một số URL audio mẫu chuẩn dự phòng chất lượng cao
    fallback_audios = [
        "uploads/audio_sample_1.mp3",
        "uploads/audio_sample_2.mp3",
        "https://www.archive.org/download/pride_and_prejudice_librivox/prideandprejudice_01-03_austen_64kb.mp3",
        "https://www.archive.org/download/count_monte_cristo_0711_librivox/count_of_monte_cristo_001_dumas_64kb.mp3",
        "https://www.archive.org/download/adventures_sherlock_holmes_1003_librivox/adventuresofsherlockholmes_01_doyle_64kb.mp3",
        "https://www.archive.org/download/alices_adventures_in_wonderland_0710_librivox/alicesadventuresinwonderland_01_carroll_64kb.mp3",
        "https://www.archive.org/download/frankenstein_or_the_modern_prometheus_1110_librivox/frankenstein_01_shelley_64kb.mp3",
        "https://www.archive.org/download/dracula_0810_librivox/dracula_01_stoker_64kb.mp3"
    ]
    
    books: List[Dict[str, Any]] = []
    seen_titles = set()
    
    pages_needed = (target_count // 32) + 2
    
    with httpx.Client(timeout=12.0, headers=HEADERS) as client:
        for page in range(1, pages_needed + 1):
            if len(books) >= target_count:
                break
            print(f">>> Đang tải trang {page}/{pages_needed} từ Gutendex (hiện có {len(books)} cuốn)...", flush=True)
            try:
                raw_books = fetch_gutendex_page(client, page)
                for b in raw_books:
                    g_id = b.get("id")
                    title = b.get("title", "").strip()
                    if not title or title.lower() in seen_titles:
                        continue
                    
                    authors = b.get("authors", [])
                    raw_author = authors[0].get("name", "") if authors else "Tác giả cổ điển"
                    author = clean_author_name(raw_author)
                    
                    formats = b.get("formats", {})
                    # Ưu tiên cover chuẩn từ Gutenberg
                    cover = formats.get("image/jpeg", "")
                    if not cover:
                        cover = f"https://www.gutenberg.org/cache/epub/{g_id}/pg{g_id}.cover.medium.jpg"
                    
                    # EPUB URL: ưu tiên file noimages siêu nhẹ hoặc file zip
                    epub_url = f"https://www.gutenberg.org/cache/epub/{g_id}/pg{g_id}.epub"
                    
                    subjects = b.get("subjects", [])
                    shelves = b.get("bookshelves", [])
                    category = map_subjects_to_category(subjects, shelves)
                    
                    # Tìm kiếm audio match từ LibriVox
                    matched_audio = get_audio_for_title(title, librivox_audio_map)
                    # Nếu thuộc top 120 cuốn hoặc có audio match thì gán audio URL
                    if matched_audio:
                        audio_url = matched_audio
                    elif len(books) < 120:
                        audio_url = fallback_audios[len(books) % len(fallback_audios)]
                    else:
                        audio_url = ""
                    
                    # Mô tả chi tiết sách
                    summary_parts = []
                    if subjects:
                        summary_parts.append(f"Chủ đề: {', '.join(subjects[:3])}.")
                    if shelves:
                        summary_parts.append(f"Tủ sách: {', '.join(shelves[:2])}.")
                    summary_parts.append(f"Tác phẩm văn học kinh điển thế giới của {author}.")
                    content = " ".join(summary_parts)
                    
                    # Rating trung bình & lượt review dựa vào download_count
                    dl_count = b.get("download_count", 100)
                    rating = round(min(5.0, max(4.1, 4.3 + (dl_count % 70) / 100.0)), 1)
                    reviews = max(15, min(850, dl_count // 8 + 25))
                    
                    book_entry = {
                        "external_id": f"gutenberg_{g_id}",
                        "title": title,
                        "author": author,
                        "content": content,
                        "image_url": cover,
                        "pdf_url": epub_url,
                        "audio_url": audio_url,
                        "category": category,
                        "rating_avg": rating,
                        "review_count": reviews,
                        "source": "Project Gutenberg" + (" & LibriVox" if audio_url else "")
                    }
                    
                    books.append(book_entry)
                    seen_titles.add(title.lower())
                    
                    if len(books) >= target_count:
                        break
                        
                time.sleep(0.3)  # Tránh gửi request quá dồn dập
            except Exception as page_err:
                print(f"⚠️ Lỗi tải trang {page}: {page_err}")
                time.sleep(1)
                
    print(f"🎉 Đã thu thập thành công {len(books)} cuốn sách!", flush=True)
    
    # Lưu ra file JSON dự phòng (seeds)
    with open(SEEDS_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    print(f"💾 Đã lưu dữ liệu vào tệp hạt giống: {SEEDS_FILE}", flush=True)
    
    return books

def save_books_to_db(books: List[Dict[str, Any]]) -> int:
    print(f">>> Đang lưu {len(books)} sách vào cơ sở dữ liệu MS SQL Server...", flush=True)
    conn = get_connection()
    cursor = conn.cursor()
    inserted_count = 0
    updated_count = 0
    
    try:
        # Đảm bảo bảng books đã có đầy đủ các cột mở rộng
        alter_stmts = [
            "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'category') ALTER TABLE books ADD category NVARCHAR(100) DEFAULT N'Tiểu thuyết';",
            "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'rating_avg') ALTER TABLE books ADD rating_avg DECIMAL(3, 2) DEFAULT 4.8;",
            "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'review_count') ALTER TABLE books ADD review_count INT DEFAULT 12;",
            "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'source') ALTER TABLE books ADD source NVARCHAR(100) DEFAULT N'BookHub';",
            "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'external_id') ALTER TABLE books ADD external_id NVARCHAR(100);"
        ]
        for s in alter_stmts:
            try:
                cursor.execute(s)
            except Exception:
                pass
                
        # Lấy danh sách external_id và title đã tồn tại để tránh trùng lặp
        cursor.execute("SELECT external_id, title FROM books")
        existing_rows = cursor.fetchall()
        existing_externals = {r['external_id'] for r in existing_rows if r.get('external_id')}
        existing_titles = {r['title'].strip().lower() for r in existing_rows if r.get('title')}
        
        insert_sql = """
            INSERT INTO books (title, author, content, image_url, pdf_url, audio_url, category, rating_avg, review_count, source, external_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for b in books:
            ext_id = b.get("external_id", "")
            title = b.get("title", "").strip()
            
            if ext_id and ext_id in existing_externals:
                continue
            if title.lower() in existing_titles:
                continue
                
            cursor.execute(
                insert_sql,
                (
                    b.get("title", "Chưa có tiêu đề")[:250],
                    b.get("author", "Chưa rõ tác giả")[:250],
                    b.get("content", ""),
                    b.get("image_url", "")[:490],
                    b.get("pdf_url", "")[:490],
                    b.get("audio_url", "")[:490],
                    b.get("category", "Tiểu thuyết")[:90],
                    b.get("rating_avg", 4.8),
                    b.get("review_count", 50),
                    b.get("source", "Project Gutenberg")[:90],
                    ext_id[:90]
                )
            )
            inserted_count += 1
            if ext_id:
                existing_externals.add(ext_id)
            existing_titles.add(title.lower())
            
        print(f"🎉 Hoàn tất! Đã thêm mới {inserted_count} sách vào bảng 'books'.")
        
        # Thống kê phân loại theo danh mục
        cursor.execute("SELECT category, COUNT(*) as cnt FROM books GROUP BY category ORDER BY cnt DESC")
        cat_stats = cursor.fetchall()
        print("\n📊 Phân bố thể loại sách hiện tại:")
        for cs in cat_stats:
            print(f"   • {cs['category']}: {cs['cnt']} cuốn")
            
        cursor.execute("SELECT COUNT(*) as total FROM books")
        total = cursor.fetchone()['total']
        print(f"\n📚 TỔNG SỐ SÁCH TRONG HỆ THỐNG: {total} cuốn.\n")
        
    except Exception as e:
        print(f"❌ Lỗi lưu dữ liệu: {e}")
    finally:
        cursor.close()
        conn.close()
        
    return inserted_count

def run_import_pipeline(target_count: int = 510):
    # Nếu file hạt giống đã tồn tại và đủ số lượng, có thể đọc trực tiếp nếu muốn nhanh
    if os.path.exists(SEEDS_FILE):
        try:
            with open(SEEDS_FILE, "r", encoding="utf-8") as f:
                cached_books = json.load(f)
            if len(cached_books) >= target_count:
                print(f"📁 Tìm thấy file hạt giống cục bộ ({len(cached_books)} sách). Nạp trực tiếp vào Database...")
                save_books_to_db(cached_books)
                return
        except Exception:
            pass
            
    books = build_500_books_dataset(target_count)
    save_books_to_db(books)

if __name__ == "__main__":
    count = 510
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass
    run_import_pipeline(count)
