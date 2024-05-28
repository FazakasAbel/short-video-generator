# api/scripts.py
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from settings import MONGO_URI, OPENAI_API_KEY
from scripts.script_generator import YouTubeScriptGenerator
import os

scripts_bp = Blueprint('script', __name__)

# Replace with your actual OpenAI API key
generator = YouTubeScriptGenerator(OPENAI_API_KEY)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.shortsdb
scripts_collection = db.scripts

@scripts_bp.route('/script/generate', methods=['POST'])
def generate_script():
    theme = request.args.get('theme')
    if not theme:
        return jsonify({"error": "Theme is required"}), 400
    
    script = generator.get_script(theme)
    if script:
        inserted_script = scripts_collection.insert_one({"theme": theme, "script": script})
        inserted_script = {
            "_id": str(inserted_script.inserted_id),
            "theme": theme,
            "script": script
        } 
        return jsonify(inserted_script), 200
    else:
        return jsonify({"error": "Failed to generate script"}), 500    

@scripts_bp.route('/script/<script_id>', methods=['GET'])
def get_script(script_id):
    try:
        script_id = ObjectId(script_id)
    except:
        return jsonify({"error": "Invalid script ID format"}), 400
    
    script = scripts_collection.find_one({"_id": script_id})
    if script:
        script['_id'] = str(script['_id']) 
        return jsonify(script), 200
    else:
        return jsonify({"error": "Failed to find script"}), 404    

@scripts_bp.route('/script/<script_id>', methods=['PUT'])
def update_script(script_id):
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

@scripts_bp.route('/script/<script_id>', methods=['DELETE'])
def delete_script(script_id):
    try:
        script_id = ObjectId(script_id)
    except:
        return jsonify({"error": "Invalid script ID format"}), 400

    script = scripts_collection.find_one({"_id": script_id})
    if script:
        scripts_collection.delete_one({"_id": script_id})
        return {}, 204
    else:
        return jsonify({"error": "Failed to find script"}), 404
