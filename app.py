from api import script, music, slideshow, user
from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(script.scripts_bp)
    app.register_blueprint(slideshow.slideshows_bp)
    app.register_blueprint(music.music_bp)
    app.register_blueprint(user.users_bp)
    return app

app = create_app()

