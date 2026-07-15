#!/usr/bin/env python3
"""Deterministic research/reference mirror for NDS Hook 86.4 Cycle R1.

This module mirrors the geometry and eligibility contract implemented in MQL5.
It has no broker, terminal, file-system mutation, or execution authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
import math


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
    cycle_closed: bool
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
class Policy:
    entry_ratio: float = 0.864
    min_x_count: int = 3
    max_x_count: int = 4
    require_confirmed_terminal: bool = True
    require_level_untouched: bool = True
    reward_r: float = 1.0

    def validate(self) -> None:
        if not math.isclose(self.entry_ratio, 0.864, rel_tol=0.0, abs_tol=1e-12):
            raise ValueError("approved_hook_entry_ratio_must_be_exactly_0_864")
        if (self.min_x_count, self.max_x_count) != (3, 4):
            raise ValueError("approved_node_count_window_must_be_exactly_3_to_4")
        if not self.require_confirmed_terminal:
            raise ValueError("confirmed_terminal_gate_must_remain_enabled")
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


def eligibility(sequence: Sequence, policy: Policy = Policy()) -> tuple[bool, str]:
    try:
        policy.validate()
    except ValueError as exc:
        return False, f"profile_config_{exc}"

    if not sequence.valid or sequence.hook_failed or not sequence.valid_hook_family:
        return False, "canonical_hook_invalid_or_failed"
    if not sequence.family_allowed:
        return False, "canonical_hook_family_not_allowed"
    if not sequence.cycle_closed:
        return False, "canonical_cycle_not_closed"
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
    if sequence.terminal_retracement_ratio + 1e-10 >= policy.entry_ratio:
        return False, "hook_864_level_already_reached_or_crossed"
    return True, "canonical_closed_cycle_x3_or_x4_before_864"


def _round_to_tick(price: float, tick: float, *, up: bool) -> float:
    if not math.isfinite(price) or not math.isfinite(tick) or tick <= 0.0:
        raise ValueError("invalid_price_or_tick")
    units = price / tick
    rounded = math.ceil(units - 1e-10) if up else math.floor(units + 1e-10)
    return rounded * tick


def build_plan(
    sequence: Sequence,
    *,
    death_price: float,
    stop_buffer: float,
    minimum_stop_distance: float,
    tick_size: float,
    policy: Policy = Policy(),
) -> Plan:
    ok, reason = eligibility(sequence, policy)
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
