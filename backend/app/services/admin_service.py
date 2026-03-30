"""
Feature F09 - Administrative time-window service.
Design intent: provide a small, explicit service for business phase control so administrators can
open and close enrollment, scheduling, and grading without editing source code.
"""
from __future__ import annotations

from datetime import datetime

from app.core.exceptions import AppError
from app.core.responses import success
from app.core.time_windows import TIME_FORMAT, TimeWindowStore


class AdminTimeService:
    def __init__(self, store: TimeWindowStore) -> None:
        self._store = store

    def update_window(self, window_name: str, start_time: str, end_time: str) -> dict:
        try:
            start_dt = datetime.strptime(start_time, TIME_FORMAT)
            end_dt = datetime.strptime(end_time, TIME_FORMAT)
            window = self._store.set(window_name, start_dt, end_dt)
        except ValueError as exc:
            raise AppError(f"时间格式错误或逻辑错误: {exc}") from exc
        return success(window.to_dict())

    def get_window(self, window_name: str) -> dict:
        window = self._store.get(window_name)
        return success(window.to_dict())
