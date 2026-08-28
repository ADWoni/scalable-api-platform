from app.core.passwords import hash_password
from app.models.user import User


class UserRepository:
    """In-memory user store for the portfolio demo."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        demo = User(
            id="user_1",
            email="builder@example.com",
            full_name="Abdulrahaman Woni",
            hashed_password=hash_password("demo-password"),
            role="builder",
        )
        self._users[demo.email.lower()] = demo

    def get_by_email(self, email: str) -> User | None:
        return self._users.get(email.lower())
