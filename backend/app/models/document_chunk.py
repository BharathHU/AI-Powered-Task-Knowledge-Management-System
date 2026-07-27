# File: models/document_chunk.py
# ORM model for the document_chunks table. Stores individual text segments
# extracted from uploaded documents. Each chunk is embedded into a FAISS
# vector index to enable semantic search across knowledge-base content.

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# Represents one piece of a document after text-splitting. The faiss_index_id
# maps this chunk to its vector inside the FAISS index file for retrieval.
class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    # Position of this chunk's embedding in the FAISS index array.
    faiss_index_id: Mapped[int] = mapped_column(Integer, nullable=False)

    document = relationship("Document", back_populates="chunks")
