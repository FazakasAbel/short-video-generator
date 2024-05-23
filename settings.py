# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
VOICE_ID = os.environ.get("VOICE_ID")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")