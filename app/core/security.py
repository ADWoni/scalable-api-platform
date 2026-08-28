from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, Header
from jose import JWTError, jwt

from app.core.config import settings
from app.core.errors import UnauthorizedError
from app.core.passwords import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository

user_repo = UserRepository()


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(authorization: Annotated[str | None, Header()] = None) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise UnauthorizedError("Missing bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email = payload.get("sub")
        if not email:
            raise UnauthorizedError("Invalid token subject")
    except JWTError as exc:
        raise UnauthorizedError("Invalid or expired token") from exc

    user = user_repo.get_by_email(email)
    if not user:
        raise UnauthorizedError("User not found")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

__all__ = [
    "CurrentUser",
    "create_access_token",
    "get_current_user",
    "hash_password",
    "verify_password",
    "user_repo",
]
