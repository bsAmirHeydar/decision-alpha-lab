from __future__ import annotations

import math
from typing import Any


def log_move(high: Any, low: Any) -> float:
    move = abs(float(high) - float(low))
    if move <= 0:
        return 0.0
    return float(math.log(move))


def in_zone(high: Any, low: Any, lower: float | None, upper: float | None) -> bool:
    if lower is None or upper is None:
        return False
    return not (float(high) < float(lower) or float(low) > float(upper))


def build_territory(node_price: float, extreme: float, zone_ratio: float) -> tuple[float, float]:
    distance = abs(float(extreme) - float(node_price))
    half_width = distance * (1.0 - float(zone_ratio))
    return float(node_price) - half_width, float(node_price) + half_width


def hunt_breached(node_type: str, node_price: float, high: Any, low: Any) -> bool:
    node_type = str(node_type).upper()
    if node_type == "LOW":
        return float(low) < float(node_price)
    if node_type == "HIGH":
        return float(high) > float(node_price)
    raise ValueError(f"Unknown node_type: {node_type!r}")


def hunt_price(node_type: str, node_price: float, high: Any, low: Any) -> float:
    node_type = str(node_type).upper()
    if node_type == "LOW":
        return min(float(low), float(node_price))
    if node_type == "HIGH":
        return max(float(high), float(node_price))
    raise ValueError(f"Unknown node_type: {node_type!r}")
