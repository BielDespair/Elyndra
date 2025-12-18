
from datetime import datetime, timezone
import random
from bson import ObjectId
from pymongo.database import Database
import json


USERS_PATH = "elyndra_database/bootstrap/seeds/usuarios.json"


def seed_usuarios(db: Database, seed: int = 42) -> None:
    random.seed(42)
    
    collection = db["usuarios"]

    with open(USERS_PATH, "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    if not usuarios:
        raise ValueError("seed.json está vazio.")

    now = datetime.now(timezone.utc)

    for user in usuarios:
        user["_id"] = ObjectId()
        user["created_at"] = now
        user["updated_at"] = now

    ids = [user["_id"] for user in usuarios]


    for user in usuarios:
        outros_ids = [i for i in ids if i != user["_id"]]

        qtd_amigos = random.randint(0, min(3, len(outros_ids)))
        amigos = random.sample(outros_ids, qtd_amigos)

        user["relacionamentos"]["amigos"] = amigos

    collection.insert_many(usuarios)

    print(f"Inserido {len(usuarios)} usuários")