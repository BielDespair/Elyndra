import json

from ..database import db;

from ..redis.redis_client import r


def get_games() -> list[dict]:
    cached = r.get("games_cache")
    if cached:
        print("Cache hit")
        return json.loads(cached)
    else:
        print("Cache miss")

    collection = db["games"]
    games = list(collection.find())
    for game in games:
        game["_id"] = str(game["_id"])

    r.set("games_cache", json.dumps(games))  # salva no Redis
    return games