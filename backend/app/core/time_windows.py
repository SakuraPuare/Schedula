"""
Feature F03 - Time-window governance.
Design intent: persist the business opening windows for enrollment, scheduling, and grading
outside transient process memory, so administrative controls remain effective after restart.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from threading import Lock


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


@dataclass
class TimeWindow:
    start_time: datetime
    end_time: datetime

    def contains(self, current_time: datetime) -> bool:
        return self.start_time <= current_time <= self.end_time

    def to_dict(self) -> dict[str, str]:
        return {
            "start_time": self.start_time.strftime(TIME_FORMAT),
            "end_time": self.end_time.strftime(TIME_FORMAT),
        }


class TimeWindowStore:
    DEFAULT_STATE = {
        "select": {
            "start_time": "1970-01-01 00:00:00",
            "end_time": "2099-12-31 23:59:59",
        },
        "grade": {
            "start_time": "1970-01-01 00:00:00",
            "end_time": "2099-12-31 23:59:59",
        },
        "schedule": {
            "start_time": "1970-01-01 00:00:00",
            "end_time": "2099-12-31 23:59:59",
        },
    }

    def __init__(self, file_path: str) -> None:
        self._file_path = Path(file_path)
        self._lock = Lock()
        self._ensure_store()

    def get(self, window_name: str) -> TimeWindow:
        state = self._read_state()
        window = state[window_name]
        return TimeWindow(
            start_time=datetime.strptime(window["start_time"], TIME_FORMAT),
            end_time=datetime.strptime(window["end_time"], TIME_FORMAT),
        )

    def set(self, window_name: str, start_time: datetime, end_time: datetime) -> TimeWindow:
        if start_time >= end_time:
            raise ValueError("开始时间必须早于结束时间")

        with self._lock:
            state = self._read_state()
            state[window_name] = {
                "start_time": start_time.strftime(TIME_FORMAT),
                "end_time": end_time.strftime(TIME_FORMAT),
            }
            self._file_path.write_text(
                json.dumps(state, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        return TimeWindow(start_time=start_time, end_time=end_time)

    def _ensure_store(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._file_path.exists():
            self._file_path.write_text(
                json.dumps(self.DEFAULT_STATE, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def _read_state(self) -> dict:
        return json.loads(self._file_path.read_text(encoding="utf-8"))
