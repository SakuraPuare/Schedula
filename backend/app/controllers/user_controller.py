from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import (
    SessionDependency,
    TokenPayloadDependency,
    require_role,
    token_service,
)
from app.api.schemas import (
    StudentProfileUpdateRequest,
    TeacherLookupQuery,
    TeacherProfileUpdateRequest,
    UserAuthRequest,
    UserFeedbackRequest,
    UserRegisterRequest,
    UserResendEmailRequest,
)
from app.core.settings import Settings
from app.repositories.user_repository import UserRepository
from app.services.mail_service import EmailVerificationService
from app.services.profile_service import ProfileService
from app.services.user_service import UserService


class UserController:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._mail_service = EmailVerificationService(settings, token_service)
        self.router = APIRouter(prefix="/user")
        self.router.add_api_route("/auth", self.auth, methods=["POST"])
        self.router.add_api_route("/register", self.register, methods=["POST"])
        self.router.add_api_route("/check", self.check, methods=["POST"])
        self.router.add_api_route("/resendEmail", self.resend_email, methods=["POST"])
        self.router.add_api_route("/verify", self.verify, methods=["GET"])
        self.router.add_api_route("/feedback", self.feedback, methods=["POST"])

    def _service(self, db: SessionDependency) -> UserService:
        return UserService(
            settings=self._settings,
            repository=UserRepository(db),
            token_service=token_service,
            mail_service=self._mail_service,
        )

    def auth(self, body: UserAuthRequest, db: SessionDependency):
        return self._service(db).authenticate(body.email, body.password, body.type)

    def register(self, body: UserRegisterRequest, db: SessionDependency):
        return self._service(db).register(body.email, body.username, body.password, body.type)

    def check(self, payload: TokenPayloadDependency, db: SessionDependency):
        return self._service(db).check_token(payload)

    def resend_email(self, body: UserResendEmailRequest, db: SessionDependency):
        return self._service(db).resend_verification_email(body.email, body.password, body.type)

    def verify(self, token: str, db: SessionDependency):
        return self._service(db).verify_email(token)

    def feedback(self, body: UserFeedbackRequest, payload: TokenPayloadDependency, db: SessionDependency):
        return self._service(db).submit_feedback(body.title, body.content)


class TeacherController:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self.router = APIRouter(prefix="/teacher")
        self.router.add_api_route("/getInfo", self.get_info, methods=["GET"])
        self.router.add_api_route("/updateInfo", self.update_info, methods=["PUT"])
        self.router.add_api_route("/listInfo", self.list_info, methods=["GET"])

    def _service(self, db: SessionDependency) -> ProfileService:
        return ProfileService(self._settings, UserRepository(db))

    def get_info(
        self,
        db: SessionDependency,
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).get_teacher_profile(payload.get("user_id"))

    def update_info(
        self,
        body: TeacherProfileUpdateRequest,
        db: SessionDependency,
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).update_teacher_profile(payload.get("user_id"), body)

    def list_info(
        self,
        db: SessionDependency,
        query: TeacherLookupQuery = Depends(),
        payload: dict = Depends(require_role("teacher")),
    ):
        return self._service(db).get_teacher_public_profile(query.id)


class StudentController:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self.router = APIRouter(prefix="/student")
        self.router.add_api_route("/getInfo", self.get_info, methods=["GET"])
        self.router.add_api_route("/updateInfo", self.update_info, methods=["PUT"])

    def _service(self, db: SessionDependency) -> ProfileService:
        return ProfileService(self._settings, UserRepository(db))

    def get_info(
        self,
        db: SessionDependency,
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).get_student_profile(payload.get("user_id"))

    def update_info(
        self,
        body: StudentProfileUpdateRequest,
        db: SessionDependency,
        payload: dict = Depends(require_role("student")),
    ):
        return self._service(db).update_student_profile(payload.get("user_id"), body)
