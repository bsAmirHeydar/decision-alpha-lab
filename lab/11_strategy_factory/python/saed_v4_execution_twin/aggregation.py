from __future__ import annotations
from collections import defaultdict


def build_summary(twin: dict) -> dict:
    by_scenario = defaultdict(list)
    for row in twin["rows"]:
        by_scenario[row["scenario_id"]].append(row)
    summaries = []
    for scenario_id, rows in sorted(by_scenario.items()):
        order_rows = [r for r in rows if r["action_class"] not in {"skip", "abstain"}]
        summaries.append({
            "scenario_id": scenario_id, "row_count": len(rows), "order_row_count": len(order_rows),
            "fill_rate": 0.0 if not order_rows else sum(r["fill_fraction"] for r in order_rows) / len(order_rows),
            "rejection_rate": 0.0 if not order_rows else sum(r["status"] == "rejected" for r in order_rows) / len(order_rows),
            "broker_infeasible_rate": 0.0 if not order_rows else sum(r["status"] == "broker_infeasible" for r in order_rows) / len(order_rows),
            "mean_incremental_cost_r": 0.0 if not order_rows else sum(r["incremental_execution_cost_r"] for r in order_rows) / len(order_rows),
            "mean_adjusted_net_r": 0.0 if not order_rows else sum(r["adjusted_net_r"] for r in order_rows) / len(order_rows),
        })
    return {"twin_id": twin["twin_id"], "twin_hash": twin["twin_hash"], "scenario_summaries": summaries, "ranking_semantics": "none"}
