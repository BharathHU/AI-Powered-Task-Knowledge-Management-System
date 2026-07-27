# File: models/task.py
# ORM model for the tasks table. Implements the task-management feature
# where admins can create and assign tasks, and users can update the
# status of tasks assigned to them.

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# Core entity for the task-management domain. Tasks have a lifecycle of
# "pending" → "completed". Non-admin users can only see/update tasks
# that are assigned to them (enforced at the service layer).
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="pending", nullable=False)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    assigned_to_user = relationship("User", foreign_keys=[assigned_to], back_populates="assigned_tasks")
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="created_tasks")
