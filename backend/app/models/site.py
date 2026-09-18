import uuid
from datetime import datetime

# --- SQLite Testing Fallbacks for PostGIS ---
# Replace Geometry with Text during SQLite testing
import sqlalchemy
from geoalchemy2 import Geometry
from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import CreateColumn
from sqlalchemy.sql import func

from app.database import Base


@compiles(CreateColumn, 'sqlite')
def use_string_for_geometry_sqlite(element, compiler, **kw):
    if isinstance(element.element.type, Geometry):
        element.element.type = sqlalchemy.String()
    return compiler.visit_create_column(element, **kw)


class Site(Base):
    """The Site model representing a geographical area bound to a project."""

    __tablename__ = "sites"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Store Polygon data with SRID 4326 (WGS 84 - Lat/Lng)
    geometry = mapped_column(Geometry("POLYGON", srid=4326), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    project: Mapped["Project"] = relationship("Project", back_populates="sites")
    metrics: Mapped[list["SiteMetric"]] = relationship("SiteMetric", back_populates="site", cascade="all, delete-orphan")
