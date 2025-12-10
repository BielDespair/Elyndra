from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Acessar as variáveis
DB_USER = os.getenv("DB_USER")
DB_PASSWORD= os.getenv("DB_PASSWORD")
DB_CLUSTER = "cluster0"
DB_NAME = "elyndra"

faltantes = []

if not DB_USER:
    faltantes.append("DB_USER")
if not DB_PASSWORD:
    faltantes.append("DB_PASSWORD")
if not DB_CLUSTER:
    faltantes.append("DB_CLUSTER")

if faltantes:
    raise RuntimeError(f"Variáveis de ambiente ausentes: {', '.join(faltantes)}.\nVocê criou um arquivo .env na raiz do projeto com as variáveis?")


print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {DB_PASSWORD}")