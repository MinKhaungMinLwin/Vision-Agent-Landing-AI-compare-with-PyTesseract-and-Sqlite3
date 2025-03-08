import cv2
import pytesseract
import json
import sqlite3
import matplotlib.pyplot as plt
from pytesseract import Output
from pymongo import MongoClient

# Load Image
image_path = "salary_slip.jpg"
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Perform OCR and extract text with bounding boxes
detection_data = pytesseract.image_to_data(gray, output_type=Output.DICT)

extracted_text = []
for i in range(len(detection_data['text'])):
    x, y, w, h = detection_data['left'][i], detection_data['top'][i], detection_data['width'][i], detection_data['height'][i]
    text = detection_data['text'][i].strip()

    if text:  # Ignore empty text
        extracted_text.append({
            "text": text,
            "bounding_box": {"x": x, "y": y, "width": w, "height": h}
        })

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# Save Extracted Text as JSON
json_filename = "extracted_text.json"
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(extracted_text, json_file, indent=4, ensure_ascii=False)

print(f"Extracted text saved to {json_filename}")

# Display Image with Bounding Boxes
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

# === Store Extracted Data in MongoDB ===
client = MongoClient("mongodb://localhost:27017/")
db = client["my_database"]  # Change database name if needed
collection = db["users"]  # Change collection name if needed

# Insert extracted data into MongoDB
if extracted_text:
    collection.insert_many(extracted_text)
    print(f"Extracted text stored in MongoDB database: ocr_database -> extracted_text")
else:
    print("No text extracted. Nothing to insert into MongoDB.")
