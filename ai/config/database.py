import os
import dotenv
from pymongo import MongoClient

dotenv.load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("Error connecting to MONGODB")


client = MongoClient(MONGO_URI)
db = client["lab_center"]
reviews_collection = db["reviews"]


print("MONGODB connected successfully!")