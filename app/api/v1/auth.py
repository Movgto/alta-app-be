from flask import Blueprint, request
from app.db import db
from app.models import User

def register_routes(bp: Blueprint):
    '''Register authentication routes with the given blueprint.'''

    @bp.route('/auth/signup', methods=['POST'])
    def signup():
        request_data = request.get_json()
        email = request_data.get("email")
        password = request_data.get("password")
        name = request_data.get("name")

        if not email or not password or not name:
            return {"message": "Missing required fields"}, 400
        
        try:
            new_user = User(email=email, password=password, name=name)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error occurred while signing up"}, 500

        return {
            "message": "User signed up successfully!"
        }

    @bp.route('/auth/login', methods=['POST'])
    def login():
        request_data = request.get_json()
        email = request_data.get("email")
        password = request_data.get("password")
        password_confirmation = request_data.get("password_confirmation")

        if not email or not password or not password_confirmation:
            return {"message": "Missing required fields"}, 400

        if password != password_confirmation:
            return {"message": "Passwords do not match"}, 400

        user: User = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return {"message": "Invalid email or password"}, 401

        return {
            "message": "User logged in successfully!"
        }