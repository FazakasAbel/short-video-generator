import requests
import json
from typing import Tuple
from settings import ELEVENLABS_API_KEY, VOICE_ID
import os
import logging as log

class ElevenLabsService:
    """
    Service class to handle audio generation using the ElevenLabs Text-to-Speech API.
    """

    def __init__(self, voice_id: str = VOICE_ID):
        """
        Initialize the service with the provided voice ID and API key.

        Args:
        - voice_id (str): The ID of the voice model to use. Default is "zrHiDhphv9ZnVXBqCLjz".
        - api_key (str): Your API key for authentication. Default is the provided key.
        """
        self.voice_id = voice_id
        self.api_key = ELEVENLABS_API_KEY

    def generate_audio(self, text_to_speak: str):
        """
        Generate audio from text using the Text-to-Speech API.

        Args:
        - text_to_speak (str): The text to convert to speech.
        - output_path (str): The path to save the output audio file.

        Returns:
        - bool: True if audio generation is successful, False otherwise.
        """
        # Define constants for the script
        CHUNK_SIZE = 1024
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"

        # Set up headers for the API request, including the API key for authentication
        headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key
        }

        # Set up the data payload for the API request, including the text and voice settings
        data = {
            "text": text_to_speak,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }

        # Make the POST request to the TTS API with headers and data, enabling streaming response
        response = requests.post(tts_url, headers=headers, json=data, stream=True)

        # Check if the request was successful
        if response.ok:
            # Read the response in chunks and return it
            audio_data = b''
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                audio_data += chunk
            # Inform the user of success
            return audio_data
        else:
            log.exception(f"Error generating audio: {response.text}")
        

def main():

    eleven_labs_service = ElevenLabsService()
    audio_data = eleven_labs_service.generate_audio("Hello, world!")

    if audio_data:
        with open("output.mp3", "wb") as f:
            f.write(audio_data)
        print("Audio saved to output.mp3")
    else:
        print("Audio generation failed.")
        

if __name__ == "__main__":
    main()

        

