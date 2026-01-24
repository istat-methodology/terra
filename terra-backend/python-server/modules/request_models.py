from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class GraphRequest:
    criterion: str
    percentage: Optional[int]
    period: Any
    position: Optional[dict]
    transport: list
    flow: int
    product: Optional[str]
    weight: bool
    edges: Optional[list]
    collapse: bool
