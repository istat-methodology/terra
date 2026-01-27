from __future__ import annotations

import json
import math
import random
from typing import Any, Optional

import numpy as np
import pandas as pd
import networkx as nx
from sqlalchemy import func, union_all, or_
from networkx.readwrite import json_graph
from distinctiveness.dc import distinctiveness


class GraphEngine:
    def __init__(self, engine, logger, session_factory, *, country_eu_table):
        self.engine = engine
        self.logger = logger
        self.Session = session_factory
        self.country_eu_table = country_eu_table

    # -------------------------
    # Helpers
    # -------------------------

    @staticmethod
    def _has_transport_mode(db_table) -> bool:
        # SQLAlchemy ORM models have attributes for columns
        return hasattr(db_table, "TRANSPORT_MODE")

    @staticmethod
    def _normalize_edge(edge: dict[str, Any], flow: int) -> tuple[str, str, Any]:
        """
        Returns (declarant_iso, partner_iso, exclude)
        Flow convention matches legacy behavior.
        """
        if flow == 1:
            partner_iso = edge["from"]
            declarant_iso = edge["to"]
        else:
            partner_iso = edge["to"]
            declarant_iso = edge["from"]
        return str(declarant_iso), str(partner_iso), edge.get("exclude")

    # -------------------------
    # Edge filtering (SAFE)
    # -------------------------

    def remove_edges(
        self,
        df: pd.DataFrame,
        edges: list[dict[str, Any]],
        flow: int,
        *,
        has_transport_mode: bool,
    ) -> pd.DataFrame:
        """
        Remove edges from df without df.query() (safer).
        If exclude contains -99 => remove whole edge (all transports)
        Else remove only rows where TRANSPORT_MODE is in exclude list (if available)
        """
        if df.empty or not edges:
            return df

        keep = pd.Series(True, index=df.index)

        for edge in edges:
            declarant_iso, partner_iso, exclude = self._normalize_edge(edge, flow)
            edge_mask = (df["DECLARANT_ISO"] == declarant_iso) & (df["PARTNER_ISO"] == partner_iso)

            if exclude is None:
                continue

            # remove entire edge
            if (isinstance(exclude, str) and "-99" in exclude) or (isinstance(exclude, list) and -99 in exclude):
                keep &= ~edge_mask
                continue

            # transport-specific removal only if dataset supports TRANSPORT_MODE
            if has_transport_mode and "TRANSPORT_MODE" in df.columns:
                exclude_vals = exclude
                if isinstance(exclude, str):
                    # try parse JSON list like "[1,2]"
                    try:
                        exclude_vals = json.loads(exclude)
                    except Exception:
                        exclude_vals = exclude

                if isinstance(exclude_vals, (list, tuple, set)):
                    keep &= ~(edge_mask & df["TRANSPORT_MODE"].isin(list(exclude_vals)))

        return df.loc[keep]

    # -------------------------
    # Metrics
    # -------------------------

    def build_metrics(self, graph: nx.DiGraph) -> dict[str, Any]:
        self.logger.info("[TERRA] Calculating graph metrics...")
        metrics = {
            "density": nx.density(graph),
            "degree": dict(graph.degree()),
            "degree_weighted": dict(graph.degree(weight="weight")),
            "out_degree": dict(graph.out_degree()),
            "out_degree_weighted": dict(graph.out_degree(weight="weight")),
            "in_degree": dict(graph.in_degree()),
            "in_degree_weighted": dict(graph.in_degree(weight="weight")),
            "closeness_weighted": nx.closeness_centrality(graph, distance="inv_weight"),
            "betweenness_weighted": nx.betweenness_centrality(graph, weight="inv_weight"),
            "distinctiveness": distinctiveness(graph.to_undirected(), alpha=1, normalize=True, measures=["D1"])["D1"],
        }
        self.logger.info("[TERRA] Graph metrics ready!")
        return metrics

    # -------------------------
    # DB extraction
    # -------------------------

    def extract_graph_table(
        self,
        *,
        chunksize: int,
        period: Any,
        percentage: Optional[int],
        transport: list[int],
        flow: int,
        product: Optional[str],
        criterion: str,
        edges: Optional[list[dict[str, Any]]],
        db_table,
        collapse: bool,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Returns:
          - df_full: aggregated edges with weights
          - df_ui: subset based on percentage cut (used for UI)
        """
        self.logger.info("[TERRA] Preparing graph table...")

        has_tm = self._has_transport_mode(db_table)

        with self.Session() as session:
            if flow == 0:
                # average across import/export (legacy behavior)
                queries = []
                for f in (1, 2):
                    cols = [
                        db_table.DECLARANT_ISO if f == 2 else db_table.PARTNER_ISO.label("DECLARANT_ISO"),
                        db_table.PARTNER_ISO if f == 2 else db_table.DECLARANT_ISO.label("PARTNER_ISO"),
                        func.sum(getattr(db_table, criterion)).label("VAL"),
                    ]

                    q = session.query(*cols).filter(db_table.FLOW == f)

                    if period is not None:
                        q = q.filter(db_table.PERIOD == period)
                    if has_tm and transport:
                        q = q.filter(db_table.TRANSPORT_MODE.in_(transport))
                    if product is not None and hasattr(db_table, "PRODUCT"):
                        q = q.filter(db_table.PRODUCT == product)
                    
                    group_cols = [db_table.DECLARANT_ISO, db_table.PARTNER_ISO]
                    
                    q = q.group_by(*group_cols)

                    queries.append(q)

                combined = union_all(*queries).alias("A")

                # --- CORREZIONE QUI SOTTO ---
                
                # 1. Definiamo le colonne su cui raggruppare (quelle NON aggregate)
                outer_group_cols = [
                    combined.c.DECLARANT_ISO,
                    combined.c.PARTNER_ISO
                ]
                
                # 2. Definiamo le colonne da selezionare
                select_cols = [
                    combined.c.DECLARANT_ISO,
                    combined.c.PARTNER_ISO,
                    func.avg(combined.c.VAL).label(criterion),
                ]
                
                # 4. Aggiungiamo .group_by(*outer_group_cols) alla query finale
                query = session.query(*select_cols).group_by(*outer_group_cols)
            else:
                # select only what we need
                select_cols = [
                    db_table.DECLARANT_ISO.label("DECLARANT_ISO"),
                    db_table.PARTNER_ISO.label("PARTNER_ISO"),
                    getattr(db_table, criterion).label(criterion),
                ]
                if has_tm:
                    select_cols.append(db_table.TRANSPORT_MODE.label("TRANSPORT_MODE"))

                query = session.query(*select_cols).filter(db_table.FLOW == flow)

                if period is not None:
                    query = query.filter(db_table.PERIOD == period)
                if has_tm and transport:
                    query = query.filter(db_table.TRANSPORT_MODE.in_(transport))
                if product is not None and hasattr(db_table, "PRODUCT"):
                    query = query.filter(db_table.PRODUCT == product)
                if product is not None and hasattr(db_table, "PRODUCT_NSTR"):
                    query = query.filter(db_table.PRODUCT_NSTR == product)

            df = pd.read_sql(query.statement, query.session.bind)

        if has_tm and "TRANSPORT_MODE" not in df.columns:
            df["TRANSPORT_MODE"] = np.nan

        self.logger.info(f"Query length: {len(df)}")

        # Remove edges in chunks (if any)
        if edges:
            for i in range(0, len(edges), chunksize):
                df = self.remove_edges(df, edges[i:i + chunksize], flow, has_transport_mode=has_tm)

        # Aggregate and sort
        df = df.groupby(["DECLARANT_ISO", "PARTNER_ISO"]).sum(numeric_only=True).reset_index()
        df = df[["DECLARANT_ISO", "PARTNER_ISO", criterion]].sort_values(criterion, ascending=False)

        self.logger.info(f"Aggregated query length: {len(df)}")

        df_ui = df
        if percentage is not None:
            total = df_ui[criterion].sum()
            if total > 0:
                df_ui = df_ui[df_ui[criterion].cumsum() / total * 100 <= percentage]

        if collapse and period is not None:
            df, df_ui = self._collapse_extraeu(df, df_ui, period, criterion, flow)

        self.logger.info(f"Final query length: {len(df)}")
        self.logger.info("[TERRA] Graph table ready!")
        return df, df_ui

    def _collapse_extraeu(self, df: pd.DataFrame, df_ui: pd.DataFrame, period: Any, criterion: str, flow: int):
        with self.Session() as session:
            t = self.country_eu_table
            q = session.query(t.CODE).filter(
                t.DAT_INI <= period,
                or_(t.DAT_FIN >= period, t.DAT_FIN.is_(None)),
            )
            codes = pd.DataFrame(q.all(), columns=["CODE"])

        df = df.merge(codes, how="left", left_on="PARTNER_ISO", right_on="CODE")
        df_ui = df_ui.merge(codes, how="left", left_on="PARTNER_ISO", right_on="CODE")

        df["PARTNER_ISO"] = df["CODE"].fillna("extraeu")
        df_ui["PARTNER_ISO"] = df_ui["CODE"].fillna("extraeu")

        if flow == 0:
            codes2 = codes.rename(columns={"CODE": "CODE_2"})
            df = df.merge(codes2, how="left", left_on="DECLARANT_ISO", right_on="CODE_2")
            df_ui = df_ui.merge(codes2, how="left", left_on="DECLARANT_ISO", right_on="CODE_2")
            df["DECLARANT_ISO"] = df["CODE_2"].fillna("extraeu")
            df_ui["DECLARANT_ISO"] = df_ui["CODE_2"].fillna("extraeu")

        df = df.groupby(["DECLARANT_ISO", "PARTNER_ISO"]).sum(numeric_only=True).reset_index()
        df_ui = df_ui.groupby(["DECLARANT_ISO", "PARTNER_ISO"]).sum(numeric_only=True).reset_index()
        df = df[["DECLARANT_ISO", "PARTNER_ISO", criterion]]
        df_ui = df_ui[["DECLARANT_ISO", "PARTNER_ISO", criterion]]
        return df, df_ui

    # -------------------------
    # Graph build
    # -------------------------

    def build_graph(
        self,
        tab4graph: pd.DataFrame,
        tab4graph_ui: pd.DataFrame,
        pos_ini: Optional[dict[str, np.ndarray]],
        weight: bool,
        flow: int,
        criterion: str,
    ):
        self.logger.info("[TERRA] Building GRAPH...")

        G = nx.DiGraph()
        country_from, country_to = ("PARTNER_ISO", "DECLARANT_ISO") if flow == 1 else ("DECLARANT_ISO", "PARTNER_ISO")

        if weight:
            total = float(tab4graph[criterion].sum())
            edges = [
                (i, j, (float(w) / total if total else 0.0))
                for i, j, w in tab4graph[[country_from, country_to, criterion]].values
            ]
        else:
            total = 1.0
            edges = [(i, j, 1.0) for i, j in tab4graph[[country_from, country_to]].values]

        G.add_weighted_edges_from(edges)

        # Edge attributes
        attr = {(i, j): {criterion: int(w * total)} for i, j, w in edges}
        inv = {(i, j): {"inv_weight": (1.0 / w if w else 1e12)} for i, j, w in edges}
        nx.set_edge_attributes(G, attr)
        nx.set_edge_attributes(G, inv)

        metrics = self.build_metrics(G)

        # Keep only UI edges
        edges_to_keep = tab4graph_ui[[country_from, country_to]].apply(tuple, axis=1).tolist()
        G.remove_edges_from([e for e in list(G.edges()) if e not in edges_to_keep])
        G.remove_nodes_from([n for n in G.nodes() if G.degree(n) == 0])

        GG = json_graph.node_link_data(G)

        # layout init: use pos_ini from client if available, else stable random
        if pos_ini:
            pos0 = pos_ini
        else:
            random.seed(88)
            pos0 = {n["id"]: np.array([random.random(), random.random()]) for n in GG["nodes"]}

        try:
            k_layout = 5
            denom = math.sqrt(max(G.order(), 1))
            coord = nx.spring_layout(G, k=k_layout / denom, pos=pos0, iterations=200)
            coord = nx.spring_layout(G, k=k_layout / denom, pos=coord, iterations=50)
        except Exception:
            return None, None, None

        df_coord = pd.DataFrame.from_dict(coord, orient="index")
        df_coord.columns = ["x", "y"]

        df_nodes = pd.DataFrame(GG["nodes"])
        df_nodes.columns = ["label"]
        df_nodes["id"] = np.arange(df_nodes.shape[0])
        df_nodes = df_nodes[["id", "label"]]

        out = pd.merge(df_nodes, df_coord, left_on="label", right_index=True)
        dict_nodes = out.T.to_dict().values()

        dfe = pd.DataFrame(GG["edges"])[["source", "target", "weight", criterion]]
        res = dfe.set_index("source").join(out[["label", "id"]].set_index("label"), on="source", how="left")
        res.columns = ["target", "source_id", "weight", criterion]
        res2 = res.set_index("target").join(out[["label", "id"]].set_index("label"), on="target", how="left")
        res2.columns = ["weight", criterion, "from", "to"]
        res2.reset_index(drop=True, inplace=True)
        dict_edges = res2.T.to_dict().values()

        payload = {"nodes": list(dict_nodes), "edges": list(dict_edges), "metrics": metrics}
        self.logger.info("[TERRA] GRAPH built!")
        return coord, json.dumps(payload), G

    def width_check(self, tab4graph: pd.DataFrame, max_size: int) -> bool:
        node_size = len(set(tab4graph["DECLARANT_ISO"]).union(set(tab4graph["PARTNER_ISO"])))
        if node_size > max_size:
            self.logger.info("[TERRA] Graph is too wide!")
            return False
        return True
