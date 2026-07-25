from datetime import datetime

from pydantic import Field

from app.schemas.base import ORMBaseModel
from app.schemas.auth import UserRead


class TaskCreateRequest(ORMBaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)
    assigned_to: int | None = None


class TaskStatusUpdateRequest(ORMBaseModel):
    status: str = Field(pattern="^(pending|completed)$")


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
