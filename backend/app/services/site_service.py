import json
import uuid
from typing import Any

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.site import Site
from app.schemas.site import SiteCreate


async def create_site(db: AsyncSession, project_id: uuid.UUID, site_in: SiteCreate) -> dict[str, Any]:
    """Create a new site linked to a project."""

    geom_str = json.dumps(site_in.geometry)
    # Using ST_GeomFromGeoJSON allows direct ingestion of the GeoJSON
    geom_db = func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom_str), 4326)

    new_site = Site(
        project_id=project_id,
        name=site_in.name,
        description=site_in.description,
        geometry=geom_db
    )
    db.add(new_site)
    await db.flush() # flush to get the ID generated

    # We must retrieve it via ST_AsGeoJSON so we have it as dictionary
    stmt = select(
        Site.id,
        Site.project_id,
        Site.name,
        Site.description,
        Site.created_at,
        func.ST_AsGeoJSON(Site.geometry).label("geojson")
    ).where(Site.id == new_site.id)

    result = await db.execute(stmt)
    row = result.one()
    await db.commit()

    return {
        "id": row.id,
        "project_id": row.project_id,
        "name": row.name,
        "description": row.description,
        "created_at": row.created_at,
        "geometry": json.loads(row.geojson) if row.geojson else site_in.geometry
    }

async def get_sites_for_project(db: AsyncSession, project_id: uuid.UUID) -> list[dict[str, Any]]:
    """Retrieve all sites for a given project."""
    stmt = select(
        Site.id,
        Site.project_id,
        Site.name,
        Site.description,
        Site.created_at,
        func.ST_AsGeoJSON(Site.geometry).label("geojson")
    ).where(Site.project_id == project_id)

    result = await db.execute(stmt)
    rows = result.all()

    sites = []
    for row in rows:
        sites.append({
            "id": row.id,
            "project_id": row.project_id,
            "name": row.name,
            "description": row.description,
            "created_at": row.created_at,
            "geometry": json.loads(row.geojson) if row.geojson else {}
        })
    return sites
