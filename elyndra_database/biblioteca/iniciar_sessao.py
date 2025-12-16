from datetime import datetime, timezone

from bson import ObjectId
from ..database import db


async def iniciar_sessao(user_id, game_id) -> bool:
    collection = db["biblioteca"]
    
    filter = {
        "user_id": ObjectId(user_id),
        "game_id": ObjectId(game_id),
    }
    
    sessao = {
        "ativa": True,
        "startedAt": datetime.now(timezone.utc),
        "lastHeartbeatAt": datetime.now(timezone.utc),
    }
    
        
    result = await collection.update_one(filter, {"$set": {"sessao": sessao}})
    
    return result.modified_count > 0



