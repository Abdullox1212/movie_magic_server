import sqlite3

def create_users_table():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT,
            is_administrator INTEGER DEFAULT 0,
            is_blocked INTEGER DEFAULT 0,
            subscribed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(user_id: int, full_name: str, username: str):
    """Foydalanuvchini ID bilan birga bazaga qo'shadi
    
    Args:
        user_id: Foydalanuvchi IDsi (raqam)
        full_name: Foydalanuvchi to'liq ismi
        username: Foydalanuvchi nomi
        
    Raises:
        ValueError: Agar ID allaqachon mavjud bo'lsa
    """
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (id, full_name, username) VALUES (?, ?, ?)",
            (user_id, full_name, username)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Bu ID allaqachon mavjud")
    finally:
        conn.close()

def get_all_users():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("SELECT id, full_name, username, subscribed FROM users")
    rows = cursor.fetchall()
    conn.close()

    users = []
    for row in rows:
        users.append({
            "id": row[0],
            "full_name": row[1],
            "username": row[2],
            "subscribed": row[3]
        })
    return users

def get_user(user_id: int) -> bool:
    """Foydalanuvchi IDsi bo'yicha mavjudligini tekshiradi
    
    Args:
        user_id: Foydalanuvchi IDsi
        
    Returns:
        True - agar foydalanuvchi mavjud bo'lsa
        False - agar foydalanuvchi mavjud bo'lmasa
    """
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    try:
        cursor.execute(
            'SELECT 1 FROM users WHERE id = ? LIMIT 1', 
            (user_id,)
        )
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()


def is_subscribed(user_id: int) -> bool:
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("SELECT subscribed FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0] == 1
    return False


def update_subscription_status(user_id: int, status: bool):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET subscribed = ? WHERE id = ?",
        (1 if status else 0, user_id)
    )
    conn.commit()
    conn.close()


def get_all_users_ids():
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users")
    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


def set_admin_status(user_id: int, is_admin: bool):
    """Foydalanuvchi admin statusini o'zgartiradi"""
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET is_administrator = ? WHERE id = ?",
            (int(is_admin), user_id)
        )
        conn.commit()
    finally:
        conn.close()

def get_admins():
    """Barcha admin foydalanuvchilarni qaytaradi"""
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row  # Dictionary-like qaytish uchun
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, full_name, username FROM users WHERE is_administrator = 1"
        )
        admins = []
        for row in cursor.fetchall():
            admins.append({
                "id": row["id"],
                "full_name": row["full_name"],
                "username": row["username"]
            })
        return admins
    finally:
        conn.close()



def get_active_users():
    """Bloklanmagan (is_blocked=False) foydalanuvchilarni olish"""
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE is_blocked = 0")
        return [row["id"] for row in cursor.fetchall()]
    finally:
        conn.close()