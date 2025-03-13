import cv2
import pytesseract

# Set Tesseract path (Change path as per your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_serial_number(image_path):
    # Read image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    # OCR to extract text
    extracted_text = pytesseract.image_to_string(thresh)
    
    # Clean the output
    serial_number = extracted_text.strip().replace("\n", "")
    return serial_number

# Example usage
image_path = "serial_number_image.jpg"
serial_number = extract_serial_number(image_path)
print(f"Extracted Serial Number: {serial_number}")
