from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.models.task import Task
from app.models.user import User
from app.services.activity_service import log_activity


def list_tasks(db: Session, *, current_user: User, status: str | None = None, assigned_to: int | None = None) -> list[Task]:
    stmt = (
        select(Task)
        .options(
            selectinload(Task.assigned_to_user).selectinload(User.role),
            selectinload(Task.created_by_user).selectinload(User.role),
        )
    )
    if current_user.role.name != "admin":
        stmt = stmt.where(Task.assigned_to == current_user.id)
    if status:
        stmt = stmt.where(Task.status == status)
    if assigned_to is not None:
        stmt = stmt.where(Task.assigned_to == assigned_to)
    return list(db.scalars(stmt.order_by(Task.created_at.desc())).all())


def _reload_task(db: Session, task: Task) -> Task:
    """Reload a task with all relationships eagerly loaded for serialization."""
    db.refresh(task)
    return db.scalar(
        select(Task)
        .options(
            selectinload(Task.assigned_to_user).selectinload(User.role),
            selectinload(Task.created_by_user).selectinload(User.role),
        )
        .where(Task.id == task.id)
    )


def create_task(db: Session, *, creator_id: int, title: str, description: str, assigned_to: int | None) -> Task:
    task = Task(title=title, description=description, assigned_to=assigned_to, created_by=creator_id, status="pending")
    db.add(task)
    db.commit()
    task = _reload_task(db, task)
    log_activity(db, user_id=creator_id, action="task_create", entity_type="task", entity_id=str(task.id), details={"assigned_to": assigned_to})
    return task


def update_task_status(db: Session, *, current_user: User, task_id: int, status: str) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise ValueError("Task not found")
    if current_user.role.name != "admin" and task.assigned_to != current_user.id:
        raise PermissionError("Not allowed to update this task")
    task.status = status
    db.commit()
    task = _reload_task(db, task)
    log_activity(db, user_id=current_user.id, action="task_update", entity_type="task", entity_id=str(task.id), details={"status": status})
    return task
