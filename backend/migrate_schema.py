import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from database import get_connection

def migrate():
    conn = get_connection()
    cur = conn.cursor()
    alter_stmts = [
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'category') ALTER TABLE books ADD category NVARCHAR(100) DEFAULT N'Tiểu thuyết';",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'rating_avg') ALTER TABLE books ADD rating_avg DECIMAL(3, 2) DEFAULT 4.8;",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'review_count') ALTER TABLE books ADD review_count INT DEFAULT 12;",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'source') ALTER TABLE books ADD source NVARCHAR(100) DEFAULT N'BookHub';",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'external_id') ALTER TABLE books ADD external_id NVARCHAR(100);"
    ]
    for s in alter_stmts:
        try:
            cur.execute(s)
        except Exception as e:
            print("Alter error:", e)
    
    cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'books'")
    cols = [r['COLUMN_NAME'] for r in cur.fetchall()]
    print("Updated columns in books table:", cols)
    cur.close()
    conn.close()

if __name__ == "__main__":
    migrate()
