from __future__ import annotations

from typing import Annotated, Callable, Optional

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.exceptions import UnauthorizedError
from app.core.security import TokenService
from app.core.settings import get_settings


settings = get_settings()
token_service = TokenService(settings)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDependency = Annotated[Session, Depends(get_db)]


def get_token_payload(authorization: Annotated[Optional[str], Header()] = None) -> dict:
    if not authorization:
        raise UnauthorizedError()
    return token_service.decode_token(authorization)


TokenPayloadDependency = Annotated[dict, Depends(get_token_payload)]


def require_role(*roles: str) -> Callable:
    def dependency(payload: dict = Depends(get_token_payload)) -> dict:
        if payload.get("usertype") not in roles:
            raise UnauthorizedError()
        return payload

    return dependency
