import sqlite3

DB_NAME = "expense_tracker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    date TEXT,
                    amount REAL,
                    category TEXT,
                    description TEXT
                )""")
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def add_expense(username, date, amount, category, description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO expenses (username, date, amount, category, description) VALUES (?, ?, ?, ?, ?)",
              (username, date, amount, category, description))
    conn.commit()
    conn.close()

def get_expenses(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT date, amount, category, description FROM expenses WHERE username=?", (username,))
    data = c.fetchall()
    conn.close()
    return data

def get_today_total(username, today):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM expenses WHERE username=? AND date=?", (username, today))
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0

def get_monthly_total(username, month):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM expenses WHERE username=? AND date LIKE ?", (username, f"{month}%"))
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0
