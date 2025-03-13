from extract_serial_number import extract_serial_number
from query_database import check_device_in_db

# Upload Image
image_path = "serial_number_image.jpg"
serial_number = extract_serial_number(image_path)

# Check in the database
result = check_device_in_db(serial_number)

print(result)
