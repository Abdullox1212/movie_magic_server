import sqlite3
import random
import string

def create_movies_table():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_code TEXT UNIQUE NOT NULL,
            movie_link TEXT,
            caption TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_movie(movie_link: str, caption: str):
    """Yangi kino qo'shish (6 xonali kod avtomatik generatsiya qilinadi)"""
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    
    try:
        movie_code = generate_6digit_code()
        cursor.execute(
            "INSERT INTO movies (movie_code, movie_link, caption) VALUES (?, ?, ?)",
            (movie_code, movie_link, caption)
        )
        conn.commit()
        return movie_code
    except sqlite3.IntegrityError:
        # Agar kod allaqachon mavjud bo'lsa (juda kam ehtimol)
        return insert_movie(movie_link, caption)  # Qayta urinib ko'ramiz
    finally:
        conn.close()

def get_movie_by_code(movie_code: str):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, movie_code, movie_link, caption FROM movies WHERE movie_code = ?",
        (movie_code,)
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "movie_code": row[1],
            "movie_link": row[2],
            "caption": row[3]
        }
    return None


def get_all_movies():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("SELECT id, movie_code, movie_link, caption FROM movies")
    rows = cursor.fetchall()
    conn.close()

    movies = []
    for row in rows:
        movies.append({
            "id": row[0],
            "movie_code": row[1],
            "movie_link": row[2],
            "caption": row[3]
        })
    return movies


def get_all_movies_codes():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("SELECT movie_code FROM movies")
    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


def generate_6digit_code():
    """6 xonali noyob raqamli kod generatsiya qilish"""
    while True:
        # 100000 dan 999999 gacha random raqam
        code = str(random.randint(100000, 999999))
        
        # Kod bazada mavjudligini tekshirish
        if not get_movie_by_code(code):
            return code