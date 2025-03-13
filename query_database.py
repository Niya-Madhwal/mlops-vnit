import sqlite3

def check_device_in_db(serial_number):
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()

    # Query database
    cursor.execute("SELECT user FROM devices WHERE serial_number=?", (serial_number,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return f"Device found. Primary User: {result[0]}"
    else:
        return "Device not found"

# Example usage
serial_number = "LAP12345"  # Change this for testing
print(check_device_in_db(serial_number))