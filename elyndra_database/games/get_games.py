from ..database import db;


def get_games() -> list[dict]:
    collection = db["games"]
    games = list(collection.find())



    for game in games:
        game["_id"] = str(game["_id"])

    return games