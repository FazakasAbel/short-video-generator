from src.repo.audio_repo import AudioRepository
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.model.audio import Audio
from src.service.audio.tts_audio_service import TTSAudioService
from src.api.exceptions.GenerationUnsuccessful import GenerationUnsuccessful
import logging

class AudioService:
    def __init__(self):
        self.repo = AudioRepository()
        self.text_to_speech_service = TTSAudioService()

    def save_audio(self, file, filename):
        audio = Audio(file=file, filename=filename)
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

    def generate_voiceover(self, text):
        voiceover = self.text_to_speech_service.generate_audio(text)
        if not voiceover:
            raise GenerationUnsuccessful("Failed to generate voiceover")
        return voiceover
