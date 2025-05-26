import psycopg2
from main import DATABASE_URL


def create_users_table():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

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

        conn.commit()
        cursor.close()
        conn.close()
        print("\u2705 Jadval yaratildi yoki allaqachon mavjud.")
    except Exception as e:
        print("\u274C Xatolik:", e)


def insert_user(user_id: int, full_name: str, username: str):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (id, full_name, username) VALUES (%s, %s, %s)",
            (user_id, full_name, username)
        )
        conn.commit()
    except psycopg2.IntegrityError:
        raise ValueError("Bu ID allaqachon mavjud")
    finally:
        cursor.close()
        conn.close()


def get_all_users():
    conn = psycopg2.connect(DATABASE_URL)
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
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        cursor.execute(
            'SELECT 1 FROM users WHERE id = %s LIMIT 1',
            (user_id,)
        )
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def is_subscribed(user_id: int) -> bool:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT subscribed FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    return False


def update_subscription_status(user_id: int, status: bool):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET subscribed = %s WHERE id = %s",
        (status, user_id)
    )
    conn.commit()
    conn.close()


def get_all_users_ids():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users")
    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


def set_admin_status(user_id: int, is_admin: bool):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET is_administrator = %s WHERE id = %s",
            (is_admin, user_id)
        )
        conn.commit()
    finally:
        conn.close()


def get_admins():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, full_name, username FROM users WHERE is_administrator = TRUE"
        )
        admins = []
        for row in cursor.fetchall():
            admins.append({
                "id": row[0],
                "full_name": row[1],
                "username": row[2]
            })
        return admins
    finally:
        conn.close()


def get_active_users():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE is_blocked = FALSE")
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()
