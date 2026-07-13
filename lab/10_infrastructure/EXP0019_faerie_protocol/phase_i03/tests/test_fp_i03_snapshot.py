import pytest
from fp_i03_time.calendar import snapshot
from fp_i03_time.enums import CalendarSegment, CalendarHealth
from fp_i03_time.golden import utc_ms
from fp_i03_time.validation import validate_snapshot

@pytest.mark.parametrize("iso,segment,session_code,day_id",[
    ("2026-07-12T21:59:59Z",CalendarSegment.WEEKEND_CLOSED,None,"NYDAY-2026-07-12"),
    ("2026-07-12T22:00:00Z",CalendarSegment.A,CalendarSegment.A,"NYDAY-2026-07-13"),
    ("2026-07-13T08:00:00Z",CalendarSegment.L,CalendarSegment.L,"NYDAY-2026-07-13"),
    ("2026-07-13T13:30:00Z",CalendarSegment.N,CalendarSegment.N,"NYDAY-2026-07-13"),
    ("2026-07-13T21:00:00Z",CalendarSegment.DAILY_GAP,None,"NYDAY-2026-07-13"),
    ("2026-07-13T22:00:00Z",CalendarSegment.A,CalendarSegment.A,"NYDAY-2026-07-14"),
    ("2026-07-17T21:00:00Z",CalendarSegment.WEEKEND_CLOSED,None,"NYDAY-2026-07-17"),
])
def test_snapshot_state(iso,segment,session_code,day_id):
    value=snapshot(utc_ms(iso))
    assert value.segment is segment
    assert value.health is CalendarHealth.READY
    assert value.trading_day.trading_day_id==day_id
    assert (value.session.session_code if value.session else None) is session_code
    assert validate_snapshot(value).passed


def test_snapshot_is_deterministic():
    a=snapshot(utc_ms("2026-07-13T12:00:00Z"))
    b=snapshot(utc_ms("2026-07-13T12:00:00Z"))
    assert a==b
    assert a.snapshot_id==b.snapshot_id
    assert a.boundary_evidence_hash==b.boundary_evidence_hash


def test_one_millisecond_boundary_change_changes_snapshot():
    before=snapshot(utc_ms("2026-07-13T13:29:59.999Z"))
    after=snapshot(utc_ms("2026-07-13T13:30:00.000Z"))
    assert before.segment is CalendarSegment.L
    assert after.segment is CalendarSegment.N
    assert before.snapshot_id!=after.snapshot_id
