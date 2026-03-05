from ..database import db

def buscar_jogos_por_categoria(categoria: str):

    pipeline = [
        {
            "$match": {
                "categoria": categoria
            }
        },
        {
            "$project": {
                "_id": 1,
                "titulo": 1,
                "categoria": 1,
                "ano_lancamento": 1
            }
        }
    ]

    result = db["games"].aggregate(pipeline)

    return list(result)

