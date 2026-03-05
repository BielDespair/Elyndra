def media_avaliacao_games(db):
    
    pipeline = [
        {
            "$group": {
                "_id": "$game_id",
                "media_avaliacao": {"$avg": "$avaliacao"},
                "total_reviews": {"$sum": 1}
            }
        }
    ]

    result = db["reviews"].aggregate(pipeline)

    return list(result)

