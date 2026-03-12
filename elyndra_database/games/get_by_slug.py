from bson import ObjectId
from ..database import db


def get_game_by_id(game_id: str) -> dict | None:

    collection = db["games"]

    game = collection.find_one({"_id": ObjectId(game_id)})

    if not game:
        return None

    game["_id"] = str(game["_id"])

    return game