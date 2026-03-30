"""
Feature F02 - Authentication primitives.
Design intent: keep password hashing and JWT creation/verification in one module so login,
email verification, and role-based access all rely on the same cryptographic policy.
"""
from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from app.core.exceptions import UnauthorizedError
from app.core.settings import Settings


def hash_string(value: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(value.encode("utf-8"))
    return sha256.hexdigest()


class TokenService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def create_token(self, payload: dict, expire_minutes: Optional[int] = None) -> str:
        token_payload = payload.copy()
        expires_delta = timedelta(
            minutes=expire_minutes or self._settings.token_expire_min
        )
        token_payload["exp"] = datetime.now(timezone.utc) + expires_delta
        return jwt.encode(
            token_payload,
            self._settings.token_key,
            algorithm=self._settings.token_algorithm,
        )

    def decode_token(self, token: str) -> dict:
        raw_token = self._strip_bearer_prefix(token)
        try:
            return jwt.decode(
                raw_token,
                self._settings.token_key,
                algorithms=[self._settings.token_algorithm],
            )
        except (jwt.PyJWTError, AttributeError, TypeError) as exc:
            raise UnauthorizedError() from exc

    @staticmethod
    def _strip_bearer_prefix(token: str) -> str:
        return token.replace("Bearer ", "").strip()
