import uuid
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.metric import SiteMetric
from app.schemas.metric import MetricCreate


async def create_metric(db: AsyncSession, site_id: uuid.UUID, metric_in: MetricCreate) -> SiteMetric:
    """Create a new metric data point for a site."""
    new_metric = SiteMetric(
        site_id=site_id,
        timestamp=metric_in.timestamp,
        metric_type=metric_in.metric_type,
        value=metric_in.value
    )
    db.add(new_metric)
    await db.commit()
    await db.refresh(new_metric)
    return new_metric

async def get_metrics_for_site(db: AsyncSession, site_id: uuid.UUID, metric_type: str | None = None) -> Sequence[SiteMetric]:
    """Retrieve time-series metrics for a site."""
    stmt = select(SiteMetric).where(SiteMetric.site_id == site_id)
    if metric_type:
        stmt = stmt.where(SiteMetric.metric_type == metric_type)

    # Sort chronologically for charting
    stmt = stmt.order_by(SiteMetric.timestamp.asc())

    result = await db.execute(stmt)
    return result.scalars().all()
