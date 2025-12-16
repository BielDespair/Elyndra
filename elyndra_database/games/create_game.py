from ..database import db;


def create_game(game_data: dict) -> int:
    collection = db["games"]
    
    
    result = collection.insert_one(game_data)
    return result.inserted_id