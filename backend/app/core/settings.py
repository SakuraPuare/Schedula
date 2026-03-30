from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
RUNTIME_DIR = BASE_DIR / "runtime"


class Settings(BaseSettings):
    app_name: str = "Schedula"
    debug: bool = False

    bind_host: str = "0.0.0.0"
    bind_port: int = 8000
    public_base_url: str = "http://127.0.0.1:8000"
    cors_origins_raw: str = "*"

    user_email_max: int = 30
    user_name_min: int = 4
    user_name_max: int = 20
    user_password_min: int = 6
    user_password_max: int = 20

    database_user: str = "app_user"
    database_password: str = "change_me"
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str = "database_exp"

    token_key: str = "change-me-before-production"
    token_algorithm: str = "HS256"
    token_expire_min: int = 1440

    email_smtp_server: str = ""
    email_smtp_port: int = 465
    email_smtp_user: str = ""
    email_smtp_password: str = ""

    schedule_address: str = "localhost:50051"
    schedule_conflict_threshold: float = 0.5
    time_window_store: str = str(RUNTIME_DIR / "time_windows.json")

    model_config = SettingsConfigDict(
        env_file=(str(BASE_DIR / "docker.env"), str(BASE_DIR / ".env")),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        raw = self.cors_origins_raw.strip()
        if not raw or raw == "*":
            return ["*"]
        return [item.strip() for item in raw.split(",") if item.strip()]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
