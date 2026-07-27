# File: services/analytics_service.py
# Provides aggregated statistics for the admin analytics dashboard.
# Computes task counts (total / completed / pending) and identifies
# the top 5 most frequent search queries from activity logs.

import json

from sqlalchemy import func, select, String
from sqlalchemy.orm import Session
from sqlalchemy import cast

from app.models.activity_log import ActivityLog
from app.models.task import Task


# Called by GET /analytics. Returns a summary dict with task statistics
# and the top search queries parsed from the activity_logs table.
def analytics_summary(db: Session) -> dict:
    # Aggregate task counts via SQL COUNT queries.
    total_tasks = db.scalar(select(func.count(Task.id))) or 0
    completed_tasks = db.scalar(select(func.count(Task.id)).where(Task.status == "completed")) or 0
    pending_tasks = db.scalar(select(func.count(Task.id)).where(Task.status == "pending")) or 0

    # Fetch all search activity logs and parse queries in Python for accurate grouping
    search_logs = db.scalars(
        select(ActivityLog)
        .where(ActivityLog.action == "search")
        .order_by(ActivityLog.created_at.desc())
    ).all()

    # In-memory aggregation of search query frequencies.
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

    # Sort descending by count and return the top 5.
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
