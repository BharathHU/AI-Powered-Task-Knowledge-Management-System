from datetime import datetime

from app.schemas.base import ORMBaseModel
from app.schemas.auth import UserRead


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


class SearchRequest(ORMBaseModel):
    query: str
    top_k: int = 5


class SearchResult(ORMBaseModel):
    document_id: int
    document_title: str
    chunk_text: str
    score: float
