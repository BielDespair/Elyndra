from datetime import datetime, timezone
import random
from pymongo.database import Database



MAX_GAMES_PER_USER = 5

def seed_biblioteca(db: Database, seed: int = 42):
    
    users = db["usuarios"].find({}, {"_id": 1}).to_list()
    games = db["games"].find({}, {"_id": 1}).to_list()
    
    if not users or not games:
        raise ValueError("Usuários ou jogos não encontrados. Certifique-se de que as coleções 'usuarios' e 'games' estejam populadas.")
    
    random.seed(seed)
    
    documents = []
    for user in users:
        num_games = random.randint(1, min(MAX_GAMES_PER_USER, len(games)))
        jogos_aleatorios = random.sample(games, num_games)

        for game in jogos_aleatorios:
            doc = {
                "user_id": user["_id"],
                "game_id": game["_id"],
                "status": "adquirido",
                "adquirido_em": datetime.now(timezone.utc),
                "minutos_jogados": 0,
                "conquistas": [],
                "sessao": None,
                "instalacao": {
                    "instalado": False,
                    "version": None,
                },
            }
            documents.append(doc)

    if documents:
        result = db["biblioteca"].insert_many(documents)
        print(f"{len(result.inserted_ids)} registros de biblioteca inseridos.")
    else:
        raise ValueError("Nenhum documento para inserir na biblioteca.")