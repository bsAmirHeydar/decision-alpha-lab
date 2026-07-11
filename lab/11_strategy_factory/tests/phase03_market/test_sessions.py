from datetime import datetime, timezone
import pytest
from strategy_factory_market import (
    ClockConfig, SessionDefinition, SessionSchedule, TimeKernel, TimezoneKind,
)

UTC = timezone.utc

def test_new_york_session_matches_in_dst() -> None:
    schedule = SessionSchedule()
    schedule.add(SessionDefinition("new_york_am", True, TimezoneKind.NEW_YORK, 0, 570, 720, 62))
    result = schedule.match(datetime(2026, 7, 13, 14, 0, tzinfo=UTC), TimeKernel(ClockConfig()))
    assert result.matched
    assert result.session_id == "new_york_am"
    assert result.local_minute_of_day == 600

def test_cross_midnight_session() -> None:
    schedule = SessionSchedule()
    schedule.add(SessionDefinition("overnight", True, TimezoneKind.UTC, 0, 1320, 120, 127))
    kernel = TimeKernel(ClockConfig())
    assert schedule.match(datetime(2026, 7, 11, 23, tzinfo=UTC), kernel).matched
    assert schedule.match(datetime(2026, 7, 12, 1, tzinfo=UTC), kernel).matched
    assert not schedule.match(datetime(2026, 7, 12, 12, tzinfo=UTC), kernel).matched

def test_duplicate_session_rejected() -> None:
    schedule = SessionSchedule()
    definition = SessionDefinition("x", True, TimezoneKind.UTC, 0, 0, 60)
    schedule.add(definition)
    with pytest.raises(ValueError):
        schedule.add(definition)
