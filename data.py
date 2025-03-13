import sqlite3

# Connect to SQLite Database (Creates a file named 'devices.db' if not exists)
conn = sqlite3.connect("devices.db")
cursor = conn.cursor()

# Create Table for Serial Numbers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS serial_numbers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        serial_number TEXT UNIQUE NOT NULL,
        primary_user TEXT,
        device_exists BOOLEAN
    )
''')

# Commit Changes & Close Connection
conn.commit()
conn.close()

print("✅ Database & Table Created Successfully!")

import sqlite3

# Connect to SQLite Database
conn = sqlite3.connect("devices.db")
cursor = conn.cursor()

# Sample Serial Numbers
serials = [
    ("ABC123", True, "John Doe"),
    ("XYZ789", True, "Jane Smith"),
    ("LMN456", False, None),
    ("PQR567", True, "Michael Scott"),
    ("DEF890", True, "Dwight Schrute"),
]

# Insert Data (Ignore Duplicates)
for serial in serials:
    cursor.execute("INSERT OR IGNORE INTO serial_numbers (serial_number, primary_user, device_exists) VALUES (?, ?, ?)", serial)

# Commit & Close
conn.commit()
conn.close()

print("✅ Sample Data Inserted!")


import sqlite3

conn = sqlite3.connect("devices.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM serial_numbers")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()

