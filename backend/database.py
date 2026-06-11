import sqlite3
import bcrypt

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
            experience TEXT,
            certifications TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(candidates)")
    columns = [row[1] for row in cursor.fetchall()]
    if "certifications" not in columns:
        cursor.execute("ALTER TABLE candidates ADD COLUMN certifications TEXT")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'user')),
            must_change_password INTEGER NOT NULL DEFAULT 1,
            failed_attempts INTEGER NOT NULL DEFAULT 0,
            lock_until TEXT,
            is_active INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
    admin_exists = cursor.fetchone()
    if not admin_exists:
        admin_password_hash = bcrypt.hashpw(
            "admin12345".encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")
        cursor.execute("""
            INSERT INTO users (username, password_hash, role, must_change_password, failed_attempts, lock_until, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "admin",
            admin_password_hash,
            "admin",
            0,
            0,
            None,
            1,
        ))

    conn.commit()
    conn.close()

def save_candidate(name, email, phone, skills, education, experience, certifications=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if candidate with same email already exists
    cursor.execute("SELECT id FROM candidates WHERE email = ?", (email,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return False   

    if certifications is None:
        certifications = []

    cursor.execute("""
        INSERT INTO candidates (name, email, phone, skills, education, experience, certifications)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        ", ".join(skills),
        ", ".join(education),
        ", ".join(experience),
        ", ".join(certifications),
    ))

    conn.commit()
    conn.close()
    return True  

def get_all_candidates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()

    conn.close()
    return candidates

def search_candidates(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM candidates
        WHERE name LIKE ?
        OR email LIKE ?
        OR skills LIKE ?
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))

    candidates = cursor.fetchall()
    conn.close()
    return candidates


def delete_candidate(candidate_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def _to_user_dict(row):
    return {
        "id": row[0],
        "username": row[1],
        "password_hash": row[2],
        "role": row[3],
        "must_change_password": row[4],
        "failed_attempts": row[5],
        "lock_until": row[6],
        "is_active": row[7],
    }


def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, password_hash, role, must_change_password, failed_attempts, lock_until, is_active
        FROM users
        WHERE username = ?
    """, (username,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return _to_user_dict(row)


def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, password_hash, role, must_change_password, failed_attempts, lock_until, is_active
        FROM users
        ORDER BY id
    """)
    rows = cursor.fetchall()
    conn.close()
    return [_to_user_dict(r) for r in rows]


def create_user(username, password_hash, role, must_change_password=1):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM users")
        next_id = cursor.fetchone()[0]
        cursor.execute("""
            INSERT INTO users (id, username, password_hash, role, must_change_password, failed_attempts, lock_until, is_active)
            VALUES (?, ?, ?, ?, ?, 0, NULL, 1)
        """, (next_id, username, password_hash, role, must_change_password))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()


def set_user_password_and_clear_flag(user_id, password_hash, must_change_password=0):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET password_hash = ?, must_change_password = ?, failed_attempts = 0, lock_until = NULL
        WHERE id = ?
    """, (password_hash, must_change_password, user_id))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def update_login_failure(user_id, failed_attempts, lock_until):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET failed_attempts = ?, lock_until = ?
        WHERE id = ?
    """, (failed_attempts, lock_until, user_id))
    conn.commit()
    conn.close()


def reset_login_failures(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET failed_attempts = 0, lock_until = NULL
        WHERE id = ?
    """, (user_id,))
    conn.commit()
    conn.close()


def update_user_must_change_password(user_id, must_change_password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET must_change_password = ?
        WHERE id = ?
    """, (must_change_password, user_id))
    conn.commit()
    conn.close()


def remove_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    deleted = cursor.rowcount > 0

    if deleted:
        cursor.execute("SELECT id FROM users ORDER BY id")
        current_ids = [row[0] for row in cursor.fetchall()]

        # Step 1: move IDs to temporary negative values to avoid PK collisions.
        for expected_id, current_id in enumerate(current_ids, start=1):
            if current_id != expected_id:
                cursor.execute("UPDATE users SET id = ? WHERE id = ?", (-expected_id, current_id))

        # Step 2: normalize temporary IDs back to positive contiguous IDs.
        cursor.execute("UPDATE users SET id = -id WHERE id < 0")

        # Keep SQLite AUTOINCREMENT sequence aligned with current max ID.
        cursor.execute("SELECT COALESCE(MAX(id), 0) FROM users")
        max_id = cursor.fetchone()[0]
        cursor.execute("UPDATE sqlite_sequence SET seq = ? WHERE name = 'users'", (max_id,))
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('users', ?)", (max_id,))

    conn.commit()
    conn.close()
    return deleted


def count_admin_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin' AND is_active = 1")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# ============ JOB FUNCTIONS ============

def init_jobs_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            department TEXT,
            location TEXT,
            experience TEXT,
            description TEXT,
            required_skills TEXT,
            required_certifications TEXT,
            posted_date TEXT,
            status TEXT DEFAULT 'open',
            posted_by TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            candidate_name TEXT,
            candidate_email TEXT,
            candidate_skills TEXT,
            candidate_certifications TEXT,
            match_score REAL,
            skills_score REAL,
            experience_score REAL,
            certifications_score REAL,
            status TEXT DEFAULT 'Applied',
            applied_date TEXT,
            resume_path TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    """)

    conn.commit()
    conn.close()


def create_job(title, department, location, experience,
               description, required_skills, required_certifications, posted_by):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    from datetime import datetime
    posted_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute("""
        INSERT INTO jobs (title, department, location, experience,
                         description, required_skills, required_certifications,
                         posted_date, status, posted_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'open', ?)
    """, (title, department, location, experience,
          description, required_skills, required_certifications,
          posted_date, posted_by))

    conn.commit()
    conn.close()


def get_all_jobs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY posted_date DESC")
    jobs = cursor.fetchall()
    conn.close()
    return jobs


def get_job_by_id(job_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    conn.close()
    return job


def update_job_status(job_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
    conn.commit()
    conn.close()


def delete_job(job_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    cursor.execute("DELETE FROM applications WHERE job_id = ?", (job_id,))
    conn.commit()
    conn.close()


def save_application(job_id, candidate_name, candidate_email,
                     candidate_skills, candidate_certifications,
                     match_score, skills_score, experience_score,
                     certifications_score, resume_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if already applied
    cursor.execute("""
        SELECT id FROM applications
        WHERE job_id = ? AND candidate_email = ?
    """, (job_id, candidate_email))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return False

    from datetime import datetime
    applied_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute("""
        INSERT INTO applications (job_id, candidate_name, candidate_email,
                                  candidate_skills, candidate_certifications,
                                  match_score, skills_score, experience_score,
                                  certifications_score, status, applied_date, resume_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Applied', ?, ?)
    """, (job_id, candidate_name, candidate_email,
          candidate_skills, candidate_certifications,
          match_score, skills_score, experience_score,
          certifications_score, applied_date, resume_path))

    conn.commit()
    conn.close()
    return True


def get_applications_by_job(job_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM applications
        WHERE job_id = ?
        ORDER BY match_score DESC
    """, (job_id,))
    applications = cursor.fetchall()
    conn.close()
    return applications


def update_application_status(application_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE applications SET status = ? WHERE id = ?",
        (status, application_id)
    )
    conn.commit()
    conn.close()

def get_applications_by_email(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            a.id,
            a.job_id,
            a.candidate_name,
            a.candidate_email,
            a.match_score,
            a.skills_score,
            a.experience_score,
            a.certifications_score,
            a.status,
            a.applied_date,
            j.title,
            j.department,
            j.location
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        WHERE LOWER(a.candidate_email) = LOWER(?)
        ORDER BY a.applied_date DESC
    """, (email,))

    applications = cursor.fetchall()
    conn.close()
    return applications

def delete_candidate(candidate_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0