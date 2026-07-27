# File: api/routes/search.py
# Semantic search route handler. Accepts a natural-language query and
# returns the most relevant document chunks from the FAISS vector index.
# Available to all authenticated users.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.schemas.document import SearchRequest, SearchResult
from app.services.activity_service import log_activity
from app.services.search_service import semantic_search

router = APIRouter()


# POST /search — performs a semantic (vector) search across all indexed
# document chunks and logs the query for analytics tracking.
@router.post("", response_model=list[SearchResult])
def search_documents(payload: SearchRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> list[SearchResult]:
    results = semantic_search(payload.query, payload.top_k)
    log_activity(db, user_id=current_user.id, action="search", entity_type="search", details={"query": payload.query, "top_k": payload.top_k, "matches": len(results)})
    return results
