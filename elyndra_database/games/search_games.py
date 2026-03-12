from ..database import db


def get_games_by_category_repo(category: str) -> list[dict]:
    collection = db["games"]

    games = list(collection.find({"generos": category}))

    for game in games:
        game["_id"] = str(game["_id"])

    return games