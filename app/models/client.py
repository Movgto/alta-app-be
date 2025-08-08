from app.db import db
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Document

class Client(db.Model):
    """Client model"""

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    representative_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    rfc: Mapped[str] = mapped_column(db.String(13), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(db.String(15), nullable=False)
    # Remove document_id to avoid circular foreign keys
    # Use relationship instead for accessing documents
    
    # Relationship to documents (one-to-one)
    document: Mapped["Document"] = relationship(
        "Document", 
        back_populates="client",
        cascade="all, delete-orphan"  # This ensures documents are deleted when client is deleted
    )

    def __init__(self, company_name: str, representative_name: str, rfc: str, email: str, phone_number: str):
        self.company_name = company_name
        self.representative_name = representative_name
        self.rfc = rfc
        self.email = email
        self.phone_number = phone_number

    def __repr__(self):
        return f"<Client {self.representative_name}>"
