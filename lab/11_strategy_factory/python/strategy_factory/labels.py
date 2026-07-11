"""Shared label construction for classification, regression, ranking, and survival."""
from __future__ import annotations

from typing import Iterable, Mapping

import pandas as pd

from .contracts import OutcomeRecord


def outcomes_to_frame(outcomes: Iterable[OutcomeRecord]) -> pd.DataFrame:
    rows = []
    for outcome in outcomes:
        outcome.validate()
        rows.append(
            {
                "candidate_id": outcome.candidate_id,
                "event_id": outcome.event_id,
                "filled": int(outcome.filled),
                "fill_time_utc": outcome.fill_time_utc,
                "exit_time_utc": outcome.exit_time_utc,
                "label_end_time_utc": outcome.label_end_time_utc,
                "gross_r": outcome.gross_r,
                "net_r": outcome.net_r,
                "mfe_r": outcome.mfe_r,
                "mae_r": outcome.mae_r,
                "holding_seconds": outcome.holding_seconds,
                "exit_reason": outcome.exit_reason,
                "spread_cost_r": outcome.spread_cost_r,
                "slippage_cost_r": outcome.slippage_cost_r,
                "commission_cost_r": outcome.commission_cost_r,
                "ambiguous_bar_count": outcome.ambiguous_bar_count,
            }
        )
    return pd.DataFrame(rows)


def add_standard_labels(frame: pd.DataFrame, thresholds: Mapping[str, float] | None = None) -> pd.DataFrame:
    thresholds = dict(thresholds or {})
    result = frame.copy()
    positive_r = float(thresholds.get("positive_r", 0.0))
    target_r = float(thresholds.get("target_r", 1.5))
    tail_r = float(thresholds.get("tail_r", 3.0))
    tolerable_mae = float(thresholds.get("tolerable_mae", -1.0))

    result["label_trade_positive"] = (result["net_r"] > positive_r).astype(int)
    result["label_target_achieved"] = (result["mfe_r"] >= target_r).astype(int)
    result["label_tail_achieved"] = (result["mfe_r"] >= tail_r).astype(int)
    result["label_survived_risk"] = (result["mae_r"] >= tolerable_mae).astype(int)
    result["label_filled"] = result["filled"].astype(int)
    result["label_net_r"] = result["net_r"].astype(float)
    result["label_mfe_r"] = result["mfe_r"].astype(float)
    result["label_mae_r"] = result["mae_r"].astype(float)
    result["label_holding_seconds"] = result["holding_seconds"].astype(float)
    return result


def add_event_ranks(frame: pd.DataFrame, value_col: str = "net_r") -> pd.DataFrame:
    if value_col not in frame.columns:
        raise KeyError(value_col)
    result = frame.copy()
    result["event_candidate_rank"] = result.groupby("event_id")[value_col].rank(
        method="dense", ascending=False
    )
    result["event_best_candidate"] = (result["event_candidate_rank"] == 1).astype(int)
    return result
