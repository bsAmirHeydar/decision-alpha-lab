from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from .acquire import AcquisitionResult
from .canonical import sha256_material
from .session_calendar import (
    HOLIDAY_RULE_VERSION,
    MINUTE_MS,
    ScheduledClosure,
    classify_scheduled_closure,
    collapse_minute_runs,
    resolve_calendar_profile,
)

NY = ZoneInfo("America/New_York")
MINUTE = MINUTE_MS


@dataclass(frozen=True, slots=True)
class QualityResult:
    status: str
    common_start_ms: int
    common_end_ms: int
    primary_bars: tuple
    secondary_bars: tuple
    report: dict


def _weekly_closed(ms: int) -> bool:
    local = datetime.fromtimestamp(ms / 1000, timezone.utc).astimezone(NY)
    weekday = local.weekday()
    minute = local.hour * 60 + local.minute
    return weekday == 4 and minute >= 17 * 60 or weekday == 5 or weekday == 6 and minute < 18 * 60


def _max_run(values: list[int]) -> int:
    best = run = 0
    previous = None
    for value in values:
        run = run + 1 if previous is not None and value - previous == MINUTE else 1
        best = max(best, run)
        previous = value
    return best


def validate_pair(
    primary: AcquisitionResult,
    secondary: AcquisitionResult,
    policy,
    minimum_common_days: int = 0,
) -> QualityResult:
    primary_by_open = {bar.bar_open_time_utc_ms: bar for bar in primary.bars}
    secondary_by_open = {bar.bar_open_time_utc_ms: bar for bar in secondary.bars}
    common = sorted(set(primary_by_open) & set(secondary_by_open))
    if not common:
        raise ValueError("no common M1 history")

    start = max(min(primary_by_open), min(secondary_by_open))
    end = min(
        max(bar.bar_close_time_utc_ms for bar in primary_by_open.values()),
        max(bar.bar_close_time_utc_ms for bar in secondary_by_open.values()),
    )
    expected = list(range(start, end, MINUTE))
    primary_missing = [
        timestamp
        for timestamp in expected
        if timestamp not in primary_by_open and not _weekly_closed(timestamp)
    ]
    secondary_missing = [
        timestamp
        for timestamp in expected
        if timestamp not in secondary_by_open and not _weekly_closed(timestamp)
    ]

    primary_missing_set = set(primary_missing)
    secondary_missing_set = set(secondary_missing)
    primary_only = sorted(primary_missing_set - secondary_missing_set)
    secondary_only = sorted(secondary_missing_set - primary_missing_set)
    joint = sorted(primary_missing_set & secondary_missing_set)

    symbol_specific_ratio = (len(primary_only) + len(secondary_only)) / max(1, 2 * len(expected))
    blockers: list[str] = []
    if len(common) < policy.minimum_common_bars:
        blockers.append("INSUFFICIENT_COMMON_M1_BARS")
    common_duration_days = (max(common) + MINUTE - min(common)) / 86_400_000
    if minimum_common_days > 0 and common_duration_days < minimum_common_days:
        blockers.append("INSUFFICIENT_COMMON_HISTORY_DAYS")
    if symbol_specific_ratio > policy.max_symbol_specific_gap_ratio:
        blockers.append("SYMBOL_SPECIFIC_GAP_RATIO_EXCEEDED")

    primary_only_max_run = _max_run(primary_only)
    secondary_only_max_run = _max_run(secondary_only)
    joint_max_run = _max_run(joint)
    if max(primary_only_max_run, secondary_only_max_run) > policy.max_unexplained_gap_minutes:
        blockers.append("UNEXPLAINED_SYMBOL_SPECIFIC_GAP_EXCEEDS_POLICY")

    joint_intervals = collapse_minute_runs(joint)
    scheduled_closures: list[ScheduledClosure] = []
    declared_short_intervals = []
    unexplained_long_intervals = []
    calendar_resolution = resolve_calendar_profile(
        primary.symbol,
        secondary.symbol,
        policy.session_calendar_profile,
    )

    for interval in joint_intervals:
        closure, _ = classify_scheduled_closure(
            interval,
            primary.symbol,
            secondary.symbol,
            policy.session_calendar_profile,
            policy.max_scheduled_closure_minutes,
            policy.require_scheduled_closure_boundary_bars,
            set(primary_by_open),
            set(secondary_by_open),
        )
        if closure is not None:
            scheduled_closures.append(closure)
        elif interval.duration_minutes > policy.max_joint_gap_minutes:
            unexplained_long_intervals.append(interval)
        else:
            declared_short_intervals.append(interval)

    if unexplained_long_intervals:
        blockers.append("UNEXPLAINED_JOINT_GAP_EXCEEDS_POLICY")

    status = (
        "BLOCKED"
        if blockers
        else "PASS_WITH_DECLARED_NON_CRITICAL_GAPS"
        if primary_missing or secondary_missing
        else "PASS"
    )
    common_start = min(common)
    common_end = max(common) + MINUTE

    scheduled_dicts = [closure.to_dict() for closure in scheduled_closures]
    report = {
        "report_id": "RTHP_MT5_M1_QUALITY_V2",
        "schema_version": "1.1.0",
        "status": status,
        "blockers": blockers,
        "canonical_source_timeframe": "M1_CLOSED_BARS",
        "sub_m1_source_allowed": False,
        "synthetic_ticks_allowed": False,
        "primary_bar_count": len(primary_by_open),
        "secondary_bar_count": len(secondary_by_open),
        "common_bar_count": len(common),
        "common_start_utc_ms": common_start,
        "common_end_utc_ms": common_end,
        "primary_missing_open_minutes": len(primary_missing),
        "secondary_missing_open_minutes": len(secondary_missing),
        "primary_only_gap_count": len(primary_only),
        "secondary_only_gap_count": len(secondary_only),
        "joint_gap_count": len(joint),
        "joint_gap_interval_count": len(joint_intervals),
        "max_primary_only_gap_run_minutes": primary_only_max_run,
        "max_secondary_only_gap_run_minutes": secondary_only_max_run,
        "max_joint_gap_run_minutes": joint_max_run,
        "max_unexplained_joint_gap_run_minutes": max(
            (interval.duration_minutes for interval in unexplained_long_intervals),
            default=0,
        ),
        "common_duration_days": common_duration_days,
        "minimum_common_days_required": minimum_common_days,
        "symbol_specific_gap_ratio": symbol_specific_ratio,
        "session_calendar_profile": calendar_resolution.resolved_profile,
        "session_calendar_resolution": calendar_resolution.to_dict(),
        "holiday_rule_version": HOLIDAY_RULE_VERSION,
        "scheduled_closure_interval_count": len(scheduled_closures),
        "scheduled_closure_minutes": sum(closure.duration_minutes for closure in scheduled_closures),
        "scheduled_closure_intervals": scheduled_dicts,
        "declared_short_joint_gap_interval_count": len(declared_short_intervals),
        "declared_short_joint_gap_minutes": sum(interval.duration_minutes for interval in declared_short_intervals),
        "unexplained_long_joint_gap_interval_count": len(unexplained_long_intervals),
        "unexplained_long_joint_gap_minutes": sum(interval.duration_minutes for interval in unexplained_long_intervals),
        "unexplained_long_joint_gap_intervals": [
            {
                "start_utc_ms": interval.start_ms,
                "end_utc_ms": interval.end_ms,
                "duration_minutes": interval.duration_minutes,
            }
            for interval in unexplained_long_intervals
        ],
        "scheduled_closures_are_forward_filled": False,
        "m15_missingness_is_unconfirmed": True,
        "forward_fill_allowed": False,
    }
    report["calendar_evidence_digest"] = sha256_material(
        {
            "profile": calendar_resolution.to_dict(),
            "holiday_rule_version": HOLIDAY_RULE_VERSION,
            "scheduled_closures": scheduled_dicts,
        }
    )
    report["report_digest"] = sha256_material(report)

    return QualityResult(
        status,
        common_start,
        common_end,
        tuple(
            bar
            for bar in primary.bars
            if common_start <= bar.bar_open_time_utc_ms and bar.bar_close_time_utc_ms <= common_end
        ),
        tuple(
            bar
            for bar in secondary.bars
            if common_start <= bar.bar_open_time_utc_ms and bar.bar_close_time_utc_ms <= common_end
        ),
        report,
    )
