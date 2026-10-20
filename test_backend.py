import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from starlette.testclient import TestClient
from main import app

client = TestClient(app)

def run_tests():
    print("=== STARTING BACKEND END-TO-END TESTS ===")
    passed = 0
    total = 0

    # Test 1: Get books
    total += 1
    res = client.get("/api/books")
    assert res.status_code == 200, f"Get books failed: {res.status_code}"
    print(f"[PASS] 1. GET /api/books: status={res.status_code}, count={len(res.json())}")
    passed += 1

    # Test 2: Get shop books
    total += 1
    res = client.get("/api/shop-books")
    assert res.status_code == 200, f"Get shop books failed: {res.status_code}"
    print(f"[PASS] 2. GET /api/shop-books: status={res.status_code}, count={len(res.json())}")
    passed += 1

    # Test 3: Progress update
    total += 1
    progress_payload = {
        "username": "test_e2e_user",
        "book_id": 1,
        "last_page": 15,
        "last_epub_cfi": "cfi_test_123",
        "last_audio_position_ms": 45000,
        "progress_percent": 30.5
    }
    res = client.post("/api/progress/update", json=progress_payload)
    assert res.status_code == 200, f"Update progress failed: {res.status_code}"
    print(f"[PASS] 3. POST /api/progress/update: status={res.status_code}, body={res.json()}")
    passed += 1

    # Test 4: Get user progress
    total += 1
    res = client.get("/api/progress/test_e2e_user")
    assert res.status_code == 200, f"Get user progress failed: {res.status_code}"
    print(f"[PASS] 4. GET /api/progress/test_e2e_user: status={res.status_code}, records={len(res.json())}")
    passed += 1

    # Test 5: Post book review
    total += 1
    review_payload = {
        "book_id": 1,
        "username": "test_e2e_user",
        "rating": 5,
        "comment": "Tuyệt vời, sách rất ý nghĩa và sâu sắc!"
    }
    res = client.post("/api/books/1/reviews", json=review_payload)
    assert res.status_code == 200, f"Post review failed: {res.status_code}"
    review_id = res.json().get("review_id")
    print(f"[PASS] 5. POST /api/books/1/reviews: status={res.status_code}, review_id={review_id}")
    passed += 1

    # Test 6: Get book reviews
    total += 1
    res = client.get("/api/books/1/reviews")
    assert res.status_code == 200, f"Get reviews failed: {res.status_code}"
    data = res.json()
    assert "average_rating" in data and "total_reviews" in data
    print(f"[PASS] 6. GET /api/books/1/reviews: avg_rating={data['average_rating']}, total={data['total_reviews']}")
    passed += 1

    # Test 7: Delete book review
    if review_id:
        total += 1
        res = client.delete(f"/api/reviews/{review_id}?username=test_e2e_user")
        assert res.status_code == 200, f"Delete review failed: {res.status_code}"
        print(f"[PASS] 7. DELETE /api/reviews/{review_id}: status={res.status_code}, msg={res.json()}")
        passed += 1

    # Test 8: Get feed posts
    total += 1
    res = client.get("/api/feed/posts?current_user=test_e2e_user")
    assert res.status_code == 200, f"Get feed posts failed: {res.status_code}"
    print(f"[PASS] 8. GET /api/feed/posts: status={res.status_code}, count={len(res.json())}")
    passed += 1

    # Test 9: Forgot Password
    total += 1
    forgot_payload = {
        "username": "admin",
        "new_password": "admin123"
    }
    res = client.post("/api/auth/forgot-password", json=forgot_payload)
    assert res.status_code == 200, f"Forgot password failed: {res.status_code}, {res.text}"
    print(f"[PASS] 9. POST /api/auth/forgot-password: status={res.status_code}, msg={res.json()}")
    passed += 1

    # Reset admin password back
    client.post("/api/auth/forgot-password", json={"username": "admin", "new_password": "123"})

    # Test 10: Audio Bookmark toggle & get
    total += 1
    audio_bm_payload = {
        "username": "admin",
        "book_id": 1,
        "page_number": 0,
        "audio_position_ms": 75000,
        "note": "Đoạn hay phút 1:15"
    }
    res = client.post("/api/bookmarks/toggle", json=audio_bm_payload)
    assert res.status_code == 200, f"Audio bookmark toggle failed: {res.status_code}"
    print(f"[PASS] 10. POST /api/bookmarks/toggle: status={res.status_code}, res={res.json()}")
    passed += 1

    # Test 11: Get book bookmarks
    total += 1
    res = client.get("/api/bookmarks/admin/1")
    assert res.status_code == 200, f"Get book bookmarks failed: {res.status_code}"
    bms = res.json()
    assert len(bms) >= 1, "Expected at least 1 bookmark"
    print(f"[PASS] 11. GET /api/bookmarks/admin/1: status={res.status_code}, count={len(bms)}")
    passed += 1

    # Test 12: Get categories
    total += 1
    res = client.get("/api/categories")
    assert res.status_code == 200, f"Get categories failed: {res.status_code}"
    cats = res.json()
    assert len(cats) >= 5, "Expected at least 5 categories"
    print(f"[PASS] 12. GET /api/categories: status={res.status_code}, category_count={len(cats)}")
    passed += 1

    # Test 13: Online Book Search (Gutendex, LibriVox, Open Library)
    total += 1
    res = client.get("/api/admin/online-books/search?query=sherlock&source=all")
    assert res.status_code == 200, f"Online search failed: {res.status_code}"
    search_results = res.json()
    print(f"[PASS] 13. GET /api/admin/online-books/search: status={res.status_code}, found={len(search_results)} online books")
    passed += 1

    # Test 14: Admin Online Book Import
    total += 1
    import_payload = {
        "username": "admin",
        "title": "Test Online Imported Book E2E",
        "author": "Arthur Conan Doyle",
        "category": "Trinh thám & Bí ẩn",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600",
        "pdf_url": "https://www.gutenberg.org/ebooks/1661.epub3.images",
        "audio_url": "https://www.archive.org/download/adventures_sherlock_holmes_1008_librivox/adventuresof_sherlockholmes_01_doyle_64kb.mp3",
        "content": "Cuốn sách mẫu kiểm thử tính năng Admin tải sách từ nguồn online vào kho sách.",
        "source": "Gutendex (Project Gutenberg)",
        "external_id": "test_e2e_import_9999"
    }
    res = client.post("/api/admin/online-books/import", json=import_payload)
    assert res.status_code == 200, f"Import book failed: {res.status_code}, {res.text}"
    imp_data = res.json()
    assert imp_data.get("status") in ["success", "already_exists"]
    print(f"[PASS] 14. POST /api/admin/online-books/import: status={res.status_code}, res={imp_data}")
    passed += 1

    # Test 15: Proxy file with Gutenberg URL
    total += 1
    res = client.get("/api/proxy-file?url=https%3A%2F%2Fwww.gutenberg.org%2Fcache%2Fepub%2F39955%2Fpg39955.epub")
    assert res.status_code == 200, f"Proxy file failed: {res.status_code}"
    assert len(res.content) > 1000, "Expected non-empty EPUB content"
    print(f"[PASS] 15. GET /api/proxy-file (Gutenberg 39955 The Dawn of Day): status={res.status_code}, size={len(res.content)} bytes, content_type={res.headers.get('content-type')}")
    passed += 1

    # Test 16: Proxy file fallback (when invalid or blocked remote URL is provided)
    total += 1
    res = client.get("/api/proxy-file?url=https%3A%2F%2Fnonexistent-fake-domain-12345.org%2Finvalid.epub")
    assert res.status_code == 200, f"Proxy fallback failed: {res.status_code}"
    assert len(res.content) > 1000, "Expected non-empty fallback content"
    print(f"[PASS] 16. GET /api/proxy-file fallback resilience: status={res.status_code}, size={len(res.content)} bytes, content_type={res.headers.get('content-type')}")
    passed += 1

    print(f"\n>>> ALL {passed}/{total} BACKEND TESTS PASSED SUCCESSFULLY! <<<\n")

if __name__ == "__main__":
    run_tests()
