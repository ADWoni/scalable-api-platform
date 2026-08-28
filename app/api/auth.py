from fastapi import APIRouter

from app.models.user import LoginRequest, TokenResponse
from app.services.project_service import AuthService

router = APIRouter(prefix="/auth")
auth_service = AuthService()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    return auth_service.login(payload)
