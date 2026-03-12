import json

from bson import ObjectId
from ..database import db;
from ..redis.redis_client import r

def get_usuario_repo(usuario_id: str) -> dict:
    cache_key = f"usuario:{usuario_id}"
    cached = r.get(cache_key)
    if cached:
        print(f"Cache hit: {cache_key}")
        return json.loads(cached)
    collection = db["usuarios"]

    try:
        oid = ObjectId(usuario_id)
    except Exception:
        return None  # ID inválido retorna None

    usuario = collection.find_one({"_id": oid})
    usuario["_id"] = str(usuario["_id"])
    r.set(cache_key, json.dumps(usuario))
    return usuario