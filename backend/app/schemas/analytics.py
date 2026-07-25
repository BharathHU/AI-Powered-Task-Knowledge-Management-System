from app.schemas.base import ORMBaseModel


class AnalyticsResponse(ORMBaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    top_search_queries: list[dict[str, int | str]]
