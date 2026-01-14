import pandas as pd
import numpy as np
import random
import math
import json
import networkx as nx
from distinctiveness.dc import distinctiveness
from networkx.readwrite import json_graph
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, union_all, or_
from resources import py_server_params
from modules import orm

class GraphEngine():

    def __init__(self, engine, logger):
        self.engine = engine
        self.logger = logger


    def build_edges_query(self, edges, flow):
        query = []
        for edge in edges:
            if flow == 1:
                partner_iso = edge["from"]
                declarant_iso = edge["to"]
            else:
                partner_iso = edge["to"]
                declarant_iso = edge["from"]
            exclude = str(edge["exclude"])

            if "-99" in exclude:
                query.append(f"(DECLARANT_ISO == '{declarant_iso}' & PARTNER_ISO == '{partner_iso}')")
            else:
                query.append(f"((DECLARANT_ISO == '{declarant_iso}' & PARTNER_ISO == '{partner_iso}' & TRANSPORT_MODE in {exclude}))")
        
        return f"not ({('|'.join(query))})"


    def remove_edges(self, df_comext, edges, flow):
        query = self.build_edges_query(edges, flow)
        df_comext = df_comext.query(query)
        return df_comext


    def build_metrics(self, graph):
        self.logger.info("[TERRA] Calculating graph metrics...")
        self.logger.info(f"Graph: {graph}")

        vulnerability = {}
        in_deg = nx.in_degree_centrality(graph)
        for k, v in in_deg.items():
            if v != 0:
                vulnerability[k] = 1 - v
            else:
                vulnerability[k] = 0
        
        graph_metrics = {}
        graph_metrics = {
            "density": nx.density(graph),
            "degree": {a: b for a, b in graph.degree(weight="weight")},
            "vulnerability": vulnerability,
            "out_degree": {
                a: b for a, b in graph.out_degree(weight="weight")
            },
            "closeness": nx.closeness_centrality(graph, distance="inv_weight"),
            "betweenness": nx.betweenness_centrality(graph, weight="inv_weight"),
            "in_degree": {
                a: b for a, b in graph.in_degree(weight="weight")
            },
            "distinctiveness": distinctiveness(graph.to_undirected(), alpha = 1, normalize = True, measures = ["D1"])["D1"]
        }

        self.logger.info("[TERRA] Graph metrics ready!")
        return graph_metrics


    def extract_graph_table(self, chunksize, period, percentage, transport, flow, product, criterion, edges, db_table, collapse):
        self.logger.info("[TERRA] Preparing graph table...")

        Session = sessionmaker(bind=self.engine)
        session = Session()
        query = ''

        if flow==0:
            queries = []
            for f in [1,2]:
                q = session.query(
                    db_table.DECLARANT_ISO if f==2 else db_table.PARTNER_ISO.label('DECLARANT_ISO'),
                    db_table.PARTNER_ISO if f==2 else db_table.DECLARANT_ISO.label('PARTNER_ISO'),
                    func.sum(db_table.VALUE_IN_EUROS).label(criterion)
                ).filter(db_table.FLOW == f)
                if period is not None:
                    q = q.filter(db_table.PERIOD == period)
                if len(transport)>0:
                    q = q.filter(db_table.TRANSPORT_MODE.in_(transport))
                if product is not None:
                    q = q.filter(db_table.PRODUCT == product)
                q = q.group_by(
                    db_table.DECLARANT_ISO,
                    db_table.PARTNER_ISO
                )
                queries.append(q)
            combined_subquery = union_all(*queries).alias('A')

            query = session.query(
                combined_subquery.c.DECLARANT_ISO,
                combined_subquery.c.PARTNER_ISO,
                func.avg(combined_subquery.c.VALUE_IN_EUROS).label(criterion)
            ).group_by(
                combined_subquery.c.DECLARANT_ISO,
                combined_subquery.c.PARTNER_ISO
            )
        else:
            query = session.query(db_table).filter(db_table.FLOW == flow)
            if period is not None:
                query = query.filter(db_table.PERIOD == period)
            if len(transport)>0:
                query = query.filter(db_table.TRANSPORT_MODE.in_(transport))
            if product is not None:
                query = query.filter(db_table.PRODUCT == product)

        query_result = query.all()
        session.close()
        columns_list = [desc['name'] for desc in query.column_descriptions] if flow==0 else [i for i in db_table.__dict__.keys() if not i.startswith('_')]
        data = [{attr: getattr(item, attr) for attr in columns_list} for item in query_result]
        df_comext = pd.DataFrame(data)
        self.logger.info(f"Query length: {len(df_comext)}")
        # Extract EDGES
        if edges is not None:
            NUMBER_OF_EDGES_CHUNKS = len(edges) // (chunksize)
            for i in range(NUMBER_OF_EDGES_CHUNKS):
                edges_i = edges[i * chunksize : (i + 1) * chunksize]
                df_comext = self.remove_edges(df_comext, edges_i, flow)
            edges_i = edges[NUMBER_OF_EDGES_CHUNKS * chunksize : len(edges)]
            
            if len(edges_i) > 0:
                df_comext = self.remove_edges(df_comext, edges_i, flow)

        # Aggregate on DECLARANT_ISO and PARTNER_ISO and sort on criterion (VALUE or QUANTITY)
        df_comext = (
            df_comext.groupby(["DECLARANT_ISO", "PARTNER_ISO"])
            .sum()
            .reset_index()[["DECLARANT_ISO", "PARTNER_ISO", criterion]]
        )
        df_comext = df_comext.sort_values(
            criterion, ascending=False
        )

        self.logger.info(f"Aggregated query length: {len(df_comext)}")
        
        # Cut graph on bottom percentile
        df_filtered = df_comext
        if percentage is not None:
            SUM = df_filtered[criterion].sum()
            df_filtered = df_filtered[
                df_filtered[criterion].cumsum(skipna=False) / SUM * 100 <= percentage
            ]

        # Collapse Extra EU
        if collapse:
            coutry_table = orm.countryEU
            Session = sessionmaker(bind=self.engine)
            session = Session()

            query = session.query(coutry_table.CODE).filter(
                coutry_table.DAT_INI <= period,
                (coutry_table.DAT_FIN >= period) | (coutry_table.DAT_FIN.is_(None))
            )
            query_result = query.all()
            session.close()
            
            columns_list = [desc['name'] for desc in query.column_descriptions]
            data = [{attr: getattr(item, attr) for attr in columns_list} for item in query_result]
            country_eu = pd.DataFrame(data)
            
            df_comext = df_comext.merge(country_eu, how="left", left_on="PARTNER_ISO", right_on="CODE")
            df_filtered = df_filtered.merge(country_eu, how="left", left_on="PARTNER_ISO", right_on="CODE")
            df_comext["PARTNER_ISO"] = df_comext["CODE"].fillna('extraeu')
            df_filtered["PARTNER_ISO"] = df_filtered["CODE"].fillna('extraeu')
            # for average
            if flow==0:
                country_eu.rename(columns={'CODE':'CODE_2'}, inplace=True)
                df_comext = df_comext.merge(country_eu, how="left", left_on="DECLARANT_ISO", right_on="CODE_2")
                df_filtered = df_filtered.merge(country_eu, how="left", left_on="DECLARANT_ISO", right_on="CODE_2")
                df_comext["DECLARANT_ISO"] = df_comext["CODE_2"].fillna('extraeu')
                df_filtered["DECLARANT_ISO"] = df_filtered["CODE_2"].fillna('extraeu')

            df_comext = (
                df_comext.groupby(["DECLARANT_ISO", "PARTNER_ISO"])
                .sum()
                .reset_index()[["DECLARANT_ISO", "PARTNER_ISO", criterion]]
            )
            df_filtered = (
                df_filtered.groupby(["DECLARANT_ISO", "PARTNER_ISO"])
                .sum()
                .reset_index()[["DECLARANT_ISO", "PARTNER_ISO", criterion]]
            )
        
        self.logger.info(f"Final query length: {len(df_comext)}")
        self.logger.info("[TERRA] Graph table ready!")
        return df_comext, df_filtered
    

    def build_graph(self, tab4graph, tab4graph_ui, pos_ini, weight, flow, criterion):
        self.logger.info("[TERRA] Building GRAPH...")

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
        if weight == True:
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
        inv_weight = {}
        for i, j, w in edges:
            attribute[(i, j)] = {criterion: int(w * WEIGHT_SUM)}
            inv_weight[(i, j)] = {"inv_weight": int(1/w) if w!=0 else 99999999999}

        nx.set_edge_attributes(G, attribute)
        nx.set_edge_attributes(G, inv_weight)

        # Build metrics
        graph_metrics = self.build_metrics(G)

        # Keep edges for the UI, based on percentage
        edges_to_keep = tab4graph_ui[[country_from, country_to]].apply(tuple, axis=1).tolist()
        current_edges = list(G.edges())
        edges_to_remove = [edge for edge in current_edges if edge not in edges_to_keep]
        G.remove_edges_from(edges_to_remove)
        nodes_to_remove = [node for node in G.nodes() if G.degree(node) == 0]
        G.remove_nodes_from(nodes_to_remove)

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
        self.logger.info("[TERRA] GRAPH built!")
        return coord, JSON, G
    
    def width_check(self, tab4graph, max_size):
        node_size = len(set(tab4graph["DECLARANT_ISO"]).union(set(tab4graph["PARTNER_ISO"])))
        if node_size > max_size:
            self.logger.info(f"[TERRA] Graph is too wide!")
            return False
        else:
            return True


class Misc():

    def __init__(self, engine, logger):
        self.engine = engine
        self.logger = logger
    
    def jsonpos2coord(self, jsonpos):
        self.logger.info("[TERRA] JSON2COORDINATES...")
        coord = {}
        for id, x, y in pd.DataFrame.from_dict(jsonpos["nodes"])[
            ["label", "x", "y"]
        ].values:
            coord[id] = np.array([x, y])
        self.logger.info("[TERRA] JSON2COORDINATES done!")
        return coord
    
    def extract_data_table(self, product_class, period, country, partner, product, flow, criterion, transport, limit):
        self.logger.info("[TERRA] Preparing data table...")

        table, column_selected, column_excluded, query = [], [], [], ""
        
        if product_class == "cpa" and flow == 1:
            table = orm.comextImp
        elif product_class == "cpa" and flow == 2:
            table = orm.comextExp
        elif product_class == "nstr":
            table = orm.trExtraUE
        
        if criterion == 1:
            column_selected = table.VALUE_IN_EUROS
            column_excluded = table.QUANTITY_IN_KG
        elif criterion == 2:
            column_selected = table.QUANTITY_IN_KG
            column_excluded = table.VALUE_IN_EUROS
        
        columns = [
            getattr(table, attr.key)
            for attr in table.__mapper__.column_attrs
            if attr.key != column_excluded.key
        ]

        if column_selected not in columns:
            columns.append(column_selected)

        Session = sessionmaker(bind=self.engine)
        session = Session()
        query = session.query(*columns).filter(table.PERIOD == period)
        if flow is not None and product_class == "nstr":
            query = query.filter(table.FLOW == flow)
        if country is not None:
            query = query.filter(table.DECLARANT_ISO == country)
        if partner is not None:
            query = query.filter(table.PARTNER_ISO == partner)
        if product is not None:
            query = query.filter(table.PRODUCT == product)
        if transport is not None and len(transport) > 0 and product_class == "nstr":
            query = query.filter(table.TRANSPORT_MODE.in_(transport))
        query = query.limit(limit)

        query_result = query.all()
        session.close()
        
        column_names = [c.key for c in columns]

        data = [
            dict(zip(column_names, row))
            for row in query_result
        ]

        self.logger.info(f"Query length: {len(data)}")
        self.logger.info("[TERRA] Data table ready!")
        return json.dumps(data, default=str)

class TimeSeries():

    def __init__(self, engine, logger):
        self.engine = engine
        self.logger = logger

    def ts_checks_and_preps(self, c_data, dataType):
        # Format dates for sorting
        c_data['year'] = c_data['PERIOD'].astype(str).str[:4].astype(int)
        c_data['month'] = c_data['PERIOD'].astype(str).str[-2:].astype(int)

        # Sort the dataset
        c_data = c_data.sort_values(['year', 'month'])
        # Create date column
        c_data['date'] = pd.to_datetime(c_data['year'].astype(str) + '-' + c_data['month'].astype(str) + '-01')

        # Create date range for comparison
        start_date = datetime(c_data['year'].iloc[0], c_data['month'].iloc[0], 1)
        end_date = datetime(c_data['year'].iloc[-1], c_data['month'].iloc[-1], 1)
        date_full = pd.date_range(start=start_date, end=end_date, freq='MS')
        
        # Select necessary columns
        c_data = c_data[['date', 'series']]

        # Compare for missing months
        if len(c_data['date']) < len(date_full):
            db_full = pd.DataFrame({'date': date_full})
            c_data = pd.merge(c_data, db_full, how='outer')

        # Sort the dataset
        c_data.sort_values('date', inplace=True)

        # Calculate Yearly Variation Series if dataType is 1
        if dataType == 1:
            c_data['series_prev'] = c_data['series'].shift(12)
            c_data['series'] = c_data['series'] - c_data['series_prev']
            c_data = c_data.dropna(subset=['series'])
            c_data = c_data[['date','series']]
        
        dict_c_data = { "date": list(c_data["date"].dt.strftime("%Y-%m-%d")), "series": list(c_data["series"].astype(float))}

        return dict_c_data
    
    # orm_table is comextImp
    def ts(self, table_import, table_export, flow, var_cpa, country_code, partner_code, data_type, tipo_var):
        self.logger.info("[TERRA] Calculating time series...")
        try:
            flow_table, column_selection, query = [], [], ""

            if flow == 1:
                flow_table = table_import
            elif flow == 2:
                flow_table = table_export
            
            if tipo_var == 1:
                column_selection = flow_table.VALUE_IN_EUROS
            elif tipo_var == 2:
                column_selection = flow_table.QUANTITY_IN_KG
            
            Session = sessionmaker(bind=self.engine)
            session = Session()
            
            # User selects a UE country, global partner, cpa
            if partner_code!="extraeu":
                query = session.query(
                    flow_table.PERIOD, column_selection
                    ).filter(
                        flow_table.DECLARANT_ISO == country_code
                        ).filter(
                            flow_table.PARTNER_ISO == partner_code
                            ).filter(
                                flow_table.PRODUCT == var_cpa
                                )
            else :
                country_table = orm.countryEU
                query = session.query(
                    flow_table.PERIOD, func.sum(column_selection)
                    ).filter(
                        flow_table.DECLARANT_ISO == country_code
                        ).filter(
                            flow_table.PRODUCT == var_cpa
                            ).outerjoin(
                                country_table, 
                                (flow_table.PARTNER_ISO == country_table.CODE) &
                                (country_table.DAT_INI <= flow_table.PERIOD) &
                                (or_(country_table.DAT_FIN >= flow_table.PERIOD, country_table.DAT_FIN.is_(None)))
                                ).filter(
                                    country_table.CODE.is_(None) 
                                    ).group_by(
                                        flow_table.PERIOD
                                        )
            c_data = pd.read_sql(query.statement, query.session.bind)
            session.close()
            c_data.columns = ['PERIOD', 'series']

            data_result = []
            if len(c_data['series']) > 0:
                data_result = self.ts_checks_and_preps(c_data, data_type)
            else:
                data_result['series'] = []

            status_main = "01" if len(data_result) > 0 and ~any(np.isnan(val) for val in data_result['series']) else "00"
            
            res_dict = {}
            res_dict["statusMain"] = status_main
            res_dict["diagMain"] = data_result
            res_json = json.dumps(res_dict)
            self.logger.info("[TERRA] Time series ready!")
            return res_json

        except Exception as e:
            session.close()
            res_dict = {
                "statusMain": ["00"],
                "error": "Something went wrong with time series creation."
            }
            self.logger.info(f"[TERRA] Something went wrong with time series creation: {str(e)}")
            return res_dict
    

class RequestHandler():

    def __init__(self, logger):
        self.logger = logger

    def get_items(self, request, time_freq):
        criterion = py_server_params.ENDPOINT_SETTINGS["CRITERION"]
        percentage = int(request["percentage"])
        if time_freq == 'monthly':
            period = int(request["period"])
        else:
            period = str(request['period'][:-2] + "T" + request['period'][-1:])        
        position = request["position"]
        if position == None or len(position["nodes"]) == 0:
            position = None
        else:
            position = Misc(self.logger).jsonpos2coord(position)
        transport = request["transport"] # 0:Unknown 1:Sea 2:Rail 3:Road 4Air 5:Post 7:Fixed Mechanism 8:Inland Waterway 9:Self Propulsion
        flow = int(request["flow"])
        product = str(request["product"])
        weight = bool(request["weight"])

        edges = request["edges"]

        collapse = bool(request["collapse"])

        results = {
            'criterion': criterion,
            'percentage': percentage,
            'period': period,
            'position': position,
            'transport': transport,
            'flow': flow,
            'product': product,
            'weight': weight,
            'edges': edges,
            'collapse': collapse
        }

        return results
