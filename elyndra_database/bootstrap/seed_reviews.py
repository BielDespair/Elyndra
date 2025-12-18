import json
from datetime import datetime, timezone
from pathlib import Path
from pymongo.database import Database


REVIEWS_PATH = Path("elyndra_database/bootstrap/seeds/reviews.json")


def seed_reviews(db: Database) -> None:
    now = datetime.now(timezone.utc)

    with open(REVIEWS_PATH, "r", encoding="utf-8") as f:
        base_reviews = json.load(f)

    if not base_reviews:
        raise ValueError("reviews.json está vazio.")

    games = list(
        db["games"].find({}, {"_id": 1}).sort("_id", 1)
    )

    biblioteca_por_jogo = {}
    for entry in db["biblioteca"].find(
        {}, {"_id": 0, "user_id": 1, "game_id": 1, "minutos_jogados": 1}
    ).sort("user_id", 1):
        biblioteca_por_jogo.setdefault(entry["game_id"], []).append(entry)

    documents = []
    review_index = 0

    for game in games:
        game_id = game["_id"]
        possuidores = biblioteca_por_jogo.get(game_id, [])

        if not possuidores:
            continue

        reviews_do_jogo = base_reviews[review_index: review_index + 3]
        review_index += len(reviews_do_jogo)

        for i, template in enumerate(reviews_do_jogo):
            if i >= len(possuidores):
                break
            doc = {
                # campos de identidade primeiro
                "user_id": possuidores[i]["user_id"],
                "game_id": game_id,

                # campos de conteúdo
                "recomendado": template.get("recomendado"),
                "texto": template.get("texto", ""),
                "minutos_jogados": max(
                    template.get("minutos_jogados", 0),
                    possuidores[i].get("minutos_jogados", 0),
                ),
                "idioma": template.get("idioma", "pt-BR"),

                "created_at": now,
                "updated_at": now,

                "upvotes": template.get("upvotes", 0),
                "downvotes": template.get("downvotes", 0),

                "visivel": template.get("visivel", True),
                "denuncias": template.get("denuncias", False),
            }

            documents.append(doc)

    db["reviews"].insert_many(documents)
    print(f"{len(documents)} reviews inseridas.")
