import os
import pandas as pd
import numpy as np
import random
import math
from networkx.readwrite import json_graph
import json
import networkx as nx
import logging
import logging.config
from opencensus.ext.azure.log_exporter import AzureLogHandler

from flask import Flask,request,Response
from flask_cors import CORS
from waitress import serve

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

RUN_LOCAL = True
FILE_SEP = ","
PROD_DIGITS = 3  # number of digits to classify transports
MAX_NODES = 70
CHUNCK_SIZE = 5

# COMEXT DATASETS
INTRA_FILE = "data" + os.sep + "cpa_intra.csv"
EXTRA_FILE = "data" + os.sep + "tr_extra_ue.csv"
INTRA_TRIM_FILE = "data" + os.sep + "cpa_trim.csv"
EXTRA_TRIM_FILE = "data" + os.sep + "tr_extra_ue_trim.csv"

CRITERION = "VALUE_IN_EUROS"  # VALUE_IN_EUROS QUANTITY_IN_KG

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

def is_application_insight_configured():
    return (
        os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY") != None
        or os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING") != None
    )

def ai_callback_function(envelope):
    if os.getenv("CLOUD_ROLE") != None:
        envelope.tags["ai.cloud.role"] = os.getenv("CLOUD_ROLE")


if is_application_insight_configured():
    log_handler = AzureLogHandler()
    log_handler.add_telemetry_processor(ai_callback_function)
    logger.addHandler(log_handler)
else:
    logger.warning("Application insights is not configured.")

DB_SETTINGS : dict = {
    "DB_PROVIDER" : "",
    "DB_SERVER" : "",
    "DB_NAME" : "",
    "DB_DRIVER" : "",
    "DB_USER" : "",
    "DB_PASS" : ""
}

Base = declarative_base()
engine = create_engine(f'{DB_SETTINGS["DB_PROVIDER"]}://{DB_SETTINGS["DB_USER"]}:{DB_SETTINGS["DB_PASS"]}@{DB_SETTINGS["DB_SERVER"]}/{DB_SETTINGS["DB_NAME"]}?driver={DB_SETTINGS["DB_DRIVER"]}')

class CPAIntra(Base):
    __tablename__ = 'cpa_intra'

    declarant_iso = Column(String, primary_key=True)
    partner_iso = Column(String, primary_key=True)
    flow = Column(Integer, primary_key=True)
    product = Column(String, primary_key=True)
    period = Column(Integer, primary_key=True)
    value_in_euros = Column(Integer)

class CPATrim(Base):
    __tablename__ = 'cpa_trim'

    declarant_iso = Column(String, primary_key=True)
    partner_iso = Column(String, primary_key=True)
    flow = Column(Integer, primary_key=True)
    product = Column("cpa", String, primary_key=True)
    period = Column("trimestre", String, primary_key=True)
    value_in_euros = Column("val_cpa", Integer)
    quantity_in_kg = Column("q_kg", Integer)

class trExtraUE(Base):
    __tablename__ = 'tr_extra_ue'

    product = Column("product_nstr", String, primary_key=True)
    declarant_iso = Column(String, primary_key=True)
    partner_iso = Column(String, primary_key=True)
    period = Column(Integer, primary_key=True)
    transport_mode = Column(Integer, primary_key=True)
    flow = Column(Integer, primary_key=True)
    value_in_euros = Column(Integer)
    quantity_in_kg = Column(Integer)

class trExtraUETrim(Base):
    __tablename__ = 'tr_extra_ue_trim'

    product = Column("product_nstr", String, primary_key=True)
    declarant_iso = Column(String, primary_key=True)
    partner_iso = Column(String, primary_key=True)
    period = Column("trimestre", String, primary_key=True)
    transport_mode = Column(String, primary_key=True)
    flow = Column(Integer, primary_key=True)
    value_in_euros = Column(Integer)
    quantity_in_kg = Column(Integer)

# Build a query to delete edges in the graph
def build_edges_query(edges, flow):
    
    # Empty query object
    query = []
    
    for edge in edges:
        if flow == 1:
            PARTNER_ISO = edge["from"]
            DECLARANT_ISO = edge["to"]
        else:
            DECLARANT_ISO = edge["from"]
            PARTNER_ISO = edge["to"]

        exclude = str(edge["exclude"])

        # Graph without TRANSPORTS
        if "-99" in exclude:
            query.append(
                "(DECLARANT_ISO == '"
                + DECLARANT_ISO
                + "' & PARTNER_ISO == '"
                + PARTNER_ISO
                + "' )"
            )
        else:
            query.append(
                "((DECLARANT_ISO == '"
                + DECLARANT_ISO
                + "' & PARTNER_ISO == '"
                + PARTNER_ISO
                + "' & TRANSPORT_MODE in "
                + exclude
                + "))"
            )
    return "not (" + ("|".join(query)) + ")"


# Remove from the transport dataframe the subset NOT containing edges
def remove_edges(df_comext, edges, flow):
    query = build_edges_query(edges, flow)
    df_comext = df_comext.query(query)
    return df_comext


def build_metrics(graph):
    logger.info("[TERRA] Calculating graph metrics...")

    in_deg = nx.in_degree_centrality(graph)
    graph_metrics = {}
    vulnerability = {}

    for k, v in in_deg.items():
        if v != 0:
            vulnerability[k] = 1 - v
        else:
            vulnerability[k] = 0
        
        graph_metrics = {
            "degree_centrality": nx.degree_centrality(graph),
            "density": nx.density(graph),
            "vulnerability": vulnerability,
            "exportation strenght": {
                a: b for a, b in graph.out_degree(weight="weight")
            },
            "hubness": nx.closeness_centrality(graph.to_undirected()),
        }
    
    logger.info("[TERRA] Graph metrics ready!")
    return graph_metrics

def extract_graph_table(period,percentage,transports,flow,product,criterion,selectedEdges,db_table):
    logger.info("[TERRA] Preparing graph table...")

    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(db_table).filter(db_table.flow == flow)
    if period is not None:
        query = query.filter(db_table.period == period)
    if transports is not None:
        query = query.filter(db_table.transport_mode.in_(transports))
    if product is not None:
        query = query.filter(db_table.product == product)

    df_comext = pd.read_sql(query.statement, query.session.bind)
    session.close()

    # Extract EDGES
    if selectedEdges is not None:
        
        NUMBER_OF_EDGES_CHUNKS = len(selectedEdges) // (CHUNCK_SIZE)

        for i in range(NUMBER_OF_EDGES_CHUNKS):
            selectedEdges_i = selectedEdges[
                i * CHUNCK_SIZE : (i + 1) * CHUNCK_SIZE
            ]
            df_comext = remove_edges(
                df_comext, selectedEdges_i, flow
            )
        selectedEdges_i = selectedEdges[
            NUMBER_OF_EDGES_CHUNKS * CHUNCK_SIZE : len(selectedEdges)
        ]
        
        if len(selectedEdges_i) > 0:
            df_comext = remove_edges(
                df_comext, selectedEdges_i, flow
            )

    # Aggregate on DECLARANT_ISO and PARTNER_ISO and sort on criterion (VALUE or QUANTITY)
    df_comext = (
        df_comext.groupby(["DECLARANT_ISO", "PARTNER_ISO"])
        .sum()
        .reset_index()[["DECLARANT_ISO", "PARTNER_ISO", criterion]]
    )
    df_comext = df_comext.sort_values(
        criterion, ascending=False
    )
    
    # Cut graph on bottom percentile
    if percentage is not None:
        SUM = df_comext[criterion].sum()
        df_comext = df_comext[
            df_comext[criterion].cumsum(skipna=False) / SUM * 100 < percentage
        ]
    
    logger.info("[TERRA] Graph table ready!")

    return df_comext



def build_graph(tab4graph, pos_ini, weight_flag, flow, criterion):
    
    logger.info("[TERRA] Building GRAPH...")

    # Create an empty graph
    G = nx.DiGraph()

    # Assign roles according to flow (IMPORT or EXPORT)
    if flow == 1:
        country_from = "PARTNER_ISO"
        country_to = "DECLARANT_ISO"
    else:
        country_from = "DECLARANT_ISO"
        country_to = "PARTNER_ISO"

    # Build the Graph with edges and nodes, if the Graph is weighted
    # assign the weight VALUE or QUANTITY depending on the criterion chosen to sort the market and perform the cut
    if weight_flag == True:
        weight = criterion
        WEIGHT_SUM = tab4graph[weight].sum()
        edges = [
            (i, j, w / WEIGHT_SUM)
            for i, j, w in tab4graph.loc[:, [country_from, country_to, weight]].values
        ]
    else:
        edges = [
            (i, j, 1) for i, j in tab4graph.loc[:, [country_from, country_to]].values
        ]

    # Add weigthed edges to the graph
    G.add_weighted_edges_from(edges)

    attribute = {}
    for i, j, w in edges:
        attribute[(i, j)] = {criterion: int(w * WEIGHT_SUM)}

    nx.set_edge_attributes(G, attribute)

    # Build metrics
    graph_metrics = build_metrics(G)

    # Json graph
    GG = json_graph.node_link_data(G)
    
    k_layout = 5
    pos_ini = {}
    random.seed(88)
    for node in GG["nodes"]:
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        pos_ini[node["id"]] = np.array([x, y])

    try:
        coord = nx.spring_layout(
            G, k=k_layout / math.sqrt(G.order()), pos=pos_ini, iterations=200
         )
        coord = nx.spring_layout(
            G, k=k_layout / math.sqrt(G.order()), pos=coord, iterations=50
        )  # stable solution

    except:
        return None, None, None

    # Create a dataframe with graph nodes coordinates
    df_coord = pd.DataFrame.from_dict(coord, orient="index")
    df_coord.columns = ["x", "y"]

    df = pd.DataFrame(GG["nodes"])
    df.columns = ["label"]
    df["id"] = np.arange(df.shape[0])
    df = df[["id", "label"]]
    out = pd.merge(df, df_coord, left_on="label", right_index=True)
    dict_nodes = out.T.to_dict().values()

    dfe = pd.DataFrame(GG["links"])[["source", "target", "weight", criterion]]
    res = dfe.set_index("source").join(
        out[["label", "id"]].set_index("label"), on="source", how="left"
    )
    res.columns = ["target", "source_id", "weight", criterion]
    res2 = res.set_index("target").join(
        out[["label", "id"]].set_index("label"), on="target", how="left"
    )
    res2.columns = ["weight", criterion, "from", "to"]
    res2.reset_index(drop=True, inplace=True)
    dict_edges = res2.T.to_dict().values()

    new_dict = {
        "nodes": list(dict_nodes),
        "edges": list(dict_edges),
        "metriche": graph_metrics,
    }

    JSON = json.dumps(new_dict)

    logger.info("[TERRA] GRAPH built!")

    return coord, JSON, G


def jsonpos2coord(jsonpos):
    logger.info("[TERRA] JSON2COORDINATES...")
    coord = {}
    for id, x, y in pd.DataFrame.from_dict(jsonpos["nodes"])[
        ["label", "x", "y"]
    ].values:
        coord[id] = np.array([x, y])
    logger.info("[TERRA] JSON2COORDINATES done!")
    return coord

app = Flask(__name__)
CORS(app, resources=r'/*')

if RUN_LOCAL is False:
    azure_exporter = AzureExporter()
    azure_exporter.add_telemetry_processor(ai_callback_function)
    if is_application_insight_configured():
        middleware = FlaskMiddleware(
            app,
            exporter=azure_exporter,
            sampler=ProbabilitySampler(rate=1.0),
        ) 


@app.route("/graphExtraMonth", methods=["POST", "GET"])
def graphExtraMonth():
    if request.method == "POST":
        logger.info("[TERRA] Graph extra month...")

        # Currently criterio is set to "VALUE_IN_EUROS" 
        criterion = CRITERION

        # User request
        jsonRequest = dict(request.json)
        
        #Get PERCENTAGE
        percentage = int(jsonRequest["tg_perc"])
        
        #Get PERIOD
        period = int(jsonRequest["tg_period"])
        
        #Get NODES COORDINATES
        pos = jsonRequest["pos"]
        if pos == "None" or len(pos["nodes"]) == 0:
            pos = None
        else:
            # Build nodes coordinates according to previous graph
            pos = jsonpos2coord(pos)

        # 0:Unknown 1:Sea 2:Rail 3:Road 4Air 5:Post 7:Fixed Mechanism 8:Inland Waterway 9:Self Propulsion
        transports = jsonRequest["listaMezzi"]  # [0,1,2,3,4,5,7,8,9]
        
        #Get FLOW
        flow = int(jsonRequest["flow"])
        
        #Get PRODUCT
        product = str(jsonRequest["product"])
        
        #Get WEIGHT_FLAG (currently hardcoded)
        weight_flag = bool(jsonRequest["weight_flag"])
        
        # This key is set in the scenario analysis
        selectedTransportEdges = jsonRequest["selezioneMezziEdges"]
        if selectedTransportEdges == "None":
            selectedTransportEdges = None
        else:
            pass

        #Build graph table
        tab4graph = extract_graph_table(
            period,
            percentage,
            transports,
            flow,
            product,
            criterion,
            selectedTransportEdges,
            trExtraUE,
        )
        logger.info(f"[TERRA] Graph shape {tab4graph.shape}")
        
        # Check the size of the graph
        NUM_NODI = len(
            set(tab4graph["DECLARANT_ISO"]).union(set(tab4graph["PARTNER_ISO"]))
        )
        if NUM_NODI > MAX_NODES:
            logger.info(f"[TERRA] Graph is too wide!")
            return json.dumps({"STATUS": "05"})
        
        # Build graph
        pos, JSON, G = build_graph(tab4graph, pos, weight_flag, flow, criterion)

        if pos is None:
            if JSON is None:
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

        # Currently criterio is set to "VALUE_IN_EUROS" 
        criterion = CRITERION

        # User request
        jsonRequest = dict(request.json)
        
        #Get PERCENTAGE
        percentage = int(jsonRequest["tg_perc"])
        
        #Get PERIOD
        period = str(jsonRequest['tg_period'][:-2] + "T" + jsonRequest['tg_period'][-1:])        
        
        #Get NODES COORDINATES
        pos = jsonRequest["pos"]
        if pos == "None" or len(pos["nodes"]) == 0:
            pos = None
        else:
            # Build nodes coordinates according to previous graph
            pos = jsonpos2coord(pos)

        # 0:Unknown 1:Sea 2:Rail 3:Road 4Air 5:Post 7:Fixed Mechanism 8:Inland Waterway 9:Self Propulsion
        transports = jsonRequest["listaMezzi"]  # [0,1,2,3,4,5,7,8,9]
        
        #Get FLOW
        flow = int(jsonRequest["flow"])
        
        #Get PRODUCT
        product = str(jsonRequest["product"])
        
        #Get WEIGHT_FLAG (currently hardcoded)
        weight_flag = bool(jsonRequest["weight_flag"])
        
        # This key is set in the scenario analysis
        selectedTransportEdges = jsonRequest["selezioneMezziEdges"]
        if selectedTransportEdges == "None":
            selectedTransportEdges = None
        else:
            pass

        #Build graph table
        tab4graph = extract_graph_table(
            period,
            percentage,
            transports,
            flow,
            product,
            criterion,
            selectedTransportEdges,
            trExtraUETrim,
        )
        logger.info(f"[TERRA] Graph shape {tab4graph.shape}")
        
        # Check the size of the graph
        NUM_NODI = len(
            set(tab4graph["DECLARANT_ISO"]).union(set(tab4graph["PARTNER_ISO"]))
        )
        if NUM_NODI > MAX_NODES:
            logger.info(f"[TERRA] Graph is too wide!")
            return json.dumps({"STATUS": "05"})
        
        # Build graph
        pos, JSON, G = build_graph(tab4graph, pos, weight_flag, flow, criterion)

        if pos is None:
            if JSON is None:
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
        logger.info("[TERRA] Graph intra month...")

        # Currently criterio is set to "VALUE_IN_EUROS" 
        criterion = CRITERION

        # User request
        jsonRequest = dict(request.json)
        
        #Get PERCENTAGE
        percentage = int(jsonRequest["tg_perc"])
        
        #Get PERIOD
        period = int(jsonRequest["tg_period"])
        
        #Get NODES COORDINATES
        pos = jsonRequest["pos"]
        if pos == "None" or len(pos["nodes"]) == 0:
            pos = None
        else:
            # Build nodes coordinates according to previous graph
            pos = jsonpos2coord(pos)

        #Get FLOW
        flow = int(jsonRequest["flow"])
        
        #Get PRODUCT
        product = str(jsonRequest["product"])
        
        #Get WEIGHT_FLAG (currently hardcoded)
        weight_flag = bool(jsonRequest["weight_flag"])
        
        # This key is set in the scenario analysis
        selectedTransportEdges = jsonRequest["selezioneMezziEdges"]
        if selectedTransportEdges == "None":
            selectedTransportEdges = None
        else:
            pass

        #Build graph table (without transports)
        tab4graph = extract_graph_table(
            period,
            percentage,
            None,
            flow,
            product,
            criterion,
            selectedTransportEdges,
            CPAIntra,
        )
        logger.info(f"[TERRA] Graph shape {tab4graph.shape}")
        
        # Check the size of the graph
        NUM_NODI = len(
            set(tab4graph["DECLARANT_ISO"]).union(set(tab4graph["PARTNER_ISO"]))
        )
        if NUM_NODI > MAX_NODES:
            logger.info(f"[TERRA] Graph is too wide!")
            return json.dumps({"STATUS": "05"})
        
        # Build graph
        pos, JSON, G = build_graph(tab4graph, pos, weight_flag, flow, criterion)

        if pos is None:
            if JSON is None:
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
        logger.info("[TERRA] Graph intra trimester...")

        # Currently criterio is set to "VALUE_IN_EUROS" 
        criterion = CRITERION

        # User request
        jsonRequest = dict(request.json)
        
        #Get PERCENTAGE
        percentage = int(jsonRequest["tg_perc"])
        
        #Get PERIOD
        period = str(jsonRequest['tg_period'][:-2] + "T" + jsonRequest['tg_period'][-1:])
        
        #Get NODES COORDINATES
        pos = jsonRequest["pos"]
        if pos == "None" or len(pos["nodes"]) == 0:
            pos = None
        else:
            # Build nodes coordinates according to previous graph
            pos = jsonpos2coord(pos)

        #Get FLOW
        flow = int(jsonRequest["flow"])
        
        #Get PRODUCT
        product = str(jsonRequest["product"])
        
        #Get WEIGHT_FLAG (currently hardcoded)
        weight_flag = bool(jsonRequest["weight_flag"])
        
        # This key is set in the scenario analysis
        selectedTransportEdges = jsonRequest["selezioneMezziEdges"]
        if selectedTransportEdges == "None":
            selectedTransportEdges = None
        else:
            pass

        #Build graph table (without transports)
        tab4graph = extract_graph_table(
            period,
            percentage,
            None,
            flow,
            product,
            criterion,
            selectedTransportEdges,
            CPATrim,
        )
        logger.info(f"[TERRA] Graph shape {tab4graph.shape}")
        
        # Check the size of the graph
        NUM_NODI = len(
            set(tab4graph["DECLARANT_ISO"]).union(set(tab4graph["PARTNER_ISO"]))
        )
        if NUM_NODI > MAX_NODES:
            logger.info(f"[TERRA] Graph is too wide!")
            return json.dumps({"STATUS": "05"})
        
        # Build graph
        pos, JSON, G = build_graph(tab4graph, pos, weight_flag, flow, criterion)

        if pos is None:
            if JSON is None:
                logger.info(f"[TERRA] Graph is empty!")
                return json.dumps({"STATUS": "06"})
        
        resp = Response(response=JSON, status=200, mimetype="application/json")
        logger.info("[TERRA] Graph intra trimester done!")
        return resp
    else:
        logger.info("[TERRA] Error in HTTP request method!")
        return str("only post")
    

if __name__ == '__main__':
    IP='127.0.0.1'
    port=5500
    serve(app, host=IP, port=port)
