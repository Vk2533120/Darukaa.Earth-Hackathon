"""
Models are specifically imported here so Alembic can discover them.
"""
from app.database import Base  # noqa
from app.models.user import User  # noqa
from app.models.project import Project  # noqa
from app.models.site import Site  # noqa
from app.models.metric import SiteMetric  # noqa
