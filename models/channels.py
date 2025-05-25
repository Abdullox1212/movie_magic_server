import sqlite3

def create_channels_table():
    """Kanallar jadvalini yaratish (agar mavjud bo'lmasa)"""
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



def add_channel(username: str):
    """Yangi kanal qo'shish"""
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO channels (username) VALUES (?)",
            (username.lower(),)  # Usernamelarni kichik harflarda saqlaymiz
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Bu kanal allaqachon mavjud")
    finally:
        conn.close()

def remove_channel(username: str):
    """Kanalni o'chirish"""
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM channels WHERE username = ?",
        (username.lower(),)
    )
    conn.commit()
    conn.close()

def get_all_channels():
    """Barcha kanallarni olish"""
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM channels")
    channels = [row["username"] for row in cursor.fetchall()]
    conn.close()
    return channels

def channel_exists(username: str) -> bool:
    """Kanal mavjudligini tekshirish"""
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM channels WHERE username = ? LIMIT 1",
        (username.lower(),)
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists