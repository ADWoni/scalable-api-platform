from uuid import uuid4

from app.core.errors import ForbiddenError, NotFoundError
from app.models.user import Project, ProjectCreate, ProjectUpdate


class ProjectRepository:
    """In-memory project store kept intentionally simple for walkthrough clarity."""

    def __init__(self) -> None:
        self._projects: dict[str, Project] = {}

    def create(self, owner_id: str, payload: ProjectCreate) -> Project:
        project = Project(
            id=f"prj_{uuid4().hex[:8]}",
            owner_id=owner_id,
            name=payload.name.strip(),
            description=payload.description.strip(),
            status="active",
        )
        self._projects[project.id] = project
        return project

    def list_for_owner(self, owner_id: str) -> list[Project]:
        return [p for p in self._projects.values() if p.owner_id == owner_id]

    def get(self, project_id: str) -> Project:
        project = self._projects.get(project_id)
        if not project:
            raise NotFoundError("Project not found")
        return project

    def update(self, project_id: str, owner_id: str, payload: ProjectUpdate) -> Project:
        project = self.get(project_id)
        if project.owner_id != owner_id:
            raise ForbiddenError("You can only update your own projects")

        data = project.model_dump()
        updates = payload.model_dump(exclude_unset=True)
        data.update(updates)
        updated = Project(**data)
        self._projects[project_id] = updated
        return updated
