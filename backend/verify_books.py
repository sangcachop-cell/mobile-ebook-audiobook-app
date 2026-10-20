import sys
sys.stdout.reconfigure(encoding='utf-8')
from backend.database import get_connection

conn = get_connection()
cursor = conn.cursor()

# Cập nhật các sách
cursor.execute("UPDATE books SET audio_url = 'uploads/nghi_giau_va_lam_giau.mp3' WHERE title = N'Nghĩ Giàu Và Làm Giàu'")
cursor.execute("UPDATE books SET audio_url = 'uploads/kheo_an_noi_se_co_duoc_thien_ha.mp3' WHERE title = N'Khéo Ăn Nói Sẽ Có Được Thiên Hạ'")
cursor.execute("UPDATE books SET audio_url = 'uploads/doc_vi_bat_ky_ai.mp3' WHERE title = N'Đọc Vị Bất Kỳ Ai'")
cursor.execute("UPDATE books SET audio_url = 'uploads/buoc_cham_lai_giua_the_gian_voi_va.mp3' WHERE title = N'Bước Chậm Lại Giữa Thế Gian Vội Vã'")
conn.commit()

cursor.execute("SELECT id, title, author, category, pdf_url, audio_url, LEN(content) as content_length FROM books ORDER BY id ASC")
books = cursor.fetchall()
print(f"Tổng số sách tiếng Việt trong cơ sở dữ liệu: {len(books)} cuốn.\n")
print(f"{'ID':<5} | {'Tên Sách':<30} | {'Tác Giả':<22} | {'Tệp Đọc':<28} | {'Audio Sách Nói':<32} | {'Độ dài chữ'}")
print("-" * 135)
for b in books:
    print(f"{b['id']:<5} | {b['title'][:29]:<30} | {b['author'][:21]:<22} | {b['pdf_url']:<28} | {b['audio_url']:<32} | {b['content_length']} ký tự")

conn.close()
