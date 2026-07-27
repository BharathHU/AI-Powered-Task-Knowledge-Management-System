# File: models/document.py
# ORM model for the documents table. Represents an uploaded file
# (PDF or TXT) along with its extracted text content. One document
# has many DocumentChunk records that are indexed for semantic search.

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# Core entity for the knowledge-management feature. Each document is
# uploaded by an admin, parsed for text content, and split into chunks
# that are embedded into a FAISS vector index for semantic search.
class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)
    # Full extracted text from the uploaded file, used for chunking.
    content_text: Mapped[str] = mapped_column(Text, nullable=False)
    uploaded_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    uploaded_by_user = relationship("User", back_populates="documents")
    # Cascade delete — removing a document removes its chunks automatically.
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
