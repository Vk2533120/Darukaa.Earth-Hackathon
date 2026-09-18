import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SiteBase(BaseModel):
    name: str
    description: str | None = None
    # We will accept standard GeoJSON Polygon format as a dictionary
    # e.g., {"type": "Polygon", "coordinates": [[[lng, lat], ...]]}
    geometry: dict[str, Any] = Field(..., description="GeoJSON Polygon representation")

class SiteCreate(SiteBase):
    pass

class SiteResponse(SiteBase):
    id: uuid.UUID
    project_id: uuid.UUID
    created_at: datetime

    # We may return geometry as WKT or GeoJSON dict depending on how
    # we unmarshal from DB. Let's ensure from_attributes covers it.
    model_config = ConfigDict(from_attributes=True)
