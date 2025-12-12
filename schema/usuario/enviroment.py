from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Acessar as variáveis
DB_USER = os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")
DB_CLUSTER = "cluster0"

missing = []

if not DB_USER:
    missing.append("DB_USER")
if not DB_PASSWORD:
    missing.append("DB_PASSWORD")
if not DB_CLUSTER:
    missing.append("DB_CLUSTER")

if missing:
    raise RuntimeError(
        f"Variáveis de ambiente ausentes: {', '.join(missing)}"
    )



print(DB_USER, DB_PASSWORD)


