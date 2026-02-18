from elyndra_database.connection import get_database

db = get_database()

print(db.list_collection_names())
