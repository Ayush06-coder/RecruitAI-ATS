import sqlite3
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

conn = sqlite3.connect('database/resumes.db')
cursor = conn.cursor()

# Delete all existing users
cursor.execute("DELETE FROM users")

# Create admin with correct hash
cursor.execute("""
    INSERT INTO users (username, password_hash, role, is_active, must_change_password, failed_attempts)
    VALUES (?, ?, ?, 1, 0, 0)
""", ('admin', hash_password('admin12345'), 'admin'))

# Create user with correct hash
cursor.execute("""
    INSERT INTO users (username, password_hash, role, is_active, must_change_password, failed_attempts)
    VALUES (?, ?, ?, 1, 0, 0)
""", ('user', hash_password('user123'), 'user'))

conn.commit()
conn.close()
print("Users created successfully!")