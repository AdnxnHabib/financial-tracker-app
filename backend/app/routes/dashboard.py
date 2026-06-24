from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_dashboard_service
from app.schemas.dashboard import DashboardRead
from app.services.dashboard import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardRead)
def get_dashboard_summary(
    year: Optional[int] = Query(default=None, ge=2000, le=2100),
    month: Optional[int] = Query(default=None, ge=1, le=12),
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.get_summary(
        year=year,
        month=month,
    )
