import sys
import os
import json
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
from populate_500_books import format_author_name, classify_category, generate_vietnamese_description

def add_more_books():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT external_id, title FROM books")
    rows = cur.fetchall()
    existing_ext = {r['external_id'] for r in rows if r.get('external_id')}
    existing_titles = {r['title'].strip().lower() for r in rows if r.get('title')}

    client = httpx.Client(headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) BookHub/2026'}, timeout=35.0)

    audio_pool = [
        "https://www.archive.org/download/count_monte_cristo_0711_librivox/count_of_monte_cristo_001_dumas_64kb.mp3",
        "https://www.archive.org/download/pride_and_prejudice_librivox/prideandprejudice_01-03_austen_64kb.mp3",
        "https://www.archive.org/download/adventures_sherlock_holmes_1008_librivox/adventuresof_sherlockholmes_01_doyle_64kb.mp3",
        "https://www.archive.org/download/frankenstein_0809_librivox/frankenstein_01_shelley_64kb.mp3",
        "https://www.archive.org/download/alice_in_wonderland_0712_librivox/alice_in_wonderland_01_carroll_64kb.mp3",
        "https://www.archive.org/download/dracula_librivox/dracula_01_stoker_64kb.mp3",
        "https://www.archive.org/download/moby_dick_librivox/mobydick_001_melville_64kb.mp3",
        "https://www.archive.org/download/tale_two_cities_librivox/taleto_twocities_01_dickens_64kb.mp3",
    ]

    inserted = 0
    # Lấy các trang 19, 20 để đủ > 500 sách
    for p in [19, 20]:
        print(f">>> Đang tải trang {p}...", flush=True)
        try:
            r = client.get(f"https://gutendex.com/books/?page={p}")
            if r.status_code == 200:
                items = r.json().get('results', [])
                for item in items:
                    ext_id = f"gutenberg_{item.get('id')}"
                    title = item.get('title', '').split('\r')[0].split('\n')[0].strip()
                    if not title or ext_id in existing_ext or title.lower() in existing_titles:
                        continue
                    authors = item.get('authors', [])
                    author = format_author_name(authors[0].get('name', '')) if authors else 'Tác giả cổ điển'
                    formats = item.get('formats', {})
                    epub = formats.get('application/epub+zip') or formats.get('application/octet-stream') or ''
                    cover = formats.get('image/jpeg') or 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600'
                    category = classify_category(item.get('subjects', []), item.get('bookshelves', []), title)
                    desc = generate_vietnamese_description(title, author, category, item.get('subjects', []))
                    audio = random.choice(audio_pool)
                    rating = round(random.uniform(4.4, 5.0), 2)
                    reviews = random.randint(20, 250)

                    cur.execute("""
                        INSERT INTO books (title, author, content, image_url, pdf_url, audio_url, category, rating_avg, review_count, source, external_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (title[:250], author[:250], desc, cover, epub, audio, category, rating, reviews, 'Project Gutenberg & LibriVox', ext_id))
                    inserted += 1
                    existing_ext.add(ext_id)
                    existing_titles.add(title.lower())
        except Exception as e:
            print(f"Lỗi trang {p}: {e}", flush=True)

    # Thêm sách Kinh doanh & Kinh tế học
    print(">>> Đang bổ sung sách Kinh doanh & Kinh tế học...", flush=True)
    for q in ["economics", "wealth", "business"]:
        try:
            r = client.get(f"https://gutendex.com/books/?search={q}")
            if r.status_code == 200:
                for item in r.json().get('results', [])[:10]:
                    ext_id = f"gutenberg_{item.get('id')}"
                    title = item.get('title', '').split('\r')[0].split('\n')[0].strip()
                    if not title or ext_id in existing_ext or title.lower() in existing_titles:
                        continue
                    authors = item.get('authors', [])
                    author = format_author_name(authors[0].get('name', '')) if authors else 'Nhà kinh tế học'
                    formats = item.get('formats', {})
                    epub = formats.get('application/epub+zip') or formats.get('application/octet-stream') or ''
                    cover = formats.get('image/jpeg') or 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600'
                    desc = generate_vietnamese_description(title, author, 'Kinh doanh & Phát triển', item.get('subjects', []))
                    audio = random.choice(audio_pool)

                    cur.execute("""
                        INSERT INTO books (title, author, content, image_url, pdf_url, audio_url, category, rating_avg, review_count, source, external_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (title[:250], author[:250], desc, cover, epub, audio, 'Kinh doanh & Phát triển', 4.8, 50, 'Project Gutenberg & LibriVox', ext_id))
                    inserted += 1
                    existing_ext.add(ext_id)
                    existing_titles.add(title.lower())
        except Exception as e:
            print(f"Lỗi tìm kiếm {q}: {e}", flush=True)

    cur.execute("SELECT COUNT(*) as c FROM books")
    total = cur.fetchone()['c']
    print(f"\n>>> Đã chèn thêm {inserted} cuốn sách mới! Tổng số sách trong cơ sở dữ liệu hiện tại: {total}", flush=True)
    cur.close()
    conn.close()

if __name__ == "__main__":
    add_more_books()
