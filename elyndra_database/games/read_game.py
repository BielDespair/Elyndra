from bson import ObjectId
from ..database import db;




def read_game(game_id):
    game = db["games"].find_one({"_id": ObjectId(game_id)})
    return game