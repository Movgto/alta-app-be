import os
from flask import Flask
from flask_cors import CORS
from app.config import config
from app.api import api_bp
from app.db import db

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Carga la configuración con la clase correspondiente
    app.config.from_object(config[config_name])

    db.init_app(app)

    print(f'Cors Origins: {app.config["CORS_ORIGINS"]}')
    print(f'Database URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    
    # Configure CORS
    CORS(app, 
         origins=app.config['CORS_ORIGINS'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         supports_credentials=True
    )

    app.register_blueprint(api_bp)

    # Import models to ensure they are registered in the DB
    from app.models import Client, Document

    with app.app_context():
        db.create_all()

    return app