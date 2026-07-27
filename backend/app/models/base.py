# File: models/base.py
# Declares the SQLAlchemy declarative base class that all ORM models inherit from.
# This single base ensures consistent metadata and table creation across the project.

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Shared declarative base for all application ORM models."""
    pass
