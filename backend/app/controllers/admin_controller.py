from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import require_role
from app.api.schemas import AdminTimeRequest
from app.services.admin_service import AdminTimeService


class AdminController:
    def __init__(self, service: AdminTimeService) -> None:
        self._service = service
        self.router = APIRouter(prefix="/admin/time")
        self.router.add_api_route("/select", self.put_select, methods=["PUT"])
        self.router.add_api_route("/select", self.get_select, methods=["GET"])
        self.router.add_api_route("/grade", self.put_grade, methods=["PUT"])
        self.router.add_api_route("/grade", self.get_grade, methods=["GET"])
        self.router.add_api_route("/schedule", self.put_schedule, methods=["PUT"])
        self.router.add_api_route("/schedule", self.get_schedule, methods=["GET"])

    def put_select(self, body: AdminTimeRequest, payload: dict = Depends(require_role("admin"))):
        return self._service.update_window("select", body.start_time, body.end_time)

    def get_select(self, payload: dict = Depends(require_role("admin"))):
        return self._service.get_window("select")

    def put_grade(self, body: AdminTimeRequest, payload: dict = Depends(require_role("admin"))):
        return self._service.update_window("grade", body.start_time, body.end_time)

    def get_grade(self, payload: dict = Depends(require_role("admin"))):
        return self._service.get_window("grade")

    def put_schedule(self, body: AdminTimeRequest, payload: dict = Depends(require_role("admin"))):
        return self._service.update_window("schedule", body.start_time, body.end_time)

    def get_schedule(self, payload: dict = Depends(require_role("admin"))):
        return self._service.get_window("schedule")
