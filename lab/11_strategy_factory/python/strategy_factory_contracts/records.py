from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .enums import Direction, FeatureQuality, FeatureType
from .hashing import stable_id
from .registry import default_registry
from .schema import SchemaIdentity
from .time import MarketTimestamp
from .validation import ContractValidationError, require, validate_finite, validate_safe_identifier

REGISTRY = default_registry()

def canonical_double(value: float, digits: int = 10) -> str:
    return f"{value:.{digits}f}"

@dataclass(frozen=True, slots=True)
class BarRecord:
    symbol: str
    timeframe_seconds: int
    open_time: MarketTimestamp
    close_time: MarketTimestamp
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    tick_volume: int
    real_volume: int
    bid_close: float
    ask_close: float
    spread_points: float
    source_id: str
    source_bar_id: str
    schema: SchemaIdentity = field(default_factory=lambda: REGISTRY.get("bar_record"))

    def __post_init__(self) -> None:
        validate_safe_identifier(self.symbol, "symbol", 64)
        require(self.timeframe_seconds > 0, "timeframe_seconds must be positive")
        require(self.open_time < self.close_time, "bar close must be after open")
        for name, value in (("open", self.open_price), ("high", self.high_price),
                            ("low", self.low_price), ("close", self.close_price)):
            validate_finite(value, name)
        require(self.high_price >= self.low_price, "high below low")
        require(self.low_price <= self.open_price <= self.high_price, "open outside range")
        require(self.low_price <= self.close_price <= self.high_price, "close outside range")
        require(self.tick_volume >= 0 and self.real_volume >= 0, "negative volume")
        if self.ask_close > 0 and self.bid_close > 0:
            require(self.ask_close >= self.bid_close, "ask below bid")
        require(self.spread_points >= 0, "negative spread")
        validate_safe_identifier(self.source_id, "source_id", 96)
        validate_safe_identifier(self.source_bar_id, "source_bar_id", 128, allow_empty=True)

    @property
    def canonical_identity(self) -> str:
        return "|".join((self.symbol, str(self.timeframe_seconds),
                         str(self.open_time.utc_epoch_milliseconds), self.source_id, self.source_bar_id))

    @property
    def bar_id(self) -> str:
        return stable_id("bar", self.canonical_identity)

@dataclass(frozen=True, slots=True)
class AnatomyEvent:
    event_id: str
    strategy_id: str
    strategy_version: str
    producer_id: str
    producer_version: str
    symbol: str
    reference_symbol: str
    direction: Direction
    event_time: MarketTimestamp
    known_time: MarketTimestamp
    confirmation_time: MarketTimestamp
    reference_price: float
    invalidation_price: float
    timeframe_seconds: int
    session_id: str
    parent_event_id: str
    market_event_cluster_id: str
    source_hash: str
    anatomy_state: str
    schema: SchemaIdentity = field(default_factory=lambda: REGISTRY.get("anatomy_event"))

    def __post_init__(self) -> None:
        for field_name, value in (("strategy_id", self.strategy_id), ("strategy_version", self.strategy_version),
                                  ("producer_id", self.producer_id), ("producer_version", self.producer_version),
                                  ("symbol", self.symbol), ("market_event_cluster_id", self.market_event_cluster_id),
                                  ("source_hash", self.source_hash)):
            validate_safe_identifier(value, field_name)
        validate_safe_identifier(self.reference_symbol, "reference_symbol", 64, allow_empty=True)
        validate_safe_identifier(self.session_id, "session_id", 128, allow_empty=True)
        validate_safe_identifier(self.parent_event_id, "parent_event_id", 128, allow_empty=True)
        validate_safe_identifier(self.anatomy_state, "anatomy_state", 128, allow_empty=True)
        require(self.direction != Direction.NONE, "direction cannot be NONE")
        require(self.event_time <= self.known_time <= self.confirmation_time,
                "required ordering: event_time <= known_time <= confirmation_time")
        validate_finite(self.reference_price, "reference_price")
        validate_finite(self.invalidation_price, "invalidation_price")
        require(self.timeframe_seconds > 0, "timeframe_seconds must be positive")
        if self.event_id:
            require(self.event_id == self.derived_event_id, "event_id does not match canonical identity")

    @property
    def canonical_identity(self) -> str:
        return "|".join((
            self.strategy_id, self.strategy_version, self.symbol, self.reference_symbol,
            self.direction.name, str(self.event_time.utc_epoch_milliseconds),
            str(self.known_time.utc_epoch_milliseconds), str(self.confirmation_time.utc_epoch_milliseconds),
            str(self.timeframe_seconds), self.parent_event_id, self.market_event_cluster_id, self.source_hash,
        ))

    @property
    def derived_event_id(self) -> str:
        return stable_id("evt", self.canonical_identity)

    def with_derived_id(self) -> "AnatomyEvent":
        from dataclasses import replace
        return replace(self, event_id=self.derived_event_id)

@dataclass(frozen=True, slots=True)
class FeatureValue:
    feature_id: str
    feature_version: str
    value_type: FeatureType
    quality: FeatureQuality
    known_time: MarketTimestamp
    source_event_id: str
    source_hash: str
    value: Any
    schema: SchemaIdentity = field(default_factory=lambda: REGISTRY.get("feature_value"))

    def __post_init__(self) -> None:
        validate_safe_identifier(self.feature_id, "feature_id")
        validate_safe_identifier(self.feature_version, "feature_version")
        validate_safe_identifier(self.source_event_id, "source_event_id", allow_empty=True)
        validate_safe_identifier(self.source_hash, "source_hash")
        if self.quality == FeatureQuality.VALID:
            if self.value_type == FeatureType.DOUBLE:
                require(isinstance(self.value, (int, float)) and not isinstance(self.value, bool), "double feature type mismatch")
                validate_finite(float(self.value), "feature value")
            elif self.value_type == FeatureType.INTEGER:
                require(isinstance(self.value, int) and not isinstance(self.value, bool), "integer feature type mismatch")
            elif self.value_type == FeatureType.BOOLEAN:
                require(isinstance(self.value, bool), "boolean feature type mismatch")
            elif self.value_type == FeatureType.STRING:
                require(isinstance(self.value, str) and len(self.value) <= 2048, "string feature type mismatch")
            elif self.value_type == FeatureType.TIMESTAMP:
                require(isinstance(self.value, MarketTimestamp), "timestamp feature type mismatch")

    @property
    def canonical(self) -> str:
        if self.value_type == FeatureType.DOUBLE:
            encoded = canonical_double(float(self.value))
        elif self.value_type == FeatureType.BOOLEAN:
            encoded = "true" if self.value else "false"
        elif self.value_type == FeatureType.TIMESTAMP:
            encoded = str(self.value.utc_epoch_milliseconds)
        elif self.value_type == FeatureType.NULL:
            encoded = "null"
        else:
            encoded = str(self.value)
        return "|".join((self.feature_id, self.feature_version, self.value_type.value,
                         self.quality.value, str(self.known_time.utc_epoch_milliseconds),
                         encoded, self.source_hash))

@dataclass(frozen=True, slots=True)
class FeatureSnapshot:
    snapshot_id: str
    event_id: str
    strategy_id: str
    snapshot_time: MarketTimestamp
    producer_id: str
    producer_version: str
    source_hash: str
    state_generation: int
    values: tuple[FeatureValue, ...]
    schema: SchemaIdentity = field(default_factory=lambda: REGISTRY.get("feature_snapshot"))

    def __post_init__(self) -> None:
        for field_name, value in (("event_id", self.event_id), ("strategy_id", self.strategy_id),
                                  ("producer_id", self.producer_id), ("producer_version", self.producer_version),
                                  ("source_hash", self.source_hash)):
            validate_safe_identifier(value, field_name)
        require(self.state_generation >= 0, "negative state_generation")
        ids = [v.feature_id for v in self.values]
        require(len(ids) == len(set(ids)), "duplicate feature_id")
        for value in self.values:
            require(value.known_time <= self.snapshot_time, "feature known_time after snapshot_time")
        if self.snapshot_id:
            require(self.snapshot_id == self.derived_snapshot_id, "snapshot_id mismatch")

    @property
    def canonical_identity(self) -> str:
        head = "|".join((self.event_id, self.strategy_id, str(self.snapshot_time.utc_epoch_milliseconds),
                         self.producer_id, self.producer_version, str(self.state_generation), self.source_hash))
        return head + "".join(f"|{value.canonical}" for value in self.values)

    @property
    def derived_snapshot_id(self) -> str:
        return stable_id("snap", self.canonical_identity)

    def with_derived_id(self) -> "FeatureSnapshot":
        from dataclasses import replace
        return replace(self, snapshot_id=self.derived_snapshot_id)

@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    artifact_id: str
    artifact_type: str
    run_id: str
    producer_id: str
    producer_version: str
    git_commit: str
    strategy_id: str
    strategy_version: str
    manifest_hash: str
    source_hash: str
    created_at: MarketTimestamp
    schema: SchemaIdentity = field(default_factory=lambda: REGISTRY.get("artifact_identity"))

    def __post_init__(self) -> None:
        for field_name, value in (("artifact_type", self.artifact_type), ("run_id", self.run_id),
                                  ("producer_id", self.producer_id), ("producer_version", self.producer_version),
                                  ("git_commit", self.git_commit), ("strategy_id", self.strategy_id),
                                  ("strategy_version", self.strategy_version), ("manifest_hash", self.manifest_hash),
                                  ("source_hash", self.source_hash)):
            validate_safe_identifier(value, field_name)
        if self.artifact_id:
            require(self.artifact_id == self.derived_artifact_id, "artifact_id mismatch")

    @property
    def canonical_identity(self) -> str:
        return "|".join((self.artifact_type, self.run_id, self.producer_id, self.producer_version,
                         self.git_commit, self.strategy_id, self.strategy_version, self.manifest_hash,
                         self.source_hash, str(self.created_at.utc_epoch_milliseconds)))

    @property
    def derived_artifact_id(self) -> str:
        return stable_id("art", self.canonical_identity)
