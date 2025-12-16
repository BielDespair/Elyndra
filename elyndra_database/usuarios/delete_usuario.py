from ..database import db;




def delete_usuario(user_id) -> bool:
    collection = db["usuarios"]
    result = collection.delete_one({"_id": user_id})
    return result.deleted_count > 0