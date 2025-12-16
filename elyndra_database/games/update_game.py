from ..database import db;


def update_game(game_id: str, update_data: dict) -> bool:
    collection = db["games"]
    
    
    result = collection.update_one(
        {"_id": game_id},
        {"$set": update_data}
    )
    return result.modified_count > 0