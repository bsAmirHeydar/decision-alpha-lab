from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd

from .math_utils import build_territory, hunt_breached, hunt_price, in_zone, log_move
from .schemas import RTVConfig, RTVEvent, ReferencePoint, events_to_dataframe


@dataclass
class _NodeRuntimeState:
    ref: ReferencePoint
    extreme: float | None
    territory_lower: float | None = None
    territory_upper: float | None = None
    consumed: bool = False
    hunted: bool = False
    in_event: bool = False
    revisit_id: int = 0
    outside_count: int = 0
    entry_index: int | None = None
    entry_time: Any | None = None
    inside_logs: list[float] = field(default_factory=list)
    inside_indices: list[int] = field(default_factory=list)
    before_logs: list[float] = field(default_factory=list)
    event_before_logs: list[float] = field(default_factory=list)
    frozen_extreme: float | None = None
    hunt_index: int | None = None
    hunt_time: Any | None = None
    hunt_price: float | None = None


def compute_rtv_events(
    candles_df: pd.DataFrame,
    reference_points: list[ReferencePoint],
    config: RTVConfig,
) -> list[RTVEvent]:
    """Compute M0001 events from candle stream and reference points.

    This is the single metric engine. Actual L-rule nodes and random baseline
    points both come through `reference_points`; therefore the metric logic is
    identical for actual-vs-random comparisons and for MQL visual export.
    """
    config.validate()
    if candles_df is None or candles_df.empty or not reference_points:
        return []

    required = {"time", "high", "low"}
    missing = required.difference(candles_df.columns)
    if missing:
        raise ValueError(f"candles_df missing columns: {sorted(missing)}")

    df = candles_df.drop_duplicates("time", keep="last").sort_values("time").reset_index(drop=True)
    states = [
        _NodeRuntimeState(ref=ref, extreme=float(ref.price))
        for ref in sorted(reference_points, key=lambda item: (item.index, item.ref_id))
        if ref.confirmed and ref.normalized_type() in {"LOW", "HIGH"}
    ]

    events: list[RTVEvent] = []
    for i, candle in df.iterrows():
        high = candle["high"]
        low = candle["low"]
        time = candle["time"]
        move = log_move(high, low)

        for state in states:
            active_from = state.ref.active_from_index
            if active_from is None:
                active_from = int(state.ref.index) + int(config.L)
            if int(i) <= int(active_from) or state.consumed:
                continue

            if state.in_event:
                _process_active_event(state, int(i), time, high, low, move, config, events)
                continue

            if state.extreme is None:
                _process_waiting_revisit(state, int(i), time, high, low, move, config)
                continue

            _process_tracking(state, int(i), time, high, low, move, config)

    return events


def compute_rtv_dataframe(
    candles_df: pd.DataFrame,
    reference_points: list[ReferencePoint],
    config: RTVConfig,
    include_visual_fields: bool = False,
) -> pd.DataFrame:
    return events_to_dataframe(
        compute_rtv_events(candles_df, reference_points, config),
        include_visual_fields=include_visual_fields,
    )


def _append_before_log(state: _NodeRuntimeState, value: float, config: RTVConfig) -> None:
    state.before_logs.append(float(value))
    if len(state.before_logs) > config.max_before_logs:
        state.before_logs.pop(0)


def _update_extreme(state: _NodeRuntimeState, high: Any, low: Any) -> None:
    if state.in_event or state.extreme is None:
        return
    if state.ref.normalized_type() == "LOW":
        if float(high) > float(state.extreme):
            state.extreme = float(high)
    else:
        if float(low) < float(state.extreme):
            state.extreme = float(low)


def _update_territory(state: _NodeRuntimeState, config: RTVConfig) -> None:
    if state.extreme is None:
        return
    lower, upper = build_territory(state.ref.price, state.extreme, config.zone_ratio)
    state.territory_lower = lower
    state.territory_upper = upper


def _check_hunt(state: _NodeRuntimeState, i: int, time: Any, high: Any, low: Any) -> None:
    if state.hunted:
        return
    if hunt_breached(state.ref.normalized_type(), state.ref.price, high, low):
        state.hunted = True
        state.hunt_index = int(i)
        state.hunt_time = time
        state.hunt_price = hunt_price(state.ref.normalized_type(), state.ref.price, high, low)


def _start_event(state: _NodeRuntimeState, i: int, time: Any, move: float) -> None:
    state.in_event = True
    state.revisit_id += 1
    state.outside_count = 0
    state.entry_index = int(i)
    state.entry_time = time
    state.inside_logs = [float(move)]
    state.inside_indices = [int(i)]
    state.event_before_logs = list(state.before_logs)
    state.frozen_extreme = state.extreme


def _process_tracking(state: _NodeRuntimeState, i: int, time: Any, high: Any, low: Any, move: float, config: RTVConfig) -> None:
    _update_extreme(state, high, low)
    _update_territory(state, config)
    _check_hunt(state, i, time, high, low)

    if in_zone(high, low, state.territory_lower, state.territory_upper):
        _start_event(state, i, time, move)
        return

    _consume_gap_hunt_if_needed(state, config)
    if not state.consumed:
        _append_before_log(state, move, config)


def _process_waiting_revisit(state: _NodeRuntimeState, i: int, time: Any, high: Any, low: Any, move: float, config: RTVConfig) -> None:
    _check_hunt(state, i, time, high, low)
    if in_zone(high, low, state.territory_lower, state.territory_upper):
        state.extreme = float(high if state.ref.normalized_type() == "LOW" else low)
        _start_event(state, i, time, move)
        return

    _consume_gap_hunt_if_needed(state, config)
    if not state.consumed:
        _append_before_log(state, move, config)


def _process_active_event(
    state: _NodeRuntimeState,
    i: int,
    time: Any,
    high: Any,
    low: Any,
    move: float,
    config: RTVConfig,
    events: list[RTVEvent],
) -> None:
    _check_hunt(state, i, time, high, low)
    inside = in_zone(high, low, state.territory_lower, state.territory_upper)

    if inside:
        state.inside_logs.append(float(move))
        state.inside_indices.append(int(i))
        state.outside_count = 0
    else:
        state.outside_count += 1

    if state.outside_count < config.exit_gap:
        return

    event = _build_event(state, exit_index=i, exit_time=time)
    if event is not None:
        events.append(event)

    _consume_if_needed(state, config)
    _reset_after_event(state)


def _build_event(state: _NodeRuntimeState, exit_index: int, exit_time: Any) -> RTVEvent | None:
    inside = list(state.inside_logs)
    n = len(inside)
    if n == 0:
        return None
    before = list(state.event_before_logs)[-n:]
    if len(before) < n:
        return None

    mean_inside = float(np.mean(inside))
    mean_before = float(np.mean(before))
    median_inside = float(np.median(inside))
    median_before = float(np.median(before))
    if mean_before == 0:
        return None

    return RTVEvent(
        node_id=int(state.ref.ref_id),
        node_time=state.ref.time,
        node_type=state.ref.normalized_type(),
        node_price=float(state.ref.price),
        revisit_id=int(state.revisit_id),
        entry_time=state.entry_time,
        exit_time=exit_time,
        event_length=int(n),
        territory_lower=float(state.territory_lower),
        territory_upper=float(state.territory_upper),
        expansion_extreme=float(state.frozen_extreme),
        mean_inside=mean_inside,
        mean_before=mean_before,
        median_inside=median_inside,
        median_before=median_before,
        RTV=float(mean_inside / mean_before),
        hunted=bool(state.hunted),
        entry_index=state.entry_index,
        exit_index=int(exit_index),
        hunt_index=state.hunt_index,
        hunt_time=state.hunt_time,
        hunt_price=state.hunt_price,
        baseline_kind=state.ref.baseline_kind,
        before_start_index=(int(state.entry_index) - int(n)) if state.entry_index is not None else None,
        before_end_index=(int(state.entry_index) - 1) if state.entry_index is not None else None,
        inside_indices=list(state.inside_indices),
    )


def _consume_if_needed(state: _NodeRuntimeState, config: RTVConfig) -> None:
    if config.consumption_mode == "touch":
        state.consumed = True
    elif config.consumption_mode == "hunt" and state.hunted:
        state.consumed = True


def _consume_gap_hunt_if_needed(state: _NodeRuntimeState, config: RTVConfig) -> None:
    if config.consumption_mode == "hunt" and state.hunted and not state.in_event:
        state.consumed = True


def _reset_after_event(state: _NodeRuntimeState) -> None:
    state.in_event = False
    state.outside_count = 0
    state.entry_index = None
    state.entry_time = None
    state.inside_logs = []
    state.inside_indices = []
    state.event_before_logs = []

    if not state.consumed:
        state.extreme = None
        state.hunted = False
        state.hunt_index = None
        state.hunt_time = None
        state.hunt_price = None
        state.before_logs = []
