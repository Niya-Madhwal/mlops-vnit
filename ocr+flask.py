import os
import cv2
import pytesseract
from fuzzywuzzy import process
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Mock database (Serial Numbers)
mock_data = {
    "ABC123": {"device_exists": True, "primary_user": "John Doe"},
    "XYZ789": {"device_exists": True, "primary_user": "Jane Smith"},
    "LMN456": {"device_exists": False, "primary_user": None},
    "PQR567": {"device_exists": True, "primary_user": "Michael Scott"},
    "DEF890": {"device_exists": True, "primary_user": "Dwight Schrute"},
}

# Set the Tesseract OCR path (Modify if necessary)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    """Preprocess the image to improve OCR accuracy."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)  # Reduce noise
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Increase contrast
    return threshold

def get_closest_match(serial_number):
    """Find the closest match from the mock database using fuzzy matching."""
    best_match, score = process.extractOne(serial_number, mock_data.keys())  # Find closest match
    return best_match if score > 60 else None  # If confidence score > 60%, return best match

@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Serial Number Checker</title>
    </head>
    <body>
        <h2>Enter Serial Number</h2>
        <form action="/check" method="post">
            <label for="serial_number">Serial Number:</label>
            <input type="text" id="serial_number" name="serial_number" required>
            <button type="submit">Check</button>
        </form>

        <h2>Or Upload an Image</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">Extract & Check</button>
        </form>
    </body>
    </html>
    '''

@app.route("/check", methods=["POST"])
def check_serial_number():
    serial_number = request.form.get("serial_number")

    if not serial_number:
        return jsonify({"error": "Serial number is missing."}), 400

    serial_number = serial_number.strip().upper()
    result = mock_data.get(serial_number)

    if result is not None:
        message = f"Device Found! Primary User: {result['primary_user']}" if result["device_exists"] else "Device Not Found in Azure AD."
    else:
        closest_match = get_closest_match(serial_number)
        if closest_match:
            result = mock_data[closest_match]
            message = f"Did you mean '{closest_match}'? Device Found! Primary User: {result['primary_user']}" if result["device_exists"] else f"Did you mean '{closest_match}'? Device Not Found."
        else:
            message = "Serial Number not recognized in the system."

    return jsonify({"Serial Number": serial_number, "Message": message})

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."}), 400

    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "No selected file."}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(filepath)

    # Preprocess and extract text
    processed_image = preprocess_image(filepath)
    extracted_text = pytesseract.image_to_string(processed_image, config="--psm 6").strip().upper()

    if not extracted_text:
        return jsonify({"error": "No text detected in image."}), 400

    return check_serial_number_from_text(extracted_text)

def check_serial_number_from_text(serial_number):
    serial_number = serial_number.strip().upper()
    result = mock_data.get(serial_number)

    if result is not None:
        message = f"Device Found! Primary User: {result['primary_user']}" if result["device_exists"] else "Device Not Found in Azure AD."
    else:
        closest_match = get_closest_match(serial_number)
        if closest_match:
            result = mock_data[closest_match]
            message = f"Did you mean '{closest_match}'? Device Found! Primary User: {result['primary_user']}" if result["device_exists"] else f"Did you mean '{closest_match}'? Device Not Found."
        else:
            message = "Serial Number not recognized in the system."

    return jsonify({"Extracted Serial Number": serial_number, "Message": message})

if __name__ == "__main__":
    print("Starting Flask server... Visit http://127.0.0.1:5000/")
    app.run(debug=True)
