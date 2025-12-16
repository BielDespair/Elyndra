
from pymongo.collection import Collection, InsertManyResult
from bson import ObjectId





def seed_usuarios(db):    
    collection: Collection  = db["usuarios"]
    collection.drop();

    ids = [ObjectId() for _ in range(10)]
    
    usuarios = [
        {"_id": ids[0], "nome": "Thales",   "idade": 22, "amigos": [ids[1], ids[2]]},
        {"_id": ids[1], "nome": "Leonardo", "idade": 24, "amigos": [ids[0]]},
        {"_id": ids[2], "nome": "Marina",   "idade": 21, "amigos": [ids[0], ids[3], ids[4]]},
        {"_id": ids[3], "nome": "Gustavo",  "idade": 29, "amigos": []},
        {"_id": ids[4], "nome": "Rafaela",  "idade": 20, "amigos": [ids[2]]},
        {"_id": ids[5], "nome": "Paulo",    "idade": 31, "amigos": [ids[6], ids[7]]},
        {"_id": ids[6], "nome": "Julia",    "idade": 26, "amigos": []},
        {"_id": ids[7], "nome": "Cesar",    "idade": 33, "amigos": [ids[5]]},
        {"_id": ids[8], "nome": "Amanda",   "idade": 23, "amigos": [ids[9], ids[2]]},
        {"_id": ids[9], "nome": "Bianca",   "idade": 28, "amigos": []},
    ]
    
    resultado: InsertManyResult = collection.insert_many(usuarios)
    
    print(f"Inserido {len(resultado.inserted_ids)} usuários")