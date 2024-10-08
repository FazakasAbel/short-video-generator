from src.api.endpoints import user, script, audio, project, render, image
from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(user.users_bp)
    app.register_blueprint(script.scripts_bp)
    app.register_blueprint(render.renders_bp)
    app.register_blueprint(audio.audios_bp)
    app.register_blueprint(project.projects_bp)
    app.register_blueprint(image.images_bp)
    CORS(app)
    return app

app = create_app()

