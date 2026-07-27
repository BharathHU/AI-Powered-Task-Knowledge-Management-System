# File: schemas/analytics.py
# Pydantic schema for the analytics dashboard response. Provides
# aggregated task statistics and the most popular search queries.

from app.schemas.base import ORMBaseModel


# GET /analytics — admin-only endpoint that returns a summary of
# task counts and the top 5 most frequent search queries.
class AnalyticsResponse(ORMBaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    top_search_queries: list[dict[str, int | str]]
