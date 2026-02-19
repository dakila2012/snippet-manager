import os
import sqlite3

def get_connection(db_path):
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    return sqlite3.connect(db_path)

def init_db(db_path):
    with get_connection(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                lang TEXT NOT NULL,
                code TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def add_snippet(db_path, name, lang, code):
    with get_connection(db_path) as conn:
        try:
            conn.execute("INSERT INTO snippets (name, lang, code) VALUES (?, ?, ?)", (name, lang, code))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def list_snippets(db_path):
    with get_connection(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM snippets ORDER BY created_at DESC").fetchall()
        return rows

def search_snippets(db_path, query):
    with get_connection(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM snippets WHERE name LIKE ? OR code LIKE ? OR lang LIKE ?",
            (f"%{query}%", f"%{query}%", f"%{query}%")
        ).fetchall()
        return rows

def delete_snippet(db_path, name):
    with get_connection(db_path) as conn:
        res = conn.execute("DELETE FROM snippets WHERE name = ?", (name,)).rowcount
        conn.commit()
        return res > 0
