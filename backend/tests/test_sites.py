from unittest.mock import patch

import pytest
from httpx import AsyncClient


@pytest.fixture
def mock_site_service():
    with patch("app.routers.sites.create_site") as mock_create, \
         patch("app.routers.sites.get_sites_for_project") as mock_get:

        mock_create.return_value = {
            "id": "11111111-1111-1111-1111-111111111111",
            "project_id": "00000000-0000-0000-0000-000000000000",
            "name": "Mock Site",
            "description": "Mocked for sqlite",
            "created_at": "2026-09-18T10:00:00Z",
            "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}
        }

        mock_get.return_value = [{
            "id": "11111111-1111-1111-1111-111111111111",
            "project_id": "00000000-0000-0000-0000-000000000000",
            "name": "Mock Site",
            "description": "Mocked for sqlite",
            "created_at": "2026-09-18T10:00:00Z",
            "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}
        }]
        yield mock_create, mock_get

@pytest.mark.asyncio
async def test_add_site_to_project(async_client: AsyncClient, auth_headers: dict[str, str], mock_site_service):
    # First create a project to link against
    payload = {"name": "Test Project for Sites", "project_type": "carbon"}
    proj_response = await async_client.post("/api/projects", json=payload, headers=auth_headers)
    project_id = proj_response.json()["id"]

    site_payload = {
        "name": "My Site",
        "description": "A polygon site",
        "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]}
    }

    response = await async_client.post(f"/api/projects/{project_id}/sites", json=site_payload, headers=auth_headers)
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_sites_for_project(async_client: AsyncClient, auth_headers: dict[str, str], mock_site_service):
    payload = {"name": "Test Project for Sites GET", "project_type": "carbon"}
    proj_response = await async_client.post("/api/projects", json=payload, headers=auth_headers)
    project_id = proj_response.json()["id"]

    response = await async_client.get(f"/api/projects/{project_id}/sites", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
