"""Deterministic US/New York DST math, independent of host broker timezone."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from .constants import MAX_SUPPORTED_YEAR, MIN_SUPPORTED_YEAR, TIME_RULE_VERSION, TIMEZONE_NAME
from .contracts import LocalResolution, NyTimestamp, TimeKernelConfig
from .enums import DstRegime, LocalResolutionPolicy, LocalTimeStatus
from .errors import FPI03Error

UTC = timezone.utc


def _check_year(year: int, config: TimeKernelConfig) -> None:
    if year < config.minimum_supported_year or year > config.maximum_supported_year:
        raise FPI03Error("FP_TRC_YEAR_UNSUPPORTED", f"year {year} outside configured deterministic rule range")


def _nth_weekday(year: int, month: int, weekday: int, occurrence: int) -> date:
    first = date(year, month, 1)
    delta = (weekday - first.weekday()) % 7
    return first + timedelta(days=delta + 7 * (occurrence - 1))


def dst_start_utc(year: int, config: TimeKernelConfig | None = None) -> datetime:
    config = config or TimeKernelConfig()
    _check_year(year, config)
    second_sunday = _nth_weekday(year, 3, 6, 2)
    return datetime(second_sunday.year, 3, second_sunday.day, 7, 0, tzinfo=UTC)


def dst_end_utc(year: int, config: TimeKernelConfig | None = None) -> datetime:
    config = config or TimeKernelConfig()
    _check_year(year, config)
    first_sunday = _nth_weekday(year, 11, 6, 1)
    return datetime(first_sunday.year, 11, first_sunday.day, 6, 0, tzinfo=UTC)


def is_dst_utc(utc_dt: datetime, config: TimeKernelConfig | None = None) -> bool:
    config = config or TimeKernelConfig()
    utc_dt = require_aware_utc(utc_dt)
    _check_year(utc_dt.year, config)
    return dst_start_utc(utc_dt.year, config) <= utc_dt < dst_end_utc(utc_dt.year, config)


def utc_offset_minutes(utc_dt: datetime, config: TimeKernelConfig | None = None) -> int:
    return -240 if is_dst_utc(utc_dt, config) else -300


def require_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise FPI03Error("FP_TRC_UTC_NAIVE", "UTC datetime must be timezone-aware")
    return value.astimezone(UTC)


def epoch_ms(value: datetime) -> int:
    return int(require_aware_utc(value).timestamp() * 1000)


def utc_from_epoch_ms(value: int) -> datetime:
    if not isinstance(value, int) or value < 0:
        raise FPI03Error("FP_TRC_TIMESTAMP_INVALID", "epoch milliseconds must be non-negative integer")
    return datetime.fromtimestamp(value / 1000, tz=UTC)


def utc_to_new_york(value: datetime | int, config: TimeKernelConfig | None = None) -> NyTimestamp:
    config = config or TimeKernelConfig()
    utc_dt = utc_from_epoch_ms(value) if isinstance(value, int) else require_aware_utc(value)
    offset = utc_offset_minutes(utc_dt, config)
    local = (utc_dt + timedelta(minutes=offset)).replace(tzinfo=None)
    end = dst_end_utc(utc_dt.year, config)
    fold = 1 if end <= utc_dt < end + timedelta(hours=1) else 0
    return NyTimestamp(
        utc_epoch_ms=epoch_ms(utc_dt),
        local_iso=local.isoformat(timespec="milliseconds"),
        local_date=local.date().isoformat(),
        second_of_day=local.hour * 3600 + local.minute * 60 + local.second,
        utc_offset_minutes=offset,
        dst_regime=DstRegime.DAYLIGHT if offset == -240 else DstRegime.STANDARD,
        fold=fold,
        timezone_name=TIMEZONE_NAME,
        time_rule_version=config.time_rule_version,
    )


def _same_local(left: datetime, right: NyTimestamp) -> bool:
    normalized = left.replace(microsecond=(left.microsecond // 1000) * 1000)
    return normalized.isoformat(timespec="milliseconds") == right.local_iso


def local_candidates_utc_ms(local_ny: datetime, config: TimeKernelConfig | None = None) -> tuple[int, ...]:
    config = config or TimeKernelConfig()
    if local_ny.tzinfo is not None:
        raise FPI03Error("FP_TRC_LOCAL_AWARE", "New York civil input must be naive")
    _check_year(local_ny.year, config)
    candidates: list[int] = []
    for offset in (-240, -300):
        candidate = (local_ny - timedelta(minutes=offset)).replace(tzinfo=UTC)
        snapshot = utc_to_new_york(candidate, config)
        if _same_local(local_ny, snapshot):
            candidates.append(epoch_ms(candidate))
    return tuple(sorted(set(candidates)))


def resolve_local(
    local_ny: datetime,
    policy: LocalResolutionPolicy,
    config: TimeKernelConfig | None = None,
) -> LocalResolution:
    config = config or TimeKernelConfig()
    candidates = local_candidates_utc_ms(local_ny, config)
    if not candidates:
        status = LocalTimeStatus.NONEXISTENT
        selected = None
        reason = "FP_TRC_LOCAL_NONEXISTENT"
    elif len(candidates) == 1:
        status = LocalTimeStatus.UNIQUE
        selected = candidates[0]
        reason = "FP_TRC_LOCAL_UNIQUE"
    else:
        status = LocalTimeStatus.AMBIGUOUS
        if policy is LocalResolutionPolicy.EARLIEST:
            selected = candidates[0]
            reason = "FP_TRC_LOCAL_AMBIGUOUS_EARLIEST"
        elif policy is LocalResolutionPolicy.LATEST:
            selected = candidates[-1]
            reason = "FP_TRC_LOCAL_AMBIGUOUS_LATEST"
        else:
            selected = None
            reason = "FP_TRC_LOCAL_AMBIGUOUS_REJECTED"
    return LocalResolution(
        local_iso=local_ny.isoformat(timespec="milliseconds"),
        status=status,
        candidate_utc_ms=candidates,
        selected_utc_ms=selected,
        policy=policy,
        reason_code=reason,
        time_rule_version=config.time_rule_version,
    )


def require_resolved_local(
    local_ny: datetime,
    policy: LocalResolutionPolicy,
    config: TimeKernelConfig | None = None,
) -> tuple[int, LocalResolution]:
    resolution = resolve_local(local_ny, policy, config)
    if resolution.selected_utc_ms is None:
        raise FPI03Error(resolution.reason_code, "New York local boundary could not be resolved", {"local": resolution.local_iso})
    return resolution.selected_utc_ms, resolution
