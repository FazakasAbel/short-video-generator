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

    def save_project(self, project):
        project_data = project.to_json(include_id=False)
        result = self.projects_collection.insert_one(project_data)
        return str(result.inserted_id)

    def get_project(self, project_id):
        data = self.projects_collection.find_one({"_id": ObjectId(project_id)})
        if not data:
            return None
        project = Project(id=str(data["_id"]), 
                          user_id=data["user_id"], 
                          title=data["title"], 
                          script_id=data["script_id"], 
                          images=data["images"], 
                          audio_id=data["audio_id"], 
                          render_id=data["render_id"], 
                          state=data["state"])
        return project

    def update_project(self, project_id, updated_data):
        updated_data_json = updated_data.to_json(include_id=False)
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": updated_data_json})

    def delete_project(self, project_id):
        self.projects_collection.delete_one({"_id": ObjectId(project_id)})

    def get_projects_by_user_id(self, user_id):
        data = self.projects_collection.find({"user_id": str(user_id)})
        projects = []
        for project_data in data:
            project = Project(str(project_data["_id"]), project_data["user_id"], project_data["title"], project_data["script_id"], project_data["images"], project_data["audio_id"], project_data["render_id"], project_data["state"])
            projects.append(project)
        return [project.to_json() for project in projects]
    
    def update_project_images(self, project_id, image_ids):
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": {"images": image_ids}})

    def update_project_script(self, project_id, script_id):
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": {"script_id": script_id}})

    def update_project_state(self, project_id, state):
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": {"state": state}})

    def update_project_render(self, project_id, render_id):
        self.projects_collection.update_one({"_id": ObjectId(project_id)}, {"$set": {"render_id": render_id}})    

