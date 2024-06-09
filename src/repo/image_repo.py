from pymongo import MongoClient
from bson import ObjectId
from settings import MONGO_URI
from src.model.image_url import ImageUrl

class ImageUrlRepository:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.shortsdb
        self.image_urls_collection = self.db.image_urls

    def save_image_url(self, image_url : ImageUrl):
        image_url_data = image_url.to_json(include_id=False)
        result = self.image_urls_collection.insert_one(image_url_data)
        return str(result.inserted_id)

    def get_image_url(self, image_url_id):  
        data = self.image_urls_collection.find_one({"_id": ObjectId(image_url_id)})
        if not data:
            return None

        image_url = ImageUrl.from_json(data)
        return image_url   

    def update_image_url(self, image_url_id, updated_data):
        updated_data_json = updated_data.to_json(include_id=False)
        self.image_urls_collection.update_one({"_id": ObjectId(image_url_id)}, {"$set": updated_data_json})

    def delete_image_url(self, image_url_id):
        delete_result = self.image_urls_collection.delete_one({"_id": ObjectId(image_url_id)})
        return delete_result.deleted_count > 0
         


