"""
Feature F00 - System bootstrap and runtime assembly.
Design intent: centralize service composition, exception handling, and router registration so
all business modules share one startup path and one response contract. This module is the
runtime entry for the backend architecture described in the documentation.
"""
from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.admin_controller import AdminController
from app.controllers.course_controller import CourseController
from app.controllers.user_controller import StudentController, TeacherController, UserController
from app.core.database import init_database
from app.core.exceptions import AppError
from app.core.responses import error_response, success
from app.core.settings import get_settings
from app.core.time_windows import TimeWindowStore
from app.services.admin_service import AdminTimeService


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    time_window_store = TimeWindowStore(settings.time_window_store)

    init_database()

    app = FastAPI(title=settings.app_name, debug=settings.debug)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    user_controller = UserController(settings)
    teacher_controller = TeacherController(settings)
    student_controller = StudentController(settings)
    course_controller = CourseController(settings, time_window_store)
    admin_controller = AdminController(AdminTimeService(time_window_store))

    app.include_router(user_controller.router)
    app.include_router(teacher_controller.router)
    app.include_router(student_controller.router)
    app.include_router(course_controller.router)
    app.include_router(admin_controller.router)

    @app.get("/")
    def root():
        return success(message="OK", version="v2.0.0", delay=0)

    @app.get("/openapi_v2")
    def openapi_v2():
        return app.openapi()

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return error_response(exc.message, exc.status_code)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        first_error = exc.errors()[0] if exc.errors() else {}
        message = first_error.get("msg", "请求参数无效")
        return error_response(message, 422)

    @app.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception):
        logger.exception("Unhandled backend exception", exc_info=exc)
        return error_response("服务器内部错误", 500)

    return app
