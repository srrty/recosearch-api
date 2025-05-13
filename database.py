import sqlite3

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS searches (keyword TEXT, result TEXT)''')
    conn.commit()
    conn.close()

def save_search(keyword, result):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO searches (keyword, result) VALUES (?, ?)", (keyword, result))
    conn.commit()
    conn.close()
