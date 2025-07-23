import sqlite3
from werkzeug.security import generate_password_hash

# Connect to SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Sample users (secure hashed passwords)
users = [
    ("John Doe", "john@example.com", generate_password_hash("password123")),
    ("Jane Smith", "jane@example.com", generate_password_hash("secret456")),
    ("Bob Johnson", "bob@example.com", generate_password_hash("qwerty789")),
]

# Insert sample users (skip if email exists)
for name, email, password in users:
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))

conn.commit()
conn.close()

print("Database initialized with sample data")
