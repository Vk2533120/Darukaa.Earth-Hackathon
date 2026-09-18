import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_project_unauthenticated(async_client: AsyncClient):
    """Ensure anonymous users cannot create a project."""
    payload = {"name": "Test Project", "project_type": "carbon"}
    response = await async_client.post("/api/projects", json=payload)
    assert response.status_code == 403  # HTTPBearer missing


@pytest.mark.asyncio
async def test_create_project_success(async_client: AsyncClient, auth_headers: dict[str, str]):
    """Ensure authenticated users can create projects and the created_by logic applies."""
    payload = {"name": "Forest Project", "description": "Protecting trees", "project_type": "biodiversity"}
    response = await async_client.post("/api/projects", json=payload, headers=auth_headers)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Forest Project"
    assert data["project_type"] == "biodiversity"
    assert "id" in data
    assert "created_by" in data


@pytest.mark.asyncio
async def test_create_project_validation_error(async_client: AsyncClient, auth_headers: dict[str, str]):
    """Ensure required fields are enforced."""
    payload = {"description": "Missing name and project_type"}
    response = await async_client.post("/api/projects", json=payload, headers=auth_headers)
    assert response.status_code == 422  # Pydantic validation error


@pytest.mark.asyncio
async def test_get_projects_list(async_client: AsyncClient, auth_headers: dict[str, str]):
    """Ensure we can list user projects."""
    payload1 = {"name": "Project 1", "project_type": "carbon"}
    payload2 = {"name": "Project 2", "project_type": "biodiversity"}
    await async_client.post("/api/projects", json=payload1, headers=auth_headers)
    await async_client.post("/api/projects", json=payload2, headers=auth_headers)

    response = await async_client.get("/api/projects", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_project_detail(async_client: AsyncClient, auth_headers: dict[str, str]):
    """Ensure we can get a specific project by id."""
    payload = {"name": "Detail Project", "project_type": "carbon"}
    create_response = await async_client.post("/api/projects", json=payload, headers=auth_headers)
    project_id = create_response.json()["id"]

    response = await async_client.get(f"/api/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == project_id
    assert response.json()["name"] == "Detail Project"


@pytest.mark.asyncio
async def test_get_project_not_found(async_client: AsyncClient, auth_headers: dict[str, str]):
    """Ensure requesting a nonexistent project returns 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await async_client.get(f"/api/projects/{fake_id}", headers=auth_headers)
    assert response.status_code == 404
