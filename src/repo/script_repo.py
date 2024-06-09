from pymongo import MongoClient
from bson import ObjectId
from settings import MONGO_URI
from src.model.script import Script

class ScriptRepository:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.shortsdb
        self.scripts_collection = self.db.scripts

    def save_script(self, script):
        script_data = script.to_json(include_id=False)
        result = self.scripts_collection.insert_one(script_data)
        return str(result.inserted_id)

    def get_script(self, script_id):
        data = self.scripts_collection.find_one({"_id": ObjectId(script_id)})
        if not data:
            return None

        script = Script.from_json(data)
        return script

    def update_script(self, script_id, updated_data):
        updated_data_json = updated_data.to_json(include_id=False)
        self.scripts_collection.update_one({"_id": ObjectId(script_id)}, {"$set": updated_data_json})

    def delete_script(self, script_id):
        delete_result = self.scripts_collection.delete_one({"_id": ObjectId(script_id)})
        return delete_result.deleted_count > 0