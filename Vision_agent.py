import requests
import os
from dotenv import load_dotenv

load_dotenv()

LANDAI_API_KEY = os.getenv('LANDAI_API_KEY')

if not LANDAI_API_KEY:
    raise ValueError("Please set the environment key")

url = "https://api.landing.ai/v1/tools/document-analysis"

path_to_image = "salary_slip.jpg"

files = {
    "image": open(path_to_image, "rb")
}

data = {
    "parse_text": True,
    "parse_tables": True,
    "parse_figures": True,
    "summary_verbosity": "normal",
    "caption_format": "json",
    "response_format": "json",
    "return_chunk_crops": False,
    "return_page_crops": False
}

headers = {
    "Authorization": f"Basic {LANDAI_API_KEY}"
}

response = requests.post(url, files=files, data=data, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)