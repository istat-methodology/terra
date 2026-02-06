from __future__ import annotations

import json
from typing import Any, Optional

import pandas as pd
from sqlalchemy import func


class TimeSeries:
    def __init__(self, engine, logger, session_factory, country_eu_table):
        self.engine = engine
        self.logger = logger
        self.Session = session_factory
        self.country_eu_table = country_eu_table

    def ts_checks_and_preps(self, c_data: pd.DataFrame, data_type: int) -> dict[str, list]:
        """
        Normalizes the time series:
          - sorts by period
          - creates monthly date index
          - fills missing months
          - optionally converts to YoY difference (data_type == 1)
        """
        # PERIOD expected as YYYYMM (int or str)
        period_str = c_data["PERIOD"].astype(str).str.zfill(6)
        c_data = c_data.copy()
        c_data["year"] = period_str.str[:4].astype(int)
        c_data["month"] = period_str.str[-2:].astype(int)

        c_data = c_data.sort_values(["year", "month"])
        c_data["date"] = pd.to_datetime(
            c_data["year"].astype(str) + "-" + c_data["month"].astype(str) + "-01",
            errors="coerce",
        )

        c_data = c_data.dropna(subset=["date"])
        c_data = c_data[["date", "series"]]

        if c_data.empty:
            return {"date": [], "series": []}

        full_range = pd.date_range(start=c_data["date"].iloc[0], end=c_data["date"].iloc[-1], freq="MS")

        if len(c_data) < len(full_range):
            c_data = pd.merge(
                c_data,
                pd.DataFrame({"date": full_range}),
                how="outer",
                on="date",
            )

        c_data = c_data.sort_values("date")

        # YoY difference
        if data_type == 1:
            c_data["series_prev"] = c_data["series"].shift(12)
            c_data["series"] = c_data["series"] - c_data["series_prev"]
            c_data = c_data.dropna(subset=["series"])[["date", "series"]]

        # Convert to JSON-friendly types
        return {
            "date": list(c_data["date"].dt.strftime("%Y-%m-%d")),
            "series": list(c_data["series"].astype(float)),
        }

    def ts(
        self,
        table_import,
        table_export,
        flow: int,
        var_cpa: str,
        country_code: str,
        partner_code: str,
        data_type: int,
        var_type: int,
    ) -> str:
        """
        Returns JSON string:
          {"statusMain": "01"|"00", "diagMain": {"date":[...], "series":[...]}}
        """
        self.logger.info("[TERRA] Calculating time series...")

        if flow not in (1, 2):
            raise ValueError("Invalid flow (expected 1=import, 2=export)")
        if var_type not in (1, 2):
            raise ValueError("Invalid var_type (expected 1=VALUE, 2=QUANTITY)")
        if data_type not in (1, 2):
            # 0 = level, 1 = YoY difference (as per your current logic)
            raise ValueError("Invalid data_type (expected 0 or 1)")

        flow_table = table_import if flow == 1 else table_export
        column = flow_table.VALUE_IN_EUROS if var_type == 1 else flow_table.QUANTITY_IN_KG

        with self.Session() as session:
            if partner_code != "extraeu":
                query = (
                    session.query(
                        flow_table.PERIOD.label("PERIOD"),
                        column.label("series"),
                    )
                    .filter(
                        flow_table.DECLARANT_ISO == country_code,
                        flow_table.PARTNER_ISO == partner_code,
                        flow_table.PRODUCT == var_cpa,
                    )
                )
            else:
                t = self.country_eu_table
                query = (
                    session.query(
                        flow_table.PERIOD.label("PERIOD"),
                        func.sum(column).label("series"),
                    )
                    .filter(
                        flow_table.DECLARANT_ISO == country_code,
                        flow_table.PRODUCT == var_cpa,
                    )
                    .outerjoin(
                        t,
                        (flow_table.PARTNER_ISO == t.CODE)
                        & (t.DAT_INI <= flow_table.PERIOD)
                        & ((t.DAT_FIN >= flow_table.PERIOD) | (t.DAT_FIN.is_(None))),
                    )
                    .filter(t.CODE.is_(None))
                    .group_by(flow_table.PERIOD)
                )

            df = pd.read_sql(query.statement, query.session.bind)

        # Already labeled as PERIOD/series, but keep defensive rename
        if list(df.columns) != ["PERIOD", "series"]:
            df.columns = ["PERIOD", "series"]

        if df.empty:
            return json.dumps({"statusMain": "00", "diagMain": {"date": [], "series": []}})

        diag = self.ts_checks_and_preps(df, data_type)

        # robust NaN check (handles None too)
        series = diag.get("series", [])
        ok = len(series) > 0 and not pd.isna(series).any()

        status = "01" if ok else "00"

        self.logger.info("[TERRA] Time series ready!")
        return json.dumps({"statusMain": status, "diagMain": diag})
