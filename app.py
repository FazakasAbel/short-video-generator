from settings import OPENAI_API_KEY, MONGO_URI
from flask import Flask, request, jsonify
from scripts.script_generator import YouTubeScriptGenerator
from pymongo import MongoClient
import os

app = Flask(__name__)

# Replace with your actual OpenAI API key
generator = YouTubeScriptGenerator(OPENAI_API_KEY)


# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.scriptsdb
scripts_collection = db.scripts

@app.route('/generate_script', methods=['POST'])
def generate_script():
    theme = request.args.get('theme')
    if not theme:
        return jsonify({"error": "Theme is required"}), 400
    
    script = generator.get_script(theme)
    if script:
        scripts_collection.insert_one({"theme": theme, "script": script})
        return jsonify(script)
    else:
        return jsonify({"error": "Failed to generate script"}), 500    

@app.route('/script/<script_id>', methods=['GET'])    
def update_script(script_id):
    assert script_id == request.view_args['script_id']
    data = request.json
    script = data.get('script')
    print(script_id + " ---- " + script)
    return {}, 200

@app.route('/slideshow/<script_id>', methods=['GET'])
def get_slideshow(script_id):
    assert script_id == request.view_args['script_id']
    data = request.json
    music = data.get('music')
    print(script_id + " ---- " + music)
    return {}, 200




if __name__ == "__main__":
    app.run(debug=True)

