# File: models/user.py
# ORM model for the users table. Represents every registered user with
# authentication credentials and a foreign key to their RBAC role.
# Frequently loaded with eager relationship loading for role checks.

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# The primary identity entity. Users authenticate via email/password,
# receive a JWT containing their user ID, and are associated with tasks
# (as creator or assignee), document uploads, and activity logs.
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    # FK to roles table — determines what the user can access via RBAC.
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

    role = relationship("Role", back_populates="users")
    created_tasks = relationship("Task", back_populates="created_by_user", foreign_keys="Task.created_by")
    assigned_tasks = relationship("Task", back_populates="assigned_to_user", foreign_keys="Task.assigned_to")
    documents = relationship("Document", back_populates="uploaded_by_user")
    logs = relationship("ActivityLog", back_populates="user")
