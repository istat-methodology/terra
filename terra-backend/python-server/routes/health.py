from __future__ import annotations

import os
from flask import Blueprint

from routes._utils import get_services, json_response

bp = Blueprint("health", __name__)


@bp.route("/health", methods=["GET"])
def health():
    services = get_services()
    logger = services["logger"]

    logger.info("[TERRA] Health check")

    return json_response(
        {
            "status": "ok",
            "version": os.getenv("APP_VERSION"),
        }
    )
