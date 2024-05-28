from pymongo import MongoClient
from bson import ObjectId
from settings import MONGO_URI

class ProjectRepository:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client['your_database_name']
        self.projects_collection = self.db['projects']

    def create_project(self, user_id, theme, state, script_id, images, music_id, render_id):
        project_data = {
            "_user_id": user_id,
            "theme": theme,
            "state": state,
            "_script_id": script_id,
            "images": images,
            "_music_id": music_id,
            "_render_id": render_id
        }
        result = self.projects_collection.insert_one(project_data)
        return str(result.inserted_id)

    def get_project(self, project_id):
        project = self.projects_collection.find_one({"_id": ObjectId(project_id)})
        return project

    def update_project(self, project_id, updated_data):
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": updated_data})

    def delete_project(self, project_id):
        self.projects_collection.delete_one({"_id": ObjectId(project_id)})
