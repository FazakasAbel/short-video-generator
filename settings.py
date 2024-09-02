# settings.py
import os
from dotenv import load_dotenv

# Define the path to the .env file
dotenv_path = "./.env"

# Check if the .env file exists before loading it
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"Warning: {dotenv_path} file not found. Proceeding without loading environment variables from local source.")


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
VOICE_ID = os.environ.get("VOICE_ID")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
MONGO_URI = os.environ.get("MONGO_URI")
ZAP_CAP_API_KEY = os.environ.get("ZAP_CAP_API_KEY")
ZAP_CAP_URI = os.environ.get("ZAP_CAP_URI")