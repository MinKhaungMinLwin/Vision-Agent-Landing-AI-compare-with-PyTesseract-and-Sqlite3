# Vision-Agent-Landing-AI-compare-with-PyTesseract-and-Sqlite3

# OCR Text Extraction and Storage

## Overview

This project extracts text from an image using Tesseract OCR (`pytesseract`), displays the detected text with bounding boxes, saves the extracted text to a JSON file, and stores the results in an SQLite database.

## Features

- Uses `pytesseract` to extract text from an image.
- Displays the extracted text with bounding boxes using OpenCV.
- Saves extracted text and bounding box coordinates to a JSON file.
- Stores extracted text in an SQLite database.

## Requirements

Ensure you have the following dependencies installed before running the script:

### Install Tesseract OCR (if not installed):

```sh
sudo apt install tesseract-ocr   # For Linux
# OR
brew install tesseract           # For macOS
```

### Install Required Python Libraries:

```sh
pip install opencv-python pytesseract matplotlib sqlite3
```

## Usage

1. **Place your image file** (e.g., `salary_slip.jpg`) in the same directory as the script.
2. **Run the script:**

```sh
python extract_text.py
```

3. **Check the output:**
   - Extracted text with bounding boxes will be displayed.
   - The extracted text is saved in `extracted_text.json`.
   - The extracted text is stored in an SQLite database (`text_data.db`).

## Output Files

- ``: Stores extracted text along with bounding box coordinates.
- ``: SQLite database containing the extracted text data.

## Database Structure

The script creates a table named `extracted_text` with the following fields:

- `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
- `text` (TEXT)
- `x` (INTEGER) - Bounding box x-coordinate
- `y` (INTEGER) - Bounding box y-coordinate
- `width` (INTEGER) - Bounding box width
- `height` (INTEGER) - Bounding box height

## Example JSON Output

```json
[
    {
        "text": "Salary Slip",
        "bounding_box": {"x": 50, "y": 30, "width": 120, "height": 40}
    },
    {
        "text": "Total Salary: $5000",
        "bounding_box": {"x": 70, "y": 80, "width": 150, "height": 40}
    }
]
```

## Example SQL Query to Retrieve Data

```sql
SELECT * FROM extracted_text;
```

## License

This project is open-source and available for modification and use under the MIT License.

