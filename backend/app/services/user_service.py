from __future__ import annotations

from app.core.exceptions import AppError, NotFoundError, UnauthorizedError
from app.core.responses import success
from app.core.security import TokenService, hash_string
from app.core.settings import Settings
from app.repositories.user_repository import UserRepository
from app.services.mail_service import EmailVerificationService


class UserService:
    def __init__(
        self,
        settings: Settings,
        repository: UserRepository,
        token_service: TokenService,
        mail_service: EmailVerificationService,
    ) -> None:
        self._settings = settings
        self._repository = repository
        self._token_service = token_service
        self._mail_service = mail_service

    def authenticate(self, email: str, password: str, user_type: str) -> dict:
        user = self._repository.find_by_role_and_email(user_type, email)
        password_hash = hash_string(password)
        if user is None or user.password != password_hash:
            raise UnauthorizedError("Wrong email or password")

        token = None
        if user_type in {"student", "teacher"}:
            if getattr(user, "verify", False):
                token = self._token_service.create_token(
                    {
                        "user_id": user.id,
                        "usertype": user_type,
                        "username": user.name,
                        "email": user.email,
                    }
                )
        else:
            token = self._token_service.create_token(
                {
                    "user_id": user.id,
                    "usertype": user_type,
                    "username": user.name,
                }
            )

        return success(
            token=token,
            userID=user.id,
            usertype=user_type,
            username=user.name,
            email=getattr(user, "email", None),
        )

    def register(self, email: str, username: str, password: str, user_type: str) -> dict:
        if len(email) > self._settings.user_email_max:
            raise AppError("Email too long")
        if not (self._settings.user_name_min <= len(username) <= self._settings.user_name_max):
            raise AppError("Username length invalid")
        if not (
            self._settings.user_password_min
            <= len(password)
            <= self._settings.user_password_max
        ):
            raise AppError("Password length invalid")

        exists = self._repository.find_by_role_and_email(user_type, email)
        if exists is not None:
            raise AppError("Email already exists")

        user = self._repository.create_account(
            role=user_type,
            username=username,
            password_hash=hash_string(password),
            email=email,
        )
        return success(
            email=user.email,
            userID=user.id,
            username=user.name,
        )

    def resend_verification_email(self, email: str, password: str, user_type: str) -> dict:
        user = self._repository.find_by_role_and_email(user_type, email)
        if user is None or user.password != hash_string(password):
            raise UnauthorizedError("Wrong email or password")
        if getattr(user, "verify", False):
            raise AppError("Email already verified")

        self._mail_service.send_verification_email(email, user_type)
        return success()

    def verify_email(self, token: str) -> str:
        payload = self._token_service.decode_token(token)
        email = payload.get("email")
        user_type = payload.get("usertype")
        user = self._repository.find_by_role_and_email(user_type, email)
        if user is None:
            raise NotFoundError("No such user")
        if getattr(user, "verify", False):
            raise AppError("Email already verified")

        user.verify = True
        self._repository.save(user)
        return "账号已激活"

    def check_token(self, payload: dict) -> dict:
        return success(
            userID=payload.get("user_id"),
            username=payload.get("username"),
            usertype=payload.get("usertype"),
        )

    def submit_feedback(self, title: str, content: str) -> dict:
        if not 0 < len(title) <= 255 or not 0 < len(content) <= 2048:
            raise AppError("Title or content too long")
        self._repository.create_feedback(title=title, content=content)
        return success()
