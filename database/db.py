import sqlite3
import os
from datetime import date

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "spendly.db")

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    db.commit()
    db.close()


def seed_db():
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        db.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = db.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    today = date.today()
    expenses = [
        (user_id, 45.50, "Food", f"{today.year}-{today.month:02d}-01", "Grocery shopping"),
        (user_id, 12.00, "Food", f"{today.year}-{today.month:02d}-05", "Coffee and snacks"),
        (user_id, 30.00, "Transport", f"{today.year}-{today.month:02d}-03", "Bus pass"),
        (user_id, 120.00, "Bills", f"{today.year}-{today.month:02d}-02", "Electric bill"),
        (user_id, 25.00, "Health", f"{today.year}-{today.month:02d}-07", "Pharmacy"),
        (user_id, 15.99, "Entertainment", f"{today.year}-{today.month:02d}-10", "Movie tickets"),
        (user_id, 65.00, "Shopping", f"{today.year}-{today.month:02d}-08", "New headphones"),
        (user_id, 20.00, "Other", f"{today.year}-{today.month:02d}-04", "Gift for friend"),
    ]
    db.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    db.commit()
    db.close()
