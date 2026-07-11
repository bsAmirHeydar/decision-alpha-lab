"""Causal OHLC candidate simulator with explicit ambiguity policy."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Optional, Sequence

import pandas as pd

from .contracts import Direction, OutcomeRecord, TradeCandidate
from .costs import CostModel


@dataclass(frozen=True)
class SimulationPolicy:
    intrabar_ambiguity: str = "stop_first"  # stop_first | target_first | reject
    market_fill_field: str = "open"
    max_bars: Optional[int] = None
    allow_fill_on_creation_bar: bool = False

    def validate(self) -> None:
        if self.intrabar_ambiguity not in {"stop_first", "target_first", "reject"}:
            raise ValueError("invalid intrabar_ambiguity policy")
        if self.market_fill_field not in {"open", "close"}:
            raise ValueError("market_fill_field must be open or close")


def _as_utc(value: object) -> datetime:
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        ts = ts.tz_localize("UTC")
    return ts.tz_convert("UTC").to_pydatetime()


def _entry_touched(candidate: TradeCandidate, row: pd.Series) -> bool:
    low = float(row["low"])
    high = float(row["high"])
    if candidate.entry_type == "market":
        return True
    if candidate.entry_type == "limit":
        return low <= candidate.entry_price <= high
    if candidate.entry_type == "stop":
        if candidate.direction == Direction.LONG:
            return high >= candidate.entry_price
        return low <= candidate.entry_price
    raise ValueError(f"unsupported entry_type: {candidate.entry_type}")


def _r(direction: Direction, entry: float, price: float, risk: float) -> float:
    sign = 1.0 if direction == Direction.LONG else -1.0
    return sign * (price - entry) / risk


def simulate_candidate(
    candidate: TradeCandidate,
    bars: pd.DataFrame,
    cost_model: Optional[CostModel] = None,
    policy: Optional[SimulationPolicy] = None,
) -> OutcomeRecord:
    candidate.validate()
    policy = policy or SimulationPolicy()
    policy.validate()
    cost_model = cost_model or CostModel(model_id=candidate.cost_model_id)

    required = {"timestamp_utc", "open", "high", "low", "close"}
    missing = required - set(bars.columns)
    if missing:
        raise ValueError(f"bars missing columns: {sorted(missing)}")
    frame = bars.copy()
    frame["timestamp_utc"] = pd.to_datetime(frame["timestamp_utc"], utc=True)
    frame = frame.sort_values("timestamp_utc", kind="stable")
    frame = frame[
        (frame["timestamp_utc"] >= pd.Timestamp(candidate.eligible_from_utc))
        & (frame["timestamp_utc"] <= pd.Timestamp(candidate.expires_at_utc) + pd.Timedelta(seconds=candidate.max_holding_seconds or 0))
    ]
    if policy.max_bars is not None:
        frame = frame.head(policy.max_bars)

    filled = False
    fill_time: Optional[datetime] = None
    fill_price: Optional[float] = None
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    exit_reason = "not_filled"
    mfe_r = 0.0
    mae_r = 0.0
    ambiguous = 0
    bars_after_fill = 0

    for _, row in frame.iterrows():
        current_time = _as_utc(row["timestamp_utc"])
        if current_time < candidate.eligible_from_utc:
            continue
        if not filled:
            if not policy.allow_fill_on_creation_bar and current_time == candidate.created_time_utc:
                continue
            if current_time > candidate.expires_at_utc:
                break
            if not _entry_touched(candidate, row):
                continue
            filled = True
            fill_time = current_time
            if candidate.entry_type == "market":
                fill_price = float(row[policy.market_fill_field])
            else:
                fill_price = candidate.entry_price

        assert fill_price is not None
        bars_after_fill += 1
        high_r = _r(candidate.direction, fill_price, float(row["high"]), candidate.risk_distance)
        low_r = _r(candidate.direction, fill_price, float(row["low"]), candidate.risk_distance)
        mfe_r = max(mfe_r, high_r, low_r)
        mae_r = min(mae_r, high_r, low_r)

        if candidate.direction == Direction.LONG:
            stop_hit = float(row["low"]) <= candidate.stop_price
            target_hit = candidate.target_price is not None and float(row["high"]) >= candidate.target_price
        else:
            stop_hit = float(row["high"]) >= candidate.stop_price
            target_hit = candidate.target_price is not None and float(row["low"]) <= candidate.target_price

        if stop_hit and target_hit:
            ambiguous += 1
            if policy.intrabar_ambiguity == "reject":
                exit_reason = "ambiguous_bar_rejected"
                exit_time = current_time
                exit_price = fill_price
                break
            if policy.intrabar_ambiguity == "stop_first":
                target_hit = False
            else:
                stop_hit = False

        if stop_hit:
            exit_time = current_time
            exit_price = candidate.stop_price
            exit_reason = "stop"
            break
        if target_hit:
            exit_time = current_time
            exit_price = candidate.target_price
            exit_reason = "target"
            break

        if candidate.max_holding_seconds is not None and fill_time is not None:
            elapsed = (current_time - fill_time).total_seconds()
            if elapsed >= candidate.max_holding_seconds:
                exit_time = current_time
                exit_price = float(row["close"])
                exit_reason = "time_stop"
                break

    if filled and exit_time is None:
        if not frame.empty:
            last = frame.iloc[-1]
            exit_time = _as_utc(last["timestamp_utc"])
            exit_price = float(last["close"])
            exit_reason = "data_end"
        else:
            exit_time = fill_time
            exit_price = fill_price
            exit_reason = "no_post_fill_data"

    if not filled:
        gross_r = net_r = 0.0
        holding_seconds = 0
        label_end = candidate.expires_at_utc
    else:
        assert fill_price is not None and exit_price is not None and fill_time is not None and exit_time is not None
        gross_r = _r(candidate.direction, fill_price, exit_price, candidate.risk_distance)
        cost_r = cost_model.cost_in_r(candidate.risk_distance)
        net_r = gross_r - cost_r
        holding_seconds = max(0, int((exit_time - fill_time).total_seconds()))
        label_end = exit_time

    outcome = OutcomeRecord(
        candidate_id=candidate.candidate_id,
        event_id=candidate.event_id,
        filled=filled,
        fill_time_utc=fill_time,
        fill_price=fill_price,
        exit_time_utc=exit_time,
        exit_price=exit_price,
        gross_r=float(gross_r),
        net_r=float(net_r),
        mfe_r=float(mfe_r),
        mae_r=float(mae_r),
        holding_seconds=holding_seconds,
        exit_reason=exit_reason,
        spread_cost_r=cost_model.spread_price / candidate.risk_distance if filled else 0.0,
        slippage_cost_r=cost_model.slippage_price / candidate.risk_distance if filled else 0.0,
        commission_cost_r=(cost_model.commission_per_unit / candidate.risk_distance) if filled else 0.0,
        ambiguous_bar_count=ambiguous,
        label_end_time_utc=label_end,
        metadata={"bars_after_fill": bars_after_fill, "ambiguity_policy": policy.intrabar_ambiguity},
    )
    outcome.validate()
    return outcome


def simulate_many(
    candidates: Sequence[TradeCandidate],
    bars_by_symbol: dict[str, pd.DataFrame],
    costs: dict[str, CostModel],
    policy: Optional[SimulationPolicy] = None,
) -> list[OutcomeRecord]:
    results = []
    for candidate in candidates:
        if candidate.symbol not in bars_by_symbol:
            raise KeyError(f"no bars supplied for symbol {candidate.symbol}")
        cost = costs.get(candidate.cost_model_id, CostModel(model_id=candidate.cost_model_id))
        results.append(simulate_candidate(candidate, bars_by_symbol[candidate.symbol], cost, policy))
    return results
