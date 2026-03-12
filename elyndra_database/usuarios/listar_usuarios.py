from ..database import db;

def listar_usuarios_repo() -> list[dict]:
    collection = db["usuarios"]
    usuarios = list(collection.find())



    for usuario in usuarios:
        usuario["_id"] = str(usuario["_id"])

    return usuarios