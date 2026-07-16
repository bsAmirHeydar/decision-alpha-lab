#!/usr/bin/env python3
"""Deterministic research mirror for the NDS Hook 86.4 Cycle R1 profile.

Canonical ownership is intentionally split exactly as in MQL5:
- Phase02 owns Hook identity, X nodes, crown, terminal and family validity.
- Phase03/04 own the Y reference and 50% X-cycle closure lifecycle.
- this mirror scans closed bars only for the first 86.4 arrival after closure.
- the existing trade adapter owns tick normalization, sizing and order lifecycle.

The module has no broker, terminal, network, subprocess, file-write or order
execution authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
import math
from typing import Iterable


class Direction(IntEnum):
    POSITIVE = 1
    NEGATIVE = -1


class SequenceState(IntEnum):
    RESET = 0
    CANDIDATE = 1
    READY = 2
    MATURE = 3
    CAPPED = 4
    REJECTED = -1


@dataclass(frozen=True)
class Sequence:
    valid: bool
    hook_failed: bool
    valid_hook_family: bool
    family_allowed: bool
    cycle_closed: bool  # Phase02 terminal availability, not Phase04 X closure.
    resolve_confirmed: bool
    cycle_crown_valid: bool
    direction: Direction
    state: SequenceState
    x_count: int
    origin_price: float
    crown_price: float
    terminal_price: float
    terminal_retracement_ratio: float


@dataclass(frozen=True)
class ClosedBar:
    time: int
    high: float
    low: float

    def validate(self) -> None:
        if self.time <= 0:
            raise ValueError("bar_time_missing")
        if not all(math.isfinite(v) and v > 0.0 for v in (self.high, self.low)):
            raise ValueError("bar_price_invalid")
        if self.low > self.high:
            raise ValueError("bar_low_above_high")


@dataclass(frozen=True)
class Phase04Evidence:
    record_valid: bool
    x_closure_candidate: bool
    x_closed: bool
    x_count: int
    closure_time: int
    closure_price: float
    closure_threshold_price: float
    origin_return_penetrated: bool
    level_touched_after_closure: bool
    first_touch_time: int = 0
    first_touch_price: float = 0.0


@dataclass(frozen=True)
class Policy:
    entry_ratio: float = 0.864
    min_x_count: int = 3
    max_x_count: int = 4
    require_confirmed_terminal: bool = True
    require_phase04_x_closed: bool = True
    closure_ratio: float = 0.50
    require_level_untouched: bool = True
    reward_r: float = 1.0

    def validate(self) -> None:
        if not math.isclose(self.entry_ratio, 0.864, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("approved_hook_entry_ratio_must_be_exactly_0_864")
        if (self.min_x_count, self.max_x_count) != (3, 4):
            raise ValueError("approved_node_count_window_must_be_exactly_3_to_4")
        if not self.require_confirmed_terminal:
            raise ValueError("confirmed_terminal_gate_must_remain_enabled")
        if not self.require_phase04_x_closed:
            raise ValueError("phase04_x_closed_gate_must_remain_enabled")
        if not math.isclose(self.closure_ratio, 0.50, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("approved_cycle_closure_ratio_must_be_exactly_0_50")
        if not self.require_level_untouched:
            raise ValueError("untouched_86_4_gate_must_remain_enabled")
        if not math.isclose(self.reward_r, 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("approved_fixed_reward_must_be_exactly_1R")


@dataclass(frozen=True)
class Plan:
    direction: Direction
    entry: float
    stop: float
    target: float
    risk_distance: float
    reward_distance: float
    realized_r: float


def raw_entry(sequence: Sequence, policy: Policy = Policy()) -> float:
    policy.validate()
    return sequence.crown_price + policy.entry_ratio * (
        sequence.origin_price - sequence.crown_price
    )


def entry_inside_cycle(sequence: Sequence, entry: float) -> bool:
    if sequence.direction is Direction.POSITIVE:
        return sequence.origin_price < entry < sequence.crown_price
    if sequence.direction is Direction.NEGATIVE:
        return sequence.crown_price < entry < sequence.origin_price
    return False


def intrinsic_eligibility(
    sequence: Sequence, policy: Policy = Policy()
) -> tuple[bool, str]:
    """Validate Phase02-owned properties only.

    `terminal_retracement_ratio` is audited but deliberately does not own the
    post-Phase04 first-arrival gate. That was the principal v1.0 integration
    defect.
    """
    try:
        policy.validate()
    except ValueError as exc:
        return False, f"profile_config_{exc}"

    if not sequence.valid or sequence.hook_failed or not sequence.valid_hook_family:
        return False, "canonical_hook_invalid_or_failed"
    if not sequence.family_allowed:
        return False, "canonical_hook_family_not_allowed"
    if not sequence.cycle_closed:
        return False, "canonical_phase02_terminal_not_available"
    if not sequence.resolve_confirmed:
        return False, "canonical_terminal_not_confirmed"
    if not sequence.cycle_crown_valid or sequence.crown_price <= 0.0:
        return False, "canonical_cycle_crown_missing"
    if not policy.min_x_count <= sequence.x_count <= policy.max_x_count:
        return False, "canonical_x_count_not_3_or_4"
    if sequence.state not in (SequenceState.MATURE, SequenceState.CAPPED):
        return False, "canonical_sequence_not_mature_or_capped"
    if sequence.origin_price <= 0.0 or sequence.terminal_price <= 0.0:
        return False, "canonical_price_missing"
    if sequence.terminal_retracement_ratio < 0.0:
        return False, "canonical_retracement_ratio_negative"

    entry = raw_entry(sequence, policy)
    if not entry_inside_cycle(sequence, entry):
        return False, "hook_864_projection_outside_canonical_cycle"
    return True, "canonical_phase02_x3_or_x4_intrinsic_valid"


# Backward-compatible name for research callers. It now means Phase02 intrinsic
# eligibility; full execution eligibility is `runtime_eligibility`.
def eligibility(sequence: Sequence, policy: Policy = Policy()) -> tuple[bool, str]:
    return intrinsic_eligibility(sequence, policy)


def first_touch_after_closure(
    bars: Iterable[ClosedBar],
    *,
    direction: Direction,
    closure_time: int,
    entry_price: float,
) -> tuple[bool, int, float]:
    """Return the first closed-bar 86.4 touch at or after the closure candle.

    The closure candle is included. If closure and 86.4 happen in the same
    candle, an order could not have been placed after observing closure, so the
    first arrival is already consumed and the strategy fails closed.
    """
    if closure_time <= 0 or not math.isfinite(entry_price) or entry_price <= 0.0:
        raise ValueError("invalid_first_touch_inputs")
    ordered = sorted(tuple(bars), key=lambda item: item.time)
    last_time = 0
    for bar in ordered:
        bar.validate()
        if bar.time <= last_time:
            raise ValueError("closed_bars_must_have_unique_ascending_times")
        last_time = bar.time
        if bar.time < closure_time:
            continue
        if direction is Direction.POSITIVE and bar.low <= entry_price:
            return True, bar.time, bar.low
        if direction is Direction.NEGATIVE and bar.high >= entry_price:
            return True, bar.time, bar.high
    return False, 0, 0.0


def build_phase04_evidence(
    sequence: Sequence,
    bars: Iterable[ClosedBar],
    *,
    record_valid: bool = True,
    x_closure_candidate: bool = True,
    x_closed: bool = True,
    closure_time: int,
    closure_price: float,
    closure_threshold_price: float,
    origin_return_penetrated: bool = False,
    policy: Policy = Policy(),
) -> Phase04Evidence:
    policy.validate()
    touched = False
    touch_time = 0
    touch_price = 0.0
    if x_closed:
        touched, touch_time, touch_price = first_touch_after_closure(
            bars,
            direction=sequence.direction,
            closure_time=closure_time,
            entry_price=raw_entry(sequence, policy),
        )
    return Phase04Evidence(
        record_valid=record_valid,
        x_closure_candidate=x_closure_candidate,
        x_closed=x_closed,
        x_count=sequence.x_count,
        closure_time=closure_time,
        closure_price=closure_price,
        closure_threshold_price=closure_threshold_price,
        origin_return_penetrated=origin_return_penetrated,
        level_touched_after_closure=touched,
        first_touch_time=touch_time,
        first_touch_price=touch_price,
    )


def runtime_eligibility(
    sequence: Sequence,
    evidence: Phase04Evidence | None,
    policy: Policy = Policy(),
) -> tuple[bool, str]:
    ok, reason = intrinsic_eligibility(sequence, policy)
    if not ok:
        return False, reason
    if evidence is None:
        return False, "phase04_evidence_not_found_for_sequence"
    if not evidence.record_valid:
        return False, "phase04_record_invalid"
    if evidence.origin_return_penetrated:
        return False, "cycle_dead_by_origin_return_before_entry"
    if not evidence.x_closure_candidate or not evidence.x_closed:
        return False, "phase04_x_cycle_not_closed"
    if not policy.min_x_count <= evidence.x_count <= policy.max_x_count:
        return False, "phase04_x_count_not_3_or_4"
    if evidence.level_touched_after_closure:
        return False, "hook_864_first_arrival_already_consumed_after_closure"
    return True, "phase04_x_closed_x3_or_x4_before_first_864_touch"


def _round_to_tick(price: float, tick: float, *, up: bool) -> float:
    if not math.isfinite(price) or not math.isfinite(tick) or tick <= 0.0:
        raise ValueError("invalid_price_or_tick")
    units = price / tick
    rounded = math.ceil(units - 1e-10) if up else math.floor(units + 1e-10)
    return rounded * tick


def build_plan(
    sequence: Sequence,
    *,
    evidence: Phase04Evidence,
    death_price: float,
    stop_buffer: float,
    minimum_stop_distance: float,
    tick_size: float,
    policy: Policy = Policy(),
) -> Plan:
    ok, reason = runtime_eligibility(sequence, evidence, policy)
    if not ok:
        raise ValueError(reason)
    if death_price <= 0.0 or stop_buffer < 0.0 or minimum_stop_distance < 0.0:
        raise ValueError("invalid_stop_inputs")

    entry_raw = raw_entry(sequence, policy)
    if sequence.direction is Direction.POSITIVE:
        entry = _round_to_tick(entry_raw, tick_size, up=False)
        death = _round_to_tick(death_price, tick_size, up=False)
        if not death < entry:
            raise ValueError("bullish_death_must_be_below_limit_entry")
        stop = _round_to_tick(death_price - stop_buffer, tick_size, up=False)
        if entry - stop < minimum_stop_distance:
            stop = _round_to_tick(entry - minimum_stop_distance, tick_size, up=False)
        if not stop < entry:
            raise ValueError("bullish_stop_must_be_below_entry")
        risk = entry - stop
        target = _round_to_tick(entry + risk * policy.reward_r, tick_size, up=True)
        if not entry < target:
            raise ValueError("bullish_target_must_be_above_entry")
    else:
        entry = _round_to_tick(entry_raw, tick_size, up=True)
        death = _round_to_tick(death_price, tick_size, up=True)
        if not death > entry:
            raise ValueError("bearish_death_must_be_above_limit_entry")
        stop = _round_to_tick(death_price + stop_buffer, tick_size, up=True)
        if stop - entry < minimum_stop_distance:
            stop = _round_to_tick(entry + minimum_stop_distance, tick_size, up=True)
        if not entry < stop:
            raise ValueError("bearish_stop_must_be_above_entry")
        risk = stop - entry
        target = _round_to_tick(entry - risk * policy.reward_r, tick_size, up=False)
        if not target < entry:
            raise ValueError("bearish_target_must_be_below_entry")

    reward = abs(target - entry)
    if reward + tick_size * 0.1 < risk * policy.reward_r:
        raise ValueError("normalized_target_below_requested_reward_r")
    return Plan(
        direction=sequence.direction,
        entry=entry,
        stop=stop,
        target=target,
        risk_distance=risk,
        reward_distance=reward,
        realized_r=reward / risk,
    )
