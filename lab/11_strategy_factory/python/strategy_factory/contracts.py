"""Canonical contracts for the Decision Alpha Lab Strategy Factory.

The contracts in this module are intentionally domain-neutral.  An anatomy
engine may describe a hook, divergence, time-cycle event, structural node,
astro state, or any future market ontology.  Once emitted, every event enters
one shared research and execution pipeline.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence
import hashlib
import json
import math


class ContractError(ValueError):
    """Raised when a canonical contract violates a hard invariant."""


class Direction(str, Enum):
    LONG = "long"
    SHORT = "short"
    NEUTRAL = "neutral"


class CandidateState(str, Enum):
    PROPOSED = "proposed"
    ELIGIBLE = "eligible"
    EXPIRED = "expired"
    FILLED = "filled"
    REJECTED = "rejected"
    CLOSED = "closed"


class DecisionAction(str, Enum):
    TRADE = "trade"
    SKIP = "skip"
    REVIEW = "review"


def ensure_utc(value: datetime, field_name: str) -> datetime:
    if value.tzinfo is None:
        raise ContractError(f"{field_name} must be timezone-aware")
    converted = value.astimezone(timezone.utc)
    return converted


def stable_hash(payload: Mapping[str, Any], *, prefix: str = "") -> str:
    """Return a deterministic SHA-256 identifier for canonical JSON content."""
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()
    return f"{prefix}{digest}"


def _finite(name: str, value: Optional[float]) -> None:
    if value is not None and not math.isfinite(float(value)):
        raise ContractError(f"{name} must be finite when supplied")


@dataclass(frozen=True)
class AnatomyEvent:
    event_id: str
    strategy_id: str
    strategy_version: str
    symbol: str
    direction: Direction
    event_time_utc: datetime
    known_time_utc: datetime
    confirmation_time_utc: datetime
    reference_price: float
    invalidation_price: Optional[float] = None
    reference_symbol: Optional[str] = None
    timeframe: Optional[str] = None
    session: Optional[str] = None
    parent_event_id: Optional[str] = None
    market_event_cluster_id: Optional[str] = None
    anatomy_state: str = "confirmed"
    source_hash: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.event_id or not self.strategy_id or not self.strategy_version:
            raise ContractError("event_id, strategy_id, and strategy_version are required")
        if not self.symbol:
            raise ContractError("symbol is required")
        event = ensure_utc(self.event_time_utc, "event_time_utc")
        known = ensure_utc(self.known_time_utc, "known_time_utc")
        confirm = ensure_utc(self.confirmation_time_utc, "confirmation_time_utc")
        if known < event:
            raise ContractError("known_time_utc cannot precede event_time_utc")
        if confirm < known:
            raise ContractError("confirmation_time_utc cannot precede known_time_utc")
        _finite("reference_price", self.reference_price)
        _finite("invalidation_price", self.invalidation_price)
        if self.direction == Direction.NEUTRAL and self.invalidation_price is not None:
            raise ContractError("neutral events may not define a directional invalidation price")

    def canonical_payload(self) -> Dict[str, Any]:
        self.validate()
        payload = asdict(self)
        payload["direction"] = self.direction.value
        for key in ("event_time_utc", "known_time_utc", "confirmation_time_utc"):
            payload[key] = ensure_utc(getattr(self, key), key).isoformat()
        payload["metadata"] = dict(sorted(self.metadata.items()))
        return payload

    @classmethod
    def build_id(cls, **kwargs: Any) -> str:
        filtered = {k: v for k, v in kwargs.items() if k != "event_id"}
        return stable_hash(filtered, prefix="evt_")[:36]


@dataclass(frozen=True)
class FeatureValue:
    name: str
    value: Any
    known_time_utc: datetime
    source: str
    version: str
    missing_reason: Optional[str] = None

    def validate(self, decision_time_utc: datetime) -> None:
        known = ensure_utc(self.known_time_utc, f"feature[{self.name}].known_time_utc")
        decision = ensure_utc(decision_time_utc, "decision_time_utc")
        if known > decision:
            raise ContractError(
                f"feature {self.name!r} became known at {known.isoformat()}, "
                f"after decision time {decision.isoformat()}"
            )
        if not self.name or not self.source or not self.version:
            raise ContractError("feature name, source, and version are required")


@dataclass(frozen=True)
class FeatureSnapshot:
    snapshot_id: str
    event_id: str
    snapshot_time_utc: datetime
    features: Sequence[FeatureValue]
    schema_version: str
    producer_version: str

    def validate(self) -> None:
        if not self.snapshot_id or not self.event_id:
            raise ContractError("snapshot_id and event_id are required")
        decision = ensure_utc(self.snapshot_time_utc, "snapshot_time_utc")
        seen: set[str] = set()
        for item in self.features:
            item.validate(decision)
            if item.name in seen:
                raise ContractError(f"duplicate feature name: {item.name}")
            seen.add(item.name)

    def as_flat_dict(self) -> Dict[str, Any]:
        self.validate()
        result: Dict[str, Any] = {
            "snapshot_id": self.snapshot_id,
            "event_id": self.event_id,
            "snapshot_time_utc": ensure_utc(self.snapshot_time_utc, "snapshot_time_utc").isoformat(),
            "schema_version": self.schema_version,
            "producer_version": self.producer_version,
        }
        result.update({item.name: item.value for item in self.features})
        return result


@dataclass(frozen=True)
class TradeCandidate:
    candidate_id: str
    event_id: str
    symbol: str
    direction: Direction
    entry_policy_id: str
    stop_policy_id: str
    exit_policy_id: str
    created_time_utc: datetime
    eligible_from_utc: datetime
    expires_at_utc: datetime
    entry_type: str
    entry_price: float
    stop_price: float
    target_price: Optional[float]
    risk_distance: float
    max_holding_seconds: Optional[int]
    cost_model_id: str
    policy_parameters: Mapping[str, Any] = field(default_factory=dict)
    state: CandidateState = CandidateState.PROPOSED

    def validate(self) -> None:
        if not self.candidate_id or not self.event_id or not self.symbol:
            raise ContractError("candidate_id, event_id, and symbol are required")
        created = ensure_utc(self.created_time_utc, "created_time_utc")
        eligible = ensure_utc(self.eligible_from_utc, "eligible_from_utc")
        expires = ensure_utc(self.expires_at_utc, "expires_at_utc")
        if eligible < created:
            raise ContractError("eligible_from_utc cannot precede created_time_utc")
        if expires <= eligible:
            raise ContractError("expires_at_utc must be later than eligible_from_utc")
        for name, value in (
            ("entry_price", self.entry_price),
            ("stop_price", self.stop_price),
            ("target_price", self.target_price),
            ("risk_distance", self.risk_distance),
        ):
            _finite(name, value)
        if self.risk_distance <= 0:
            raise ContractError("risk_distance must be positive")
        expected = abs(self.entry_price - self.stop_price)
        tolerance = max(1e-12, expected * 1e-8)
        if abs(expected - self.risk_distance) > tolerance:
            raise ContractError("risk_distance must equal abs(entry_price - stop_price)")
        if self.direction == Direction.LONG and self.stop_price >= self.entry_price:
            raise ContractError("long candidate stop must be below entry")
        if self.direction == Direction.SHORT and self.stop_price <= self.entry_price:
            raise ContractError("short candidate stop must be above entry")
        if self.target_price is not None:
            if self.direction == Direction.LONG and self.target_price <= self.entry_price:
                raise ContractError("long candidate target must be above entry")
            if self.direction == Direction.SHORT and self.target_price >= self.entry_price:
                raise ContractError("short candidate target must be below entry")


@dataclass(frozen=True)
class OutcomeRecord:
    candidate_id: str
    event_id: str
    filled: bool
    fill_time_utc: Optional[datetime]
    fill_price: Optional[float]
    exit_time_utc: Optional[datetime]
    exit_price: Optional[float]
    gross_r: float
    net_r: float
    mfe_r: float
    mae_r: float
    holding_seconds: int
    exit_reason: str
    spread_cost_r: float = 0.0
    slippage_cost_r: float = 0.0
    commission_cost_r: float = 0.0
    ambiguous_bar_count: int = 0
    label_end_time_utc: Optional[datetime] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        for name, value in (
            ("gross_r", self.gross_r),
            ("net_r", self.net_r),
            ("mfe_r", self.mfe_r),
            ("mae_r", self.mae_r),
            ("spread_cost_r", self.spread_cost_r),
            ("slippage_cost_r", self.slippage_cost_r),
            ("commission_cost_r", self.commission_cost_r),
        ):
            _finite(name, value)
        if self.holding_seconds < 0:
            raise ContractError("holding_seconds cannot be negative")
        if self.filled:
            if self.fill_time_utc is None or self.fill_price is None:
                raise ContractError("filled outcomes require fill_time_utc and fill_price")
            ensure_utc(self.fill_time_utc, "fill_time_utc")
        if self.exit_time_utc is not None:
            ensure_utc(self.exit_time_utc, "exit_time_utc")
        if self.label_end_time_utc is not None:
            ensure_utc(self.label_end_time_utc, "label_end_time_utc")


@dataclass(frozen=True)
class ModelDecision:
    decision_id: str
    event_id: str
    candidate_id: Optional[str]
    model_id: str
    model_version: str
    decision_time_utc: datetime
    action: DecisionAction
    predicted_probability: Optional[float]
    expected_net_r: Optional[float]
    expected_mfe_r: Optional[float]
    expected_mae_r: Optional[float]
    confidence_tier: str
    feature_schema_version: str
    model_artifact_hash: str
    explanations: Mapping[str, float] = field(default_factory=dict)

    def validate(self) -> None:
        ensure_utc(self.decision_time_utc, "decision_time_utc")
        if self.predicted_probability is not None and not 0.0 <= self.predicted_probability <= 1.0:
            raise ContractError("predicted_probability must be within [0, 1]")
        for name, value in (
            ("expected_net_r", self.expected_net_r),
            ("expected_mfe_r", self.expected_mfe_r),
            ("expected_mae_r", self.expected_mae_r),
        ):
            _finite(name, value)
        if self.action == DecisionAction.TRADE and not self.candidate_id:
            raise ContractError("trade decisions require candidate_id")


@dataclass(frozen=True)
class ExecutionIntent:
    intent_id: str
    event_id: str
    candidate_id: str
    symbol: str
    direction: Direction
    created_time_utc: datetime
    entry_type: str
    entry_price: float
    stop_price: float
    target_price: Optional[float]
    volume: float
    risk_dollars: float
    expires_at_utc: datetime
    strategy_id: str
    strategy_version: str
    model_decision_id: Optional[str] = None

    def validate(self) -> None:
        ensure_utc(self.created_time_utc, "created_time_utc")
        ensure_utc(self.expires_at_utc, "expires_at_utc")
        for name, value in (
            ("entry_price", self.entry_price),
            ("stop_price", self.stop_price),
            ("target_price", self.target_price),
            ("volume", self.volume),
            ("risk_dollars", self.risk_dollars),
        ):
            _finite(name, value)
        if self.volume <= 0 or self.risk_dollars <= 0:
            raise ContractError("volume and risk_dollars must be positive")


@dataclass(frozen=True)
class ExecutionTrace:
    intent_id: str
    broker_adapter_id: str
    request_time_utc: datetime
    response_time_utc: Optional[datetime]
    order_id: Optional[str]
    position_id: Optional[str]
    state: str
    fill_price: Optional[float] = None
    filled_volume: float = 0.0
    slippage_price: float = 0.0
    reject_reason: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        request = ensure_utc(self.request_time_utc, "request_time_utc")
        if self.response_time_utc is not None:
            response = ensure_utc(self.response_time_utc, "response_time_utc")
            if response < request:
                raise ContractError("response_time_utc cannot precede request_time_utc")
        if self.filled_volume < 0:
            raise ContractError("filled_volume cannot be negative")
        _finite("fill_price", self.fill_price)
        _finite("slippage_price", self.slippage_price)


def validate_all(items: Iterable[Any]) -> None:
    for item in items:
        validator = getattr(item, "validate", None)
        if validator is None:
            raise ContractError(f"object {type(item)!r} does not expose validate()")
        validator()
