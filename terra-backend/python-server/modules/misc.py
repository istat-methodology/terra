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
        period: int | str | None,
        country: Optional[str],
        flow: Optional[int],
        criterion: int,
        period_from: int | str | None = None,
        period_to: int | str | None = None,
        product: Optional[str] = None,
        partner: Optional[str] = None,
        transport: Optional[list[int]] = None,
    ) -> str:
        """
        Returns rows for either one period or an inclusive period range.

        Raises ValueError instead of silently truncating results exceeding
        DOWNLOAD_LIMIT.
        """
        self.logger.info("[TERRA] Preparing data table...")

        table = self._select_table(product_class, flow)
        period_start, period_end = self._resolve_period_range(
            period=period,
            period_from=period_from,
            period_to=period_to,
        )

        if criterion == 0:
            column_selected = [
                table.VALUE_IN_EUROS,
                table.QUANTITY_IN_KG,
            ]
            column_excluded = []
            
            #TO REMOVE WHEN CPA QTY IS FIXED
            if product_class == "cpa":
                column_selected = [table.VALUE_IN_EUROS]
                column_excluded = [table.QUANTITY_IN_KG]
        
        elif criterion == 1:
            column_selected = [table.VALUE_IN_EUROS]
            column_excluded = [table.QUANTITY_IN_KG]

        elif criterion == 2:
            column_selected = [table.QUANTITY_IN_KG]
            column_excluded = [table.VALUE_IN_EUROS]
            
            #TO REMOVE WHEN CPA QTY IS FIXED
            if product_class == "cpa":
                raise ValueError(
                    "Invalid criterion for CPA data (expected 0=ALL, 1=VALUE)"
                )
        else:
            raise ValueError(
                "Invalid criterion (expected 0=ALL, 1=VALUE, 2=QUANTITY)"
            )

        columns = [
            getattr(table, attr.key)
            for attr in table.__mapper__.column_attrs
            if attr.key not in {col.key for col in column_excluded}
        ]

        for col in column_selected:
            if col not in columns:
                columns.append(col)

        with self.Session() as session:
            q = session.query(*columns).filter(
                table.PERIOD.between(period_start, period_end)
            )

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

            q = q.order_by(
                table.PERIOD,
                table.DECLARANT_ISO,
                table.PARTNER_ISO,
                table.PRODUCT,
            )
            download_limit = py_server_params.ENDPOINT_SETTINGS["DOWNLOAD_LIMIT"]
            q = q.limit(download_limit + 1)
            rows = q.all()

        if len(rows) > download_limit:
            raise ValueError(
                f"The selected filters exceed the download limit of {download_limit} rows. "
                "Please narrow the period or the other filters."
            )

        column_names = [c.key for c in columns]
        data = [dict(zip(column_names, row)) for row in rows]

        self.logger.info(f"Query length: {len(data)}")
        self.logger.info("[TERRA] Data table ready!")
        return json.dumps(data, default=str)

    @staticmethod
    def _resolve_period_range(
        period: int | str | None,
        period_from: int | str | None,
        period_to: int | str | None,
    ) -> tuple[int, int]:
        has_period = period is not None
        has_period_from = period_from is not None
        has_period_to = period_to is not None

        if has_period and (has_period_from or has_period_to):
            raise ValueError(
                "Use either 'period' or 'period_from'/'period_to', not both."
            )

        if has_period:
            parsed_period = Misc._parse_period(period, "period")
            return parsed_period, parsed_period

        if not has_period_from or not has_period_to:
            raise ValueError(
                "Provide 'period' or both 'period_from' and 'period_to'."
            )

        parsed_from = Misc._parse_period(period_from, "period_from")
        parsed_to = Misc._parse_period(period_to, "period_to")
        if parsed_from > parsed_to:
            raise ValueError("'period_from' must not be later than 'period_to'.")

        return parsed_from, parsed_to

    @staticmethod
    def _parse_period(value: int | str, field_name: str) -> int:
        period = str(value).strip()
        if len(period) != 6 or not period.isdigit():
            raise ValueError(f"'{field_name}' must use the YYYYMM format.")

        month = int(period[4:])
        if month < 1 or month > 12:
            raise ValueError(f"'{field_name}' contains an invalid month.")

        return int(period)

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
