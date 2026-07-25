from datetime import date
import pytest
from fp_i02_kernel.contracts import SymbolPair
from fp_i02_kernel.enums import WindowKind
from fp_i03_time.calendar import build_week_from_sunday, previous_completed_week, week_for_reference
from fp_i03_time.golden import utc_ms
from fp_i03_time.enums import WeekState


def test_week_is_sunday_18_to_friday_17():
    week,evidence=build_week_from_sunday(date(2026,7,12))
    assert week.start_ny_iso=="2026-07-12T18:00:00"
    assert week.end_ny_iso=="2026-07-17T17:00:00"
    assert week.elapsed_seconds==119*3600
    assert len(evidence)==2

@pytest.mark.parametrize("iso,contains,state",[
    ("2026-07-12T21:59:59Z",False,WeekState.CLOSED_AFTER_FRIDAY),
    ("2026-07-12T22:00:00Z",True,WeekState.ACTIVE),
    ("2026-07-17T20:59:59Z",True,WeekState.ACTIVE),
    ("2026-07-17T21:00:00Z",False,WeekState.CLOSED_AFTER_FRIDAY),
    ("2026-07-18T12:00:00Z",False,WeekState.CLOSED_AFTER_FRIDAY),
])
def test_week_half_open_ownership(iso,contains,state):
    week,_=week_for_reference(utc_ms(iso))
    assert week.contains_reference_time is contains
    assert week.state is state


def test_previous_completed_week_during_active_week_is_prior_week():
    week=previous_completed_week(utc_ms("2026-07-15T12:00:00Z"))
    assert week.week_id=="NYWEEK-2026-07-05"


def test_previous_completed_week_during_weekend_is_just_closed_week():
    week=previous_completed_week(utc_ms("2026-07-18T12:00:00Z"))
    assert week.week_id=="NYWEEK-2026-07-12"


def test_week_adapts_to_i02_week_key():
    pair=SymbolPair("SPXUSD","NDXUSD")
    week=build_week_from_sunday(date(2026,7,12))[0]
    key=week.to_i02_window_key("FP-CONTEXT-001",pair.pair_id,"REV")
    assert key.kind is WindowKind.W
    assert key.week_id==week.week_id
