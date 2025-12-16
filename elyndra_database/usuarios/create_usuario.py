from ..database import db;



def create_usuario(user: dict):
    collection = db["usuarios"]
    result = collection.insert_one(user)
    return result.inserted_id