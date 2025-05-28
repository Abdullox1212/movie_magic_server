import random
from db import get_cursor
from typing import Dict, List, Optional
import psycopg2

def create_movies_table():
    try:
        with get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movies (
                    id SERIAL PRIMARY KEY,
                    movie_code TEXT UNIQUE NOT NULL,
                    movie_link TEXT,
                    caption TEXT
                )
            ''')
        print("✅ 'movies' jadvali yaratildi yoki allaqachon mavjud.")
    except Exception as e:
        print("❌ Xatolik:", e)

def insert_movie(movie_link: str, caption: str) -> Optional[str]:
    """Yangi kino qo'shish (6 xonali noyob kod bilan)"""
    try:
        movie_code = generate_4digit_code()
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO movies (movie_code, movie_link, caption) VALUES (%s, %s, %s)",
                (movie_code, movie_link, caption)
            )
        return movie_code
    except psycopg2.IntegrityError:
        # Kod mavjud bo'lsa, qayta uriniladi
        return insert_movie(movie_link, caption)
    except Exception as e:
        print("❌ Xatolik:", e)
        return None

def get_movie_by_code(movie_code: str) -> Optional[Dict]:
    try:
        with get_cursor(dict_cursor=True) as cursor:
            cursor.execute(
                "SELECT id, movie_code, movie_link, caption FROM movies WHERE movie_code = %s",
                (movie_code,)
            )
            return cursor.fetchone()
    except Exception as e:
        print("❌ Xatolik:", e)
        return None

def get_all_movies() -> List[Dict]:
    try:
        with get_cursor(dict_cursor=True) as cursor:
            cursor.execute("SELECT id, movie_code, movie_link, caption FROM movies")
            return cursor.fetchall()
    except Exception as e:
        print("❌ Xatolik:", e)
        return []

def get_all_movies_codes() -> List[str]:
    """Barcha film kodlarini olish (optimallashtirilgan versiya)"""
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT movie_code FROM movies")
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print("❌ Xatolik:", e)
        return []

def generate_4digit_code() -> str:
    """4 xonali noyob raqamli kod generatsiya qilish"""
    existing_codes = set(get_all_movies_codes())  # Barcha mavjud kodlarni olish
    max_attempts = 200  # Maksimum urinishlar soni (xavfsizlik uchun)
    
    for _ in range(max_attempts):
        code = str(random.randint(1000, 9999))  # 1000-9999 orasida tasodifiy son
        if code not in existing_codes:
            return code
    
    raise ValueError("4 xonalik noyob kod generatsiya qilib bo'lmadi. Barcha imkoniyatlar tugadi.")