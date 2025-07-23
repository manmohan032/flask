import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = 'users.db'


class User:
    @staticmethod
    def get_connection():
        return sqlite3.connect(DB_PATH)

    @staticmethod
    def create_table():
        with User.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

    @staticmethod
    def create(name, email, password):
        hashed_password = generate_password_hash(password)
        with User.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all():
        with User.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users")
            return cursor.fetchall()

    @staticmethod
    def get_by_id(user_id):
        with User.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
            return cursor.fetchone()

    @staticmethod
    def get_by_email(email):
        with User.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, password FROM users WHERE email = ?", (email,))
            return cursor.fetchone()

    @staticmethod
    def update(user_id, name, email):
        with User.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (name, email, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(user_id):
        with User.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def check_password(email, plain_password):
        user = User.get_by_email(email)
        if not user:
            return None
        user_id, name, email, hashed_password = user
        if check_password_hash(hashed_password, plain_password):
            return user_id
        return None
