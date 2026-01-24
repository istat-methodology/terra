from __future__ import annotations

import json
from typing import Any, Mapping

from flask import current_app, Response


def get_services() -> dict[str, Any]:
    """
    Shortcut to access shared services injected in app.config["SERVICES"]
    """
    return current_app.config["SERVICES"]


def json_response(payload: str | Mapping[str, Any], status: int = 200) -> Response:
    """
    Standard JSON response for all endpoints.
    - If payload is str, assume it is already JSON
    - If payload is dict-like, serialize it
    """
    if isinstance(payload, str):
        body = payload
    else:
        body = json.dumps(payload, ensure_ascii=False)

    return Response(
        response=body,
        status=status,
        mimetype="application/json",
    )


def bad_request(message: str, *, status: int = 400) -> Response:
    """
    Standard 4xx response for invalid client input
    """
    return json_response(
        {"STATUS": "00", "error": message},
        status=status,
    )
