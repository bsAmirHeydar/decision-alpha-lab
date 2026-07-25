from __future__ import annotations
from dataclasses import dataclass
from .models import BrokerProfile

@dataclass(frozen=True)
class BrokerFeasibility:
    feasible: bool
    reason_codes: tuple[str, ...]
    normalized_volume: float


def normalize_volume(volume: float, broker: BrokerProfile) -> float:
    steps = round((volume - broker.minimum_volume) / broker.volume_step)
    normalized = broker.minimum_volume + max(0, steps) * broker.volume_step
    return round(min(broker.maximum_volume, max(broker.minimum_volume, normalized)), 10)


def evaluate_broker_feasibility(action_class: str, order_volume: float, source_row: dict, broker: BrokerProfile) -> BrokerFeasibility:
    if action_class in {"skip", "abstain"}:
        return BrokerFeasibility(True, ("non_order_action",), 0.0)
    reasons: list[str] = []
    normalized = normalize_volume(order_volume, broker)
    if not broker.minimum_volume <= order_volume <= broker.maximum_volume:
        reasons.append("volume_outside_bounds")
    if "market" not in broker.allowed_order_types:
        reasons.append("market_order_not_allowed")
    entry = source_row.get("entry_price")
    stop = source_row.get("stop_price")
    if entry is not None and stop is not None and abs(float(entry) - float(stop)) < broker.stop_level_points:
        reasons.append("stop_level_violation")
    return BrokerFeasibility(not reasons, tuple(sorted(reasons)), normalized)
