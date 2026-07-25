from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import ActivityLog, Document, DocumentChunk, Role, Task, User
from app.models.base import Base

def _build_engine(database_url: str):
    if database_url.startswith("sqlite"):
        return create_engine(database_url, connect_args={"check_same_thread": False})
    return create_engine(database_url, pool_pre_ping=True)


def _sqlite_fallback_url() -> str:
    fallback_path = Path("storage") / "local.db"
    fallback_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{fallback_path.resolve().as_posix()}"


engine = _build_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    global engine, SessionLocal

    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        engine = _build_engine(_sqlite_fallback_url())
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        Base.metadata.create_all(bind=engine)
