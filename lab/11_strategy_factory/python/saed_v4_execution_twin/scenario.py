from __future__ import annotations
from typing import Any
from .canonical import deterministic_unit_interval
from .broker import evaluate_broker_feasibility
from .latency import realize_latency
from .queue import realize_queue
from .hazard import fill_probability
from .impact import market_impact_points
from .adverse import adverse_selection_points
from .lifecycle import build_lifecycle


def _risk_points(source_row: dict[str, Any]) -> float:
    entry, stop = source_row.get("entry_price"), source_row.get("stop_price")
    if entry is not None and stop is not None and abs(float(entry) - float(stop)) > 0:
        return abs(float(entry) - float(stop))
    gross_points, gross_r = abs(float(source_row.get("gross_points", 0.0))), abs(float(source_row.get("gross_r", 0.0)))
    if gross_r > 1e-12:
        return max(1e-12, gross_points / gross_r)
    return 1.0


def simulate_scenario(source_row: dict[str, Any], cube: dict[str, Any], profile, scenario) -> dict[str, Any]:
    action_class = str(source_row["action_class"])
    row_hash = str(source_row["row_hash"])
    source_spread = float(source_row.get("cost", {}).get("entry_spread_points", 0.0)) + float(source_row.get("cost", {}).get("exit_spread_points", 0.0))
    latency = realize_latency(row_hash, scenario, profile)
    queue = realize_queue(row_hash, scenario, profile)
    broker = evaluate_broker_feasibility(action_class, profile.order_volume, source_row, profile.broker)
    probability = 0.0 if action_class in {"skip", "abstain"} else fill_probability(source_spread, scenario, profile, latency, queue)
    reject_draw = deterministic_unit_interval(row_hash, scenario.scenario_id, "reject")
    fill_draw = deterministic_unit_interval(row_hash, scenario.scenario_id, "fill")
    if action_class in {"skip", "abstain"}:
        status, fill_fraction = "non_order", 0.0
    elif not broker.feasible:
        status, fill_fraction = "broker_infeasible", 0.0
    elif reject_draw < scenario.rejection_threshold:
        status, fill_fraction = "rejected", 0.0
    elif not source_row.get("filled", False) or fill_draw > probability:
        status, fill_fraction = "unfilled", 0.0
    else:
        raw_fraction = min(1.0, max(profile.queue.participation_rate, probability))
        fill_fraction = min(scenario.partial_fill_cap, raw_fraction)
        if not profile.broker.partial_fills_allowed:
            fill_fraction = 1.0 if fill_fraction >= 1.0 else 0.0
        status = "filled" if fill_fraction >= 1.0 else ("partially_filled" if fill_fraction > 0 else "unfilled")
    impact_points = market_impact_points(fill_fraction, scenario, profile)
    adverse_points = 0.0 if fill_fraction <= 0 else adverse_selection_points(probability, latency, profile)
    incremental_spread = source_spread * max(0.0, scenario.spread_multiplier - 1.0) * fill_fraction
    latency_points = profile.latency.latency_points_per_second * (latency.total_to_fill_ms / 1000.0) * fill_fraction
    incremental_points = round(incremental_spread + impact_points + adverse_points + latency_points, 12)
    risk_points = _risk_points(source_row)
    incremental_r = round(incremental_points / risk_points, 12)
    source_gross_r = float(source_row.get("gross_r", 0.0))
    source_net_r = float(source_row.get("net_r", 0.0))
    adjusted_gross_r = round(source_gross_r * fill_fraction, 12)
    adjusted_net_r = round(source_net_r * fill_fraction - incremental_r, 12)
    lifecycle = build_lifecycle(int(cube["decision_time_ms"]), action_class, status, fill_fraction, latency, profile.maximum_lifecycle_events_per_row)
    result = {
        "source_row_id": source_row["row_id"], "source_row_hash": row_hash, "node_id": source_row["node_id"], "node_hash": source_row["node_hash"],
        "action_class": action_class, "scenario_id": scenario.scenario_id, "scenario_hash": scenario.scenario_hash, "status": status,
        "broker_feasible": broker.feasible, "broker_reason_codes": list(broker.reason_codes), "normalized_volume": broker.normalized_volume,
        "fill_probability": probability, "fill_fraction": round(fill_fraction, 12), "queue_ahead_units": queue.queue_ahead_units,
        "queue_uncertainty_draw": queue.uncertainty_draw, "submit_latency_ms": latency.submit_ms, "acknowledgement_latency_ms": latency.acknowledgement_ms,
        "fill_latency_ms": latency.fill_ms, "total_to_fill_ms": latency.total_to_fill_ms, "source_spread_points": source_spread,
        "incremental_spread_points": round(incremental_spread, 12), "latency_slippage_points": round(latency_points, 12),
        "market_impact_points": impact_points, "adverse_selection_points": adverse_points, "incremental_execution_cost_points": incremental_points,
        "incremental_execution_cost_r": incremental_r, "source_gross_r": source_gross_r, "source_net_r": source_net_r,
        "adjusted_gross_r": adjusted_gross_r, "adjusted_net_r": adjusted_net_r, "lifecycle_events": lifecycle,
        "synthetic_watermark": profile.synthetic_watermark,
        "limitations": ["Deterministic reference execution stress; not a broker fill forecast.", "Does not replace prospective paper, shadow, or I18 qualification."],
    }
    from .canonical import content_hash, stable_id
    result["twin_row_id"] = stable_id("exectwinrow", result)
    result["twin_row_hash"] = content_hash(result)
    return result
