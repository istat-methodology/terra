from __future__ import annotations

from flask import Blueprint, request

from routes._utils import get_services, json_response, bad_request

bp = Blueprint("timeseries", __name__)


@bp.route("/ts", methods=["POST"])
def ts():
    services = get_services()
    logger = services["logger"]
    timeseries = services["timeseries"]
    orm = services["orm"]

    payload = dict(request.json or {})

    try:
        result = timeseries.ts(
            table_import=orm.comextImp,
            table_export=orm.comextExp,
            flow=int(payload["flow"]),
            var_cpa=payload["var"],
            country_code=payload["country"],
            partner_code=payload["partner"],
            data_type=int(payload["dataType"]),
            var_type=int(payload["varType"]),
        )
    except KeyError as e:
        msg = f"Missing required field: {e}"
        logger.warning(f"[TERRA] {msg}")
        return bad_request(msg)
    except ValueError as e:
        logger.warning(f"[TERRA] Invalid parameter in /ts: {e}")
        return bad_request(str(e))
    except Exception as e:
        logger.exception("[TERRA] Error while computing time series")
        return json_response(
            {"statusMain": "00", "error": "Internal error while computing time series"},
            status=500,
        )

    return json_response(result)
