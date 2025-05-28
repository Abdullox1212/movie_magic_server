from db import get_cursor
from typing import List, Optional
import psycopg2

def create_channels_table():
    """Kanallar jadvalini yaratish (agar mavjud bo'lmasa)"""
    try:
        with get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS channels (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL
                )
            ''')
        print("✅ 'channels' jadvali yaratildi yoki allaqachon mavjud.")
    except Exception as e:
        print("❌ Xatolik:", e)

def add_channel(username: str):
    """Yangi kanal qo'shish"""
    try:
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO channels (username) VALUES (%s)",
                (username.lower(),)
            )
    except psycopg2.IntegrityError:
        raise ValueError("Bu kanal allaqachon mavjud")
    except Exception as e:
        print("❌ Xatolik:", e)
        raise

def remove_channel(username: str) -> bool:
    """Kanalni o'chirish va o'chirilganligini tekshirish"""
    try:
        with get_cursor() as cursor:
            cursor.execute(
                "DELETE FROM channels WHERE username = %s",
                (username.lower(),)
            )
            return cursor.rowcount > 0
    except Exception as e:
        print("❌ Xatolik:", e)
        return False

def get_all_channels() -> List[str]:
    """Barcha kanallarni olish"""
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT username FROM channels")
            return [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print("❌ Xatolik:", e)
        return []

def channel_exists(username: str) -> bool:
    """Kanal mavjudligini tekshirish"""
    try:
        with get_cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM channels WHERE username = %s LIMIT 1",
                (username.lower(),)
            )
            return cursor.fetchone() is not None
    except Exception as e:
        print("❌ Xatolik:", e)
        return False