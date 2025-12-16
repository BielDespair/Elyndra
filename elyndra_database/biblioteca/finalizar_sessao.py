from ..database import db


async def finalizar_sessao(user_id, game_id) -> bool:
    collection = db["biblioteca"]
    
    filter = {
        "user_id": user_id,
        "game_id": game_id,
    }
    
    sessao_ativa = await collection.find_one(filter, {"sessao": 1})
    
    if (not sessao_ativa["sessao"]["ativa"]):
        return False
    
    
    inicio = sessao_ativa["sessao"]["startedAt"]
    fim = sessao_ativa["sessao"]["lastHeartbeatAt"]
    
    delta = fim - inicio
    minutos_jogados = delta.total_seconds() / 60
    
    sessao = {
        "ativa": False,
        "startedAt": None,
        "lastHeartbeatAt": None,
    }
    
    ultima_sessao = {
        "fim": fim,
        "minutos_jogados": minutos_jogados,
    }
    
    result = await collection.update_one(filter, {"$set": {"sessao": sessao, "ultima_sessao": ultima_sessao}, "$inc": {"minutos_jogados": minutos_jogados}})
    
    return result.modified_count > 0