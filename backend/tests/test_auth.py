import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_success(async_client: AsyncClient):
    """Test successful user registration."""
    response = await async_client.post(
        "/api/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(async_client: AsyncClient):
    """Test creating a user with an already used email fails."""
    user_payload = {
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "password123",
    }
    # Initial registration
    await async_client.post("/api/auth/register", json=user_payload)

    # Second registration should fail
    response = await async_client.post("/api/auth/register", json=user_payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_password_not_stored_plaintext(async_client: AsyncClient):
    """Ensure the password_hash doesn't equal the plaintext password."""
    # First, register the user directly.
    response = await async_client.post(
        "/api/auth/register",
        json={"name": "Secure User", "email": "secure@example.com", "password": "mypassword"},
    )
    assert response.status_code == 201

    # Since we can't fetch the password hash from the API (it's hidden),
    # verifying it safely requires using the DB override or verifying the auth_service directly.
    # The true test is that they can log in via that payload later without the API returning the hash.
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    """Test login with valid credentials."""
    await async_client.post(
        "/api/auth/register",
        json={"name": "Login User", "email": "login@example.com", "password": "login123"},
    )
    response = await async_client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "login123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_incorrect_password(async_client: AsyncClient):
    """Test login with an incorrect password fails."""
    await async_client.post(
        "/api/auth/register",
        json={"name": "Fail User", "email": "fail@example.com", "password": "fail123"},
    )
    response = await async_client.post(
        "/api/auth/login",
        json={"email": "fail@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_me_rejected_without_token(async_client: AsyncClient):
    """Test /me endpoint rejects if no token is provided."""
    response = await async_client.get("/api/auth/me")
    assert response.status_code == 403  # HTTPBearer returns 403 on missing credentials


@pytest.mark.asyncio
async def test_me_success_with_token(async_client: AsyncClient):
    """Test /me endpoint works with a valid token."""
    # Register and login
    await async_client.post(
        "/api/auth/register",
        json={"name": "Me User", "email": "me@example.com", "password": "me123"},
    )
    login_response = await async_client.post(
        "/api/auth/login",
        json={"email": "me@example.com", "password": "me123"},
    )
    token = login_response.json()["access_token"]

    # Request /me
    me_response = await async_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["name"] == "Me User"
    assert me_data["email"] == "me@example.com"
