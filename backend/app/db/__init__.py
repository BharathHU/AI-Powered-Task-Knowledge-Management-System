# Package: app.db
# Database layer that bootstraps the SQLAlchemy engine, session factory,
# and provides fallback logic from MySQL to SQLite.
# Also re-exports all ORM models so Alembic / metadata.create_all can
# discover them without importing each model individually.

