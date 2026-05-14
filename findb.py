import sqlite3


def init_db():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            income REAL,
            expenses REAL,
            invest REAL
        )
    """)

    conn.commit()
    conn.close()


def save_calculation(user_id, income, expenses, invest):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO calculations (user_id, income, expenses, invest)
        VALUES (?, ?, ?, ?)
    """, (user_id, income, expenses, invest))

    conn.commit()
    conn.close()


def get_history(user_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT income, expenses, invest
        FROM calculations
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 5
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return rows