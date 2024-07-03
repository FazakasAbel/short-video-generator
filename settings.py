# settings.py
import os
from dotenv import load_dotenv

dotenv_path = "./.env"
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
VOICE_ID = os.environ.get("VOICE_ID")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
MONGO_URI = os.environ.get("MONGO_URI")
ZAP_CAP_API_KEY = os.environ.get("ZAP_CAP_API_KEY")
ZAP_CAP_URI = os.environ.get("ZAP_CAP_URI")