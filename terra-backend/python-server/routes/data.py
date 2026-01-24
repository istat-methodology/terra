from __future__ import annotations

from flask import Blueprint, request

from routes._utils import get_services, json_response, bad_request

bp = Blueprint("data", __name__)


@bp.route("/downloadData", methods=["POST"])
def download_data():
    services = get_services()
    logger = services["logger"]
    misc = services["misc"]

    logger.info("[TERRA] Data download...")

    payload = dict(request.json or {})

    try:
        data_json = misc.extract_data_table(
            product_class=payload["product_class"],
            period=payload["period"],
            country=payload["country"],
            partner=payload.get("partner"),
            product=payload.get("product"),
            flow=int(payload["flow"]) if payload.get("flow") is not None else None,
            criterion=int(payload["criterion"]),
            transport=payload.get("transport"),
        )
    except KeyError as e:
        msg = f"Missing required field: {e}"
        logger.warning(f"[TERRA] {msg}")
        return bad_request(msg)
    except ValueError as e:
        logger.warning(f"[TERRA] Invalid parameter in /downloadData: {e}")
        return bad_request(str(e))
    except Exception:
        logger.exception("[TERRA] Error while downloading data")
        return json_response({"STATUS": "00", "error": "Internal error while downloading data"}, status=500)

    logger.info("[TERRA] Data download done!")
    return json_response(data_json)
