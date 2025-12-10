


def seed_catalogo(db):
    collection = db["catalogo"]
    resultado = collection.insert_one({})
    
    print("Conectado ao MongoDB!")
    print("ID inserido:", resultado.inserted_id)

