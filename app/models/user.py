from app.db import db
from sqlalchemy.orm import mapped_column, Mapped

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(128), nullable=False)

    def __init__(self, email: str, password: str, name: str):
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return f'<User {self.email}>'

    # TODO: Later we could compare a hash password with the plain password
    def check_password(self, password: str) -> bool:
        return self.password == password
