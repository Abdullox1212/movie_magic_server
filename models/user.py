from db import get_cursor
from typing import List, Dict, Optional
import psycopg2

def create_users_table():
    try:
        with get_cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    full_name TEXT,
                    username TEXT,
                    is_administrator BOOLEAN DEFAULT FALSE,
                    is_blocked BOOLEAN DEFAULT FALSE,
                    subscribed BOOLEAN DEFAULT FALSE
                )
            ''')
        print("\u2705 Jadval yaratildi yoki allaqachon mavjud.")
    except Exception as e:
        print("\u274C Xatolik:", e)

def insert_user(user_id: int, full_name: str, username: str):
    try:
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (id, full_name, username) VALUES (%s, %s, %s)",
                (user_id, full_name, username)
            )
    except psycopg2.IntegrityError:
        raise ValueError("Bu ID allaqachon mavjud")

def get_all_users() -> List[Dict]:
    with get_cursor(dict_cursor=True) as cursor:
        cursor.execute("SELECT id, full_name, username, subscribed FROM users")
        return cursor.fetchall()

def get_user(user_id: int) -> bool:
    try:
        with get_cursor() as cursor:
            cursor.execute(
                'SELECT 1 FROM users WHERE id = %s LIMIT 1',
                (user_id,)
            )
            return cursor.fetchone() is not None
    except Exception:
        return False

def is_subscribed(user_id: int) -> bool:
    with get_cursor() as cursor:
        cursor.execute("SELECT subscribed FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        return row[0] if row else False

def update_subscription_status(user_id: int, status: bool):
    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE users SET subscribed = %s WHERE id = %s",
            (status, user_id)
        )

def get_all_users_ids() -> List[int]:
    with get_cursor() as cursor:
        cursor.execute("SELECT id FROM users")
        return [row[0] for row in cursor.fetchall()]

def set_admin_status(user_id: int, is_admin: bool):
    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE users SET is_administrator = %s WHERE id = %s",
            (is_admin, user_id)
        )

def get_admins() -> List[Dict]:
    with get_cursor(dict_cursor=True) as cursor:
        cursor.execute(
            "SELECT id, full_name, username FROM users WHERE is_administrator = TRUE"
        )
        return cursor.fetchall()

def get_active_users() -> List[int]:
    with get_cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE is_blocked = FALSE")
        return [row[0] for row in cursor.fetchall()]