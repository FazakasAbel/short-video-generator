
# api/script.py
from flask import Blueprint, request, jsonify
from src.service.script.script_service import ScriptService
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone    
from bson.objectid import ObjectId
from src.model.script import Script
from src.model.scene import Scene
import logging

scripts_bp = Blueprint('script', __name__)
script_service = ScriptService()

@scripts_bp.route('/api/script', methods=['POST'])
def generate_script():
    try:
        theme = request.args.get('theme')

        if not theme:
            return jsonify({"error": "Theme and script are required"}), 400


        scene_list : list[Scene] = script_service.generate_script(theme)
        if scene_list:
            script_id = script_service.save_script(Script(theme=theme, script=scene_list))
            return jsonify({"id": f"{script_id}"}), 201 # return jsonify(script_id), 201
        return jsonify({"error": "Failed to generate script"}), 500

    except Exception as e:
        logging.exception(f"Failed to create script: {str(e)}")
        return jsonify({"error": "Failed to create script"}), 500


@scripts_bp.route('/api/script/<script_id>', methods=['GET'])
def get_script(script_id):
    try:
        script_id = ObjectId(script_id)
        script = script_service.get_script(script_id)
        return script.to_json(), 200

    except DocumentNotFound as e:
        return jsonify({"error": "Script not found"}), 404

    except Exception as e:
        logging.exception(f"Failed to get script: {str(e)}")
        return jsonify({"error": "Failed to get script"}), 500


@scripts_bp.route('/script/<script_id>', methods=['PUT'])
def update_script(script_id):
    try:
        script_id = ObjectId(script_id)
        data = request.json
        script = Script.from_json(data)

        updated_script = script
        script_service.update_script(script_id, updated_script)
        return {}, 204

    except DocumentNotFound as e:
        return jsonify({"error": "Script not found"}), 404

    except Exception as e:
        logging.exception(f"Failed to update script: {str(e)}")
        return jsonify({"error": "Failed to update script"}), 500


@scripts_bp.route('/script/<script_id>', methods=['DELETE'])
def delete_script(script_id):
    try:
        script_id = ObjectId(script_id)
        script_service.delete_script(script_id)
        return {}, 204

    except DocumentNotFound as e:
        return jsonify({"error": "Script not found"}), 404

    except Exception as e:
        logging.exception(f"Failed to delete script: {str(e)}")
        return jsonify({"error": "Failed to delete script"}), 500

