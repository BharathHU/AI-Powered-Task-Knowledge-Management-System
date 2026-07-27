# File: schemas/task.py
# Pydantic schemas for the task-management domain. Validates inputs
# for creating and updating tasks, and defines the full response shape
# with nested user data.

from datetime import datetime

from pydantic import Field

from app.schemas.base import ORMBaseModel
from app.schemas.auth import UserRead


# POST /tasks — request body for creating a new task (admin only).
class TaskCreateRequest(ORMBaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    assigned_to: int | None = None


# PATCH /tasks/{id}/status — request body for updating task status.
class TaskStatusUpdateRequest(ORMBaseModel):
    status: str = Field(pattern="^(pending|completed)$")


# Response shape for all task endpoints, includes assigned/creator user info.
class TaskRead(ORMBaseModel):
    id: int
    title: str
    description: str
    status: str
    assigned_to: int | None
    created_by: int
    created_at: datetime
    updated_at: datetime
    assigned_to_user: UserRead | None = None
    created_by_user: UserRead | None = None
