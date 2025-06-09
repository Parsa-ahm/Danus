import sqlite3
import os
import time
from typing import List, Tuple

DB_PATH = os.path.join(os.getcwd(), 'danus_memory', 'memory.db')

def _ensure_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS messages ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT, '
        'role TEXT NOT NULL, '
        'content TEXT NOT NULL, '
        'ts REAL NOT NULL'
        ')'
    )
    conn.commit()
    conn.close()


def add_message(role: str, content: str) -> None:
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO messages (role, content, ts) VALUES (?, ?, ?)',
              (role, content, time.time()))
    conn.commit()
    conn.close()


def get_history(days: int = 7) -> List[Tuple[str, str, float]]:
    _ensure_db()
    cutoff = time.time() - days * 86400
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT role, content, ts FROM messages WHERE ts >= ? ORDER BY id DESC', (cutoff,))
    rows = c.fetchall()
    conn.close()
    return rows
