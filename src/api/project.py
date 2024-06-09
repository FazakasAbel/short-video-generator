# api/project.py
from flask import Blueprint, request, jsonify
from src.service.project_service import ProjectService
from src.service.script_service import ScriptService
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.GenerationUnsuccessful import GenerationUnsuccessful
from src.api.exceptions.NoUpdateDone import NoUpdateDone    
from bson.objectid import ObjectId
from src.model.project import Project
import logging

projects_bp = Blueprint('project', __name__)

project_service = ProjectService()


@projects_bp.route('/project', methods=['POST'])
def save_project():
    try:
        data = request.json
        title = data.get('title')
        user_id = data.get('user_id')
        state = data.get('state')

        if not user_id or not state or not title:
            return jsonify({"error": "Theme, title, state and user_id are required"}), 400
        
        project_id = project_service.save_project(title=title, user_id=user_id, state=state)
        return jsonify(project_id), 201
    except Exception as e:
        logging.exception(f"Failed to create project: {str(e)}")
        return jsonify({"error": "Failed to create project"}), 500


@projects_bp.route('/project/<project_id>', methods=['GET'])
def get_project(project_id):
    try:
        project_id = ObjectId(project_id)
        project = project_service.get_project(project_id)
        return project.to_json(), 200
    
    except DocumentNotFound as e:
        return jsonify({"error": "Project not found"}), 404
    
    except Exception as e:
        logging.exception(f"Failed to get project: {str(e)}")
        return jsonify({"error": "Failed to get project"}), 500


@projects_bp.route('/project/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        project_id = ObjectId(project_id)
        project_service.delete_project(project_id)
        return {}, 204
    
    except DocumentNotFound as e:
        return jsonify({"error": "Project not found"}), 404
    
    except Exception as e:
        logging.exception(f"Failed to delete project: {str(e)}")
        return jsonify({"error": "Failed to delete project"}), 500


@projects_bp.route('/project/<project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        project_id = ObjectId(project_id)
        data = request.json
        title = data.get('title')
        script_id = data.get('script_id')
        images = data.get('images')
        audio_id = data.get('audio_id')
        render_id = data.get('render_id')
        state = data.get('state')
        
        if not title and not script_id and not images and not audio_id and not render_id and not state:
            return jsonify({"error": "Title, script id, images, audio id, render id or state are required"}), 400
        
        update_project = Project(title=title, script_id=script_id, images=images, audio_id=audio_id, render_id=render_id, state=state)
        project = project_service.update_project(project_id, update_project)
        return project.to_json(), 200
    
    except DocumentNotFound as e:
        return jsonify({"error": "Project not found"}), 404
    
    except NoUpdateDone as e:
        return jsonify({"error": "No update done"}), 409
    
    except Exception as e:
        logging.exception(f"Failed to update project: {str(e)}")
        return jsonify({"error": "Failed to update project"}), 500
    
@projects_bp.route('/projects/<user_id>', methods=['GET'])
def get_projects_by_user_id(user_id):
    try:
        user_id = ObjectId(user_id)
        projects = project_service.get_projects_by_user_id(user_id)
        return jsonify(projects), 200
    except Exception as e:
        logging.exception(f"Failed to update project: {str(e)}")
        return jsonify({"error": "Failed to update project"}), 500    
    
@projects_bp.route('/project/<project_id>/state', methods=['PUT'])
def update_project_state(project_id):
    try:
        project_id = ObjectId(project_id)
        data = request.json
        state = data.get('state')
        project = project_service.update_project_state(project_id, state)
        return jsonify(project), 200
    except DocumentNotFound as e:
        return jsonify({"error": "Project not found"}), 404
    except NoUpdateDone as e:
        return jsonify({"error": "No update done"}), 409
    except Exception as e:
        logging.exception(f"Failed to update project: {str(e)}")
        return jsonify({"error": "Failed to update project"}), 500
    
@projects_bp.route('/project/<project_id>/generate/images', methods=['POST'])
def generate_project_images(project_id):
    try:
        project_id = ObjectId(project_id)
        image_ids = project_service.generate_images(project_id)
        return jsonify(image_ids), 204
    except DocumentNotFound as e:
        return jsonify({"error": e.message}), 404
    except NoUpdateDone:
        return jsonify({"error": "No update done"}), 409
    except Exception as e:
        logging.exception(f"Failed to update project: {str(e)}")
        return jsonify({"error": "Failed to update project"}), 500

@projects_bp.route('/project/<project_id>/generate/script', methods=['POST'])
def generate_project_script(project_id):
    theme = request.args.get('theme')
    if not theme:
        return jsonify({"error": "Theme and script are required"}), 400

    try:
        project_id = ObjectId(project_id)
        script_id = project_service.generate_script(project_id, theme)
        return jsonify(script_id), 204
    except GenerationUnsuccessful as e:
        return jsonify({"error": e.message}), 404    
    except DocumentNotFound as e:
        return jsonify({"error": e.message}), 404
    except NoUpdateDone:
        return jsonify({"error": "No update done"}), 409
    except Exception as e:
        logging.exception(f"Failed to update project: {str(e)}")
        return jsonify({"error": "Failed to update project"}), 500

@projects_bp.route('/project/<project_id>/generate/slideshow', methods=['POST'])
def generate_project_slideshow(project_id):
    try:
        project_id = ObjectId(project_id)
        render_id = project_service.generate_project_slideshow(project_id)
        return jsonify(render_id), 204
    except DocumentNotFound as e:
        return jsonify({"error": e.message}), 404
    except NoUpdateDone:
        return jsonify({"error": "No update done"}), 409
    except Exception as e:
        logging.exception(f"Failed to update project: {str(e)}")
        return jsonify({"error": "Failed to update project"}), 500
