from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, require_role
from app.schemas.task import TaskCreateRequest, TaskRead, TaskStatusUpdateRequest
from app.services.task_service import create_task, list_tasks, update_task_status

router = APIRouter()


@router.get("", response_model=list[TaskRead])
def get_tasks(
    status: str | None = None,
    assigned_to: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> list[TaskRead]:
    return list_tasks(db, current_user=current_user, status=status, assigned_to=assigned_to)


@router.post("", response_model=TaskRead, dependencies=[Depends(require_role("admin"))])
def post_task(payload: TaskCreateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> TaskRead:
    return create_task(db, creator_id=current_user.id, title=payload.title, description=payload.description, assigned_to=payload.assigned_to)


@router.patch("/{task_id}/status", response_model=TaskRead)
def patch_task_status(task_id: int, payload: TaskStatusUpdateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> TaskRead:
    try:
        return update_task_status(db, current_user=current_user, task_id=task_id, status=payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from None
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from None
