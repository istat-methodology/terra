from __future__ import annotations

from flask import Blueprint, request

from routes._utils import get_services, json_response, bad_request

bp = Blueprint("graph", __name__)


def _handle_graph(endpoint_label: str, frequency: str, db_table, transport_from_request: bool):
    services = get_services()
    logger = services["logger"]
    graphs = services["graphs"]
    rh = services["request_handler"]
    params = services["params"]

    logger.info(f"[TERRA] {endpoint_label}...")

    json_request = dict(request.json or {})

    try:
        req = rh.get_graph_items(json_request, frequency)
    except ValueError as e:
        logger.warning(f"[TERRA] Bad request in {endpoint_label}: {e}")
        return bad_request(str(e))

    tab4graph, tab4graph_ui = graphs.extract_graph_table(
        chunksize=int(params.ENDPOINT_SETTINGS["CHUNK_SIZE"]),
        period=req.period,
        percentage=req.percentage,
        transport=req.transport if transport_from_request else [],
        flow=req.flow,
        product=req.product,
        criterion=req.criterion,
        edges=req.edges,
        db_table=db_table,
        collapse=req.collapse,
    )
    logger.info(f"[TERRA] Graph shape {tab4graph.shape}")

    if not graphs.width_check(tab4graph_ui, int(params.ENDPOINT_SETTINGS["MAX_NODES"])):
        return json_response({"STATUS": "05"})

    position, graph_json, _ = graphs.build_graph(
        tab4graph=tab4graph,
        tab4graph_ui=tab4graph_ui,
        pos_ini=req.position,
        weight=req.weight,
        flow=req.flow,
        criterion=req.criterion,
    )

    if position is None and graph_json is None:
        logger.info("[TERRA] Graph is empty!")
        return json_response({"STATUS": "06"})

    logger.info(f"[TERRA] {endpoint_label} done!")
    return json_response(graph_json)


@bp.route("/graphExtraMonth", methods=["POST"])
def graph_extra_month():
    orm = get_services()["orm"]
    return _handle_graph("Graph extra month", "monthly", orm.trExtraUE, True)


@bp.route("/graphExtraTrim", methods=["POST"])
def graph_extra_trim():
    orm = get_services()["orm"]
    return _handle_graph("Graph extra trimester", "quarterly", orm.trExtraUETrim, True)


@bp.route("/graphIntraMonth", methods=["POST"])
def graph_intra_month():
    orm = get_services()["orm"]
    return _handle_graph("Graph intra month", "monthly", orm.CPAIntra, False)


@bp.route("/graphIntraTrim", methods=["POST"])
def graph_intra_trim():
    orm = get_services()["orm"]
    return _handle_graph("Graph intra trimester", "quarterly", orm.CPATrim, False)
