from app.core.errors import UnauthorizedError
from app.core.passwords import verify_password
from app.core.security import create_access_token, user_repo
from app.models.user import LoginRequest, Project, ProjectCreate, ProjectUpdate, TokenResponse, User
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, users: UserRepository | None = None) -> None:
        # Prefer shared repo so tokens resolve against the same users as login.
        self.users = users or user_repo

    def login(self, payload: LoginRequest) -> TokenResponse:
        user = self.users.get_by_email(payload.email.lower())
        if not user or not verify_password(payload.password, user.hashed_password):
            # Fail closed: do not reveal whether email exists.
            raise UnauthorizedError("Invalid email or password")
        token = create_access_token(user.email)
        return TokenResponse(access_token=token)


class ProjectService:
    def __init__(self, projects: ProjectRepository | None = None) -> None:
        self.projects = projects or ProjectRepository()

    def create_project(self, user: User, payload: ProjectCreate) -> Project:
        return self.projects.create(owner_id=user.id, payload=payload)

    def list_projects(self, user: User) -> list[Project]:
        return self.projects.list_for_owner(user.id)

    def update_project(self, user: User, project_id: str, payload: ProjectUpdate) -> Project:
        return self.projects.update(project_id=project_id, owner_id=user.id, payload=payload)
