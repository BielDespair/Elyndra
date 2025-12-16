from ..database import db;

def read_usuario(user_id) -> dict:
    collection = db["usuarios"]
    user = collection.find_one({"_id": user_id})
    return user