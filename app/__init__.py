# ==== app/__init__.py ====
from flask import Flask
from flask_cors import CORS
from app.routes.api import api_blueprint
from app.config import Config
from app.extensions.db import mysql
from app.routes.soal_routes import soal_bp
from app.routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = 'ini_rahasia_sangat_rahasia_123'
    CORS(app)

    # Load config
    app.config.from_object(Config)

    # Init MySQL
    mysql.init_app(app)

    # Register API Blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(soal_bp)
    app.register_blueprint(user_bp)

    return app
