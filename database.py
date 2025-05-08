import sqlite3
from pathlib import Path

db_path = Path("data/flashcards.db")
db_path.parent.mkdir(exist_ok=True)

def init_db():
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                acronym TEXT NOT NULL,
                meaning TEXT NOT NULL
            )
        """)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                flashcard_id INTEGER,
                user_id INTEGER,
                correct BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                interval INTEGER DEFAULT 1,
                next_due DATETIME,
                FOREIGN KEY(flashcard_id) REFERENCES flashcards(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
         )
        ''')
        conn.commit()

import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(conn, name, password):
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, password_hash FROM users WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row:
        user_id, stored_hash = row
        return user_id if hash_password(password) == stored_hash else None
    return None
