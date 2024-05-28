# api/users.py
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from settings import MONGO_URI
import os

users_bp = Blueprint('users', __name__)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.shortsdb
users_collection = db.users

@users_bp.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    
    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400
    
    user = {
        "username": username,
        "email": email,
        "projects": []
    }
    
    inserted_user_result = users_collection.insert_one(user)
    inserted_user = {
        "_id": str(inserted_user_result.inserted_id),
        "username": username,
        "email": email
    }
    
    return jsonify(inserted_user), 201

@users_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user_id = ObjectId(user_id)
    except:
        return jsonify({"error": "Invalid user ID format"}), 400
    
    user = users_collection.find_one({"_id": user_id})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@users_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_id = ObjectId(user_id)
    except:
        return jsonify({"error": "Invalid user ID format"}), 400
    
    user = users_collection.find_one({"_id": user_id})
    if user:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        
        if not username or not email:
            return jsonify({"error": "Username and email are required"}), 400

        users_collection.update_one({"_id": user_id}, {"$set": {"username": username, "email": email}})
        updated_user = users_collection.find_one({"_id": user_id})
        updated_user['_id'] = str(updated_user['_id'])
        
        return jsonify(updated_user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@users_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_id = ObjectId(user_id)
    except:
        return jsonify({"error": "Invalid user ID format"}), 400
    
    user = users_collection.find_one({"_id": user_id})
    if user:
        users_collection.delete_one({"_id": user_id})
        return {}, 204
    else:
        return jsonify({"error": "User not found"}), 404
