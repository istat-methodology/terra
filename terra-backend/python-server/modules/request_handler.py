from __future__ import annotations

from typing import Any, Mapping, Optional

import numpy as np
import pandas as pd

from .request_models import GraphRequest


def jsonpos2coord(jsonpos: Mapping[str, Any]) -> dict[str, np.ndarray]:
    """
    Convert UI node positions into a dict: {label: np.array([x, y])}.
    Expected input format:
      {"nodes": [{"label": "...", "x": 0.1, "y": 0.2}, ...]}
    """
    nodes = jsonpos.get("nodes") or []
    if not nodes:
        return {}

    df = pd.DataFrame.from_dict(nodes)
    # Defensive: allow missing columns without exploding with KeyError
    if not {"label", "x", "y"}.issubset(df.columns):
        return {}

    coord: dict[str, np.ndarray] = {}
    for label, x, y in df[["label", "x", "y"]].values:
        coord[str(label)] = np.array([float(x), float(y)], dtype=float)
    return coord


class RequestHandler:
    """
    Parse incoming request payloads into strongly-typed request objects.
    Keeps endpoints thin and centralizes input normalization.
    """

    def __init__(self, logger, *, criterion: str):
        self.logger = logger
        self.criterion = criterion

    def get_graph_items(self, request: Mapping[str, Any], time_freq: str) -> GraphRequest:
        # percentage can be None
        percentage_raw = request.get("percentage")
        percentage = int(percentage_raw) if percentage_raw is not None else None

        period = self._parse_period(request.get("period"), time_freq)

        position_raw = request.get("position")
        if not position_raw or not (position_raw.get("nodes") if isinstance(position_raw, dict) else None):
            position = None
        else:
            position = jsonpos2coord(position_raw)

        flow_raw = request.get("flow")
        if flow_raw is None:
            raise ValueError("Missing required field: flow")
        flow = int(flow_raw)

        return GraphRequest(
            criterion=self.criterion,
            percentage=percentage,
            period=period,
            position=position,
            transport=request.get("transport") or [],
            flow=flow,
            product=request.get("product"),
            weight=bool(request.get("weight")),
            edges=request.get("edges"),
            collapse=bool(request.get("collapse")),
        )

    def _parse_period(self, period_raw: Any, time_freq: str) -> Any:
        """
        Monthly: expects YYYYMM (int or str), returns int.
        Quarterly: expects YYYYMM (e.g. '202401'), returns 'YYYYTq' (e.g. '2024T1').
        """
        if period_raw is None:
            return None

        p = str(period_raw).strip()

        if len(p) != 6 or not p.isdigit():
            raise ValueError(f"Invalid period format (expected YYYYMM): {period_raw}")

        year = p[:4]
        month = int(p[4:6])

        if time_freq == "monthly":
            return int(p)

        # quarterly
        if not 1 <= month <= 12:
            raise ValueError(f"Invalid month in period: {period_raw}")

        quarter = (month - 1) // 3 + 1
        return f"{year}T{quarter}"

