import sqlite3

DB_PATH = "database/resumes.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            skills TEXT,
            education TEXT,
            experience TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_candidate(name, email, phone, skills, education, experience):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidates (name, email, phone, skills, education, experience)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        ", ".join(skills),
        ", ".join(education),
        ", ".join(experience)
    ))

    conn.commit()
    conn.close()

def get_all_candidates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()

    conn.close()
    return candidates