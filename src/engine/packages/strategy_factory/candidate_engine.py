"""Domain-neutral candidate policy engine.

Every anatomy event can be converted into a controlled universe of execution
candidates.  Strategies provide parameters; the shared engine owns the
Cartesian product, compatibility filtering, identity, and hard validation.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from itertools import product
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Sequence, Tuple

from .contracts import AnatomyEvent, CandidateState, Direction, TradeCandidate, stable_hash
from .manifest import StrategyManifest


PriceFn = Callable[[AnatomyEvent, Mapping[str, Any]], float]
TargetFn = Callable[[AnatomyEvent, Mapping[str, Any], float, float], Optional[float]]


@dataclass(frozen=True)
class EntryPolicy:
    policy_id: str
    price_fn: PriceFn
    entry_type: str


@dataclass(frozen=True)
class StopPolicy:
    policy_id: str
    price_fn: PriceFn


@dataclass(frozen=True)
class ExitPolicy:
    policy_id: str
    target_fn: TargetFn


class PolicyRegistry:
    def __init__(self) -> None:
        self.entries: Dict[str, EntryPolicy] = {}
        self.stops: Dict[str, StopPolicy] = {}
        self.exits: Dict[str, ExitPolicy] = {}

    def register_entry(self, policy: EntryPolicy) -> None:
        if policy.policy_id in self.entries:
            raise ValueError(f"entry policy already registered: {policy.policy_id}")
        self.entries[policy.policy_id] = policy

    def register_stop(self, policy: StopPolicy) -> None:
        if policy.policy_id in self.stops:
            raise ValueError(f"stop policy already registered: {policy.policy_id}")
        self.stops[policy.policy_id] = policy

    def register_exit(self, policy: ExitPolicy) -> None:
        if policy.policy_id in self.exits:
            raise ValueError(f"exit policy already registered: {policy.policy_id}")
        self.exits[policy.policy_id] = policy


def _direction_sign(event: AnatomyEvent) -> float:
    if event.direction == Direction.LONG:
        return 1.0
    if event.direction == Direction.SHORT:
        return -1.0
    raise ValueError("neutral events cannot generate directional candidates")


def default_registry() -> PolicyRegistry:
    registry = PolicyRegistry()

    registry.register_entry(
        EntryPolicy(
            "market_on_confirmation",
            lambda event, ctx: float(ctx.get("confirmation_close", event.reference_price)),
            "market",
        )
    )
    registry.register_entry(
        EntryPolicy(
            "reference_limit",
            lambda event, ctx: float(event.reference_price),
            "limit",
        )
    )
    registry.register_entry(
        EntryPolicy(
            "retracement_fraction",
            lambda event, ctx: float(ctx["impulse_end"] - _direction_sign(event) * abs(ctx["impulse_end"] - ctx["impulse_start"]) * float(ctx.get("retracement_fraction", 0.5))),
            "limit",
        )
    )
    registry.register_entry(
        EntryPolicy(
            "breakout_offset",
            lambda event, ctx: float(ctx["breakout_level"] + _direction_sign(event) * float(ctx.get("entry_offset", 0.0))),
            "stop",
        )
    )

    registry.register_stop(
        StopPolicy(
            "anatomy_invalidation",
            lambda event, ctx: float(
                event.invalidation_price
                if event.invalidation_price is not None
                else ctx["invalidation_price"]
            ),
        )
    )
    registry.register_stop(
        StopPolicy(
            "reference_extreme",
            lambda event, ctx: float(ctx["reference_extreme"]),
        )
    )
    registry.register_stop(
        StopPolicy(
            "atr_buffered_invalidation",
            lambda event, ctx: float(
                (event.invalidation_price if event.invalidation_price is not None else ctx["invalidation_price"])
                - _direction_sign(event) * float(ctx.get("atr", 0.0)) * float(ctx.get("atr_buffer", 0.2))
            ),
        )
    )

    def fixed_r(event: AnatomyEvent, ctx: Mapping[str, Any], entry: float, stop: float) -> float:
        reward_r = float(ctx.get("reward_r", 2.0))
        return entry + _direction_sign(event) * abs(entry - stop) * reward_r

    registry.register_exit(ExitPolicy("fixed_r", fixed_r))
    registry.register_exit(
        ExitPolicy(
            "explicit_target",
            lambda event, ctx, entry, stop: float(ctx["target_price"]),
        )
    )
    registry.register_exit(ExitPolicy("time_only", lambda event, ctx, entry, stop: None))
    return registry


def _normalize_policy_item(item: Any) -> Tuple[str, Dict[str, Any]]:
    if isinstance(item, str):
        return item, {}
    if isinstance(item, Mapping):
        if "id" not in item:
            raise ValueError("policy object requires id")
        params = dict(item.get("parameters", {}))
        return str(item["id"]), params
    raise TypeError("policy specification must be string or object")


def generate_candidates(
    event: AnatomyEvent,
    context: Mapping[str, Any],
    manifest: StrategyManifest,
    registry: Optional[PolicyRegistry] = None,
) -> Sequence[TradeCandidate]:
    event.validate()
    if event.direction == Direction.NEUTRAL:
        return []
    registry = registry or default_registry()
    universe = manifest.section("candidate_universe")
    entries = [_normalize_policy_item(item) for item in universe["entries"]]
    stops = [_normalize_policy_item(item) for item in universe["stops"]]
    exits = [_normalize_policy_item(item) for item in universe["exits"]]
    incompatibilities = {
        tuple(item)
        for item in universe.get("incompatible_policy_triplets", [])
        if isinstance(item, list) and len(item) == 3
    }
    default_expiry = int(universe.get("default_expiration_seconds", 3600))
    default_holding = universe.get("default_max_holding_seconds")
    cost_model_id = str(universe.get("cost_model_id", "default"))

    candidates = []
    for entry_spec, stop_spec, exit_spec in product(entries, stops, exits):
        entry_id, entry_params = entry_spec
        stop_id, stop_params = stop_spec
        exit_id, exit_params = exit_spec
        if (entry_id, stop_id, exit_id) in incompatibilities:
            continue
        if entry_id not in registry.entries or stop_id not in registry.stops or exit_id not in registry.exits:
            raise KeyError(f"unregistered policy combination: {entry_id}, {stop_id}, {exit_id}")

        merged = dict(context)
        merged.update(entry_params)
        merged.update(stop_params)
        merged.update(exit_params)
        entry_price = float(registry.entries[entry_id].price_fn(event, merged))
        stop_price = float(registry.stops[stop_id].price_fn(event, merged))
        risk_distance = abs(entry_price - stop_price)
        if risk_distance <= 0:
            continue
        target_price = registry.exits[exit_id].target_fn(event, merged, entry_price, stop_price)
        candidate_payload = {
            "event_id": event.event_id,
            "entry": entry_id,
            "stop": stop_id,
            "exit": exit_id,
            "entry_price": entry_price,
            "stop_price": stop_price,
            "target_price": target_price,
            "parameters": merged,
            "manifest_hash": manifest.manifest_hash,
        }
        candidate = TradeCandidate(
            candidate_id=stable_hash(candidate_payload, prefix="cand_")[:40],
            event_id=event.event_id,
            symbol=event.symbol,
            direction=event.direction,
            entry_policy_id=entry_id,
            stop_policy_id=stop_id,
            exit_policy_id=exit_id,
            created_time_utc=event.confirmation_time_utc,
            eligible_from_utc=event.confirmation_time_utc,
            expires_at_utc=event.confirmation_time_utc + timedelta(seconds=default_expiry),
            entry_type=registry.entries[entry_id].entry_type,
            entry_price=entry_price,
            stop_price=stop_price,
            target_price=None if target_price is None else float(target_price),
            risk_distance=risk_distance,
            max_holding_seconds=None if default_holding is None else int(default_holding),
            cost_model_id=cost_model_id,
            policy_parameters={
                "entry": entry_params,
                "stop": stop_params,
                "exit": exit_params,
            },
            state=CandidateState.ELIGIBLE,
        )
        candidate.validate()
        candidates.append(candidate)

    max_candidates = int(universe["max_candidates_per_event"])
    if len(candidates) > max_candidates:
        candidates = candidates[:max_candidates]
    return candidates
