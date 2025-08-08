from flask import Blueprint, render_template
from app.api.v1 import clients, auth

api_bp = Blueprint('api', __name__, url_prefix='/api')

clients.register_routes(api_bp)
auth.register_routes(api_bp)
