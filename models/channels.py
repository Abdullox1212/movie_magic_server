import psycopg2
from main import DATABASE_URL

def create_channels_table():
    """Kanallar jadvalini yaratish (agar mavjud bo‘lmasa)"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()
    except Exception as e:
        print("❌ Xatolik:", e)
    finally:
        cursor.close()
        conn.close()


def add_channel(username: str):
    """Yangi kanal qo‘shish"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO channels (username) VALUES (%s)",
            (username.lower(),)
        )
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        raise ValueError("Bu kanal allaqachon mavjud")
    except Exception as e:
        print("❌ Xatolik:", e)
    finally:
        cursor.close()
        conn.close()


def remove_channel(username: str):
    """Kanalni o‘chirish"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM channels WHERE username = %s",
            (username.lower(),)
        )
        conn.commit()
    except Exception as e:
        print("❌ Xatolik:", e)
    finally:
        cursor.close()
        conn.close()


def get_all_channels():
    """Barcha kanallarni olish"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM channels")
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        print("❌ Xatolik:", e)
        return []
    finally:
        cursor.close()
        conn.close()


def channel_exists(username: str) -> bool:
    """Kanal mavjudligini tekshirish"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM channels WHERE username = %s LIMIT 1",
            (username.lower(),)
        )
        exists = cursor.fetchone() is not None
        return exists
    except Exception as e:
        print("❌ Xatolik:", e)
        return False
    finally:
        cursor.close()
        conn.close()
