import random
import psycopg2
from main import DATABASE_URL

def create_movies_table():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id SERIAL PRIMARY KEY,
                movie_code TEXT UNIQUE NOT NULL,
                movie_link TEXT,
                caption TEXT
            )
        ''')

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ 'movies' jadvali yaratildi yoki allaqachon mavjud.")
    except Exception as e:
        print("❌ Xatolik:", e)


def insert_movie(movie_link: str, caption: str):
    """Yangi kino qo‘shish (6 xonali noyob kod bilan)"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        movie_code = generate_6digit_code()

        cursor.execute(
            "INSERT INTO movies (movie_code, movie_link, caption) VALUES (%s, %s, %s)",
            (movie_code, movie_link, caption)
        )
        conn.commit()

        return movie_code
    except psycopg2.IntegrityError:
        # Kod mavjud bo‘lsa, qayta uriniladi
        conn.rollback()
        return insert_movie(movie_link, caption)
    except Exception as e:
        print("❌ Xatolik:", e)
    finally:
        cursor.close()
        conn.close()


def get_movie_by_code(movie_code: str):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, movie_code, movie_link, caption FROM movies WHERE movie_code = %s",
            (movie_code,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "movie_code": row[1],
                "movie_link": row[2],
                "caption": row[3]
            }
        return None
    except Exception as e:
        print("❌ Xatolik:", e)
        return None
    finally:
        cursor.close()
        conn.close()


def get_all_movies():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT id, movie_code, movie_link, caption FROM movies")
        rows = cursor.fetchall()

        movies = []
        for row in rows:
            movies.append({
                "id": row[0],
                "movie_code": row[1],
                "movie_link": row[2],
                "caption": row[3]
            })
        return movies
    except Exception as e:
        print("❌ Xatolik:", e)
        return []
    finally:
        cursor.close()
        conn.close()


def get_all_movies_codes():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT movie_code FROM movies")
        rows = cursor.fetchall()

        return [row[0] for row in rows]
    except Exception as e:
        print("❌ Xatolik:", e)
        return []
    finally:
        cursor.close()
        conn.close()


def generate_6digit_code():
    """6 xonali noyob raqamli kod generatsiya qilish"""
    while True:
        code = str(random.randint(100000, 999999))
        if not get_movie_by_code(code):
            return code
