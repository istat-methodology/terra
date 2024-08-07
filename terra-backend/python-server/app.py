import json
import os

from flask import Flask, request, Response
from flask_cors import CORS
from waitress import serve

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler

from modules import utils, orm, functions
from resources import py_server_params

from dotenv import load_dotenv

load_dotenv()

logger = utils.get_logger()
utils.execute_preliminaries(logger)
engine = orm.orm_setup(py_server_params.DB_SETTINGS)
misc = functions.Misc(logger)
graphs = functions.GraphEngine(engine, logger)
timeseries  = functions.TimeSeries(engine, logger)


#### SERVER ####
app = Flask(__name__)
CORS(app, resources=r'/*')

try:
    azure_exporter = AzureExporter()
    azure_exporter.add_telemetry_processor(utils.ai_callback_function)
    middleware = FlaskMiddleware(
        app,
        exporter=azure_exporter,
        sampler=ProbabilitySampler(rate=1.0),
    )
except BaseException as e:
    logger.warning(e)

@app.route('/hello')
def hello():
    return str('Version '+str(os.getenv('APP_VERSION')))

@app.route("/graphExtraMonth", methods=["POST"])
def graphExtraMonth():
    logger.info("[TERRA] Graph extra month...")

    json_request = dict(request.json)
    request_items = functions.RequestHandler(logger).get_items(json_request, "monthly")

    tab4graph, tab4graph_ui = graphs.extract_graph_table(
        chunksize=py_server_params.ENDPOINT_SETTINGS["CHUNK_SIZE"],
        period=request_items["period"],
        percentage=request_items["percentage"],
        transport=request_items["transport"],
        flow=request_items["flow"],
        product=request_items["product"],
        criterion=request_items["criterion"],
        edges=request_items["edges"],
        db_table=orm.trExtraUE,
        collapse=request_items["collapse"]
    )
    logger.info(f"[TERRA] Graph shape {tab4graph.shape}")

    if graphs.width_check(tab4graph_ui, py_server_params.ENDPOINT_SETTINGS["MAX_NODES"]) is False:
        return json.dumps({"STATUS": "05"})
    
    position, JSON, G = graphs.build_graph(
        tab4graph=tab4graph,
        tab4graph_ui=tab4graph_ui,
        pos_ini=request_items["position"],
        weight=request_items["weight"],
        flow=request_items["flow"],
        criterion=request_items["criterion"]
    )

    if position is None and JSON is None:
        logger.info(f"[TERRA] Graph is empty!")
        return json.dumps({"STATUS": "06"})
    
    resp = Response(response=JSON, status=200, mimetype="application/json")
    logger.info("[TERRA] Graph extra month done!")
    return resp

@app.route("/graphExtraTrim", methods=["POST"])
def graphExtraTrim():
    logger.info("[TERRA] Graph extra trimester...")

    json_request = dict(request.json)
    request_items = functions.RequestHandler(logger).get_items(json_request, "quarterly")

    tab4graph, tab4graph_ui = graphs.extract_graph_table(
        chunksize=py_server_params.ENDPOINT_SETTINGS["CHUNK_SIZE"],
        period=request_items["period"],
        percentage=request_items["percentage"],
        transport=request_items["transport"],
        flow=request_items["flow"],
        product=request_items["product"],
        criterion=request_items["criterion"],
        edges=request_items["edges"],
        db_table=orm.trExtraUETrim,
        collapse=request_items["collapse"]
    )
    logger.info(f"[TERRA] Graph shape {tab4graph.shape}")

    if graphs.width_check(tab4graph_ui, py_server_params.ENDPOINT_SETTINGS["MAX_NODES"]) is False:
        return json.dumps({"STATUS": "05"})
    
    # Build graph
    position, JSON, G = graphs.build_graph(
        tab4graph=tab4graph,
        tab4graph_ui=tab4graph_ui,
        pos_ini=request_items["position"],
        weight=request_items["weight"],
        flow=request_items["flow"],
        criterion=request_items["criterion"]
    )

    if position is None and JSON is None:
        logger.info(f"[TERRA] Graph is empty!")
        return json.dumps({"STATUS": "06"})
    
    resp = Response(response=JSON, status=200, mimetype="application/json")
    logger.info("[TERRA] Graph extra trimester done!")
    return resp

@app.route('/graphIntraMonth', methods=['POST'])
def graphIntraMonth():
    logger.info("[TERRA] Graph intra month...")

    json_request = dict(request.json)
    request_items = functions.RequestHandler(logger).get_items(json_request, "monthly")

    tab4graph, tab4graph_ui = graphs.extract_graph_table(
        chunksize=py_server_params.ENDPOINT_SETTINGS["CHUNK_SIZE"],
        period=request_items["period"],
        percentage=request_items["percentage"],
        transport=[],
        flow=request_items["flow"],
        product=request_items["product"],
        criterion=request_items["criterion"],
        edges=request_items["edges"],
        db_table=orm.CPAIntra,
        collapse=request_items["collapse"]
    )
    logger.info(f"[TERRA] Graph shape {tab4graph.shape}")

    if graphs.width_check(tab4graph_ui, py_server_params.ENDPOINT_SETTINGS["MAX_NODES"]) is False:
        return json.dumps({"STATUS": "05"})
    
    # Build graph
    position, JSON, G = graphs.build_graph(
        tab4graph=tab4graph,
        tab4graph_ui=tab4graph_ui,
        pos_ini=request_items["position"],
        weight=request_items["weight"],
        flow=request_items["flow"],
        criterion=request_items["criterion"]
    )

    if position is None and JSON is None:
        logger.info(f"[TERRA] Graph is empty!")
        return json.dumps({"STATUS": "06"})
    
    resp = Response(response=JSON, status=200, mimetype="application/json")
    logger.info("[TERRA] Graph intra month done!")
    return resp

@app.route('/graphIntraTrim', methods=['POST'])
def graphIntraTrim():
    logger.info("[TERRA] Graph extra trimester...")

    json_request = dict(request.json)
    request_items = functions.RequestHandler(logger).get_items(json_request, "quarterly")

    tab4graph, tab4graph_ui = graphs.extract_graph_table(
        chunksize=py_server_params.ENDPOINT_SETTINGS["CHUNK_SIZE"],
        period=request_items["period"],
        percentage=request_items["percentage"],
        transport=[],
        flow=request_items["flow"],
        product=request_items["product"],
        criterion=request_items["criterion"],
        edges=request_items["edges"],
        db_table=orm.CPATrim,
        collapse=request_items["collapse"]
    )
    logger.info(f"[TERRA] Graph shape {tab4graph.shape}")

    if graphs.width_check(tab4graph_ui, py_server_params.ENDPOINT_SETTINGS["MAX_NODES"]) is False:
        return json.dumps({"STATUS": "05"})
    
    # Build graph
    position, JSON, G = graphs.build_graph(
        tab4graph=tab4graph,
        tab4graph_ui=tab4graph_ui,
        pos_ini=request_items["position"],
        weight=request_items["weight"],
        flow=request_items["flow"],
        criterion=request_items["criterion"]
    )

    if position is None and JSON is None:
        logger.info(f"[TERRA] Graph is empty!")
        return json.dumps({"STATUS": "06"})
    
    resp = Response(response=JSON, status=200, mimetype="application/json")
    logger.info("[TERRA] Graph intra trimester done!")
    return resp


@app.route('/ts', methods=['POST'])
def ts():
    jsonRequest = dict(request.json)

    flow = jsonRequest['flow']
    var = jsonRequest['var']
    country = jsonRequest['country']
    partner = jsonRequest['partner']
    dataType = jsonRequest['dataType']
    tipovar = jsonRequest['tipovar'] # cambiare da tipovar a vartype
    
    result = timeseries.ts(
         table_import=orm.comextImp,
         table_export=orm.comextExp,
         flow=flow,
         var_cpa=var,
         country_code=country,
         partner_code=partner,
         data_type=dataType,
         tipo_var=tipovar
    )
    response = Response(response=result, status=200, mimetype="application/json")
    return response
    
if __name__ == '__main__':
    IP='0.0.0.0'
    port=5500
    serve(app, host=IP, port=port)
