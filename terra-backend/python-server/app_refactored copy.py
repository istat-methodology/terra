import json

from flask import Flask, request, Response
from flask_cors import CORS
from waitress import serve

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler

from modules import utils, orm, functions
from resources import py_server_params

logger = utils.get_logger()
utils.execute_preliminaries(logger)
engine = orm.orm_setup(py_server_params.DB_SETTINGS)
misc = functions.Misc(logger)
graphs = functions.GraphEngine(engine, logger)
timeseries  = functions.TimeSeries(engine, logger)


#### SERVER ####
app = Flask(__name__)
CORS(app, resources=r'/*')

if py_server_params.RUN_LOCAL is False:
    azure_exporter = AzureExporter()
    azure_exporter.add_telemetry_processor(utils.ai_callback_function)
    if utils.is_application_insight_configured():
        middleware = FlaskMiddleware(
            app,
            exporter=azure_exporter,
            sampler=ProbabilitySampler(rate=1.0),
        )


@app.route("/graphExtraMonth", methods=["POST", "GET"])
def graphExtraMonth():
    if request.method == "POST":
        logger.info("[TERRA] Graph extra month...")

        json_request = dict(request.json)
        request_items = functions.RequestHandler(logger).get_items(json_request, "monthly")

        tab4graph = graphs.extract_graph_table(
            chunksize=py_server_params.ENDPOINT_SETTINGS["CHUNK_SIZE"],
            period=request_items["period"],
            percentage=request_items["percentage"],
            transports=request_items["transport"],
            flow=request_items["flow"],
            product=request_items["product"],
            criterion=request_items["criterion"],
            selectedEdges=request_items["selected_transport_edges"],
            db_table=orm.trExtraUE
        )
        logger.info(f"[TERRA] Graph shape {tab4graph.shape}")

        if graphs.width_check(tab4graph, py_server_params.ENDPOINT_SETTINGS["MAX_NODES"]) is False:
            return json.dumps({"STATUS": "05"})
        
        pos, JSON, G = graphs.build_graph(
            tab4graph=tab4graph,
            pos_ini=request_items["pos"],
            weight_flag=request_items["weight_flag"],
            flow=request_items["flow"],
            criterion=request_items["criterion"]
        )

        if pos is None and JSON is None:
            logger.info(f"[TERRA] Graph is empty!")
            return json.dumps({"STATUS": "06"})
        
        resp = Response(response=JSON, status=200, mimetype="application/json")
        logger.info("[TERRA] Graph extra month done!")
        return resp

    else:
        logger.info("[TERRA] Error in HTTP request method!")
        return str("only post")


@app.route("/graphExtraTrim", methods=["POST", "GET"])
def graphExtraTrim():
    if request.method == "POST":
        logger.info("[TERRA] Graph extra trimester...")

        json_request = dict(request.json)
        request_items = functions.RequestHandler(logger).get_items(json_request, "quarterly")

        tab4graph = graphs.extract_graph_table(
            chunksize=py_server_params.ENDPOINT_SETTINGS["CHUNK_SIZE"],
            period=request_items["period"],
            percentage=request_items["percentage"],
            transports=request_items["transport"],
            flow=request_items["flow"],
            product=request_items["product"],
            criterion=request_items["criterion"],
            selectedEdges=request_items["selected_transport_edges"],
            db_table=orm.trExtraUETrim
        )
        logger.info(f"[TERRA] Graph shape {tab4graph.shape}")

        if graphs.width_check(tab4graph, py_server_params.ENDPOINT_SETTINGS["MAX_NODES"]) is False:
                    return json.dumps({"STATUS": "05"})
        
        # Build graph
        pos, JSON, G = graphs.build_graph(
            tab4graph=tab4graph,
            pos_ini=request_items["pos"],
            weight_flag=request_items["weight_flag"],
            flow=request_items["flow"],
            criterion=request_items["criterion"]
        )

        if pos is None and JSON is None:
            logger.info(f"[TERRA] Graph is empty!")
            return json.dumps({"STATUS": "06"})
        
        resp = Response(response=JSON, status=200, mimetype="application/json")
        logger.info("[TERRA] Graph extra trimester done!")
        return resp

    else:
        logger.info("[TERRA] Error in HTTP request method!")
        return str("only post")


@app.route('/graphIntraMonth', methods=['POST','GET'])
def graphIntraMonth():
    if request.method == 'POST':
        logger.info("[TERRA] Graph extra trimester...")

        json_request = dict(request.json)
        request_items = functions.RequestHandler(logger).get_items(json_request, "monthly")

        tab4graph = graphs.extract_graph_table(
            chunksize=py_server_params.ENDPOINT_SETTINGS["CHUNK_SIZE"],
            period=request_items["period"],
            percentage=request_items["percentage"],
            transports=[],
            flow=request_items["flow"],
            product=request_items["product"],
            criterion=request_items["criterion"],
            selectedEdges=request_items["selected_transport_edges"],
            db_table=orm.CPAIntra
        )
        logger.info(f"[TERRA] Graph shape {tab4graph.shape}")

        if graphs.width_check(tab4graph, py_server_params.ENDPOINT_SETTINGS["MAX_NODES"]) is False:
                    return json.dumps({"STATUS": "05"})
        
        # Build graph
        pos, JSON, G = graphs.build_graph(
            tab4graph=tab4graph,
            pos_ini=request_items["pos"],
            weight_flag=request_items["weight_flag"],
            flow=request_items["flow"],
            criterion=request_items["criterion"]
        )

        if pos is None and JSON is None:
            logger.info(f"[TERRA] Graph is empty!")
            return json.dumps({"STATUS": "06"})
        
        resp = Response(response=JSON, status=200, mimetype="application/json")
        logger.info("[TERRA] Graph intra month done!")
        return resp
    
    else:
        logger.info("[TERRA] Error in HTTP request method!")
        return str("only post")


@app.route('/graphIntraTrim', methods=['POST','GET'])
def graphIntraTrim():
    if request.method == 'POST':
        logger.info("[TERRA] Graph extra trimester...")

        json_request = dict(request.json)
        request_items = functions.RequestHandler(logger).get_items(json_request, "quarterly")

        tab4graph = graphs.extract_graph_table(
            chunksize=py_server_params.ENDPOINT_SETTINGS["CHUNK_SIZE"],
            period=request_items["period"],
            percentage=request_items["percentage"],
            transports=[],
            flow=request_items["flow"],
            product=request_items["product"],
            criterion=request_items["criterion"],
            selectedEdges=request_items["selected_transport_edges"],
            db_table=orm.CPATrim
        )
        logger.info(f"[TERRA] Graph shape {tab4graph.shape}")

        if graphs.width_check(tab4graph, py_server_params.ENDPOINT_SETTINGS["MAX_NODES"]) is False:
                    return json.dumps({"STATUS": "05"})
        
        # Build graph
        pos, JSON, G = graphs.build_graph(
            tab4graph=tab4graph,
            pos_ini=request_items["pos"],
            weight_flag=request_items["weight_flag"],
            flow=request_items["flow"],
            criterion=request_items["criterion"]
        )

        if pos is None and JSON is None:
            logger.info(f"[TERRA] Graph is empty!")
            return json.dumps({"STATUS": "06"})
        
        resp = Response(response=JSON, status=200, mimetype="application/json")
        logger.info("[TERRA] Graph intra trimester done!")
        return resp
    
    else:
        logger.info("[TERRA] Error in HTTP request method!")
        return str("only post")


@app.route('/itsa', methods=['GET','POST'])
def itsa():
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
         country=country,
         partner=partner,
         dataType=dataType,
         tipo_var=tipovar
    )
    response = Response(response=result, status=200, mimetype="application/json")
    return response
    
if __name__ == '__main__':
    IP='127.0.0.1'
    port=5500
    serve(app, host=IP, port=port)
