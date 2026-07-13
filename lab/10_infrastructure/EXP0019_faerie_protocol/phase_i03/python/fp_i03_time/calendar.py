"""Trading-day, A/L/N session, daily-gap, and NY-week calendar engine."""
from __future__ import annotations

from datetime import date, datetime, time, timedelta

from fp_i02_kernel.canonical import canonical_sha256, stable_id

from .constants import (
    A_END_SECOND, A_START_SECOND, GAP_END_SECOND, GAP_START_SECOND, L_END_SECOND, L_START_SECOND,
    N_END_SECOND, N_START_SECOND, TIMEZONE_NAME,
)
from .contracts import (
    BoundaryEvidence, CalendarSnapshot, SessionDefinition, SessionWindow, TimeKernelConfig,
    TradingDayWindow, WeekWindow, canonical_session_definitions,
)
from .enums import (
    BoundaryKind, CalendarHealth, CalendarSegment, LocalResolutionPolicy, WeekState,
)
from .errors import FPI03Error
from .time_math import resolve_local, utc_to_new_york


def _local_midnight(day: date) -> datetime:
    return datetime.combine(day, time(0, 0))


def _at_second(day: date, second: int) -> datetime:
    return _local_midnight(day) + timedelta(seconds=second)


def _resolve_boundary(local_dt: datetime, kind: BoundaryKind, policy: LocalResolutionPolicy, config: TimeKernelConfig) -> tuple[int, BoundaryEvidence]:
    resolution = resolve_local(local_dt, policy, config)
    if resolution.selected_utc_ms is None:
        raise FPI03Error(resolution.reason_code, f"cannot resolve {kind.value}", {"local": resolution.local_iso})
    ny = utc_to_new_york(resolution.selected_utc_ms, config)
    evidence = BoundaryEvidence(
        boundary_kind=kind,
        local_iso=resolution.local_iso,
        utc_epoch_ms=resolution.selected_utc_ms,
        resolved_offset_minutes=ny.utc_offset_minutes,
        resolution_policy=policy,
        reason_code=resolution.reason_code,
    )
    return resolution.selected_utc_ms, evidence


def trading_date_for_local(local_ny: datetime) -> date:
    second = local_ny.hour * 3600 + local_ny.minute * 60 + local_ny.second
    return local_ny.date() + timedelta(days=1) if second >= A_START_SECOND else local_ny.date()


def trading_day_id(trading_date: date) -> str:
    return f"NYDAY-{trading_date.isoformat()}"


def build_trading_day(trading_date: date, config: TimeKernelConfig | None = None) -> tuple[TradingDayWindow, tuple[BoundaryEvidence, ...]]:
    config = config or TimeKernelConfig()
    start_local = _at_second(trading_date - timedelta(days=1), A_START_SECOND)
    end_local = _at_second(trading_date, GAP_START_SECOND)
    start_utc, start_ev = _resolve_boundary(start_local, BoundaryKind.TRADING_DAY_START, config.ambiguous_start_policy, config)
    end_utc, end_ev = _resolve_boundary(end_local, BoundaryKind.TRADING_DAY_END, config.ambiguous_end_policy, config)
    window = TradingDayWindow(
        trading_day_id=trading_day_id(trading_date),
        trading_date=trading_date.isoformat(),
        start_ny_iso=start_local.isoformat(timespec="seconds"),
        end_ny_iso=end_local.isoformat(timespec="seconds"),
        start_utc_ms=start_utc,
        end_utc_ms=end_utc,
        elapsed_seconds=(end_utc - start_utc) // 1000,
        timezone_name=TIMEZONE_NAME,
        calendar_version=config.calendar_version,
    )
    return window, (start_ev, end_ev)


def session_definition(code: CalendarSegment) -> SessionDefinition:
    for item in canonical_session_definitions():
        if item.code is code:
            return item
    raise FPI03Error("FP_TRC_SESSION_CODE_INVALID", f"unknown session code {code}")


def classify_intraday_segment(local_ny: datetime) -> CalendarSegment:
    second = local_ny.hour * 3600 + local_ny.minute * 60 + local_ny.second
    if second >= A_START_SECOND or second < A_END_SECOND:
        return CalendarSegment.A
    if L_START_SECOND <= second < L_END_SECOND:
        return CalendarSegment.L
    if N_START_SECOND <= second < N_END_SECOND:
        return CalendarSegment.N
    if GAP_START_SECOND <= second < GAP_END_SECOND:
        return CalendarSegment.DAILY_GAP
    raise FPI03Error("FP_TRC_SEGMENT_UNCLASSIFIED", "second of day did not map to A/L/N/gap")


def build_session(trading_date: date, code: CalendarSegment, reference_utc_ms: int | None = None, config: TimeKernelConfig | None = None) -> tuple[SessionWindow, tuple[BoundaryEvidence, ...]]:
    config = config or TimeKernelConfig()
    definition = session_definition(code)
    if code is CalendarSegment.A:
        start_local = _at_second(trading_date - timedelta(days=1), A_START_SECOND)
        end_local = _at_second(trading_date, A_END_SECOND)
    else:
        start_local = _at_second(trading_date, definition.start_second)
        end_local = _at_second(trading_date, definition.end_second)
    start_utc, start_ev = _resolve_boundary(start_local, BoundaryKind.SESSION_START, config.ambiguous_start_policy, config)
    end_utc, end_ev = _resolve_boundary(end_local, BoundaryKind.SESSION_END, config.ambiguous_end_policy, config)
    contains = reference_utc_ms is not None and start_utc <= reference_utc_ms < end_utc
    sid = f"FPSESSION-{trading_date.isoformat()}-{code.value}"
    window = SessionWindow(
        session_id=sid,
        session_code=code,
        trading_day_id=trading_day_id(trading_date),
        trading_date=trading_date.isoformat(),
        start_ny_iso=start_local.isoformat(timespec="seconds"),
        end_ny_iso=end_local.isoformat(timespec="seconds"),
        start_utc_ms=start_utc,
        end_utc_ms=end_utc,
        elapsed_seconds=(end_utc - start_utc) // 1000,
        contains_reference_time=contains,
        registry_version=config.session_registry_version,
    )
    return window, (start_ev, end_ev)


def build_daily_gap(trading_date: date, config: TimeKernelConfig | None = None) -> tuple[int, int, tuple[BoundaryEvidence, ...]]:
    config = config or TimeKernelConfig()
    start_local = _at_second(trading_date, GAP_START_SECOND)
    end_local = _at_second(trading_date, GAP_END_SECOND)
    start_utc, start_ev = _resolve_boundary(start_local, BoundaryKind.DAILY_GAP_START, config.ambiguous_start_policy, config)
    end_utc, end_ev = _resolve_boundary(end_local, BoundaryKind.DAILY_GAP_END, config.ambiguous_end_policy, config)
    return start_utc, end_utc, (start_ev, end_ev)


def _most_recent_sunday(local_ny: datetime) -> date:
    days_since_sunday = (local_ny.weekday() + 1) % 7
    sunday = local_ny.date() - timedelta(days=days_since_sunday)
    if local_ny < _at_second(sunday, A_START_SECOND):
        sunday -= timedelta(days=7)
    return sunday


def build_week_from_sunday(start_sunday: date, reference_utc_ms: int | None = None, config: TimeKernelConfig | None = None) -> tuple[WeekWindow, tuple[BoundaryEvidence, ...]]:
    config = config or TimeKernelConfig()
    if start_sunday.weekday() != 6:
        raise FPI03Error("FP_TRC_WEEK_START_NOT_SUNDAY", "week start date must be Sunday")
    end_friday = start_sunday + timedelta(days=5)
    start_local = _at_second(start_sunday, A_START_SECOND)
    end_local = _at_second(end_friday, GAP_START_SECOND)
    start_utc, start_ev = _resolve_boundary(start_local, BoundaryKind.WEEK_START, config.ambiguous_start_policy, config)
    end_utc, end_ev = _resolve_boundary(end_local, BoundaryKind.WEEK_END, config.ambiguous_end_policy, config)
    contains = reference_utc_ms is not None and start_utc <= reference_utc_ms < end_utc
    if contains:
        state = WeekState.ACTIVE
    elif reference_utc_ms is not None and reference_utc_ms >= end_utc:
        state = WeekState.CLOSED_AFTER_FRIDAY
    else:
        state = WeekState.CLOSED_BEFORE_SUNDAY_OPEN
    week_id = f"NYWEEK-{start_sunday.isoformat()}"
    window = WeekWindow(
        week_id=week_id,
        start_date=start_sunday.isoformat(),
        end_date=end_friday.isoformat(),
        start_ny_iso=start_local.isoformat(timespec="seconds"),
        end_ny_iso=end_local.isoformat(timespec="seconds"),
        start_utc_ms=start_utc,
        end_utc_ms=end_utc,
        elapsed_seconds=(end_utc - start_utc) // 1000,
        state=state,
        contains_reference_time=contains,
        calendar_version=config.calendar_version,
    )
    return window, (start_ev, end_ev)


def week_for_reference(reference_utc_ms: int, config: TimeKernelConfig | None = None) -> tuple[WeekWindow, tuple[BoundaryEvidence, ...]]:
    config = config or TimeKernelConfig()
    ny = utc_to_new_york(reference_utc_ms, config)
    local = datetime.fromisoformat(ny.local_iso)
    sunday = _most_recent_sunday(local)
    return build_week_from_sunday(sunday, reference_utc_ms, config)


def previous_completed_week(reference_utc_ms: int, config: TimeKernelConfig | None = None) -> WeekWindow:
    config = config or TimeKernelConfig()
    current, _ = week_for_reference(reference_utc_ms, config)
    start = date.fromisoformat(current.start_date)
    if current.contains_reference_time:
        target = start - timedelta(days=7)
    else:
        # During the weekend closure, the just-closed week is the previous completed week.
        target = start
    return build_week_from_sunday(target, None, config)[0]


def snapshot(reference_utc_ms: int, config: TimeKernelConfig | None = None) -> CalendarSnapshot:
    config = config or TimeKernelConfig()
    ny = utc_to_new_york(reference_utc_ms, config)
    local = datetime.fromisoformat(ny.local_iso)
    tdate = trading_date_for_local(local)
    tday, tday_ev = build_trading_day(tdate, config)
    gap_start, gap_end, gap_ev = build_daily_gap(tdate, config)
    week, week_ev = week_for_reference(reference_utc_ms, config)
    intraday = classify_intraday_segment(local)
    evidence = list(tday_ev + gap_ev + week_ev)
    if week.contains_reference_time:
        segment = intraday
    else:
        segment = CalendarSegment.WEEKEND_CLOSED
    session = None
    if segment in (CalendarSegment.A, CalendarSegment.L, CalendarSegment.N):
        session, session_ev = build_session(tdate, segment, reference_utc_ms, config)
        evidence.extend(session_ev)
        if not session.contains_reference_time:
            raise FPI03Error("FP_TRC_SESSION_OWNERSHIP_MISMATCH", "classified session does not contain reference time")
    reason = {
        CalendarSegment.A: "FP_TRC_SESSION_A",
        CalendarSegment.L: "FP_TRC_SESSION_L",
        CalendarSegment.N: "FP_TRC_SESSION_N",
        CalendarSegment.DAILY_GAP: "FP_TRC_DAILY_GAP",
        CalendarSegment.WEEKEND_CLOSED: "FP_TRC_WEEKEND_CLOSED",
    }[segment]
    evidence_hash = canonical_sha256(evidence)
    material = {
        "reference_utc_ms": reference_utc_ms,
        "ny_timestamp_id": ny.timestamp_id,
        "trading_day_window_id": tday.window_id,
        "segment": segment.value,
        "session_window_id": session.window_id if session else "",
        "week_window_id": week.window_id,
        "config_hash": config.config_hash,
        "boundary_evidence_hash": evidence_hash,
    }
    return CalendarSnapshot(
        snapshot_id=stable_id("FPCAL", material, 32),
        reference_utc_ms=reference_utc_ms,
        ny_timestamp=ny,
        trading_day=tday,
        segment=segment,
        session=session,
        week=week,
        daily_gap_start_utc_ms=gap_start,
        daily_gap_end_utc_ms=gap_end,
        health=CalendarHealth.READY,
        reason_code=reason,
        config_hash=config.config_hash,
        boundary_evidence_hash=evidence_hash,
    )
