from bson import ObjectId

class UserRepository:

    def __init__(self, db):
        self.collection = db["users"]

    def create(self, data: dict):
        return self.collection.insert_one(data)

    def find_by_email(self, email: str):
        return self.collection.find_one({"email": email})

    def find_by_id(self, user_id: str):
        return self.collection.find_one({"_id": ObjectId(user_id)})
