from src.model.project import Project
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone 
from pymongo import MongoClient
from bson import ObjectId
from settings import MONGO_URI

class ProjectRepository:

    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.shortsdb
        self.projects_collection = self.db.projects

    def save_project(self, project : Project) -> str:
        project_data = project.to_json(include_id=False)
        result = self.projects_collection.insert_one(project_data)
        return str(result.inserted_id)

    def get_project(self, project_id : str) -> Project:
        data = self.projects_collection.find_one({"_id": ObjectId(project_id)})
        if not data:
            return None
        project = Project.from_json(data)
        return project
    
    def get_projects(self) -> list[Project]:
        data = self.projects_collection.find()
        return [Project.from_json(project_data) for project_data in data]

    def update_project(self, project_id, updated_data):
        updated_data_json = updated_data.to_json(include_id=False)
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": updated_data_json})

    def delete_project(self, project_id):
        self.projects_collection.delete_one({"_id": ObjectId(project_id)})

    def get_projects_by_user_id(self, user_id) -> list[Project]:
        data = self.projects_collection.find({"user_id": str(user_id)})
        return [Project.from_json(project_data) for project_data in data]
    
    def update_project_images(self, project_id, image_ids):
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": {"images": image_ids}})

    def update_project_script(self, project_id, script_id):
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": {"script_id": script_id}})

    def update_project_state(self, project_id, state):
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": {"state": state}})

    def update_project_render(self, project_id, render_id):
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": {"render_id": render_id}})   

    def update_project_voiceovers(self, project_id, audio_ids):
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": {"voiceovers": audio_ids}})     

