import cv2
import pytesseract
import json
import matplotlib.pyplot as plt
from pymongo import MongoClient

# Load Image
image_path = "salary_slip.jpg"
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Perform OCR and extract only the text
raw_text = pytesseract.image_to_string(gray)

# Remove extra spaces and line breaks
cleaned_text = "\n".join([line.strip() for line in raw_text.split("\n") if line.strip()])

# Save Extracted Text as JSON
json_filename = "extracted_text.json"
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump({"filename": image_path, "extracted_text": cleaned_text}, json_file, indent=4, ensure_ascii=False)

print(f"Extracted text saved to {json_filename}")

# Display Image
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

# === Store Extracted Data in MongoDB as One Document ===
client = MongoClient("mongodb://localhost:27017/")
db = client["my_database"]  # Change database name if needed
collection = db["users"]  # Change collection name if needed

# Insert a single document
document = {
    "filename": image_path,
    "extracted_text": cleaned_text
}

collection.insert_one(document)
print(f"Extracted text stored as a single document in MongoDB: ocr_database -> extracted_text")
