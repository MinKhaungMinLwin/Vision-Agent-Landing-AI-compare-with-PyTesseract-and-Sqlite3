import cv2
import pytesseract
import easyocr
import re
import json
from pymongo import MongoClient

# Setup Tesseract OCR Path (For Windows users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["invoice_db"]
collection = db["invoices"]

def preprocess_image(image_path):
    """Preprocess invoice image for better OCR"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return threshold

def extract_text_tesseract(image_path):
    """Extract text using Tesseract OCR"""
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image)
    return text

def extract_text_easyocr(image_path):
    """Extract text using EasyOCR"""
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path, detail=0)
    return "\n".join(result)

def extract_invoice_data(text):
    """Extract key information from OCR text using regex"""
    invoice_data = {}

    # Extract Invoice Number
    invoice_no = re.search(r'Invoice\s*No[:\s]*([\w-]+)', text, re.IGNORECASE)
    invoice_data['invoice_number'] = invoice_no.group(1) if invoice_no else None

    # Extract Date (YYYY-MM-DD format)
    date = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    invoice_data['date'] = date.group(1) if date else None

    # Extract Total Amount (Currency Format)
    total = re.search(r'Total\s*[:\s]*([0-9,]+\.\d{2})', text, re.IGNORECASE)
    invoice_data['total_amount'] = total.group(1) if total else None

    # Extract Vendor Name (Example pattern)
    vendor = re.search(r'From[:\s]*(.+)', text, re.IGNORECASE)
    invoice_data['vendor'] = vendor.group(1).strip() if vendor else None

    return invoice_data

def save_to_mongodb(invoice_data):
    """Save structured invoice data to MongoDB"""
    if invoice_data:
        collection.insert_one(invoice_data)
        print("Data saved successfully:", invoice_data)
    else:
        print("No data to save.")

def process_invoice(image_path, use_easyocr=False):
    """Main function to process invoice and save data"""
    if use_easyocr:
        text = extract_text_easyocr(image_path)
    else:
        text = extract_text_tesseract(image_path)

    invoice_data = extract_invoice_data(text)
    
    if invoice_data:
        invoice_data_json = json.dumps(invoice_data, indent=4)
        print("Extracted JSON Data:\n", invoice_data_json)
        save_to_mongodb(invoice_data)
    else:
        print("No valid data found in invoice.")

# Example Usage
invoice_image = "invoice_sample.jpg"  # Change this to your invoice image path
process_invoice(invoice_image, use_easyocr=True)  # Set to True for EasyOCR
