from src.repo.audio_repo import audioRepository
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.model.audio import audio
import logging

class audioService:
    def __init__(self):
        self.repo = audioRepository()

    def save_audio(self, file, filename):
        audio = audio(file=file, filename=filename)
        return self.repo.save_audio(audio)

    def get_audio(self, audio_id):
        audio = self.repo.get_audio(audio_id)
        if not audio:
            raise DocumentNotFound
        
        return audio    

    def delete_audio(self, audio_id):
        audio = self.repo.get_audio(audio_id)
        if not audio:
            raise DocumentNotFound
        
        self.repo.delete_audio(audio_id)    
