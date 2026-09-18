import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.metric import MetricCreate, MetricResponse
from app.services.analytics_service import create_metric, get_metrics_for_site

# In a real app we'd verify the site belongs to a project the user owns,
# for hackathon simplicity we'll authenticate the user but assume site access.

router = APIRouter(prefix="/api/sites/{site_id}/analytics", tags=["Analytics"])

@router.post("", response_model=MetricResponse, status_code=status.HTTP_201_CREATED)
async def add_metric(
    site_id: uuid.UUID,
    metric_in: MetricCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a metric data point to a site."""
    return await create_metric(db, site_id, metric_in)

@router.get("", response_model=list[MetricResponse])
async def get_metrics(
    site_id: uuid.UUID,
    metric_type: str | None = Query(None, description="Filter by metric type"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve metrics for a site."""
    return await get_metrics_for_site(db, site_id, metric_type)
