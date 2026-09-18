import uuid
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.project import Project
from app.schemas.project import ProjectCreate


async def create_project(db: AsyncSession, project_in: ProjectCreate, user_id: uuid.UUID) -> Project:
    """Create a new project matching the requested schema and store in DB."""
    new_project = Project(
        name=project_in.name,
        description=project_in.description,
        project_type=project_in.project_type,
        created_by=user_id,
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


async def get_projects(db: AsyncSession, user_id: uuid.UUID) -> Sequence[Project]:
    """Retrieve all projects for a given user."""
    stmt = select(Project).where(Project.created_by == user_id).order_by(Project.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_project_by_id(db: AsyncSession, project_id: uuid.UUID, user_id: uuid.UUID) -> Project | None:
    """Retrieve a specific project by id ensuring the requested user owns it."""
    stmt = select(Project).where(Project.id == project_id, Project.created_by == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
