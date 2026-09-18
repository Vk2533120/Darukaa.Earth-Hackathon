import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.site import SiteCreate, SiteResponse
from app.services.project_service import get_project_by_id
from app.services.site_service import create_site, get_sites_for_project

router = APIRouter(prefix="/api/projects/{project_id}/sites", tags=["Sites"])

@router.post("", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
async def add_site_to_project(
    project_id: uuid.UUID,
    site_in: SiteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a new geospatial site to a project."""
    project = await get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    return await create_site(db, project_id, site_in)

@router.get("", response_model=list[SiteResponse])
async def list_project_sites(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all sites for a project."""
    project = await get_project_by_id(db, project_id, current_user.id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or access denied")

    return await get_sites_for_project(db, project_id)
