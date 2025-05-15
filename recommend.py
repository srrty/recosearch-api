import sqlite3
from difflib import get_close_matches

def recommend_related(keyword: str, db_path: str, max_recs: int = 5) -> list[str]:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT keyword FROM searches")
    all_keywords = [row[0] for row in cur.fetchall()]
    conn.close()
    return get_close_matches(keyword, all_keywords, n=max_recs, cutoff=0.4)
