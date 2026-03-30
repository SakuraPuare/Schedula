from fastapi import Header, HTTPException

from app.api.dependencies import token_service
from app.core.exceptions import UnauthorizedError


def create_token(payload: dict) -> str:
    return token_service.create_token(payload)


def extract_payload(token: str) -> dict:
    return token_service.decode_token(token)


def _validate_role(token: str, role: str | None = None) -> dict:
    try:
        payload = extract_payload(token)
    except UnauthorizedError as exc:
        raise HTTPException(status_code=401, detail="token无效, 请重新验证") from exc

    if role and payload.get("usertype") != role:
        raise HTTPException(status_code=401, detail="token无效, 请重新验证")
    return payload


def validate_token(authorization=Header(None)) -> dict:
    return _validate_role(authorization)


def validate_student_token(authorization=Header(None)) -> dict:
    return _validate_role(authorization, "student")


def validate_teacher_token(authorization=Header(None)) -> dict:
    return _validate_role(authorization, "teacher")


def validate_admin_token(authorization=Header(None)) -> dict:
    return _validate_role(authorization, "admin")
