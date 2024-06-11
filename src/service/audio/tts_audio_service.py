from settings import OPENAI_API_KEY
from openai import OpenAI
from pathlib import Path
import json
from tempfile import NamedTemporaryFile

class TTSAudioService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def generate_audio(self, text):
        response = self.client.audio.speech.with_streaming_response.create(
          model="tts-1",
          voice="alloy",
          input=text
        )

        with NamedTemporaryFile(suffix=".mp4") as temp_file:
            temp_filename = temp_file.name
            response.stream_to_file(temp_filename)
            temp_file.seek(0)
            return temp_file.read()