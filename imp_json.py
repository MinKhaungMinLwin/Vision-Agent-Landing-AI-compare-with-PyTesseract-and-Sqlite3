import json
from pymongo import MongoClient

# MongoDB ကို ချိတ်ဆက်မယ် (localhost မှာ MongoDB server run နေရပါစေ)
client = MongoClient("mongodb://localhost:27017/")

# MongoDB Database နဲ့ Collection သတ်မှတ်မယ်
db = client["my_database"]  # Database Name
collection = db["users"]  # Collection Name

# JSON ဖိုင်ကို ဖွင့်ပြီး data ကို ဖတ်မယ်
with open("extracted_text.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # JSON Data ကို Python Dictionary ပြောင်းမယ်

# MongoDB ထဲကို Data Import လုပ်မယ်
if isinstance(data, list):
    collection.insert_many(data)  # JSON Data list ဖြစ်ရင် insert_many()
else:
    collection.insert_one(data)  # JSON Data တစ်ခုတည်းဆိုရင် insert_one()

print("JSON data ကို MongoDB ထဲထည့်ပြီးပြီ!")
