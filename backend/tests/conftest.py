from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.schemas.auth import TokenResponse

# We can safely use StaticPool with :memory: if we share one engine across all tests
# and just drop the tables instead of calling dispose. Actually, StaticPool in memory
# is perfect if we have one global fixture.
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=StaticPool,
)
TestingSessionLocal = async_sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(autouse=True, scope="session")
async def cleanup_engine():
    yield
    await engine_test.dispose()

@pytest_asyncio.fixture(autouse=True, loop_scope="function")
async def setup_database():
    """Create and drop tables per test."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(loop_scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture(loop_scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    # Override get_db dependency per test
    def override_get_db_safe():
        return db_session

    app.dependency_overrides[get_db] = override_get_db_safe

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(loop_scope="function")
async def auth_headers(async_client: AsyncClient) -> dict[str, str]:
    """Helper fixture to log in and return HTTP auth headers."""
    await async_client.post(
        "/api/auth/register",
        json={"name": "Global Test User", "email": "global@example.com", "password": "password123"},
    )
    response = await async_client.post(
        "/api/auth/login",
        json={"email": "global@example.com", "password": "password123"},
    )
    token_response = TokenResponse(**response.json())
    return {"Authorization": f"Bearer {token_response.access_token}"}
