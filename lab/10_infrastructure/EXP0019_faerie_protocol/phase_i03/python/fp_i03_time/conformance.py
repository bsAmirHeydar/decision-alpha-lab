"""Executable FP-I03 conformance report."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fp_i02_kernel.canonical import canonical_sha256
from .calendar import build_session, build_week_from_sunday, snapshot
from .contracts import TimeKernelConfig, canonical_registry_snapshot
from .enums import CalendarSegment, LocalResolutionPolicy, LocalTimeStatus
from .golden import golden_vector_material, utc_ms
from .registry import DEFAULT_TIME_CONTRACT_REGISTRY
from .time_math import resolve_local, utc_to_new_york


@dataclass(frozen=True, slots=True)
class ConformanceCheck:
    check_id: str
    passed: bool
    detail: str


def run_conformance() -> dict:
    config = TimeKernelConfig()
    checks: list[ConformanceCheck] = []
    registry = canonical_registry_snapshot()
    checks.append(ConformanceCheck("registry_frozen", registry.frozen, registry.registry_hash))
    checks.append(ConformanceCheck("contract_count", len(DEFAULT_TIME_CONTRACT_REGISTRY.all()) == 11, str(len(DEFAULT_TIME_CONTRACT_REGISTRY.all()))))
    # Differential UTC->NY check against host IANA database over transition-heavy dates.
    zone = ZoneInfo("America/New_York")
    points = []
    for year in (2007, 2020, 2026, 2035):
        for month, day in ((3, 1), (3, 8), (3, 15), (7, 1), (11, 1), (11, 8), (12, 1)):
            for hour in (0, 5, 6, 7, 12, 23):
                points.append(datetime(year, month, min(day, 28), hour, tzinfo=timezone.utc))
    mismatch = []
    for point in points:
        ours = utc_to_new_york(point, config)
        theirs = point.astimezone(zone)
        if ours.utc_offset_minutes != int(theirs.utcoffset().total_seconds() // 60) or ours.local_iso[:19] != theirs.replace(tzinfo=None).isoformat(timespec="seconds"):
            mismatch.append(point.isoformat())
    checks.append(ConformanceCheck("iana_differential", not mismatch, f"points={len(points)} mismatch={mismatch[:3]}"))
    ambiguous = resolve_local(datetime(2026, 11, 1, 1, 30), LocalResolutionPolicy.REJECT, config)
    checks.append(ConformanceCheck("fall_ambiguous", ambiguous.status is LocalTimeStatus.AMBIGUOUS and len(ambiguous.candidate_utc_ms) == 2, str(ambiguous.candidate_utc_ms)))
    nonexistent = resolve_local(datetime(2026, 3, 8, 2, 30), LocalResolutionPolicy.REJECT, config)
    checks.append(ConformanceCheck("spring_nonexistent", nonexistent.status is LocalTimeStatus.NONEXISTENT, nonexistent.reason_code))
    # Exact half-open boundaries.
    boundary_expectations = {
        "2026-07-12T21:59:59Z": CalendarSegment.WEEKEND_CLOSED,
        "2026-07-12T22:00:00Z": CalendarSegment.A,
        "2026-07-13T07:59:59Z": CalendarSegment.A,
        "2026-07-13T08:00:00Z": CalendarSegment.L,
        "2026-07-13T13:29:59Z": CalendarSegment.L,
        "2026-07-13T13:30:00Z": CalendarSegment.N,
        "2026-07-13T20:59:59Z": CalendarSegment.N,
        "2026-07-13T21:00:00Z": CalendarSegment.DAILY_GAP,
        "2026-07-13T22:00:00Z": CalendarSegment.A,
        "2026-07-17T21:00:00Z": CalendarSegment.WEEKEND_CLOSED,
    }
    for iso, expected in boundary_expectations.items():
        actual = snapshot(utc_ms(iso), config).segment
        checks.append(ConformanceCheck(f"boundary_{iso}", actual is expected, f"{actual.value}/{expected.value}"))
    # Session and week windows fixed by civil boundaries.
    monday = datetime(2026, 7, 13).date()
    for code, expected_seconds in ((CalendarSegment.A, 10 * 3600), (CalendarSegment.L, 5 * 3600 + 30 * 60), (CalendarSegment.N, 7 * 3600 + 30 * 60)):
        window = build_session(monday, code)[0]
        checks.append(ConformanceCheck(f"duration_{code.value}", window.elapsed_seconds == expected_seconds, str(window.elapsed_seconds)))
    week = build_week_from_sunday(datetime(2026, 7, 12).date())[0]
    checks.append(ConformanceCheck("week_duration", week.elapsed_seconds == 119 * 3600, str(week.elapsed_seconds)))
    checks.append(ConformanceCheck("golden_vector", len(golden_vector_material()["vector_hash"]) == 64, golden_vector_material()["vector_hash"]))
    passed = all(item.passed for item in checks)
    payload = {"phase": "FP-I03", "passed": passed, "check_count": len(checks), "checks": [asdict(item) for item in checks]}
    payload["report_hash"] = canonical_sha256(payload)
    return payload
