# api/image.py
from flask import Blueprint, jsonify, request
from src.service.image_service import ImageService
from src.api.exceptions.DocumentNotFound import DocumentNotFound
from bson.objectid import ObjectId
from src.model.image_url import ImageUrl
import logging

images_bp = Blueprint('image', __name__)
image_service = ImageService()

@images_bp.route('/image', methods=['POST'])
def save_image():
    try:
        data = request.json
        url = data.get('url')
        duration = data.get('duration')

        if not url or not duration:
            return jsonify({'error': 'URL and duration are required'}), 400

        image_id = image_service.save_image_url(url, duration)
        return jsonify(image_id), 201

    except Exception as e:
        logging.exception(f"Failed to save image: {str(e)}")
        return jsonify({'error': 'Failed to save image'}), 500


@images_bp.route('/image/<image_id>', methods=['GET'])
def get_image_url(image_id):
    try:
        image_id = ObjectId(image_id)
        image_url = image_service.get_image_url(image_id)
        return image_url.to_json(), 200
    except DocumentNotFound as e:
        return jsonify({'error': 'Image not found'}), 404

    except Exception as e:
        logging.exception(f"Failed to get image URL: {str(e)}")
        return jsonify({'error': 'Failed to get image URL'}), 500

