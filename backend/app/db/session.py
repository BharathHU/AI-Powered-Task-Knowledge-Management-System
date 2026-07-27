# File: db/session.py
# Database engine and session factory initialisation. Attempts to connect
# to the configured MySQL database; if that fails it falls back to a local
# SQLite file so development can proceed without an external database server.

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import ActivityLog, Document, DocumentChunk, Role, Task, User
from app.models.base import Base


# Creates a SQLAlchemy engine with SQLite-specific settings when needed.
# SQLite requires `check_same_thread=False` for multi-tenginehreaded FastAPI usage.
def _build_engine(database_url: str):
    if database_url.startswith("sqlite"):
        return create_engine(database_url, connect_args={"check_same_thread": False})
    return create_engine(database_url, pool_pre_ping=True)


# Constructs a filesystem path for the SQLite fallback database file.
def _sqlite_fallback_url() -> str:
    fallback_path = Path("storage") / "local.db"
    fallback_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{fallback_path.resolve().as_posix()}"


# Module-level engine and session factory — referenced by api/deps.py and init_db().
engine = _build_engine(settings.database_url)
print("Database URL:", engine.url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Creates all database tables. If the primary database (MySQL) is unreachable,
# it transparently falls back to a local SQLite database for offline development.
def init_db() -> None:
    global engine, SessionLocal

    try:
        Base.metadata.create_all(bind=engine)
    except OperationalError:
        # MySQL unavailable → switch to SQLite fallback
        engine = _build_engine(_sqlite_fallback_url())
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        Base.metadata.create_all(bind=engine)
