import cv2
import pytesseract
import json
import sqlite3
from pytesseract import Output
import matplotlib.pyplot as plt


image_path = "salary_slip.jpg"
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


detection_data = pytesseract.image_to_data(gray, output_type=Output.DICT)# Perform OCR and extract data


extracted_text = []
for i in range(len(detection_data['text'])):
    x, y, w, h = detection_data['left'][i], detection_data['top'][i], detection_data['width'][i], detection_data['height'][i]
    text = detection_data['text'][i].strip()
    
    if text:  # Only process non-empty text
        extracted_text.append({
            "text": text,
            "bounding_box": {"x": x, "y": y, "width": w, "height": h}
        })
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)


json_filename = "extracted_text.json"
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(extracted_text, json_file, indent=4, ensure_ascii=False)

print(f"Extracted text saved to {json_filename}")


plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()


db_name = "text_data.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_text (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT,
                    x INTEGER,
                    y INTEGER,
                    width INTEGER,
                    height INTEGER)''')


for item in extracted_text:
    cursor.execute("INSERT INTO extracted_text (text, x, y, width, height) VALUES (?, ?, ?, ?, ?)", 
                   (item["text"], item["bounding_box"]["x"], item["bounding_box"]["y"], 
                    item["bounding_box"]["width"], item["bounding_box"]["height"]))


conn.commit()
conn.close()

print(f"Extracted text stored in {db_name}")
