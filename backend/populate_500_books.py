"""
populate_500_books.py
Script thu thập và nạp ~500 sách chất lượng cao từ Gutendex (Project Gutenberg)
kết hợp sách nói (MP3) từ LibriVox API vào cơ sở dữ liệu MS SQL Server.
Dữ liệu được phân loại thành 10 thể loại đa dạng, đầy đủ bìa, EPUB, Audio, mô tả và điểm đánh giá.
"""

import sys
import os
import json
import time
import re
import random
import httpx

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

DATASET_FILE = os.path.join(CURRENT_DIR, "books_500_dataset.json")

# Danh mục phân loại sách
CATEGORIES = [
    "Văn học & Tiểu thuyết",
    "Phiêu lưu & Kỳ ảo",
    "Trinh thám & Bí ẩn",
    "Khoa học & Viễn tưởng",
    "Triết học & Tư tưởng",
    "Lịch sử & Tiểu sử",
    "Tâm lý & Xã hội",
    "Thiếu nhi & Cổ tích",
    "Thơ ca & Kịch nghệ",
    "Kinh doanh & Phát triển",
]

def format_author_name(raw_name: str) -> str:
    if not raw_name:
        return "Nhiều tác giả"
    parts = raw_name.split(",")
    if len(parts) == 2:
        return f"{parts[1].strip()} {parts[0].strip()}"
    return raw_name.strip()

def classify_category(subjects, bookshelves, title) -> str:
    combined = " ".join((subjects or []) + (bookshelves or []) + [title]).lower()
    
    if any(k in combined for k in ["adventure", "sea stories", "pirate", "voyage", "wilderness", "expedition", "treasure", "western"]):
        return "Phiêu lưu & Kỳ ảo"
    if any(k in combined for k in ["detective", "mystery", "crime", "murder", "sherlock", "investigation", "horror", "gothic", "ghost"]):
        return "Trinh thám & Bí ẩn"
    if any(k in combined for k in ["science fiction", "fantasy", "space", "utopia", "dystopia", "time travel", "future", "alien", "mars"]):
        return "Khoa học & Viễn tưởng"
    if any(k in combined for k in ["philosophy", "ethics", "logic", "plato", "aristotle", "nietzsche", "kant", "meditation", "reason", "moral"]):
        return "Triết học & Tư tưởng"
    if any(k in combined for k in ["history", "biography", "war", "civil war", "revolution", "historical", "rome", "napoleon", "monarchy", "memoir"]):
        return "Lịch sử & Tiểu sử"
    if any(k in combined for k in ["psychology", "social", "society", "human", "behavior", "relationship", "family", "education"]):
        return "Tâm lý & Xã hội"
    if any(k in combined for k in ["children", "fairy", "nursery", "fables", "juvenile", "wonderland", "tales", "youth"]):
        return "Thiếu nhi & Cổ tích"
    if any(k in combined for k in ["poetry", "poems", "verse", "drama", "plays", "ballad", "tragedy", "comedy", "shakespeare"]):
        return "Thơ ca & Kịch nghệ"
    if any(k in combined for k in ["economics", "wealth", "business", "commerce", "money", "industry", "capital", "management", "success"]):
        return "Kinh doanh & Phát triển"
        
    return "Văn học & Tiểu thuyết"

def generate_vietnamese_description(title: str, author: str, category: str, subjects: list) -> str:
    sub_text = ", ".join(subjects[:4]) if subjects else "Tác phẩm kinh điển"
    clean_title = title.split("\n")[0].strip()
    return (
        f"\"{clean_title}\" là một kiệt tác nổi tiếng của tác giả {author}, thuộc thể loại {category}. "
        f"Tác phẩm mang lại chiều sâu tư tưởng độc đáo, được độc giả trên toàn thế giới yêu thích qua nhiều thế hệ. "
        f"Các chủ đề chính bao gồm: {sub_text}. Sách hỗ trợ đọc bản điện tử (EPUB) và nghe sách nói chất lượng cao."
    )

def fetch_librivox_audiobooks(client: httpx.Client, limit: int = 60) -> list:
    print(f">>> Đang tải danh sách sách nói từ LibriVox API (limit={limit})...", flush=True)
    audio_tracks = []
    try:
        url = f"https://librivox.org/api/feed/audiobooks/?format=json&limit={limit}&extended=1"
        res = client.get(url, timeout=30.0)
        if res.status_code == 200:
            books = res.json().get("books", [])
            for b in books:
                title = b.get("title", "").strip()
                sections = b.get("sections", [])
                listen_url = ""
                if sections:
                    for sec in sections:
                        if sec.get("listen_url"):
                            listen_url = sec["listen_url"]
                            break
                if not listen_url and b.get("url_zip_file"):
                    listen_url = b.get("url_zip_file")
                
                if title and listen_url:
                    audio_tracks.append({
                        "title": title,
                        "audio_url": listen_url,
                        "source": "LibriVox"
                    })
            print(f">>> Đã lấy thành công {len(audio_tracks)} bản ghi audiobook từ LibriVox!", flush=True)
    except Exception as e:
        print(f"Lỗi tải LibriVox: {e}", flush=True)
        
    # Thêm fallback audio tracks mẫu chất lượng cao
    fallback_audios = [
        "https://www.archive.org/download/count_monte_cristo_0711_librivox/count_of_monte_cristo_001_dumas_64kb.mp3",
        "https://www.archive.org/download/pride_and_prejudice_librivox/prideandprejudice_01-03_austen_64kb.mp3",
        "https://www.archive.org/download/adventures_sherlock_holmes_1008_librivox/adventuresof_sherlockholmes_01_doyle_64kb.mp3",
        "https://www.archive.org/download/frankenstein_0809_librivox/frankenstein_01_shelley_64kb.mp3",
        "https://www.archive.org/download/alice_in_wonderland_0712_librivox/alice_in_wonderland_01_carroll_64kb.mp3",
        "https://www.archive.org/download/dracula_librivox/dracula_01_stoker_64kb.mp3",
        "https://www.archive.org/download/moby_dick_librivox/mobydick_001_melville_64kb.mp3",
        "https://www.archive.org/download/tale_two_cities_librivox/taleto_twocities_01_dickens_64kb.mp3",
    ]
    for url in fallback_audios:
        audio_tracks.append({"title": "Sample Audiobook Chapter", "audio_url": url, "source": "LibriVox"})
    return audio_tracks

def fetch_gutendex_books(client: httpx.Client, target_count: int = 512) -> list:
    print(f">>> Đang tải danh sách sách chữ & EPUB từ Gutendex (Mục tiêu: {target_count} sách)...", flush=True)
    all_books = []
    page = 1
    max_pages = (target_count // 32) + 2
    
    while len(all_books) < target_count and page <= max_pages:
        url = f"https://gutendex.com/books/?page={page}"
        print(f"    - Đang tải trang {page}/{max_pages} (Hiện có {len(all_books)} sách)...", flush=True)
        try:
            res = client.get(url, timeout=30.0)
            if res.status_code == 200:
                data = res.json()
                results = data.get("results", [])
                if not results:
                    break
                all_books.extend(results)
                page += 1
                time.sleep(0.3)
            else:
                print(f"      Cảnh báo: HTTP {res.status_code} tại trang {page}, thử lại sau 2s...", flush=True)
                time.sleep(2.0)
                continue
        except Exception as err:
            print(f"      Lỗi mạng khi tải trang {page}: {err}, tiếp tục thử lại...", flush=True)
            time.sleep(2.0)
            page += 1
            
    print(f">>> Tổng số sách tải về từ Gutendex: {len(all_books)}", flush=True)
    return all_books

def build_500_dataset() -> list:
    # Nếu file cache đã tồn tại và đủ 500 sách thì đọc trực tiếp
    if os.path.exists(DATASET_FILE):
        try:
            with open(DATASET_FILE, "r", encoding="utf-8") as f:
                cached = json.load(f)
                if len(cached) >= 480:
                    print(f">>> Nạp thành công {len(cached)} sách từ tệp cache cục bộ {DATASET_FILE}")
                    return cached
        except Exception as e:
            print(f"Lỗi đọc cache: {e}")

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) BookHub/2026"}
    with httpx.Client(headers=headers, timeout=35.0, follow_redirects=True) as client:
        # 1. Tải LibriVox Audiobooks
        audio_pool = fetch_librivox_audiobooks(client, limit=120)
        
        # 2. Tải Gutendex Books
        raw_books = fetch_gutendex_books(client, target_count=520)

    # 3. Chuẩn hóa & Xây dựng Dataset
    print(">>> Đang phân loại và định dạng dữ liệu sách...")
    dataset = []
    audio_idx = 0

    for item in raw_books:
        b_id = item.get("id")
        raw_title = item.get("title", "Không có tiêu đề").split("\r")[0].split("\n")[0].strip()
        if not raw_title or len(raw_title) < 2:
            continue
        
        # Xử lý tên tác giả
        authors = item.get("authors", [])
        author_name = format_author_name(authors[0].get("name", "")) if authors else "Tác giả cổ điển"

        # Định dạng file EPUB / PDF
        formats = item.get("formats", {})
        epub_url = formats.get("application/epub+zip") or formats.get("application/octet-stream") or formats.get("text/html") or ""
        cover_url = formats.get("image/jpeg") or "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600"

        # Phân loại thể loại
        subjects = item.get("subjects", [])
        bookshelves = item.get("bookshelves", [])
        category = classify_category(subjects, bookshelves, raw_title)

        # Gán sách nói (Audiobook)
        matched_audio = ""
        # Thử khớp tên sách với audio pool
        clean_t_lower = raw_title.lower()
        for a in audio_pool:
            if a["title"].lower() in clean_t_lower or clean_t_lower in a["title"].lower():
                matched_audio = a["audio_url"]
                break
        
        # Nếu chưa khớp thì gán luân phiên từ pool audio thực tế để sách nào cũng có thể trải nghiệm nghe audio
        if not matched_audio and audio_pool:
            matched_audio = audio_pool[audio_idx % len(audio_pool)]["audio_url"]
            audio_idx += 1

        # Mô tả tiếng Việt
        description = generate_vietnamese_description(raw_title, author_name, category, subjects)

        # Đánh giá sao ngẫu nhiên chân thực (4.3 - 5.0)
        rating_avg = round(random.uniform(4.3, 5.0), 2)
        review_count = random.randint(15, 380)

        book_record = {
            "title": raw_title[:250],
            "author": author_name[:250],
            "content": description,
            "category": category,
            "image_url": cover_url,
            "pdf_url": epub_url,
            "audio_url": matched_audio,
            "rating_avg": rating_avg,
            "review_count": review_count,
            "source": "Project Gutenberg & LibriVox",
            "external_id": f"gutenberg_{b_id}"
        }
        dataset.append(book_record)
        if len(dataset) >= 510:
            break

    # Lưu lại vào tệp JSON cache
    try:
        with open(DATASET_FILE, "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=2)
        print(f">>> Đã lưu {len(dataset)} sách vào tệp cache: {DATASET_FILE}")
    except Exception as e:
        print(f"Lỗi lưu cache: {e}")

    return dataset

def seed_database(books: list):
    print(f">>> Bắt đầu nạp {len(books)} sách vào MS SQL Server...")
    conn = get_connection()
    cur = conn.cursor()
    
    # Đảm bảo các cột mở rộng đã tồn tại
    alter_stmts = [
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'category') ALTER TABLE books ADD category NVARCHAR(100) DEFAULT N'Văn học & Tiểu thuyết';",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'rating_avg') ALTER TABLE books ADD rating_avg DECIMAL(3, 2) DEFAULT 4.8;",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'review_count') ALTER TABLE books ADD review_count INT DEFAULT 12;",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'source') ALTER TABLE books ADD source NVARCHAR(100) DEFAULT N'BookHub';",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'external_id') ALTER TABLE books ADD external_id NVARCHAR(100);"
    ]
    for s in alter_stmts:
        try:
            cur.execute(s)
        except Exception:
            pass

    # Lấy danh sách external_id hoặc title đã có sẵn để tránh duplicate
    cur.execute("SELECT title, external_id FROM books")
    existing_rows = cur.fetchall()
    existing_ext = {r['external_id'] for r in existing_rows if r.get('external_id')}
    existing_titles = {r['title'].strip().lower() for r in existing_rows if r.get('title')}

    inserted_count = 0
    updated_count = 0

    insert_sql = """
        INSERT INTO books (title, author, content, image_url, pdf_url, audio_url, category, rating_avg, review_count, source, external_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for b in books:
        ext_id = b.get("external_id")
        title_lower = b.get("title", "").strip().lower()

        if ext_id and ext_id in existing_ext:
            # Sách đã tồn tại theo external_id
            continue
        if title_lower in existing_titles:
            # Cập nhật thêm thông tin category nếu thiếu
            continue

        try:
            cur.execute(insert_sql, (
                b['title'],
                b['author'],
                b['content'],
                b['image_url'],
                b['pdf_url'],
                b['audio_url'],
                b['category'],
                float(b['rating_avg']),
                int(b['review_count']),
                b['source'],
                b['external_id']
            ))
            inserted_count += 1
            existing_ext.add(ext_id)
            existing_titles.add(title_lower)
        except Exception as e:
            print(f"Lỗi thêm sách \"{b['title']}\": {e}")

    # Kiểm tra tổng số sách trong bảng books
    cur.execute("SELECT COUNT(*) as total FROM books")
    total_books = cur.fetchone()['total']

    # Thống kê số lượng sách theo thể loại
    cur.execute("SELECT category, COUNT(*) as cnt FROM books GROUP BY category ORDER BY cnt DESC")
    stats = cur.fetchall()

    cur.close()
    conn.close()

    print("\n" + "="*60)
    print(f"🎉 HOÀN TẤT NẠP SÁCH VÀO CƠ SỞ DỮ LIỆU:")
    print(f"   - Số sách mới chèn vào DB: {inserted_count}")
    print(f"   - Tổng số sách hiện có trong DB: {total_books}")
    print("\n📊 Phân bố theo thể loại:")
    for s in stats:
        cat = s.get('category') or 'Khác'
        cnt = s.get('cnt', 0)
        print(f"   • {cat.ljust(26)}: {cnt} cuốn")
    print("="*60 + "\n")

if __name__ == "__main__":
    books = build_500_dataset()
    seed_database(books)
