import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_database():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    uri = f"mongodb+srv://{user}:{password}@cluster0.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(uri)
    return client["elyndra"]
