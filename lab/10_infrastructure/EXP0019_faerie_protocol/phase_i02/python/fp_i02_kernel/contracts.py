"""Immutable public data contracts for the Faerie Protocol context kernel."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Mapping

from .canonical import canonical_sha256, require_identifier, require_semver, require_sha256
from .enums import (
    CandidateState,
    ContextProfile,
    DataState,
    Direction,
    EligibilityState,
    ExecutionAuthority,
    HealthState,
    PriceSide,
    QuotaState,
    ReferenceState,
    RelationCode,
    SymbolRole,
    WWState,
    WindowKind,
    WindowScope,
)
from .errors import FPI02Error


def _required(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FPI02Error("FP_RC_INVALID_CONFIG", f"{field_name} is required", {"field": field_name})
    return value


def _finite(value: float, field_name: str) -> float:
    if not math.isfinite(float(value)):
        raise FPI02Error("FP_RC_NONFINITE_NUMBER", f"{field_name} must be finite", {"field": field_name})
    return float(value)


@dataclass(frozen=True, slots=True)
class SymbolPair:
    primary_symbol: str
    secondary_symbol: str
    pair_version: str = "1.0.0"

    def __post_init__(self) -> None:
        _required(self.primary_symbol, "primary_symbol")
        _required(self.secondary_symbol, "secondary_symbol")
        require_semver(self.pair_version, "pair_version")
        if self.primary_symbol == self.secondary_symbol:
            raise FPI02Error("FP_RC_SYMBOL_PAIR_INVALID", "pair symbols must be distinct")

    @property
    def canonical_symbols(self) -> tuple[str, str]:
        return tuple(sorted((self.primary_symbol, self.secondary_symbol)))

    @property
    def pair_id(self) -> str:
        return "FPPAIR_" + canonical_sha256({"symbols": self.canonical_symbols, "version": self.pair_version})[:24]

    def contains(self, symbol: str) -> bool:
        return symbol in self.canonical_symbols

    def counterpart(self, symbol: str) -> str:
        if symbol == self.primary_symbol:
            return self.secondary_symbol
        if symbol == self.secondary_symbol:
            return self.primary_symbol
        raise FPI02Error("FP_RC_SYMBOL_PAIR_INVALID", f"symbol {symbol} is not in pair")


@dataclass(frozen=True, slots=True)
class WindowKey:
    context_id: str
    pair_id: str
    kind: WindowKind
    scope: WindowScope
    trading_day_id: str
    start_utc_ms: int
    end_utc_ms: int
    timezone: str
    calendar_offset: int = 0
    week_id: str = ""
    data_revision: str = ""

    def __post_init__(self) -> None:
        require_identifier(self.context_id, "context_id")
        _required(self.pair_id, "pair_id")
        _required(self.trading_day_id, "trading_day_id")
        _required(self.timezone, "timezone")
        if self.start_utc_ms < 0 or self.end_utc_ms <= self.start_utc_ms:
            raise FPI02Error("FP_RC_WINDOW_INTERVAL_INVALID", "window must be non-empty half-open interval")
        if self.kind is WindowKind.W and not self.week_id:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "weekly window requires week_id")
        if self.scope is WindowScope.EXACT_PRIOR_CALENDAR_OFFSET and self.calendar_offset <= 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "prior-calendar scope requires positive calendar_offset")
        if self.scope is not WindowScope.EXACT_PRIOR_CALENDAR_OFFSET and self.calendar_offset != 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "calendar_offset only belongs to prior-calendar scope")

    @property
    def window_id(self) -> str:
        return "FPWIN_" + canonical_sha256(self)[:32]


@dataclass(frozen=True, slots=True)
class WindowRecord:
    key: WindowKey
    data_state: DataState
    high_by_symbol: Mapping[str, float]
    low_by_symbol: Mapping[str, float]
    bar_count_by_symbol: Mapping[str, int]
    source_revision_hash: str
    completed: bool
    record_version: str = "1.0.0"

    def __post_init__(self) -> None:
        require_semver(self.record_version, "window_record_version")
        require_sha256(self.source_revision_hash, "source_revision_hash")
        symbols = set(self.high_by_symbol)
        if symbols != set(self.low_by_symbol) or symbols != set(self.bar_count_by_symbol) or len(symbols) != 2:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "window symbol maps must contain the same two symbols")
        for symbol in symbols:
            high = _finite(self.high_by_symbol[symbol], f"high_by_symbol[{symbol}]")
            low = _finite(self.low_by_symbol[symbol], f"low_by_symbol[{symbol}]")
            if high < low:
                raise FPI02Error("FP_RC_INVALID_CONFIG", "window high cannot be below low")
            if int(self.bar_count_by_symbol[symbol]) < 0:
                raise FPI02Error("FP_RC_INVALID_CONFIG", "bar count cannot be negative")
        if self.data_state is DataState.COMPLETE and (not self.completed or any(int(v) <= 0 for v in self.bar_count_by_symbol.values())):
            raise FPI02Error("FP_RC_REFERENCE_INCOMPLETE", "complete window requires completed interval and bars for both symbols")

    @property
    def record_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True, slots=True)
class ReferenceSideKey:
    window_id: str
    symbol: str
    side: PriceSide
    price: float
    data_revision: str

    def __post_init__(self) -> None:
        _required(self.window_id, "window_id")
        _required(self.symbol, "symbol")
        _finite(self.price, "price")
        _required(self.data_revision, "data_revision")

    @property
    def reference_side_id(self) -> str:
        return "FPREF_" + canonical_sha256(self)[:32]


@dataclass(frozen=True, slots=True)
class ReferenceSideRecord:
    key: ReferenceSideKey
    state: ReferenceState
    first_hunter_event_id: str = ""
    consumed_event_id: str = ""
    last_transition_utc_ms: int = 0
    reason_code: str = "FP_RC_READY"

    def __post_init__(self) -> None:
        if self.last_transition_utc_ms < 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "transition time cannot be negative")
        if self.state is ReferenceState.HUNTER_SEEN and not self.first_hunter_event_id:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "HUNTER_SEEN requires first_hunter_event_id")
        if self.state is ReferenceState.CONSUMED_BY_PROTECTED_TOUCH and not self.consumed_event_id:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "consumed reference requires consumed_event_id")

    @property
    def record_id(self) -> str:
        return "FPREFSTATE_" + canonical_sha256(self)[:32]


@dataclass(frozen=True, slots=True)
class HuntFact:
    context_epoch_id: str
    relation: RelationCode
    reference_side_id: str
    check_window_id: str
    pair_id: str
    symbol: str
    role: SymbolRole
    side: PriceSide
    m1_open_utc_ms: int
    observed_price: float
    reference_price: float
    data_revision: str
    source_fingerprint: str
    reason_code: str = "FP_RC_READY"

    def __post_init__(self) -> None:
        for field_name in ("context_epoch_id", "reference_side_id", "check_window_id", "pair_id", "symbol", "data_revision"):
            _required(getattr(self, field_name), field_name)
        require_sha256(self.source_fingerprint, "source_fingerprint")
        if self.m1_open_utc_ms < 0 or self.m1_open_utc_ms % 60000 != 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "hunt canonical time must be aligned M1 open")
        _finite(self.observed_price, "observed_price")
        _finite(self.reference_price, "reference_price")

    @property
    def hunt_id(self) -> str:
        return "FPHUNT_" + canonical_sha256(self)[:32]


@dataclass(frozen=True, slots=True)
class DivergenceCandidate:
    context_epoch_id: str
    relation: RelationCode
    direction: Direction
    pair_id: str
    hunter_symbol: str
    protected_symbol: str
    reference_window_id: str
    check_window_id: str
    reference_side: PriceSide
    hunter_hunt_id: str
    first_hunt_m1_utc_ms: int
    confirmation_deadline_utc_ms: int
    resolved_confirmation_timeframe_seconds: int
    calendar_offset: int
    state: CandidateState
    data_revision: str
    reason_code: str
    candidate_version: str = "1.0.0"

    def __post_init__(self) -> None:
        require_semver(self.candidate_version, "candidate_version")
        if self.hunter_symbol == self.protected_symbol:
            raise FPI02Error("FP_RC_SYMBOL_PAIR_INVALID", "candidate roles must be different symbols")
        if self.first_hunt_m1_utc_ms < 0 or self.first_hunt_m1_utc_ms % 60000 != 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "candidate first hunt must be M1 aligned")
        if self.confirmation_deadline_utc_ms <= self.first_hunt_m1_utc_ms:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "confirmation deadline must follow hunt")
        if self.resolved_confirmation_timeframe_seconds <= 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "resolved confirmation timeframe must be positive")
        if self.relation in {RelationCode.NA, RelationCode.NL, RelationCode.NN} and self.calendar_offset <= 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "N cross-day relation requires positive calendar offset")
        if self.relation not in {RelationCode.NA, RelationCode.NL, RelationCode.NN} and self.calendar_offset != 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "calendar offset forbidden for this relation")

    @property
    def candidate_id(self) -> str:
        material = {
            "context_epoch_id": self.context_epoch_id,
            "relation": self.relation,
            "direction": self.direction,
            "pair_id": self.pair_id,
            "hunter_symbol": self.hunter_symbol,
            "protected_symbol": self.protected_symbol,
            "reference_window_id": self.reference_window_id,
            "check_window_id": self.check_window_id,
            "reference_side": self.reference_side,
            "first_hunt_m1_utc_ms": self.first_hunt_m1_utc_ms,
            "confirmation_deadline_utc_ms": self.confirmation_deadline_utc_ms,
            "resolved_confirmation_timeframe_seconds": self.resolved_confirmation_timeframe_seconds,
            "calendar_offset": self.calendar_offset,
            "data_revision": self.data_revision,
            "candidate_version": self.candidate_version,
        }
        return "FPCAND_" + canonical_sha256(material)[:32]


@dataclass(frozen=True, slots=True)
class ConfirmationEvent:
    candidate_id: str
    confirmation_bar_open_utc_ms: int
    confirmation_bar_close_utc_ms: int
    confirmation_price: float
    state: CandidateState
    reason_code: str
    data_revision: str
    event_version: str = "1.0.0"

    def __post_init__(self) -> None:
        require_semver(self.event_version, "confirmation_event_version")
        _required(self.candidate_id, "candidate_id")
        if self.confirmation_bar_open_utc_ms < 0 or self.confirmation_bar_close_utc_ms <= self.confirmation_bar_open_utc_ms:
            raise FPI02Error("FP_RC_WINDOW_INTERVAL_INVALID", "confirmation candle interval invalid")
        _finite(self.confirmation_price, "confirmation_price")

    @property
    def confirmation_event_id(self) -> str:
        return "FPCONF_" + canonical_sha256(self)[:32]


@dataclass(frozen=True, slots=True)
class ConfirmedSignal:
    candidate_id: str
    confirmation_event_id: str
    relation: RelationCode
    direction: Direction
    pair_id: str
    hunter_symbol: str
    protected_symbol: str
    first_hunt_m1_utc_ms: int
    confirmed_utc_ms: int
    eligibility: EligibilityState
    reason_code: str
    active_ww_id: str = ""
    quota_key_id: str = ""
    semantic_config_hash: str = ""
    signal_version: str = "1.0.0"

    def __post_init__(self) -> None:
        require_semver(self.signal_version, "signal_version")
        require_sha256(self.semantic_config_hash, "semantic_config_hash")
        if self.confirmed_utc_ms < self.first_hunt_m1_utc_ms:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "signal confirmation cannot precede hunt")

    @property
    def signal_id(self) -> str:
        material = {
            "candidate_id": self.candidate_id,
            "confirmation_event_id": self.confirmation_event_id,
            "relation": self.relation,
            "direction": self.direction,
            "pair_id": self.pair_id,
            "hunter_symbol": self.hunter_symbol,
            "protected_symbol": self.protected_symbol,
            "first_hunt_m1_utc_ms": self.first_hunt_m1_utc_ms,
            "confirmed_utc_ms": self.confirmed_utc_ms,
            "semantic_config_hash": self.semantic_config_hash,
            "signal_version": self.signal_version,
        }
        return "FPSIG_" + canonical_sha256(material)[:32]


@dataclass(frozen=True, slots=True)
class WWContextRecord:
    signal_id: str
    direction: Direction
    state: WWState
    confirmed_utc_ms: int
    neutralized_utc_ms: int = 0
    neutralizing_hunt_id: str = ""
    reason_code: str = "FP_RC_CONFIRMED_ACTIVE"

    def __post_init__(self) -> None:
        _required(self.signal_id, "signal_id")
        if self.confirmed_utc_ms < 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "WW confirmation time cannot be negative")
        if self.state is WWState.NEUTRALIZED and (self.neutralized_utc_ms <= self.confirmed_utc_ms or not self.neutralizing_hunt_id):
            raise FPI02Error("FP_RC_INVALID_CONFIG", "neutralized WW requires later time and neutralizing hunt")

    @property
    def ww_context_id(self) -> str:
        return "FPWW_" + canonical_sha256(self)[:32]


@dataclass(frozen=True, slots=True)
class QuotaKey:
    context_epoch_id: str
    trading_day_id: str
    pair_id: str
    session: WindowKind

    def __post_init__(self) -> None:
        if self.session not in {WindowKind.A, WindowKind.L, WindowKind.N}:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "quota session must be A/L/N")
        for name in ("context_epoch_id", "trading_day_id", "pair_id"):
            _required(getattr(self, name), name)

    @property
    def quota_key_id(self) -> str:
        return "FPQUOTA_" + canonical_sha256(self)[:32]


@dataclass(frozen=True, slots=True)
class QuotaRecord:
    key: QuotaKey
    state: QuotaState
    winner_signal_id: str = ""
    winner_first_hunt_m1_utc_ms: int = 0
    reservation_event_id: str = ""
    consumption_event_id: str = ""
    release_event_id: str = ""
    reason_code: str = "FP_RC_READY"

    def __post_init__(self) -> None:
        if self.state is QuotaState.AVAILABLE and any((self.winner_signal_id, self.reservation_event_id, self.consumption_event_id, self.release_event_id)):
            raise FPI02Error("FP_RC_INVALID_CONFIG", "available quota cannot have owner events")
        if self.state in {QuotaState.RESERVED, QuotaState.CONSUMED} and (not self.winner_signal_id or self.winner_first_hunt_m1_utc_ms <= 0):
            raise FPI02Error("FP_RC_INVALID_CONFIG", "reserved/consumed quota requires winner")
        if self.state is QuotaState.RESERVED and not self.reservation_event_id:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "reserved quota requires reservation_event_id")
        if self.state is QuotaState.CONSUMED and not self.consumption_event_id:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "consumed quota requires consumption_event_id")
        if self.state is QuotaState.RELEASED and not self.release_event_id:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "released quota requires release_event_id")

    @property
    def quota_record_id(self) -> str:
        return "FPQUOTASTATE_" + canonical_sha256(self)[:32]


@dataclass(frozen=True, slots=True)
class ReasonEvidence:
    reason_code: str
    subject_id: str
    observed_utc_ms: int
    details: Mapping[str, Any] = field(default_factory=dict)
    parent_event_id: str = ""

    def __post_init__(self) -> None:
        _required(self.reason_code, "reason_code")
        _required(self.subject_id, "subject_id")
        if self.observed_utc_ms < 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "observed time cannot be negative")

    @property
    def evidence_id(self) -> str:
        return "FPREASON_" + canonical_sha256(self)[:32]


@dataclass(frozen=True, slots=True)
class HealthStatus:
    state: HealthState
    primary_reason_code: str
    reason_codes: tuple[str, ...]
    checked_utc_ms: int
    semantic_config_hash: str
    dependency_snapshot_hash: str

    def __post_init__(self) -> None:
        require_sha256(self.semantic_config_hash, "semantic_config_hash")
        require_sha256(self.dependency_snapshot_hash, "dependency_snapshot_hash")
        if self.checked_utc_ms < 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "health check time cannot be negative")
        if not self.reason_codes or self.primary_reason_code not in self.reason_codes:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "primary reason must appear in reason_codes")

    @property
    def health_id(self) -> str:
        return "FPHEALTH_" + canonical_sha256(self)[:32]


@dataclass(frozen=True, slots=True)
class ContextManifestRecord:
    schema_version: str
    context_id: str
    context_version: str
    decision_set_id: str
    profile: ContextProfile
    pair: SymbolPair
    semantic_config_hash: str
    projection_config_hash: str
    dependency_snapshot_hash: str
    relation_registry_hash: str
    reason_registry_hash: str
    execution_authority: ExecutionAuthority
    open_decision_ids: tuple[str, ...]
    resolved_confirmation_timeframe_seconds: int
    created_utc_ms: int

    def __post_init__(self) -> None:
        require_semver(self.schema_version, "manifest_schema_version")
        require_semver(self.context_version, "context_version")
        require_identifier(self.context_id, "context_id")
        _required(self.decision_set_id, "decision_set_id")
        for field_name in ("semantic_config_hash", "projection_config_hash", "dependency_snapshot_hash", "relation_registry_hash", "reason_registry_hash"):
            require_sha256(getattr(self, field_name), field_name)
        if self.resolved_confirmation_timeframe_seconds <= 0 or self.created_utc_ms < 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "manifest time values invalid")
        if self.execution_authority is ExecutionAuthority.LIVE and self.open_decision_ids:
            raise FPI02Error("FP_RC_OPEN_DECISION_BLOCKS_LIVE", "live manifest cannot contain open decisions")

    @property
    def context_epoch_id(self) -> str:
        material = {
            "schema_version": self.schema_version,
            "context_id": self.context_id,
            "context_version": self.context_version,
            "decision_set_id": self.decision_set_id,
            "profile": self.profile,
            "pair_id": self.pair.pair_id,
            "semantic_config_hash": self.semantic_config_hash,
            "dependency_snapshot_hash": self.dependency_snapshot_hash,
            "relation_registry_hash": self.relation_registry_hash,
            "reason_registry_hash": self.reason_registry_hash,
            "execution_authority": self.execution_authority,
            "open_decision_ids": self.open_decision_ids,
            "resolved_confirmation_timeframe_seconds": self.resolved_confirmation_timeframe_seconds,
        }
        return "FPEPOCH_" + canonical_sha256(material)[:32]

    @property
    def manifest_hash(self) -> str:
        return canonical_sha256(self)
