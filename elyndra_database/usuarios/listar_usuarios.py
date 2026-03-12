from ..database import db;

from bson import json_util

def listar_usuarios_repo():
    usuarios = list(db["usuarios"].find())
    json_data = json_util.dumps(usuarios)
    return json_data