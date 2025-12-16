from ..database import db;



def update_usuario(user_id, update_fields: dict):

    collection = db["usuarios"]
    result = collection.update_one({"_id": user_id}, {"$set": update_fields})
    return result.modified_count