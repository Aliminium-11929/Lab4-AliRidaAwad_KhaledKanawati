"""SQLite operations for the Lab 5 user API."""
import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "database.db"
FIELDS = ("name", "email", "phone", "address", "country")

def connect_to_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_db_table():
    with connect_to_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        )""")

def get_users():
    with connect_to_db() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM users ORDER BY user_id")]

def get_user_by_id(user_id):
    with connect_to_db() as conn:
        row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

def insert_user(user):
    with connect_to_db() as conn:
        cur = conn.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            tuple(user[field] for field in FIELDS),
        )
        new_id = cur.lastrowid
    return get_user_by_id(new_id)

def update_user(user):
    with connect_to_db() as conn:
        cur = conn.execute(
            "UPDATE users SET name=?, email=?, phone=?, address=?, country=? WHERE user_id=?",
            tuple(user[field] for field in FIELDS) + (user["user_id"],),
        )
        affected = cur.rowcount
    return get_user_by_id(user["user_id"]) if affected else None

def delete_user(user_id):
    with connect_to_db() as conn:
        cur = conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        return cur.rowcount > 0
