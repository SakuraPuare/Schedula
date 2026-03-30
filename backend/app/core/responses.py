from __future__ import annotations

from fastapi.responses import JSONResponse


def success(data=None, message: str = "OK", **extra):
    payload = {"status": 0, "message": message}
    if data is not None:
        payload["data"] = data
    payload.update(extra)
    return payload


def error_response(message: str, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"status": 1, "message": message},
    )
