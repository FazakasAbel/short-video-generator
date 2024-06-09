# api/users.py
from flask import Blueprint, request, jsonify
from service.user_service import UserService
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from src.api.exceptions.NoUpdateDone import NoUpdateDone    
from bson.objectid import ObjectId
from src.model.user import User
import logging

users_bp = Blueprint('user', __name__)

user_service = UserService()

@users_bp.route('/user', methods=['POST'])
def save_user():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        
        if not username or not email:
            return jsonify({"error": "Username and email are required"}), 400
        
        user_id = user_service.save_user(username, email)
        return jsonify(user_id), 201
    except Exception as e:
        logging.exception(f"Failed to create user: {str(e)}")
        return jsonify({"error": "Failed to create user"}), 500

@users_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user_id = ObjectId(user_id)
        user = user_service.get_user(user_id)
        return user.to_json(), 200
    
    except DocumentNotFound as e:
        return jsonify({"error": "User not found"}), 404
    
    except Exception as e:
        logging.exception(f"Failed to get user: {str(e)}")
        return jsonify({"error": "Failed to get user"}), 500

@users_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_id = ObjectId(user_id)
        data = request.json
        username = data.get('username')
        email = data.get('email')
        project_ids = data.get('project_ids')
        
        if not username or not email or not project_ids:
            return jsonify({"error": "Username, email and project ids are required"}), 400
        
        update_user = User(username=username, email=email, project_ids=project_ids)
        user = user_service.update_user(user_id, update_user)
        return user.to_json(), 200
    
    except DocumentNotFound as e:
        return jsonify({"error": "User not found"}), 404
    
    except NoUpdateDone as e:
        return jsonify({"error": "No update was done"}), 409
    
    except Exception as e:
        logging.exception(f"Failed to update user: {str(e)}")
        return jsonify({"error": "Failed to update user"}), 500

@users_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_id = ObjectId(user_id)
        user_service.delete_user(user_id)
        return {}, 204
    
    except DocumentNotFound as e:
        return jsonify({"error": "User not found"}), 404
    
    except Exception as e:
        logging.exception(f"Failed to delete user: {str(e)}")
        return jsonify({"error": "Failed to delete user"}), 500


