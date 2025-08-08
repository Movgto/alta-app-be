from app.db import db
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Client

class Document(db.Model):
    """Document model for storing file metadata"""
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(db.ForeignKey('client.id', ondelete='CASCADE'), nullable=False)    
    # Use database-specific types for maximum size
    document_data: Mapped[bytes] = mapped_column(MEDIUMBLOB, nullable=False)  # MySQL: ~4GB
    document_filename: Mapped[str] = mapped_column(db.String(255), nullable=False)
    document_mimetype: Mapped[str] = mapped_column(db.String(100), nullable=False)
    
    # Relationship back to client (many-to-one)
    client: Mapped["Client"] = relationship("Client", back_populates="document")

    def __init__(self, document_data: bytes, document_filename: str, document_mimetype: str, client_id: int):
        self.document_data = document_data
        self.document_filename = document_filename
        self.document_mimetype = document_mimetype
        self.client_id = client_id
    
    def __repr__(self):
        return f"<Document {self.document_filename}>"