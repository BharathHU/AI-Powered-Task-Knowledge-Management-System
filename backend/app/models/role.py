# File: models/role.py
# ORM model for the roles table. Implements a simple Role-Based Access
# Control (RBAC) system with two roles: "admin" and "user".
# Referenced by the require_role() dependency in api/deps.py.

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# Defines access tiers for the application. The "admin" role can upload
# documents, create tasks, and view analytics; "user" role is limited
# to viewing/updating their own tasks and performing searches.
class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    users = relationship("User", back_populates="role")
