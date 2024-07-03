from pymongo import MongoClient
from bson import ObjectId
from settings import MONGO_URI
from src.model.image_url import Image

class ImageUrlRepository:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.shortsdb
        self.images_collection = self.db.images

    def save_image(self, image : Image) -> str:
        image_data = image.to_json(include_id=False)
        result = self.images_collection.insert_one(image_data)
        return str(result.inserted_id)

    def get_image(self, image_id : str) -> Image:  
        data = self.images_collection.find_one({"_id": ObjectId(image_id)})
        if not data:
            return None

        image_url = Image.from_json(data)
        return image_url   

    def update_image(self, image_id : str, updated_data : Image):
        updated_data_json = updated_data.to_json(include_id=False)
        self.images_collection.update_one({"_id": ObjectId(image_id)}, {"$set": updated_data_json})

    def delete_image(self, image_id : str) -> bool:
        delete_result = self.images_collection.delete_one({"_id": ObjectId(image_id)})
        return delete_result.deleted_count > 0
         


