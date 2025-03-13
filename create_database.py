import sqlite3

# Connect to SQLite database (or create it if not exists)
conn = sqlite3.connect("devices.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS devices (
    serial_number TEXT PRIMARY KEY,
    user TEXT
)
""")

# Insert sample data
sample_data = [
    ("LAP12345", "John Doe"),
    ("LAP67890", "Alice Smith"),
    ("LAP54321", "Bob Johnson")
]

cursor.executemany("INSERT OR IGNORE INTO devices (serial_number, user) VALUES (?, ?)", sample_data)
conn.commit()
conn.close()

print("Sample database created successfully.")
