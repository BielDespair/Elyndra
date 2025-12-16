import json


SEED_PATH = "elyndra_database/bootstrap/seeds/games.json"


def seed_games(db):
    collection = db["games"]
    
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
        
    result = collection.insert_many(data)
    
    
    print(f"Inserido {len(result.inserted_ids)} games")