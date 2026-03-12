from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Acessar as variáveis
DB_USER = os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")
DB_CLUSTER = "cluster0"
DB_NAME = "elyndra"

REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

faltantes = []

if not DB_USER:
    faltantes.append("DB_USER")
if not DB_PASSWORD:
    faltantes.append("DB_PASSWORD")
if not DB_CLUSTER:
    faltantes.append("DB_CLUSTER")
if not REDIS_USER:
    faltantes.append("REDIS_USER")
if not REDIS_PASSWORD:
    faltantes.append("REDIS_PASSWORD")

if faltantes:
    raise RuntimeError(f"Variáveis de ambiente ausentes: {', '.join(faltantes)}.\nVocê criou um arquivo .env na raiz do projeto com as variáveis?")


print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
print(f"REDIS_USER: {REDIS_USER}")
print(f"REDIS_PASSWORD: {REDIS_PASSWORD}")