from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
import logging
from datetime import datetime
from flask.json.provider import DefaultJSONProvider
import json
from app.extensions import db, migrate, jwt, mail, cache, celery
from app.api import bp as api_bp

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json_encoder = CustomJSONEncoder

    # Initialize extensions
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    celery.conf.update(app.config)

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    app.register_blueprint(api_bp, url_prefix='/api')

    from app.customer import bp as customer_bp
    app.register_blueprint(customer_bp, url_prefix='/api/customer')

    from app.professional import bp as professional_bp
    app.register_blueprint(professional_bp, url_prefix='/api/professional')

    from app.services import bp as services_bp
    app.register_blueprint(services_bp, url_prefix='/api/services')

    # Add CORS headers to all responses
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
        return response

    @app.route('/test')
    def test():
        print("Flask application is working!")
        return jsonify({'message': 'Flask application is working!'})

    # Create database tables
    with app.app_context():
        db.create_all()

    return app