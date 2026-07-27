# File: schemas/document.py
# Pydantic schemas for the document management and semantic search
# features. Covers file upload responses, search queries, and results.

from datetime import datetime

from app.schemas.base import ORMBaseModel
from app.schemas.auth import UserRead


# Response shape for document upload and listing endpoints.
class DocumentRead(ORMBaseModel):
    id: int
    title: str
    file_name: str
    file_path: str
    file_type: str
    content_text: str
    uploaded_by: int
    created_at: datetime
    uploaded_by_user: UserRead | None = None


# POST /search — request body with the query string and result limit.
class SearchRequest(ORMBaseModel):
    query: str
    top_k: int = 5


# Individual search result containing the matched chunk and similarity score.
class SearchResult(ORMBaseModel):
    document_id: int
    document_title: str
    chunk_text: str
    score: float
