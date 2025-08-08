from app.models import User
from app.db import db
from bcrypt import hashpw, gensalt, checkpw
import jwt
from start import app
from datetime import datetime, timedelta

class AuthService:    

    @staticmethod
    def signup(email: str, password: str, name: str) -> bool:
        try:
            new_user = User(email=email, password=password, name=name)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"message": "Error occurred while signing up"}, 500
        
        return {"message": "User signed up successfully!"}, 200

    @staticmethod
    def login(email: str, password: str) -> bool:        
        try:
            user: User = User.query.filter_by(email=email).first()
        except Exception as e:
            return {"message": f"Error occurred while logging in: {str(e)}"}, 500
        if not user or not user.check_password(password):
            return {"message": "Invalid email or password"}, 401
        return {"message": "Login successful"}, 200

    @staticmethod
    def get_user_profile(user_id: int) -> dict:
        try:
            user: User = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
        except Exception as e:
            return {"message": f"Error occurred while fetching user profile: {str(e)}"}, 500

        return {"email": user.email, "name": user.name}, 200

    @staticmethod
    def hash_password(password: str) -> str:
        salt = gensalt()
        return hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed: str) -> bool:
        return checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def generate_jwt(user: User, expiration_hours: int) -> str:
        payload = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.now() + timedelta(hours=expiration_hours),
            "iat": datetime.now()
        }
        return jwt.encode(payload, app.config["JWT_SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            payload = jwt.decode(token, app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return {"message": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Invalid token"}, 401
