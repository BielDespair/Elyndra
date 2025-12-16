
from datetime import datetime
from time import timezone

from bson import ObjectId
from ..database import db


async def adquirir_game(user_id, game_id):
    collection = db["biblioteca"]
    
    user_oid = ObjectId(user_id)
    game_oid = ObjectId(game_id)
    
    if not await db["usuarios"].find_one({"_id": user_oid}, {"_id": 1}):
        raise ValueError("Usuário não existe")

    if not await db["games"].find_one({"_id": game_oid}, {"_id": 1}):
        raise ValueError("Jogo não existe")
    
    
    document = {
        "user_id": user_oid,
        "game_id": game_oid,
        
        "status": "adquirido",
        "adquirido_em": datetime.now(timezone.utc),
    
        "minutos_jogados": 0,
        "conquistas": [],
        "sessao": None,
          
        "instalacao": {
            "instalado": False,
            "version": None,
        },
    }
    
    result = await collection.insert_one(document)
    return result.inserted_id