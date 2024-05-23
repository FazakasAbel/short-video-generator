from settings import OPENAI_API_KEY, MONGO_URI
from flask import Flask, request, jsonify
from scripts.script_generator import YouTubeScriptGenerator
from pymongo import MongoClient
from bson import ObjectId
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
        inserted_script = scripts_collection.insert_one({"theme": theme, "script": script})
        return jsonify(inserted_script), 200
    else:
        return jsonify({"error": "Failed to generate script"}), 500    

@app.route('/script/<script_id>', methods=['GET'])
def get_script(script_id):
    assert script_id == request.view_args['script_id']
    try:
        script_id = ObjectId(script_id)
    except:
        return jsonify({"error": "Invalid script ID format"}), 400
    
    script = scripts_collection.find_one({"_id": script_id})
    script['_id'] = str(script['_id']) 
    if script:
        return jsonify(script), 200
    else:
        return jsonify({"error": "Failed to find script"}), 404    

@app.route('/script/<script_id>', methods=['PUT'])
def update_script(script_id):
    assert script_id == request.view_args['script_id']
    try:
        script_id = ObjectId(script_id)
    except:
        return jsonify({"error": "Invalid script ID format"}), 400

    script = scripts_collection.find_one({"_id": script_id})
    if script:
        new_script = request.json.get('script')
        if new_script:
            scripts_collection.update_one({"_id": script_id}, {"$set": {"script": new_script}})
            updated_script = scripts_collection.find_one({"_id": script_id})
            updated_script['_id'] = str(updated_script['_id']) 
            return jsonify(updated_script), 200
        else:
            return jsonify({"error": "Content is required in the request body"}), 400
    else:
        return jsonify({"error": "Failed to find script"}), 404

@app.route('/slideshow/<script_id>', methods=['GET'])
def get_slideshow(script_id):
    assert script_id == request.view_args['script_id']
    data = request.json
    music = data.get('music')
    print(script_id + " ---- " + music)
    return {}, 200




if __name__ == "__main__":
    app.run(debug=True)

