from fastapi import APIRouter

from app.core.security import CurrentUser
from app.models.user import Project, ProjectCreate, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects")
project_service = ProjectService()


@router.get("", response_model=list[Project])
def list_projects(user: CurrentUser) -> list[Project]:
    return project_service.list_projects(user)


@router.post("", response_model=Project, status_code=201)
def create_project(payload: ProjectCreate, user: CurrentUser) -> Project:
    return project_service.create_project(user, payload)


@router.patch("/{project_id}", response_model=Project)
def update_project(project_id: str, payload: ProjectUpdate, user: CurrentUser) -> Project:
    return project_service.update_project(user, project_id, payload)
