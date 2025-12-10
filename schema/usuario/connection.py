from pymongo import MongoClient
from enviroment import *

# 2. Criar a connection string
connection_string = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER}.bqi6pbv.mongodb.net/?appName=Cluster0"

# 3. Conectar no MongoDB
client = MongoClient(connection_string)

# 4. Escolher um banco e uma coleção
db = client["elyndra"]
collection = db["usuarios"]

# 5. Teste: inserir um documento
resultado = collection.insert_one({"nome": "Thales", "idade": 22})

print("Conectado ao MongoDB!")
print("ID inserido:", resultado.inserted_id)


