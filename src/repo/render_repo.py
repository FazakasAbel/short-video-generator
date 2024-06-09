import gridfs
from bson import ObjectId
from pymongo import MongoClient
from settings import MONGO_URI
from src.model.render import Render
from src.api.exceptions.DocumentNotFound import DocumentNotFound

class RenderRepository:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.shortsdb
        self.render_collection = gridfs.GridFS(self.db)

    def save_render(self, render):
        inserted_id = self.render_collection.put(render.file, filename=render.filename)
        return str(inserted_id)

    def get_render(self, render_id):
        try:
            data = self.render_collection.get(ObjectId(render_id))
            if not data:
                return None
            
            render = Render(str(data._id), data, data.filename)
            return render
        except gridfs.errors.NoFile:
            return None
        
    def delete_render(self, render_id):
        self.render_collection.delete(ObjectId(render_id))   
