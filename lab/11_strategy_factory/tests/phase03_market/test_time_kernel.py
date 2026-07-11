from __future__ import annotations
from datetime import datetime, timezone
import pytest
from strategy_factory_market import ClockConfig, ClockMode, TimeKernel, TimezoneKind

UTC = timezone.utc

def test_new_york_offsets_across_seasons() -> None:
    assert TimeKernel.new_york_utc_offset_minutes(datetime(2026, 1, 15, 12, tzinfo=UTC)) == -300
    assert TimeKernel.new_york_utc_offset_minutes(datetime(2026, 7, 15, 12, tzinfo=UTC)) == -240

def test_2026_dst_transition_boundaries_are_half_open() -> None:
    start = TimeKernel.new_york_dst_start_utc(2026)
    end = TimeKernel.new_york_dst_end_utc(2026)
    assert start == datetime(2026, 3, 8, 7, tzinfo=UTC)
    assert end == datetime(2026, 11, 1, 6, tzinfo=UTC)
    assert not TimeKernel.is_new_york_dst(start.replace(minute=0) - __import__("datetime").timedelta(milliseconds=1))
    assert TimeKernel.is_new_york_dst(start)
    assert TimeKernel.is_new_york_dst(end - __import__("datetime").timedelta(milliseconds=1))
    assert not TimeKernel.is_new_york_dst(end)

def test_broker_wall_clock_conversion() -> None:
    kernel = TimeKernel(ClockConfig(ClockMode.BROKER_FIXED_OFFSET, 120))
    result = kernel.broker_to_utc(datetime(2026, 7, 11, 16, 30))
    assert result == datetime(2026, 7, 11, 14, 30, tzinfo=UTC)

def test_naive_utc_input_is_rejected() -> None:
    kernel = TimeKernel(ClockConfig())
    with pytest.raises(ValueError):
        kernel.trading_day_id(datetime(2026, 7, 11, 12), TimezoneKind.UTC, 0)

def test_trading_day_rollover() -> None:
    kernel = TimeKernel(ClockConfig())
    before = datetime(2026, 7, 11, 20, 59, tzinfo=UTC)
    after = datetime(2026, 7, 11, 21, 1, tzinfo=UTC)
    assert kernel.trading_day_id(before, TimezoneKind.UTC, 21 * 60) == 20260710
    assert kernel.trading_day_id(after, TimezoneKind.UTC, 21 * 60) == 20260711
