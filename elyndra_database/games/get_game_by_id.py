import json

from bson import ObjectId
from ..redis.redis_client import CACHE_TTL, r
from ..database import db


def get_game_by_id(game_id: str) -> dict | None:

    cache_key = f"game:{game_id}"
    cached = r.get(cache_key)
    if cached:
        print(f"Cache hit | Key: {cache_key}")
        return json.loads(cached)
    
    

    collection = db["games"]

    game = collection.find_one({"_id": ObjectId(game_id)})

    if not game:
        return None

    game["_id"] = str(game["_id"])
    r.setex(
        cache_key,
        CACHE_TTL,
        json.dumps(game)
    )

    return game