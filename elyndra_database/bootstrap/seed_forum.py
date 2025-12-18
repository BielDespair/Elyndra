import json
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path
from pymongo.database import Database
from bson import ObjectId


FORUM_PATH = Path("elyndra_database/bootstrap/seeds/forum.json")
MAX_REPLIES_PER_POST = 10


def seed_forum(db: Database, seed: int = 42) -> None:
    random.seed(seed)
    now = datetime.now(timezone.utc)

    with open(FORUM_PATH, "r", encoding="utf-8") as f:
        templates = json.load(f)

    if not templates:
        raise ValueError("forum.json está vazio.")

    games = list(db["games"].find({}, {"_id": 1}).sort("_id", 1))
    if not games:
        raise ValueError("Nenhum jogo encontrado.")
    
    biblioteca_por_jogo = {}
    for entry in db["biblioteca"].find(
        {}, {"_id": 0, "user_id": 1, "game_id": 1}
    ):
        biblioteca_por_jogo.setdefault(entry["game_id"], []).append(entry["user_id"])

    documents = []
    template_index = 0

    for game in games:
        game_id = game["_id"]
        users = biblioteca_por_jogo.get(game_id, [])

        if not users:
            continue

        num_posts = random.randint(1, min(2, len(users)))
        posts_templates = templates[template_index: template_index + num_posts]
        template_index += len(posts_templates)

        for i, tpl in enumerate(posts_templates):
            user_id = users[i % len(users)]

            created_at = now
            updated_at = now

            replies = []
            raw_replies = tpl.get("replies", [])[:MAX_REPLIES_PER_POST]

            for j, reply_tpl in enumerate(raw_replies):
                reply_user = users[(i + j + 1) % len(users)]

                replies.append({
                    "_id": ObjectId(),
                    "user_id": reply_user,
                    "conteudo": reply_tpl["conteudo"],
                    "created_at": created_at + timedelta(hours=j + 1),
                    "upvotes": random.randint(0, 5),
                    "downvotes": 0,
                    "deleted": False
                })

            doc = {
                "game_id": game_id,
                "user_id": user_id,

                "titulo": tpl["titulo"],
                "conteudo": tpl["conteudo"],
                "tags": tpl.get("tags", []),

                "created_at": created_at,
                "updated_at": updated_at,

                "upvotes": random.randint(0, 10),
                "downvotes": 0,

                "pinned": False,
                "locked": False,
                "deleted": False,

                "replies": replies
            }

            documents.append(doc)

    if not documents:
        raise ValueError("Nenhum post de fórum gerado.")

    db["forum"].insert_many(documents)
    print(f"{len(documents)} tópicos de fórum inseridos.")
