from __future__ import annotations

from urllib.parse import urlsplit

from app.core.settings import Settings, get_settings
from app.core.time_windows import TimeWindowStore


class LegacyConfig:
    WINDOW_FIELD_MAP = {
        "select_start_time": ("select", "start_time"),
        "select_end_time": ("select", "end_time"),
        "grade_start_time": ("grade", "start_time"),
        "grade_end_time": ("grade", "end_time"),
        "schedule_start_time": ("schedule", "start_time"),
        "schedule_end_time": ("schedule", "end_time"),
    }

    def __init__(self, settings: Settings) -> None:
        object.__setattr__(self, "_settings", settings)
        object.__setattr__(self, "_time_window_store", TimeWindowStore(settings.time_window_store))

    def __getattr__(self, name: str):
        if name == "backend_host":
            parsed = urlsplit(self._settings.public_base_url)
            return f"{parsed.scheme}://{parsed.netloc}".rstrip(":")

        if name in self.WINDOW_FIELD_MAP:
            window_name, attr_name = self.WINDOW_FIELD_MAP[name]
            return getattr(self._time_window_store.get(window_name), attr_name)

        return getattr(self._settings, name)

    def __setattr__(self, name: str, value):
        if name in {"_settings", "_time_window_store"}:
            object.__setattr__(self, name, value)
            return

        if name in self.WINDOW_FIELD_MAP:
            window_name, attr_name = self.WINDOW_FIELD_MAP[name]
            current_window = self._time_window_store.get(window_name)
            start_time = current_window.start_time
            end_time = current_window.end_time
            if attr_name == "start_time":
                start_time = value
            else:
                end_time = value
            self._time_window_store.set(window_name, start_time, end_time)
            return

        setattr(self._settings, name, value)


config = LegacyConfig(get_settings())
