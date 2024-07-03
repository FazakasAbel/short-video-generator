import gridfs
from bson import ObjectId
from pymongo import MongoClient
from settings import MONGO_URI
from src.model.audio import Audio

class AudioRepository:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client.shortsdb
        self.audio_collection = gridfs.GridFS(self.db)

    def save_audio(self, audio):
        inserted_id = self.audio_collection.put(audio.file, filename=audio.filename)
        return str(inserted_id)

    def get_audio(self, audio_id):
        try:
            data = self.audio_collection.get(ObjectId(audio_id)) 
            if not data:
                return None
            
            audio = Audio(str(data._id), data, data.filename)
            return audio
        except gridfs.errors.NoFile:
            return None

    def delete_audio(self, audio_id):
        self.audio_collection.delete(ObjectId(audio_id))