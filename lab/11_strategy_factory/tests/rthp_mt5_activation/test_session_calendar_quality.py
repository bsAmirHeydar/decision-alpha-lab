from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from strategy_factory_rthp_mt5_activation_v1.acquire import AcquisitionResult
from strategy_factory_rthp_mt5_activation_v1.config import QualityConfig
from strategy_factory_rthp_mt5_activation_v1.m1_schema import CanonicalM1Bar
from strategy_factory_rthp_mt5_activation_v1.quality import validate_pair
from strategy_factory_rthp_mt5_activation_v1.session_calendar import (
    PROFILE_US_INDEX_CFD_NY,
    PROFILE_WEEKLY_ONLY,
    collapse_minute_runs,
    resolve_calendar_profile,
    us_market_holidays,
)
from strategy_factory_rthp_mt5_activation_v1.symbols import ResolvedSymbol

MINUTE = 60_000


def _symbol(name: str, description: str, path: str = "Spot\\Indices\\Major") -> ResolvedSymbol:
    metadata = {
        "name": name,
        "description": description,
        "path": path,
        "canonical_instrument_id": name,
        "currency_profit": "USD",
        "trade_tick_size": 0.01,
    }
    return ResolvedSymbol(name, name, name, metadata, "sha256:test")


def _bar(symbol: str, open_ms: int) -> CanonicalM1Bar:
    return CanonicalM1Bar(
        symbol=symbol,
        canonical_instrument_id=symbol,
        timeframe_seconds=60,
        bar_open_time_utc_ms=open_ms,
        bar_close_time_utc_ms=open_ms + MINUTE,
        known_time_utc_ms=open_ms + MINUTE,
        open=100.0,
        high=101.0,
        low=99.0,
        close=100.5,
        tick_volume=1,
        spread=1,
        real_volume=0,
        tick_size=0.01,
        source_sequence=open_ms // MINUTE,
        source_terminal_id="TEST",
        source_revision="R1",
    )


def _pair_with_joint_gap(profile_symbols: bool = True) -> tuple[AcquisitionResult, AcquisitionResult]:
    start = datetime(2026, 5, 25, 16, 0, tzinfo=timezone.utc)
    end = datetime(2026, 5, 26, 4, 0, tzinfo=timezone.utc)
    gap_start = datetime(2026, 5, 25, 19, 55, tzinfo=timezone.utc)
    gap_end = datetime(2026, 5, 26, 1, 0, tzinfo=timezone.utc)
    primary_symbol = _symbol("#USSPX500", "US S&P500 Spot Index CFD") if profile_symbols else _symbol("GENERIC_A", "Generic instrument", "Other")
    secondary_symbol = _symbol("#USNDAQ100", "US Nasdaq 100 Spot Index CFD") if profile_symbols else _symbol("GENERIC_B", "Generic instrument", "Other")
    primary_bars = []
    secondary_bars = []
    cursor = start
    while cursor < end:
        if not gap_start <= cursor < gap_end:
            open_ms = int(cursor.timestamp() * 1000)
            primary_bars.append(_bar(primary_symbol.broker_symbol, open_ms))
            secondary_bars.append(_bar(secondary_symbol.broker_symbol, open_ms))
        cursor += timedelta(minutes=1)
    return (
        AcquisitionResult(primary_symbol, tuple(primary_bars), ()),
        AcquisitionResult(secondary_symbol, tuple(secondary_bars), ()),
    )


def _policy(profile: str = "AUTO") -> QualityConfig:
    return QualityConfig(
        minimum_common_bars=100,
        max_symbol_specific_gap_ratio=0.02,
        max_joint_gap_minutes=240,
        max_unexplained_gap_minutes=15,
        require_exact_m15_coverage=True,
        reject_sub_m1=True,
        drop_incomplete_current_bar=True,
        session_calendar_profile=profile,
        max_scheduled_closure_minutes=1440,
        require_scheduled_closure_boundary_bars=True,
    )


def test_memorial_day_2026_is_in_declared_calendar():
    holidays = us_market_holidays(2026)
    assert holidays[datetime(2026, 5, 25).date()] == "US_MEMORIAL_DAY"


def test_auto_profile_resolves_only_when_both_symbols_match():
    primary, secondary = _pair_with_joint_gap(profile_symbols=True)
    resolution = resolve_calendar_profile(primary.symbol, secondary.symbol, "AUTO")
    assert resolution.resolved_profile == PROFILE_US_INDEX_CFD_NY
    generic_primary, generic_secondary = _pair_with_joint_gap(profile_symbols=False)
    conservative = resolve_calendar_profile(generic_primary.symbol, generic_secondary.symbol, "AUTO")
    assert conservative.resolved_profile == PROFILE_WEEKLY_ONLY


def test_joint_gap_runs_are_collapsed_deterministically():
    intervals = collapse_minute_runs([0, MINUTE, 2 * MINUTE, 10 * MINUTE])
    assert [(x.start_ms, x.end_ms, x.duration_minutes) for x in intervals] == [
        (0, 3 * MINUTE, 3),
        (10 * MINUTE, 11 * MINUTE, 1),
    ]


def test_memorial_day_joint_gap_is_classified_not_forward_filled():
    primary, secondary = _pair_with_joint_gap(profile_symbols=True)
    result = validate_pair(primary, secondary, _policy(), minimum_common_days=0)
    assert result.status == "PASS_WITH_DECLARED_NON_CRITICAL_GAPS"
    assert result.report["scheduled_closure_interval_count"] == 1
    assert result.report["scheduled_closure_minutes"] == 305
    assert result.report["scheduled_closure_intervals"][0]["holiday_id"] == "US_MEMORIAL_DAY"
    assert result.report["unexplained_long_joint_gap_interval_count"] == 0
    assert result.report["scheduled_closures_are_forward_filled"] is False
    assert result.report["forward_fill_allowed"] is False


def test_same_long_gap_blocks_under_conservative_profile():
    primary, secondary = _pair_with_joint_gap(profile_symbols=False)
    result = validate_pair(primary, secondary, _policy("AUTO"), minimum_common_days=0)
    assert result.status == "BLOCKED"
    assert "UNEXPLAINED_JOINT_GAP_EXCEEDS_POLICY" in result.report["blockers"]
    assert result.report["scheduled_closure_interval_count"] == 0


def test_scheduled_closure_requires_bars_on_both_boundaries():
    primary, secondary = _pair_with_joint_gap(profile_symbols=True)
    bars = tuple(bar for bar in secondary.bars if bar.bar_open_time_utc_ms != int(datetime(2026, 5, 26, 1, 0, tzinfo=timezone.utc).timestamp() * 1000))
    secondary_without_boundary = AcquisitionResult(secondary.symbol, bars, ())
    result = validate_pair(primary, secondary_without_boundary, _policy(), minimum_common_days=0)
    assert result.status == "BLOCKED"
    assert result.report["scheduled_closure_interval_count"] == 0
    assert "UNEXPLAINED_JOINT_GAP_EXCEEDS_POLICY" in result.report["blockers"]
