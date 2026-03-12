from ..database import db;



def create_usuario_repo(user: dict):
    collection = db["usuarios"]

    result = collection.insert_one(user)
    return str(result.inserted_id)