from ..database import db

def jogos_mais_jogados(limit: int = 5):

    pipeline = [
        {
            "$group": {
                "_id": "$game_id",
                "total_minutos": {"$sum": "$minutos_jogados"},
                "jogadores": {"$sum": 1}
            }
        },
        {
            "$sort": {"total_minutos": -1}
        },
        {
            "$limit": limit
        },
        {
            "$lookup": {
                "from": "games",
                "localField": "_id",
                "foreignField": "_id",
                "as": "game"
            }
        },
        {
            "$unwind": "$game"
        },
        {
            "$project": {
                "_id": 0,
                "game_id": "$game._id",
                "titulo": "$game.titulo",
                "total_minutos": 1,
                "jogadores": 1
            }
        }
    ]

    return list(db["biblioteca"].aggregate(pipeline))