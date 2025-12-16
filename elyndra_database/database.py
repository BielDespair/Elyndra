from pymongo import MongoClient
from environment import DB_NAME, DB_USER, DB_CLUSTER, DB_PASSWORD

connection_string = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER}.bqi6pbv.mongodb.net/?appName=Cluster0"
client = MongoClient(connection_string)
db = client[DB_NAME]