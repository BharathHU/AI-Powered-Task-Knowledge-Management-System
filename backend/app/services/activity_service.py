# File: services/activity_service.py
# Audit-logging service that records user actions to the activity_logs
# table. Called by auth, document, task, and search services to create
# an immutable audit trail consumed by the analytics dashboard.

import json

from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog


# Persists a structured activity record. Accepts an optional dict for
# details (auto-serialised to JSON). Called after every significant
# user-facing operation: login, register, upload, search, task CRUD.
def log_activity(
    db: Session,
    *,
    user_id: int | None,
    action: str,
    entity_type: str | None = None,
    entity_id: str | None = None,
    details: dict | str | None = None,
) -> ActivityLog:
    log = ActivityLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=json.dumps(details) if isinstance(details, dict) else details,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
