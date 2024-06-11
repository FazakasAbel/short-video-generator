# api/render.py
from flask import Blueprint, request, jsonify, send_file
from src.service.render.render_service import RenderService
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone
from bson.objectid import ObjectId
from io import BytesIO
import logging

renders_bp = Blueprint('render', __name__)

render_service = RenderService()

@renders_bp.route('/render', methods=['POST'])
def save_render():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        render_id = render_service.save_render(file, file.filename)
        return jsonify(render_id), 201

    except Exception as e:
        logging.exception(f"Failed to save render: {str(e)}")
        return jsonify({"error": "Failed to save render"}), 500


@renders_bp.route('/render/<render_id>', methods=['GET'])
def get_render(render_id):
    try:
        render_id = ObjectId(render_id)
    except:
        return jsonify({"error": "Invalid render ID format"}), 400
    
    try:
        render = render_service.get_render(render_id)
        if not render:
            return jsonify({"error": "Render not found"}), 404
        
        
        file_data = BytesIO(render.file.read())
        file_data.seek(0)

        return send_file(
            file_data,
            mimetype='audio/mp3',
            as_attachment=True,
            download_name=render.filename
        )
    except Exception as e:
        logging.exception(f"Failed to get render: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@renders_bp.route('/render/<render_id>', methods=['DELETE'])
def delete_render(render_id):
    try:
        render_id = ObjectId(render_id)
        render_service.delete_render(render_id)
        return {}, 204
    
    except DocumentNotFound as e:
        return jsonify({"error": "Render not found"}), 404
    
    except Exception as e:
        logging.exception(f"Failed to delete render: {str(e)}")
        return jsonify({"error": "Failed to delete render"}), 500
        