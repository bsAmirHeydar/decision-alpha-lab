"""Semantic/projection configuration separation and manifest construction."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .canonical import projection_hash, require_semver, require_sha256, semantic_hash
from .contracts import ContextManifestRecord, SymbolPair
from .enums import (
    ConfirmationDeadlinePolicy,
    ContextProfile,
    ExecutionAuthority,
    FirstSweepAuthority,
    IntervalSemantics,
    LookbackPolicy,
    NoActiveWWPolicy,
    QuotaConsumptionPolicy,
    QuotaScope,
    QuotaWinnerPolicy,
    ReferenceReusePolicy,
    SellStopAdjustmentPolicy,
    SuppressedDrawingPolicy,
    TimeframeSource,
    WWNeutralizationPolicy,
    WWResolutionPolicy,
    WWTradeabilityPolicy,
    WeekBoundaryPolicy,
)
from .errors import FPI02Error
from .reason_codes import DEFAULT_REASON_REGISTRY
from .relations import DEFAULT_RELATION_REGISTRY


@dataclass(frozen=True, slots=True)
class SemanticConfiguration:
    schema_version: str
    decision_set_id: str
    pair: SymbolPair
    timezone: str
    interval_semantics: IntervalSemantics
    first_sweep_authority: FirstSweepAuthority
    trading_day_start: str
    trading_day_end_exclusive: str
    session_a: tuple[str, str]
    session_l: tuple[str, str]
    session_n: tuple[str, str]
    week_boundary_policy: WeekBoundaryPolicy
    confirmation_timeframe_source: TimeframeSource
    resolved_confirmation_timeframe_seconds: int
    confirmation_deadline_policy: ConfirmationDeadlinePolicy
    lookback_policy: LookbackPolicy
    historical_n_depth: int
    replace_missing_offsets: bool
    reference_reuse_policy: ReferenceReusePolicy
    ww_neutralization_policy: WWNeutralizationPolicy
    ww_tradeability_policy: WWTradeabilityPolicy
    no_active_ww_policy: NoActiveWWPolicy
    ww_resolution_policy: WWResolutionPolicy
    quota_scope: QuotaScope
    quota_winner_policy: QuotaWinnerPolicy
    quota_consumption_policy: QuotaConsumptionPolicy
    sell_stop_policy: SellStopAdjustmentPolicy
    risk_uses_adjusted_stop: bool
    relation_registry_version: str
    reason_registry_version: str
    source_data_revision: str
    adapter_snapshot_hash: str
    enabled_relations: tuple[str, ...] = ("AL", "AN", "LN", "NA", "NL", "NN", "WW")

    def __post_init__(self) -> None:
        require_semver(self.schema_version, "semantic_config_schema_version")
        require_semver(self.relation_registry_version, "relation_registry_version")
        require_semver(self.reason_registry_version, "reason_registry_version")
        require_sha256(self.adapter_snapshot_hash, "adapter_snapshot_hash")
        if self.timezone != "America/New_York":
            raise FPI02Error("FP_RC_INVALID_CONFIG", "canonical timezone must be America/New_York")
        if self.resolved_confirmation_timeframe_seconds <= 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "resolved confirmation timeframe must be positive")
        if self.historical_n_depth <= 0:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "historical N depth must be positive")
        if self.replace_missing_offsets:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "calendar-day policy forbids replacement of missing offsets")
        if set(self.enabled_relations) != {"AL", "AN", "LN", "NA", "NL", "NN", "WW"}:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "canonical profile requires all seven relations")
        if not self.source_data_revision.strip():
            raise FPI02Error("FP_RC_INVALID_CONFIG", "source_data_revision is required")

    @property
    def config_hash(self) -> str:
        return semantic_hash(self)


@dataclass(frozen=True, slots=True)
class ProjectionConfiguration:
    schema_version: str
    suppressed_drawing_policy: SuppressedDrawingPolicy
    style_registry_version: str
    line_width: int = 1
    active_opacity: int = 255
    suppressed_opacity: int = 120
    show_session_boxes: bool = True
    show_reference_levels: bool = True
    show_hunt_markers: bool = True
    show_candidate_lines: bool = True
    show_confirmed_signals: bool = True
    show_ww_context: bool = True
    show_health_panel: bool = True
    label_font_size: int = 9
    palette: Mapping[str, str] = field(default_factory=lambda: {
        "bullish": "#22C55E",
        "bearish": "#EF4444",
        "neutral": "#94A3B8",
        "warning": "#F59E0B",
    })

    def __post_init__(self) -> None:
        require_semver(self.schema_version, "projection_config_schema_version")
        require_semver(self.style_registry_version, "style_registry_version")
        if self.line_width < 1 or self.line_width > 5:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "line width must be in [1,5]")
        if not 0 <= self.active_opacity <= 255 or not 0 <= self.suppressed_opacity <= 255:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "opacity must be in [0,255]")
        if self.label_font_size < 6 or self.label_font_size > 30:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "font size must be in [6,30]")

    @property
    def config_hash(self) -> str:
        return projection_hash(self)


@dataclass(frozen=True, slots=True)
class OperationalConfiguration:
    schema_version: str = "1.0.0"
    timer_interval_ms: int = 1000
    max_objects_per_chart: int = 3000
    max_history_calendar_days: int = 130
    diagnostic_level: str = "NORMAL"
    checkpoint_enabled: bool = True

    def __post_init__(self) -> None:
        require_semver(self.schema_version, "operational_config_schema_version")
        if self.timer_interval_ms < 100 or self.timer_interval_ms > 60000:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "timer interval out of range")
        if self.max_objects_per_chart < 100 or self.max_history_calendar_days < 1:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "operational limits invalid")
        if self.diagnostic_level not in {"QUIET", "NORMAL", "VERBOSE"}:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "unknown diagnostic level")

    @property
    def config_hash(self) -> str:
        return projection_hash(self)


@dataclass(frozen=True, slots=True)
class ConfigurationBundle:
    semantic: SemanticConfiguration
    projection: ProjectionConfiguration
    operational: OperationalConfiguration
    profile: ContextProfile
    context_version: str = "1.0.0"
    context_id: str = "FP-CONTEXT-001"
    open_decision_ids: tuple[str, ...] = ("FP-DEC-012",)

    def __post_init__(self) -> None:
        require_semver(self.context_version, "context_version")
        if self.profile is ContextProfile.CANONICAL_LIVE and self.semantic.quota_consumption_policy is QuotaConsumptionPolicy.UNSET:
            raise FPI02Error("FP_RC_OPEN_DECISION_BLOCKS_LIVE", "live profile requires frozen quota-consumption policy")
        if self.semantic.quota_consumption_policy is not QuotaConsumptionPolicy.UNSET and "FP-DEC-012" in self.open_decision_ids:
            raise FPI02Error("FP_RC_INVALID_CONFIG", "frozen quota policy conflicts with open-decision list")

    @property
    def bundle_hash(self) -> str:
        return semantic_hash({
            "semantic_hash": self.semantic.config_hash,
            "projection_hash": self.projection.config_hash,
            "operational_hash": self.operational.config_hash,
            "profile": self.profile,
            "context_version": self.context_version,
            "context_id": self.context_id,
            "open_decision_ids": self.open_decision_ids,
        })

    def execution_authority(self) -> ExecutionAuthority:
        if self.profile in {ContextProfile.CANONICAL_RESEARCH, ContextProfile.NON_CANONICAL_EXPERIMENT}:
            return ExecutionAuthority.NONE
        if self.profile is ContextProfile.CANONICAL_PAPER:
            return ExecutionAuthority.PAPER_ONLY
        if self.semantic.quota_consumption_policy is QuotaConsumptionPolicy.UNSET:
            return ExecutionAuthority.NONE
        return ExecutionAuthority.LIVE

    def build_manifest(self, created_utc_ms: int) -> ContextManifestRecord:
        dependency_hash = self.semantic.adapter_snapshot_hash
        return ContextManifestRecord(
            schema_version="1.0.0",
            context_id=self.context_id,
            context_version=self.context_version,
            decision_set_id=self.semantic.decision_set_id,
            profile=self.profile,
            pair=self.semantic.pair,
            semantic_config_hash=self.semantic.config_hash,
            projection_config_hash=self.projection.config_hash,
            dependency_snapshot_hash=dependency_hash,
            relation_registry_hash=DEFAULT_RELATION_REGISTRY.registry_hash,
            reason_registry_hash=DEFAULT_REASON_REGISTRY.registry_hash,
            execution_authority=self.execution_authority(),
            open_decision_ids=self.open_decision_ids,
            resolved_confirmation_timeframe_seconds=self.semantic.resolved_confirmation_timeframe_seconds,
            created_utc_ms=created_utc_ms,
        )


def canonical_research_bundle(
    primary_symbol: str = "SPXUSD",
    secondary_symbol: str = "NDXUSD",
    resolved_confirmation_timeframe_seconds: int = 3600,
    historical_n_depth: int = 13,
    source_data_revision: str = "FIXTURE-DATA-REV-001",
    adapter_snapshot_hash: str = "0" * 64,
) -> ConfigurationBundle:
    semantic = SemanticConfiguration(
        schema_version="1.0.0",
        decision_set_id="FP-OWNER-DECISIONS-2026-07-13-V2",
        pair=SymbolPair(primary_symbol, secondary_symbol),
        timezone="America/New_York",
        interval_semantics=IntervalSemantics.HALF_OPEN,
        first_sweep_authority=FirstSweepAuthority.M1_ONLY,
        trading_day_start="18:00:00",
        trading_day_end_exclusive="17:00:00",
        session_a=("18:00:00", "04:00:00"),
        session_l=("04:00:00", "09:30:00"),
        session_n=("09:30:00", "17:00:00"),
        week_boundary_policy=WeekBoundaryPolicy.NY_TRADING_WEEK_SUN_1800_TO_FRI_1700,
        confirmation_timeframe_source=TimeframeSource.HOST_CHART,
        resolved_confirmation_timeframe_seconds=resolved_confirmation_timeframe_seconds,
        confirmation_deadline_policy=ConfirmationDeadlinePolicy.STRICT_SAME_SESSION_CLOSE,
        lookback_policy=LookbackPolicy.CALENDAR_DAY_DEPTH,
        historical_n_depth=historical_n_depth,
        replace_missing_offsets=False,
        reference_reuse_policy=ReferenceReusePolicy.ALLOW_UNTIL_PROTECTED_TOUCH,
        ww_neutralization_policy=WWNeutralizationPolicy.NEUTRALIZE_ON_SECOND_SYMBOL_TOUCH,
        ww_tradeability_policy=WWTradeabilityPolicy.WW_GATE_AND_TRADEABLE_SETUP,
        no_active_ww_policy=NoActiveWWPolicy.ALLOW_BOTH_DIRECTIONS_WHEN_NO_ACTIVE_WW,
        ww_resolution_policy=WWResolutionPolicy.NEWEST_ACTIVE_CONFIRMED_WW_WINS,
        quota_scope=QuotaScope.PAIR_GLOBAL_FIRST_ENTRY_PER_SESSION,
        quota_winner_policy=QuotaWinnerPolicy.EARLIEST_HUNT_M1_TIME_WINS,
        quota_consumption_policy=QuotaConsumptionPolicy.UNSET,
        sell_stop_policy=SellStopAdjustmentPolicy.SELL_STOP_PLUS_ONE_SPREAD,
        risk_uses_adjusted_stop=True,
        relation_registry_version="2.0.0",
        reason_registry_version="1.0.0",
        source_data_revision=source_data_revision,
        adapter_snapshot_hash=adapter_snapshot_hash,
    )
    projection = ProjectionConfiguration(
        schema_version="1.0.0",
        suppressed_drawing_policy=SuppressedDrawingPolicy.ALWAYS_DRAW_WITH_DISTINCT_STYLE,
        style_registry_version="2.0.0",
    )
    return ConfigurationBundle(semantic, projection, OperationalConfiguration(), ContextProfile.CANONICAL_RESEARCH)
