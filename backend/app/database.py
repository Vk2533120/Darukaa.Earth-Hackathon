from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

# ---------------------------------------------------------------------------
# Engine — the core connection to PostgreSQL via asyncpg.
# echo=True prints SQL statements to the console during development.
# ---------------------------------------------------------------------------
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.APP_ENV == "development"),
    future=True,
)

# ---------------------------------------------------------------------------
# Session factory — creates new database sessions for each request.
# expire_on_commit=False keeps loaded data available after a commit so that
# FastAPI can return it in a response without triggering a lazy‑load error.
# ---------------------------------------------------------------------------
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ---------------------------------------------------------------------------
# Base — every future ORM model (User, Project, Site, SiteAnalytics) will
# inherit from this class.  Alembic also reads it to auto‑detect tables.
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    pass
