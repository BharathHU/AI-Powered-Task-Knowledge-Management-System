from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_role
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics_service import analytics_summary

router = APIRouter()


@router.get("", response_model=AnalyticsResponse, dependencies=[Depends(require_role("admin"))])
def get_analytics(db: Session = Depends(get_db)) -> AnalyticsResponse:
    return analytics_summary(db)
