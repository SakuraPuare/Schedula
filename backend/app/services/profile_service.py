from __future__ import annotations

from app.core.exceptions import AppError, NotFoundError
from app.core.responses import success
from app.core.security import hash_string
from app.core.settings import Settings
from app.repositories.user_repository import UserRepository


class ProfileService:
    def __init__(self, settings: Settings, repository: UserRepository) -> None:
        self._settings = settings
        self._repository = repository

    def get_student_profile(self, user_id: int) -> dict:
        user = self._repository.get_by_role_and_id("student", user_id)
        if user is None:
            raise NotFoundError("User Not Found")
        return success(
            {
                "name": user.name,
                "idcard": user.idcard,
                "sex": user.sex,
                "classer": user.classer,
                "profession": user.profession,
                "college": user.college,
                "email": user.email,
            }
        )

    def update_student_profile(self, user_id: int, payload) -> dict:
        user = self._repository.get_by_role_and_id("student", user_id)
        if user is None:
            raise NotFoundError("User Not Found")

        self._validate_common_fields(payload.username, payload.password, payload.sex, payload.idcard)

        if payload.username:
            user.name = payload.username
        if payload.password:
            user.password = hash_string(payload.password)
        if payload.sex:
            user.sex = payload.sex
        if payload.classer:
            user.classer = payload.classer
        if payload.profession:
            user.profession = payload.profession
        if payload.college:
            user.college = payload.college
        if payload.idcard:
            user.idcard = payload.idcard

        self._repository.save(user)
        return success()

    def get_teacher_profile(self, user_id: int) -> dict:
        user = self._repository.get_by_role_and_id("teacher", user_id)
        if user is None:
            raise NotFoundError("User Not Found")
        return success(
            {
                "name": user.name,
                "idcard": user.idcard,
                "sex": user.sex,
                "introduction": user.introduction,
                "profession": user.profession,
                "college": user.college,
                "email": user.email,
            }
        )

    def update_teacher_profile(self, user_id: int, payload) -> dict:
        user = self._repository.get_by_role_and_id("teacher", user_id)
        if user is None:
            raise NotFoundError("User Not Found")

        self._validate_common_fields(payload.username, payload.password, payload.sex, payload.idcard)

        if payload.username:
            user.name = payload.username
        if payload.password:
            user.password = hash_string(payload.password)
        if payload.sex:
            user.sex = payload.sex
        if payload.introduction:
            user.introduction = payload.introduction
        if payload.profession:
            user.profession = payload.profession
        if payload.college:
            user.college = payload.college
        if payload.idcard:
            user.idcard = payload.idcard

        self._repository.save(user)
        return success()

    def get_teacher_public_profile(self, teacher_id: int) -> dict:
        user = self._repository.get_by_role_and_id("teacher", teacher_id)
        if user is None:
            raise NotFoundError("User Not Found")
        return success(
            {
                "name": user.name,
                "sex": user.sex,
                "introduction": user.introduction,
                "profession": user.profession,
                "college": user.college,
                "email": user.email,
            }
        )

    def _validate_common_fields(
        self, username: str, password: str, sex: str, idcard: str
    ) -> None:
        if username and not (
            self._settings.user_name_min <= len(username) <= self._settings.user_name_max
        ):
            raise AppError("Username length invalid")
        if password and not (
            self._settings.user_password_min
            <= len(password)
            <= self._settings.user_password_max
        ):
            raise AppError("Password length invalid")
        if sex and sex not in {"M", "F", "U"}:
            raise AppError("Sex invalid")
        if idcard and len(idcard) != 18:
            raise AppError("IDcard length invalid")
