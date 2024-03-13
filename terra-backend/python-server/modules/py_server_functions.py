import pandas as pd
import numpy as np
import os
import logging
import networkx as nx
from opencensus.ext.azure.log_exporter import AzureLogHandler

class PyServerLogger:
    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def get_logger():
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        return logging.getLogger(__name__)


class ApplicationInsightsSetup:
    def __init__(self):
        raise NotImplementedError()
    
    @staticmethod
    def is_application_insight_configured():
        return (
            os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY") != None
            or os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING") != None
        )

    @staticmethod    
    def ai_callback_function(envelope):
        if os.getenv("CLOUD_ROLE") != None:
            envelope.tags["ai.cloud.role"] = os.getenv("CLOUD_ROLE")
    
    @staticmethod
    def azure_setup(logger):
        if ApplicationInsightsSetup.is_application_insight_configured():
            log_handler = AzureLogHandler()
            log_handler.add_telemetry_processor(ApplicationInsightsSetup.ai_callback_function)
            logger.addHandler(log_handler)
            return True
        else:
            logger.warning("Applicaiton insights is not configured.")
            return False


class DataLoading:
    def __init__(self, logger, paths: dict, labels: dict, column_names: dict, dtypes: dict):
        try:
            self.logger = logger
            self.logger_intro = "[TERRA]"
            self.product_label = labels["Product"]
            self.paths = paths
            self.date_label = labels["Date"]
            self.column_names = column_names
            self.dtypes = dtypes

        except Exception as e:
            logger.error(f"Error initializing DataLoading class: {str(e)}")

    def load_data(self, filename, product_digits: int):
        try:
            self.logger.info(f"{self.logger_intro} Loading {filename}...")

            column_names = self.column_names[filename]
            dtypes = self.dtypes[filename]
            df = pd.read_csv(f"{self.paths[filename]}", low_memory=False, dtype=dtypes)
            df = df[list(column_names.keys())]
            df.columns = list(column_names.values())
            df[self.date_label] = np.int32(df[self.date_label].apply(lambda x: str(x).replace("T", "0")))
            if product_digits is not None:
                df = df.loc[df[self.product_label].apply(lambda x: len(str(x).strip()) == product_digits)]
            
            n_records = df.shape[0]
            min_date = df[self.date_label].min()
            max_date = df[self.date_label].max()

            self.logger.info(f"{self.logger_intro} {filename} loaded!")
            self.logger.info(f"{self.logger_intro} {filename} contains {n_records} records")
            self.logger.info(f"{self.logger_intro} {filename} time range: {min_date} - {max_date}")

            info = {
                "n_records" : n_records,
                "min_date"  : min_date,
                "max_date"  : max_date
            }

            return df, info
        
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")


class UtilityFunctions:
    def __init__(self, logger, labels):
        self.logger = logger
        self.logger_intro = "[TERRA]"
        self.product_label = labels["Product"]
        self.date_label = labels["Date"]
        self.flow_label = labels["Flow"]
        self.transport_mode_label = labels["Transport Mode"]
        self.declarant_label = labels["Declarant"]
        self.partner_label = labels["Partner"]

    def build_edges_query(self, edges: list, flow: int):
        query = []
        for edge in edges:
            partner_iso = edge["from"] if flow == 1 else edge["to"]
            declarant_iso = edge["to"] if flow == 1 else edge["from"]
            exclude = str(edge["exclude"])

            if "-99" in exclude:
                query.append(f"(DECLARANT_ISO == '{declarant_iso}' & PARTNER_ISO == '{partner_iso}')")
            else:
                query.append(f"((DECLARANT_ISO == '{declarant_iso}' & PARTNER_ISO == '{partner_iso}' & TRANSPORT_MODE in {exclude}))")
        return f"not ({('|').join(query)})"
    
    def remove_edges(self, df_comext, edges, flow):
        query = self.build_edges_query(edges, flow)
        df = df_comext.query(query)
        return df
    
    def build_metrics(self, graph):
        self.logger.info(f"{self.logger_intro} Calculating graph metrics...")

        in_degree_centrality = nx.in_degree_centrality(graph)
        graph_metrics, vulnerability = {}, {}

        for node, in_degree_value in in_degree_centrality.items():
            vulnerability[node] = (1 - in_degree_value) if in_degree_value != 0 else 0
        
        graph_metrics = {
            "degree_centrality": nx.degree_centrality(graph),
            "density": nx.density(graph),
            "vulnerability": vulnerability,
            "exportation strength": {
                node: out_degree for node, out_degree in graph.out_degree(weight="weight")
            },
            "hubness": nx.closeness_centrality(graph.to_undirected())
        }
        self.logger.info(f"{self.logger_intro} Graph metrics ready!")

        return graph_metrics

    def extract_graph_table(self, period, percentage, transports, flow, product, criterion, selected_edges, df_comext, chunk_size):
        self.logger.info(f"{self.logger_intro} Preparing graph table...")

        df = df_comext.loc[df_comext[self.flow_label] == flow]
        if period is not None:
            df = df.loc[df[self.date_label] == np.int32(period)]
        
        df = df.loc[df[self.date_label] == np.int32(period)] if period else df
        df = df.loc[df[self.transport_mode_label].isin(transports)] if transports else df
        df = df.loc[df[self.product_label] == np.int32(period)] if product else df

        if selected_edges is not None:
            number_of_edges_chunk = len(selected_edges) // chunk_size
            for n_edges in range(number_of_edges_chunk):
                selected_edges_chunk = selected_edges_chunk[n_edges * chunk_size : (n_edges + 1) * chunk_size]
                df = self.remove_edges(df, selected_edges_chunk, flow)
            selected_edges_chunk = selected_edges[number_of_edges_chunk * chunk_size : len(selected_edges)]
            df = self.remove_edges(df, selected_edges_chunk, flow) if len(selected_edges_chunk) > 0 else df
        
        df = (df.groupby([self.declarant_label, self.partner_label]).sum().reset_index()[[self.declarant_label, self.partner_label, criterion]])
        df.sort_values(criterion, ascending=False, inplace=True)

        if percentage is not None:
            summation = df[criterion].sum()
            df = df.loc[df[criterion].cumsum(skipna=False) * 100 / summation < percentage]
        
        self.logger.info("[TERRA] Graph table ready")

        return df