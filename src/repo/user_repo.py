from pymongo import MongoClient
from bson import ObjectId
from settings import MONGO_URI
from src.model.user import User

class UserRepository:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.shortsdb
        self.users_collection = self.db.users

    def save_user(self, user):
        user_data = user.to_json(include_id=False)
        result = self.users_collection.insert_one(user_data)
        return str(result.inserted_id)

    def get_user(self, user_id):
        data = self.users_collection.find_one({"_id": ObjectId(user_id)})
        if not data:
            return None
        
        user = User(str(data["_id"]), data["username"], data["email"], data["project_ids"])
        return user

    def update_user(self, user_id, updated_data):
        updated_data_json = updated_data.to_json(include_id=False)
        self.users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data_json})

    def delete_user(self, user_id):
        self.users_collection.delete_one({"_id": ObjectId(user_id)})