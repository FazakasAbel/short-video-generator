# api/audio.py
from flask import Blueprint, request, jsonify, send_file
from src.service.audio_service import AudioService
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone    
from bson.objectid import ObjectId
from io import BytesIO
import logging

audios_bp = Blueprint('audio', __name__)

audio_service = AudioService()

@audios_bp.route('/audio', methods=['POST'])
def save_audio():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        audio_id = audio_service.save_audio(file.file, file.filename)
        return jsonify(audio_id), 201

    except Exception as e:
        logging.exception(f"Failed to save audio: {str(e)}")
        return jsonify({"error": "Failed to save audio"}), 500


@audios_bp.route('/audio/<audio_id>', methods=['GET'])
def get_audio(audio_id):
    try:
        audio_id = ObjectId(audio_id)
    except:
        return jsonify({"error": "Invalid audio ID format"}), 400
    
    try:
        audio = audio_service.get_audio(audio_id)
        if not audio:
            return jsonify({"error": "audio not found"}), 404
        
        file_data = BytesIO(audio.file.read())
        file_data.seek(0)

        return send_file(
            file_data,
            mimetype='audio/mp3',
            as_attachment=True,
            download_name=audio.filename
        )
    except Exception as e:
        logging.exception(f"Failed to get audio: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
    
@audios_bp.route("/audio/<audio_id>", methods=["DELETE"])
def delete_audio(audio_id):
    try:
        audio_id = ObjectId(audio_id)
        audio_service.delete_audio(audio_id)
        return {}, 204
    except DocumentNotFound as e:
        return jsonify({"error": "audio not found"}), 404  
    
    except Exception as e:
        logging.exception(f"Failed to delete user: {str(e)}")
        return jsonify({"error": "Failed to delete user"}), 500