# api/music.py
from flask import Blueprint, request, jsonify, send_file
from pymongo import MongoClient
import gridfs
from settings import MONGO_URI
from bson.objectid import ObjectId
import os
from io import BytesIO

music_bp = Blueprint('music', __name__)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.shortsdb
fs = gridfs.GridFS(db)

@music_bp.route('/music', methods=['POST'])
def upload_music():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    artist = request.form.get('artist')
    title = request.form.get('title')
    
    if not artist or not title:
        return jsonify({"error": "Artist and title are required"}), 400
    
    music_id = fs.put(file, filename=file.filename, artist=artist, title=title)
    return jsonify({"_id": str(music_id), "artist": artist, "title": title}), 201

@music_bp.route('/music/<music_id>', methods=['GET'])
def get_music(music_id):
    try:
        music_id = ObjectId(music_id)
    except:
        return jsonify({"error": "Invalid music ID format"}), 400
    
    try:
        music_file = fs.get(music_id)
        if not music_file:
            return jsonify({"error": "Music file not found"}), 404
        response = {
            "_id": str(music_file._id),
            "filename": music_file.filename,
            "artist": music_file.artist,
            "title": music_file.title
        }
        
        # Using send_file correctly without headers as parameter
        file_data = BytesIO(music_file.read())
        file_data.seek(0)  # Ensure we're at the start of the BytesIO object

        return send_file(
            file_data,
            mimetype='audio/mp3',
            as_attachment=True,
            download_name=music_file.filename
        )
    except gridfs.errors.NoFile:
        print("Music file not found")
        return jsonify({"error": "Music file not found"}), 404
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    except:
        return jsonify({"error": "Can't read the music file properly"}), 500

@music_bp.route('/music/metadata/<music_id>', methods=['GET'])
def get_music_metadata(music_id):
    try:
        music_id = ObjectId(music_id)
    except:
        return jsonify({"error": "Invalid music ID format"}), 400
    
    try:
        music_file = fs.get(music_id)
        if not music_file:
            return jsonify({"error": "Music file not found"}), 404
        response = {
            "_id": str(music_file._id),
            "filename": music_file.filename,
            "artist": music_file.artist,
            "title": music_file.title
        }
        
        return jsonify(response), 200
    except gridfs.errors.NoFile:
        print("Music file not found")
        return jsonify({"error": "Music file not found"}), 404


@music_bp.route('/music/<music_id>', methods=['DELETE'])
def delete_music(music_id):
    try:
        music_id = ObjectId(music_id)
    except:
        return jsonify({"error": "Invalid music ID format"}), 400
    
    try:
        fs.delete(music_id)
        return {}, 204
    except:
        return jsonify({"error": "Music file not found"}), 404
