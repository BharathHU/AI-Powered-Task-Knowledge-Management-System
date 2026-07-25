from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import Document
from app.models.document_chunk import DocumentChunk

_model: Any | None = None
_model_loaded = False
_fallback_dimension = 384


def get_model() -> Any | None:
    global _model, _model_loaded
    if _model_loaded:
        return _model
    _model_loaded = True
    try:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(settings.embedding_model)
    except Exception:
        _model = None
    return _model


def ensure_index_dir() -> Path:
    index_dir = Path(settings.index_dir)
    index_dir.mkdir(parents=True, exist_ok=True)
    return index_dir


def index_path() -> Path:
    return ensure_index_dir() / "documents.faiss"


def meta_path() -> Path:
    return ensure_index_dir() / "documents_meta.json"


def load_index() -> tuple[faiss.Index, list[dict[str, Any]]]:
    model = get_model()
    dimension = model.get_sentence_embedding_dimension() if model is not None else _fallback_dimension
    if index_path().exists() and meta_path().exists():
        index = faiss.read_index(str(index_path()))
        metadata = json.loads(meta_path().read_text(encoding="utf-8"))
        return index, metadata
    return faiss.IndexFlatIP(dimension), []


def save_index(index: faiss.Index, metadata: list[dict[str, Any]]) -> None:
    ensure_index_dir()
    faiss.write_index(index, str(index_path()))
    meta_path().write_text(json.dumps(metadata, ensure_ascii=True), encoding="utf-8")


def embed_texts(texts: list[str]) -> np.ndarray:
    model = get_model()
    if model is not None:
        vectors = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return np.asarray(vectors, dtype=np.float32)

    vectors = []
    for text in texts:
        vector = np.zeros(_fallback_dimension, dtype=np.float32)
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            position = int.from_bytes(digest[:4], "little") % _fallback_dimension
            vector[position] += 1.0
        norm = np.linalg.norm(vector)
        if norm:
            vector /= norm
        vectors.append(vector)
    return np.asarray(vectors, dtype=np.float32)


def rebuild_index_from_documents(db: Session) -> None:
    documents = db.scalars(select(Document)).all()
    index, metadata = load_index()
    if metadata:
        index = faiss.IndexFlatIP(index.d)
        metadata = []
    for document in documents:
        for chunk in document.chunks:
            vector = embed_texts([chunk.chunk_text])
            index.add(vector)
            metadata.append(
                {
                    "document_id": document.id,
                    "document_title": document.title,
                    "chunk_id": chunk.id,
                    "chunk_text": chunk.chunk_text,
                }
            )
    save_index(index, metadata)


def index_chunks(db: Session, document: Document) -> None:
    index, metadata = load_index()
    chunk_texts = [chunk.chunk_text for chunk in document.chunks]
    if not chunk_texts:
        return
    vectors = embed_texts(chunk_texts)
    index.add(vectors)
    for chunk in document.chunks:
        metadata.append(
            {
                "document_id": document.id,
                "document_title": document.title,
                "chunk_id": chunk.id,
                "chunk_text": chunk.chunk_text,
            }
        )
    save_index(index, metadata)


def semantic_search(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    if not index_path().exists() or not meta_path().exists():
        return []

    index, metadata = load_index()
    if index.ntotal == 0:
        return []

    query_vector = embed_texts([query])
    scores, ids = index.search(query_vector, min(top_k, index.ntotal))
    results: list[dict[str, Any]] = []
    for score, idx in zip(scores[0], ids[0]):
        if idx < 0 or idx >= len(metadata):
            continue
        item = metadata[idx]
        results.append(
            {
                "document_id": item["document_id"],
                "document_title": item["document_title"],
                "chunk_text": item["chunk_text"],
                "score": float(score),
            }
        )
    return results
