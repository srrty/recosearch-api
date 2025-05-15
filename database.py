import sqlite3
import json
from datetime import datetime


DEFAULT_DB = "searches.db"

def init_db(db_path: str = DEFAULT_DB):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            results TEXT NOT NULL,
            searched_at TIMESTAMP NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def save_search(keyword: str, results: list[dict], db_path: str = DEFAULT_DB):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO searches (keyword, results, searched_at) VALUES (?, ?, ?)"
        , (keyword, json.dumps(results, ensure_ascii=False), datetime.utcnow())
    )
    conn.commit()
    conn.close()