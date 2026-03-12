from bson import ObjectId
class UserRepository:
    def __init__(self, db):
        self.collection = db["usuarios"]

    def create(self, data: dict):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def find_by_email(self, email: str):
        user = self.collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user

    def find_by_id(self, user_id: str):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
        return user

    def listar(self):
        usuarios = list(self.collection.find())
        for usuario in usuarios:
            usuario["_id"] = str(usuario["_id"])  # necessário
        return usuarios
