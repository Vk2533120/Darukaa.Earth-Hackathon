import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MetricBase(BaseModel):
    timestamp: datetime
    metric_type: str
    value: float

class MetricCreate(MetricBase):
    pass

class MetricResponse(MetricBase):
    id: uuid.UUID
    site_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
