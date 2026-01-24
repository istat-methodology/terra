from __future__ import annotations

import json
from typing import Any, Optional

from resources import py_server_params
from modules import orm


class Misc:
    def __init__(self, engine, logger, session_factory):
        self.engine = engine
        self.logger = logger
        self.Session = session_factory

    def extract_data_table(
        self,
        product_class: str,
        period: int | str,
        country: Optional[str],
        flow: Optional[int],
        criterion: int,
        product: Optional[str] = None,
        partner: Optional[str] = None,
        transport: Optional[list[int]] = None,
    ) -> str:
        """
        Returns a JSON string containing rows from the selected table, limited by DOWNLOAD_LIMIT.
        product_class:
          - 'cpa' uses comextImp/comextExp based on flow (1=import, 2=export)
          - 'nstr' uses trExtraUE (flow can be None or 1/2)
        criterion:
          - 1 => VALUE_IN_EUROS
          - 2 => QUANTITY_IN_KG
        """
        self.logger.info("[TERRA] Preparing data table...")

        table = self._select_table(product_class, flow)

        if criterion == 1:
            column_selected = table.VALUE_IN_EUROS
            column_excluded = table.QUANTITY_IN_KG
        elif criterion == 2:
            column_selected = table.QUANTITY_IN_KG
            column_excluded = table.VALUE_IN_EUROS
        else:
            raise ValueError("Invalid criterion (expected 1=VALUE, 2=QUANTITY)")

        columns = [
            getattr(table, attr.key)
            for attr in table.__mapper__.column_attrs
            if attr.key != column_excluded.key
        ]
        if column_selected not in columns:
            columns.append(column_selected)

        with self.Session() as session:
            q = session.query(*columns).filter(table.PERIOD == period)

            # trExtraUE supports FLOW, comext tables are already split
            if product_class == "nstr" and flow is not None:
                q = q.filter(table.FLOW == flow)

            if country is not None:
                q = q.filter(table.DECLARANT_ISO == country)
            if partner is not None:
                q = q.filter(table.PARTNER_ISO == partner)
            if product is not None:
                q = q.filter(table.PRODUCT == product)
            if transport and product_class == "nstr":
                q = q.filter(table.TRANSPORT_MODE.in_(transport))

            q = q.limit(py_server_params.ENDPOINT_SETTINGS["DOWNLOAD_LIMIT"])
            rows = q.all()

        column_names = [c.key for c in columns]
        data = [dict(zip(column_names, row)) for row in rows]

        self.logger.info(f"Query length: {len(data)}")
        self.logger.info("[TERRA] Data table ready!")
        return json.dumps(data, default=str)

    def _select_table(self, product_class: str, flow: Optional[int]):
        if product_class == "cpa":
            if flow == 1:
                return orm.comextImp
            if flow == 2:
                return orm.comextExp
            raise ValueError("For product_class='cpa', flow must be 1 (import) or 2 (export).")

        if product_class == "nstr":
            return orm.trExtraUE

        raise ValueError("Invalid product_class (expected 'cpa' or 'nstr').")
