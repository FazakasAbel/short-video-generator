# Example usage in Flask route
from flask import Blueprint, request, jsonify
from src.repo.project_repo import ProjectRepository

projects_bp = Blueprint('project', __name__)
project_repository = ProjectRepository()

@projects_bp.route('/project', methods=['POST'])
def create_project():
    data = request.json
    project_id = project_repository.create_project(
        data.get('_user_id'),
        data.get('theme'),
        data.get('state'),
        data.get('_script_id'),
        data.get('images'),
        data.get('_music_id'),
        data.get('_render_id')
    )
    return jsonify({"project_id": project_id}), 201
