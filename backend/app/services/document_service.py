# File: services/document_service.py
# Document processing pipeline: validates file type, saves to disk,
# extracts text (PDF via pdfplumber / TXT via read_text), splits into
# chunks, persists chunks in the database, and indexes them into FAISS.
# Called by the POST /documents endpoint.

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import pdfplumber
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.user import User
from app.services.activity_service import log_activity
from app.services.search_service import index_chunks

# Only PDF and plain-text files are accepted for knowledge-base ingestion.
ALLOWED_FILE_TYPES = {"txt", "pdf"}


# Ensures the configured upload directory exists on disk.
def ensure_upload_dir() -> Path:
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


# Splits a large text into overlapping chunks for granular vector indexing.
# The overlap prevents context loss at chunk boundaries during retrieval.
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    normalized = " ".join(text.split())
    if not normalized:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        chunks.append(normalized[start:end])
        if end >= len(normalized):
            break
        start = max(0, end - overlap)
    return chunks


# Extracts plain text from a file based on its type.
# TXT: direct read; PDF: page-by-page extraction via pdfplumber.
def extract_text(file_path: Path, file_type: str) -> str:
    if file_type == "txt":
        return file_path.read_text(encoding="utf-8", errors="ignore")
    if file_type == "pdf":
        text_parts: list[str] = []
        with pdfplumber.open(str(file_path)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text() or ""
                text_parts.append(extracted)
        return "\n".join(text_parts)
    raise ValueError("Unsupported file type")


# Persists the uploaded file to the local storage directory.
def save_upload(file: UploadFile) -> Path:
    upload_dir = ensure_upload_dir()
    destination = upload_dir / file.filename
    destination.write_bytes(file.file.read())
    file.file.seek(0)
    return destination


# Full document-creation pipeline: validate, save, extract, chunk,
# persist chunks, build FAISS index, and log the activity.
# Called by POST /documents (admin only).
def create_document(db: Session, *, uploader_id: int, title: str, file: UploadFile) -> Document:
    # File-type validation — reject unsupported formats early.
    file_type = (Path(file.filename).suffix or "").lstrip(".").lower()
    if file_type not in ALLOWED_FILE_TYPES:
        raise ValueError("Only .txt and .pdf files are supported")

    saved_path = save_upload(file)
    content = extract_text(saved_path, file_type)

    # Create the Document record in the database.
    document = Document(
        title=title,
        file_name=file.filename,
        file_path=str(saved_path),
        file_type=file_type,
        content_text=content,
        uploaded_by=uploader_id,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    # Split the extracted text into chunks and persist each chunk.
    chunks = chunk_text(content)
    for index, chunk_text_value in enumerate(chunks):
        db.add(DocumentChunk(document_id=document.id, chunk_index=index, chunk_text=chunk_text_value, faiss_index_id=index))
    db.commit()

    # Reload document with eager-loaded relationships for serialization
    document = db.scalar(
        select(Document)
        .options(selectinload(Document.uploaded_by_user).selectinload(User.role))
        .where(Document.id == document.id)
    )
    # Embed chunks into the FAISS vector index for semantic search.
    index_chunks(db, document)
    log_activity(db, user_id=uploader_id, action="document_upload", entity_type="document", entity_id=str(document.id), details={"title": title})
    return document

