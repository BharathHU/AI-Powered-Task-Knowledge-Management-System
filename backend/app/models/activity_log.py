# File: models/activity_log.py
# ORM model for the activity_logs table. Records user actions
# (login, register, search, upload, task operations) for audit trails
# and the analytics dashboard's "top search queries" feature.

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# Tracks every significant user action for auditing, analytics and debugging.
# The analytics_service reads from this table to compute top search queries.
class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Nullable to allow system-generated events that aren't tied to a user.
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
    # JSON string storing action-specific metadata (e.g. search query text).
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="logs")
