# File: api/routes/analytics.py
# Analytics dashboard route handler. Returns aggregated task statistics
# and the most popular search queries. Restricted to admin users only.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics_service import analytics_summary

router = APIRouter()


# GET /analytics — provides a high-level summary of task counts and
# the top 5 search queries logged via activity logs (admin only).
@router.get("", response_model=AnalyticsResponse, dependencies=[Depends(require_role("admin"))])
def get_analytics(db: Session = Depends(get_db)) -> AnalyticsResponse:
    return analytics_summary(db)
