"""Immutable public contracts for the FP-I03 time/calendar kernel."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Mapping

from fp_i02_kernel.canonical import canonical_sha256, require_identifier, require_semver, require_sha256, stable_id
from fp_i02_kernel.contracts import WindowKey
from fp_i02_kernel.enums import WindowKind, WindowScope

from .constants import (
    A_END_SECOND, A_START_SECOND, CALENDAR_VERSION, GAP_END_SECOND, GAP_START_SECOND,
    KERNEL_VERSION, L_END_SECOND, L_START_SECOND, MAX_SUPPORTED_YEAR, MIN_SUPPORTED_YEAR,
    N_END_SECOND, N_START_SECOND, SESSION_REGISTRY_VERSION, TIMEZONE_NAME, TIME_RULE_VERSION,
)
from .enums import (
    BoundaryKind, CalendarHealth, CalendarSegment, DstRegime, LocalResolutionPolicy,
    LocalTimeStatus, TimeSource, WeekState,
)
from .errors import FPI03Error


def _required(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FPI03Error("FP_TRC_REQUIRED_FIELD", f"{field_name} is required", {"field": field_name})
    return value


def _second(value: int, field_name: str) -> int:
    if not isinstance(value, int) or value < 0 or value >= 86400:
        raise FPI03Error("FP_TRC_SECOND_OF_DAY_INVALID", f"{field_name} must be [0,86400)")
    return value


@dataclass(frozen=True, slots=True)
class TimeKernelConfig:
    context_id: str = "FP-CONTEXT-001"
    timezone_name: str = TIMEZONE_NAME
    time_rule_version: str = TIME_RULE_VERSION
    calendar_version: str = CALENDAR_VERSION
    session_registry_version: str = SESSION_REGISTRY_VERSION
    kernel_version: str = KERNEL_VERSION
    minimum_supported_year: int = MIN_SUPPORTED_YEAR
    maximum_supported_year: int = MAX_SUPPORTED_YEAR
    ambiguous_start_policy: LocalResolutionPolicy = LocalResolutionPolicy.EARLIEST
    ambiguous_end_policy: LocalResolutionPolicy = LocalResolutionPolicy.LATEST

    def __post_init__(self) -> None:
        require_identifier(self.context_id, "context_id")
        _required(self.timezone_name, "timezone_name")
        _required(self.time_rule_version, "time_rule_version")
        _required(self.calendar_version, "calendar_version")
        _required(self.session_registry_version, "session_registry_version")
        require_semver(self.kernel_version, "kernel_version")
        if self.timezone_name != TIMEZONE_NAME:
            raise FPI03Error("FP_TRC_TIMEZONE_UNSUPPORTED", "canonical timezone must be America/New_York")
        if self.minimum_supported_year < 2007 or self.maximum_supported_year < self.minimum_supported_year:
            raise FPI03Error("FP_TRC_YEAR_RANGE_INVALID", "supported year range is invalid")

    @property
    def config_hash(self) -> str:
        return canonical_sha256(self)


@dataclass(frozen=True, slots=True)
class BrokerTimestamp:
    broker_epoch_ms: int
    broker_utc_offset_minutes: int
    source: TimeSource = TimeSource.BROKER_EXPLICIT_OFFSET

    def __post_init__(self) -> None:
        if self.broker_epoch_ms < 0:
            raise FPI03Error("FP_TRC_TIMESTAMP_INVALID", "broker timestamp must be non-negative")
        if self.broker_utc_offset_minutes < -840 or self.broker_utc_offset_minutes > 840:
            raise FPI03Error("FP_TRC_BROKER_OFFSET_INVALID", "broker offset outside [-840,840]")
        if self.source is not TimeSource.BROKER_EXPLICIT_OFFSET:
            raise FPI03Error("FP_TRC_TIME_SOURCE_INVALID", "broker timestamp requires explicit offset source")

    @property
    def utc_epoch_ms(self) -> int:
        return self.broker_epoch_ms - self.broker_utc_offset_minutes * 60_000


@dataclass(frozen=True, slots=True)
class NyTimestamp:
    utc_epoch_ms: int
    local_iso: str
    local_date: str
    second_of_day: int
    utc_offset_minutes: int
    dst_regime: DstRegime
    fold: int
    timezone_name: str
    time_rule_version: str

    def __post_init__(self) -> None:
        if self.utc_epoch_ms < 0:
            raise FPI03Error("FP_TRC_TIMESTAMP_INVALID", "UTC timestamp must be non-negative")
        _required(self.local_iso, "local_iso")
        _required(self.local_date, "local_date")
        _second(self.second_of_day, "second_of_day")
        if self.utc_offset_minutes not in (-300, -240):
            raise FPI03Error("FP_TRC_NY_OFFSET_INVALID", "NY offset must be -300 or -240")
        if self.fold not in (0, 1):
            raise FPI03Error("FP_TRC_FOLD_INVALID", "fold must be 0 or 1")
        if self.timezone_name != TIMEZONE_NAME:
            raise FPI03Error("FP_TRC_TIMEZONE_UNSUPPORTED", "NY timestamp timezone mismatch")

    @property
    def timestamp_id(self) -> str:
        return stable_id("FPNYTS", self, 32)


@dataclass(frozen=True, slots=True)
class LocalResolution:
    local_iso: str
    status: LocalTimeStatus
    candidate_utc_ms: tuple[int, ...]
    selected_utc_ms: int | None
    policy: LocalResolutionPolicy
    reason_code: str
    time_rule_version: str

    def __post_init__(self) -> None:
        _required(self.local_iso, "local_iso")
        if tuple(sorted(set(self.candidate_utc_ms))) != self.candidate_utc_ms:
            raise FPI03Error("FP_TRC_CANDIDATES_NONCANONICAL", "UTC candidates must be unique and ascending")
        expected = {LocalTimeStatus.NONEXISTENT: 0, LocalTimeStatus.UNIQUE: 1, LocalTimeStatus.AMBIGUOUS: 2}[self.status]
        if len(self.candidate_utc_ms) != expected:
            raise FPI03Error("FP_TRC_LOCAL_STATUS_MISMATCH", "candidate count conflicts with local status")
        if self.selected_utc_ms is not None and self.selected_utc_ms not in self.candidate_utc_ms:
            raise FPI03Error("FP_TRC_LOCAL_SELECTION_INVALID", "selected UTC must be a candidate")
        if self.policy is LocalResolutionPolicy.REJECT and self.status is not LocalTimeStatus.UNIQUE and self.selected_utc_ms is not None:
            raise FPI03Error("FP_TRC_LOCAL_SELECTION_INVALID", "reject policy cannot select ambiguous/nonexistent time")
        _required(self.reason_code, "reason_code")

    @property
    def resolution_id(self) -> str:
        return stable_id("FPLOCAL", self, 32)


@dataclass(frozen=True, slots=True)
class SessionDefinition:
    code: CalendarSegment
    start_second: int
    end_second: int
    wraps_midnight: bool
    ordinal: int
    version: str = "1.0.0"

    def __post_init__(self) -> None:
        if self.code not in (CalendarSegment.A, CalendarSegment.L, CalendarSegment.N):
            raise FPI03Error("FP_TRC_SESSION_CODE_INVALID", "session definition must be A, L, or N")
        _second(self.start_second, "start_second")
        _second(self.end_second, "end_second")
        if self.start_second == self.end_second:
            raise FPI03Error("FP_TRC_SESSION_INTERVAL_INVALID", "session cannot be empty")
        if self.wraps_midnight != (self.end_second <= self.start_second):
            raise FPI03Error("FP_TRC_SESSION_WRAP_INVALID", "wrap flag conflicts with interval")
        if self.ordinal not in (0, 1, 2):
            raise FPI03Error("FP_TRC_SESSION_ORDINAL_INVALID", "session ordinal must be 0..2")
        require_semver(self.version, "session_definition_version")

    @property
    def definition_id(self) -> str:
        return stable_id("FPSESSDEF", self, 24)


@dataclass(frozen=True, slots=True)
class TradingDayWindow:
    trading_day_id: str
    trading_date: str
    start_ny_iso: str
    end_ny_iso: str
    start_utc_ms: int
    end_utc_ms: int
    elapsed_seconds: int
    timezone_name: str
    calendar_version: str

    def __post_init__(self) -> None:
        _required(self.trading_day_id, "trading_day_id")
        _required(self.trading_date, "trading_date")
        if self.end_utc_ms <= self.start_utc_ms or self.elapsed_seconds != (self.end_utc_ms - self.start_utc_ms) // 1000:
            raise FPI03Error("FP_TRC_TRADING_DAY_INTERVAL_INVALID", "trading day interval mismatch")

    @property
    def window_id(self) -> str:
        return stable_id("FPTDAY", self, 32)


@dataclass(frozen=True, slots=True)
class SessionWindow:
    session_id: str
    session_code: CalendarSegment
    trading_day_id: str
    trading_date: str
    start_ny_iso: str
    end_ny_iso: str
    start_utc_ms: int
    end_utc_ms: int
    elapsed_seconds: int
    contains_reference_time: bool
    registry_version: str

    def __post_init__(self) -> None:
        _required(self.session_id, "session_id")
        if self.session_code not in (CalendarSegment.A, CalendarSegment.L, CalendarSegment.N):
            raise FPI03Error("FP_TRC_SESSION_CODE_INVALID", "session window requires A/L/N")
        if self.end_utc_ms <= self.start_utc_ms or self.elapsed_seconds != (self.end_utc_ms - self.start_utc_ms) // 1000:
            raise FPI03Error("FP_TRC_SESSION_INTERVAL_INVALID", "session interval mismatch")

    @property
    def window_id(self) -> str:
        return stable_id("FPSESS", self, 32)

    def to_i02_window_key(self, context_id: str, pair_id: str, data_revision: str = "") -> WindowKey:
        kind = {CalendarSegment.A: WindowKind.A, CalendarSegment.L: WindowKind.L, CalendarSegment.N: WindowKind.N}[self.session_code]
        return WindowKey(
            context_id=context_id,
            pair_id=pair_id,
            kind=kind,
            scope=WindowScope.SAME_TRADING_DAY,
            trading_day_id=self.trading_day_id,
            start_utc_ms=self.start_utc_ms,
            end_utc_ms=self.end_utc_ms,
            timezone=TIMEZONE_NAME,
            data_revision=data_revision,
        )


@dataclass(frozen=True, slots=True)
class WeekWindow:
    week_id: str
    start_date: str
    end_date: str
    start_ny_iso: str
    end_ny_iso: str
    start_utc_ms: int
    end_utc_ms: int
    elapsed_seconds: int
    state: WeekState
    contains_reference_time: bool
    calendar_version: str

    def __post_init__(self) -> None:
        _required(self.week_id, "week_id")
        if self.end_utc_ms <= self.start_utc_ms or self.elapsed_seconds != (self.end_utc_ms - self.start_utc_ms) // 1000:
            raise FPI03Error("FP_TRC_WEEK_INTERVAL_INVALID", "week interval mismatch")

    @property
    def window_id(self) -> str:
        return stable_id("FPWEEK", self, 32)

    def to_i02_window_key(self, context_id: str, pair_id: str, data_revision: str = "") -> WindowKey:
        return WindowKey(
            context_id=context_id,
            pair_id=pair_id,
            kind=WindowKind.W,
            scope=WindowScope.CURRENT_NY_WEEK,
            trading_day_id=f"NYDAY-{self.end_date}",
            start_utc_ms=self.start_utc_ms,
            end_utc_ms=self.end_utc_ms,
            timezone=TIMEZONE_NAME,
            week_id=self.week_id,
            data_revision=data_revision,
        )


@dataclass(frozen=True, slots=True)
class BoundaryEvidence:
    boundary_kind: BoundaryKind
    local_iso: str
    utc_epoch_ms: int
    resolved_offset_minutes: int
    resolution_policy: LocalResolutionPolicy
    reason_code: str

    def __post_init__(self) -> None:
        _required(self.local_iso, "local_iso")
        if self.utc_epoch_ms < 0:
            raise FPI03Error("FP_TRC_TIMESTAMP_INVALID", "boundary UTC must be non-negative")
        if self.resolved_offset_minutes not in (-300, -240):
            raise FPI03Error("FP_TRC_NY_OFFSET_INVALID", "boundary offset invalid")
        _required(self.reason_code, "reason_code")

    @property
    def evidence_id(self) -> str:
        return stable_id("FPBOUND", self, 32)


@dataclass(frozen=True, slots=True)
class CalendarSnapshot:
    snapshot_id: str
    reference_utc_ms: int
    ny_timestamp: NyTimestamp
    trading_day: TradingDayWindow
    segment: CalendarSegment
    session: SessionWindow | None
    week: WeekWindow
    daily_gap_start_utc_ms: int
    daily_gap_end_utc_ms: int
    health: CalendarHealth
    reason_code: str
    config_hash: str
    boundary_evidence_hash: str

    def __post_init__(self) -> None:
        _required(self.snapshot_id, "snapshot_id")
        require_sha256(self.config_hash, "config_hash")
        require_sha256(self.boundary_evidence_hash, "boundary_evidence_hash")
        if self.reference_utc_ms != self.ny_timestamp.utc_epoch_ms:
            raise FPI03Error("FP_TRC_SNAPSHOT_TIME_MISMATCH", "snapshot reference and NY timestamp differ")
        if self.segment in (CalendarSegment.A, CalendarSegment.L, CalendarSegment.N) and self.session is None:
            raise FPI03Error("FP_TRC_SESSION_MISSING", "active session segment requires session window")
        if self.segment in (CalendarSegment.DAILY_GAP, CalendarSegment.WEEKEND_CLOSED) and self.session is not None:
            raise FPI03Error("FP_TRC_SESSION_UNEXPECTED", "closed/gap segment cannot carry session window")
        _required(self.reason_code, "reason_code")


@dataclass(frozen=True, slots=True)
class CalendarRegistrySnapshot:
    registry_version: str
    sessions: tuple[SessionDefinition, ...]
    timezone_name: str
    time_rule_version: str
    calendar_version: str
    frozen: bool = True

    def __post_init__(self) -> None:
        codes = tuple(item.code for item in self.sessions)
        if codes != (CalendarSegment.A, CalendarSegment.L, CalendarSegment.N):
            raise FPI03Error("FP_TRC_SESSION_REGISTRY_INVALID", "registry must contain A,L,N in canonical order")
        if not self.frozen:
            raise FPI03Error("FP_TRC_SESSION_REGISTRY_MUTABLE", "canonical registry must be frozen")

    @property
    def registry_hash(self) -> str:
        return canonical_sha256(self)


def canonical_session_definitions() -> tuple[SessionDefinition, ...]:
    return (
        SessionDefinition(CalendarSegment.A, A_START_SECOND, A_END_SECOND, True, 0),
        SessionDefinition(CalendarSegment.L, L_START_SECOND, L_END_SECOND, False, 1),
        SessionDefinition(CalendarSegment.N, N_START_SECOND, N_END_SECOND, False, 2),
    )


def canonical_registry_snapshot() -> CalendarRegistrySnapshot:
    return CalendarRegistrySnapshot(
        registry_version=SESSION_REGISTRY_VERSION,
        sessions=canonical_session_definitions(),
        timezone_name=TIMEZONE_NAME,
        time_rule_version=TIME_RULE_VERSION,
        calendar_version=CALENDAR_VERSION,
    )
