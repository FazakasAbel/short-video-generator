# api/slideshows.py
from flask import Blueprint, request, jsonify

slideshows_bp = Blueprint('slideshow', __name__)

@slideshows_bp.route('/slideshow/<script_id>', methods=['GET'])
def get_slideshow(script_id):
    data = request.json
    music = data.get('music')
    print(script_id + " ---- " + music)
    return {}, 200
