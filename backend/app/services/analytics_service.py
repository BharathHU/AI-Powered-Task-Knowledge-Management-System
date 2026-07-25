import json

from sqlalchemy import func, select, String
from sqlalchemy.orm import Session
from sqlalchemy import cast

from app.models.activity_log import ActivityLog
from app.models.task import Task


def analytics_summary(db: Session) -> dict:
    total_tasks = db.scalar(select(func.count(Task.id))) or 0
    completed_tasks = db.scalar(select(func.count(Task.id)).where(Task.status == "completed")) or 0
    pending_tasks = db.scalar(select(func.count(Task.id)).where(Task.status == "pending")) or 0

    # Fetch all search activity logs and parse queries in Python for accurate grouping
    search_logs = db.scalars(
        select(ActivityLog)
        .where(ActivityLog.action == "search")
        .order_by(ActivityLog.created_at.desc())
    ).all()

    query_counts: dict[str, int] = {}
    for log in search_logs:
        query_text = ""
        if log.details:
            try:
                parsed = json.loads(log.details)
                query_text = parsed.get("query", "") or ""
            except (json.JSONDecodeError, TypeError):
                query_text = str(log.details)
        if query_text:
            query_counts[query_text] = query_counts.get(query_text, 0) + 1

    top_search_queries = [
        {"query": query, "count": count}
        for query, count in sorted(query_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    ]

    return {
        "total_tasks": int(total_tasks),
        "completed_tasks": int(completed_tasks),
        "pending_tasks": int(pending_tasks),
        "top_search_queries": top_search_queries,
    }
