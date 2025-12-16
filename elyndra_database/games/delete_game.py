from bson import ObjectId
from ..database import db;



def delete_game(game_id: str) -> bool:
    result = db["games"].delete_one({"_id": ObjectId(game_id)})
    return result.deleted_count > 0