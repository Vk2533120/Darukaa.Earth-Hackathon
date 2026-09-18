from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings
from app.database import Base, async_session_factory, engine


def test_database_configuration():
    """Verify the database infrastructure components are instantiated correctly
    without requiring an active connection to PostgreSQL.
    """
    assert isinstance(settings.DATABASE_URL, str)
    assert settings.DATABASE_URL.startswith("postgresql+asyncpg://")

    # Verify SQLAlchemy components are set up
    assert isinstance(engine, AsyncEngine)
    assert isinstance(async_session_factory, async_sessionmaker)
    assert issubclass(Base, DeclarativeBase)


def test_models_init():
    """Verify that importing app.models works and Base is available for Alembic."""
    from app.models import Base as ModelsBase

    assert ModelsBase is Base
