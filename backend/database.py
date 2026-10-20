import pyodbc
import re

# Cau hinh ket noi SQL Server
SERVER_NAME = r".\MSSQLSERVER08"
DATABASE_NAME = "ebook_app"

CONNECTION_STRING = (
    "Driver={ODBC Driver 17 for SQL Server};"
    f"Server={SERVER_NAME};"
    f"Database={DATABASE_NAME};"
    "Trusted_Connection=yes;"
)

class MSSQLCursor:
    def __init__(self, pyodbc_cursor):
        self._cursor = pyodbc_cursor
        self.lastrowid = None

    def execute(self, sql, params=None):
        # Chuyen doi %s cua MySQL sang ? cua SQL Server / pyodbc
        sql_converted = sql.replace("%s", "?")
        
        # Xu ly cau lenh SELECT dac thu neu can
        if params is not None:
            if not isinstance(params, (list, tuple)):
                params = (params,)
            res = self._cursor.execute(sql_converted, params)
        else:
            res = self._cursor.execute(sql_converted)

        # Xu ly lay lastrowid cho cac cau lenh INSERT
        stripped = sql.strip().upper()
        if stripped.startswith("INSERT"):
            try:
                id_cur = self._cursor.connection.cursor()
                id_cur.execute("SELECT @@IDENTITY")
                row = id_cur.fetchone()
                if row and row[0] is not None:
                    self.lastrowid = int(row[0])
                id_cur.close()
            except Exception:
                pass
        return res

    def fetchone(self):
        row = self._cursor.fetchone()
        if row is None:
            return None
        columns = [col[0] for col in self._cursor.description]
        return dict(zip(columns, row))

    def fetchall(self):
        if not self._cursor.description:
            return []
        columns = [col[0] for col in self._cursor.description]
        rows = self._cursor.fetchall()
        return [dict(zip(columns, r)) for r in rows]

    def close(self):
        try:
            self._cursor.close()
        except Exception:
            pass

class MSSQLConnection:
    def __init__(self):
        self._conn = pyodbc.connect(CONNECTION_STRING, autocommit=True)

    def cursor(self):
        return MSSQLCursor(self._conn.cursor())

    def commit(self):
        try:
            self._conn.commit()
        except Exception:
            pass

    def close(self):
        try:
            self._conn.close()
        except Exception:
            pass

def get_connection():
    return MSSQLConnection()

def init_db():
    # Kiem tra va tao database neu chua ton tai
    try:
        master_conn = pyodbc.connect(
            f"Driver={{ODBC Driver 17 for SQL Server}};Server={SERVER_NAME};Database=master;Trusted_Connection=yes;",
            autocommit=True
        )
        m_cur = master_conn.cursor()
        m_cur.execute(f"IF DB_ID('{DATABASE_NAME}') IS NULL CREATE DATABASE [{DATABASE_NAME}];")
        m_cur.close()
        master_conn.close()
    except Exception as e:
        print(f"Lỗi kiểm tra/tạo database: {e}")

    conn = get_connection()
    cursor = conn.cursor()
    
    tables_ddl = [
        """
        IF OBJECT_ID('books', 'U') IS NULL
        CREATE TABLE books (
            id INT IDENTITY(1,1) PRIMARY KEY,
            title NVARCHAR(500) NOT NULL,
            author NVARCHAR(500),
            content NVARCHAR(MAX),
            audio_url NVARCHAR(1000),
            image_url NVARCHAR(1000),
            pdf_url NVARCHAR(1000),
            category NVARCHAR(100) DEFAULT N'Văn học & Tiểu thuyết',
            rating_avg DECIMAL(3, 2) DEFAULT 4.8,
            review_count INT DEFAULT 12,
            source NVARCHAR(100) DEFAULT N'Project Gutenberg & LibriVox',
            external_id NVARCHAR(100)
        )
        """,
        """
        IF OBJECT_ID('shop_books', 'U') IS NULL
        CREATE TABLE shop_books (
            id INT IDENTITY(1,1) PRIMARY KEY,
            title NVARCHAR(255) NOT NULL,
            author NVARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            image_path NVARCHAR(500),
            description NVARCHAR(MAX),
            created_at DATETIME DEFAULT GETDATE()
        )
        """,
        """
        IF OBJECT_ID('users', 'U') IS NULL
        CREATE TABLE users (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(100) UNIQUE NOT NULL,
            password NVARCHAR(100) NOT NULL,
            is_admin BIT DEFAULT 0,
            full_name NVARCHAR(255),
            avatar_url NVARCHAR(500)
        )
        """,
        """
        IF OBJECT_ID('bookmarks', 'U') IS NULL
        CREATE TABLE bookmarks (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(100) NOT NULL,
            book_id INT NOT NULL,
            page_number INT NOT NULL,
            note NVARCHAR(MAX),
            created_at DATETIME DEFAULT GETDATE(),
            CONSTRAINT UQ_bookmark_user_book_page UNIQUE (username, book_id, page_number),
            CONSTRAINT FK_bookmark_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        )
        """,
        """
        IF OBJECT_ID('posts', 'U') IS NULL
        CREATE TABLE posts (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(100) NOT NULL,
            content NVARCHAR(MAX) NOT NULL,
            image_url NVARCHAR(500),
            status NVARCHAR(50) DEFAULT 'pending',
            created_at DATETIME DEFAULT GETDATE()
        )
        """,
        """
        IF OBJECT_ID('likes', 'U') IS NULL
        CREATE TABLE likes (
            id INT IDENTITY(1,1) PRIMARY KEY,
            post_id INT NOT NULL,
            username NVARCHAR(100) NOT NULL,
            CONSTRAINT UQ_like_user_post UNIQUE (username, post_id),
            CONSTRAINT FK_like_post FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
        )
        """,
        """
        IF OBJECT_ID('comments', 'U') IS NULL
        CREATE TABLE comments (
            id INT IDENTITY(1,1) PRIMARY KEY,
            post_id INT NOT NULL,
            username NVARCHAR(100) NOT NULL,
            content NVARCHAR(MAX) NOT NULL,
            created_at DATETIME DEFAULT GETDATE(),
            CONSTRAINT FK_comment_post FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
        )
        """,
        """
        IF OBJECT_ID('orders', 'U') IS NULL
        CREATE TABLE orders (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(100) NOT NULL,
            full_name NVARCHAR(255) NOT NULL,
            phone NVARCHAR(50) NOT NULL,
            address NVARCHAR(MAX) NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL,
            status NVARCHAR(50) DEFAULT 'pending',
            created_at DATETIME DEFAULT GETDATE()
        )
        """,
        """
        IF OBJECT_ID('order_items', 'U') IS NULL
        CREATE TABLE order_items (
            id INT IDENTITY(1,1) PRIMARY KEY,
            order_id INT NOT NULL,
            book_id INT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            CONSTRAINT FK_orderitem_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            CONSTRAINT FK_orderitem_book FOREIGN KEY (book_id) REFERENCES shop_books(id) ON DELETE CASCADE
        )
        """,
        """
        IF OBJECT_ID('reading_progress', 'U') IS NULL
        CREATE TABLE reading_progress (
            id INT IDENTITY(1,1) PRIMARY KEY,
            username NVARCHAR(100) NOT NULL,
            book_id INT NOT NULL,
            last_page INT DEFAULT 0,
            last_epub_cfi NVARCHAR(500),
            last_audio_position_ms INT DEFAULT 0,
            progress_percent DECIMAL(5, 2) DEFAULT 0.0,
            updated_at DATETIME DEFAULT GETDATE(),
            CONSTRAINT UQ_progress_user_book UNIQUE (username, book_id),
            CONSTRAINT FK_progress_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        )
        """,
        """
        IF OBJECT_ID('book_reviews', 'U') IS NULL
        CREATE TABLE book_reviews (
            id INT IDENTITY(1,1) PRIMARY KEY,
            book_id INT NOT NULL,
            username NVARCHAR(100) NOT NULL,
            rating INT NOT NULL,
            comment NVARCHAR(MAX),
            created_at DATETIME DEFAULT GETDATE(),
            CONSTRAINT FK_review_book FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
        )
        """,
        """
        IF OBJECT_ID('bookmarks', 'U') IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('bookmarks') AND name = 'audio_position_ms'
        )
        ALTER TABLE bookmarks ADD audio_position_ms INT DEFAULT 0;
        """,
        """
        IF OBJECT_ID('users', 'U') IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('users') AND name = 'email'
        )
        ALTER TABLE users ADD email NVARCHAR(255);
        """,
        """
        IF OBJECT_ID('users', 'U') IS NOT NULL AND NOT EXISTS (
            SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('users') AND name = 'phone'
        )
        ALTER TABLE users ADD phone NVARCHAR(50);
        """
    ]

    for ddl in tables_ddl:
        try:
            cursor.execute(ddl)
        except Exception as e:
            print(f"Lỗi tạo bảng: {e}")

    # Tao tai khoan admin mac dinh neu chua co
    try:
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password, is_admin, full_name) VALUES ('admin', '123', 1, N'Quản trị viên')")
            print(f">>> Da tao tai khoan admin mac dinh (admin / 123) tren {SERVER_NAME} / {DATABASE_NAME}")
    except Exception as e:
        print(f"Lỗi tạo admin: {e}")

    # Tao sach mac dinh neu chua co
    try:
        cursor.execute("SELECT COUNT(*) as cnt FROM books")
        row = cursor.fetchone()
        if not row or row.get('cnt', 0) == 0:
            dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books_500_dataset.json")
            if os.path.exists(dataset_path):
                import json
                with open(dataset_path, "r", encoding="utf-8") as f:
                    books_data = json.load(f)
                for b in books_data:
                    cursor.execute(
                        """
                        INSERT INTO books (title, author, content, image_url, pdf_url, audio_url, category, rating_avg, review_count, source, external_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            b.get('title', '')[:250],
                            b.get('author', '')[:250],
                            b.get('content', ''),
                            b.get('image_url', ''),
                            b.get('pdf_url', ''),
                            b.get('audio_url', ''),
                            b.get('category', 'Văn học & Tiểu thuyết'),
                            float(b.get('rating_avg', 4.8)),
                            int(b.get('review_count', 12)),
                            b.get('source', 'Project Gutenberg & LibriVox'),
                            b.get('external_id', '')
                        )
                    )
                print(f">>> Da nap thanh cong {len(books_data)} sach tu kho du lieu books_500_dataset.json!")
            else:
                sample_books = [
                    ("Đắc Nhân Tâm", "Dale Carnegie", "Học cách thu phục lòng người và thành công trong cuộc sống.", "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600", "uploads/dac_nhan_tam.pdf", "uploads/audio_sample_1.mp3", "Kinh doanh & Phát triển"),
                    ("Nhà Giả Kim", "Paulo Coelho", "Hành trình theo đuổi ước mơ và lắng nghe tiếng gọi trái tim.", "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600", "uploads/nha_gia_kim.epub", "uploads/audio_sample_2.mp3", "Văn học & Tiểu thuyết"),
                    ("Tuổi Trẻ Đáng Giá Bao Nhiêu", "Rosie Nguyễn", "Cuốn sách thức tỉnh người trẻ sống hết mình và theo đuổi đam mê.", "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=600", "uploads/tuoi_tre_dang_gia_bao_nhieu.pdf", "uploads/audio_sample_1.mp3", "Tâm lý & Xã hội"),
                    ("Nghĩ Giàu Và Làm Giàu", "Napoleon Hill", "Triết lý thành công được đúc kết từ hàng trăm nhân vật vĩ đại.", "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=600", "uploads/nghi_giau_lam_giau.pdf", "uploads/audio_sample_2.mp3", "Kinh doanh & Phát triển"),
                ]
                for title, author, desc, img, pdf, audio, cat in sample_books:
                    cursor.execute(
                        "INSERT INTO books (title, author, content, image_url, pdf_url, audio_url, category) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (title, author, desc, img, pdf, audio, cat)
                    )
                print(">>> Da tao danh sach sach dien tu & sach noi mac dinh thanh cong!")
    except Exception as e:
        print(f"Lỗi tạo sách mặc định: {e}")

    # Tao sach ban gian hang mac dinh neu chua co
    try:
        cursor.execute("SELECT COUNT(*) as cnt FROM shop_books")
        row = cursor.fetchone()
        if not row or row.get('cnt', 0) == 0:
            sample_shop = [
                ("Đắc Nhân Tâm (Bìa cứng đặc biệt)", "Dale Carnegie", 125000, "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600", "Bản in cao cấp bìa cứng dập nổi kim tuyến, giấy xốp chống cận thị."),
                ("Nhà Giả Kim (Ấn bản kỷ niệm)", "Paulo Coelho", 89000, "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600", "Tác phẩm bán chạy thứ hai thế giới sau Kinh Thánh, truyền cảm hứng sống."),
                ("Tư Duy Nhanh Và Chậm", "Daniel Kahneman", 165000, "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=600", "Kiệt tác về tâm lý học hành vi và kinh tế học nhận giải Nobel."),
                ("Sức Mạnh Của Thói Quen", "Charles Duhigg", 115000, "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=600", "Khám phá cơ chế hình thành và thay đổi thói quen để làm chủ cuộc đời."),
            ]
            for title, author, price, img, desc in sample_shop:
                cursor.execute(
                    "INSERT INTO shop_books (title, author, price, image_path, description) VALUES (%s, %s, %s, %s, %s)",
                    (title, author, price, img, desc)
                )
            print(">>> Da tao danh sach sach ban gian hang mac dinh thanh cong!")
    except Exception as e:
        print(f"Lỗi tạo sách bán mặc định: {e}")

    cursor.close()
    conn.close()
