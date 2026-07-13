from datetime import datetime, timedelta, timezone
import pytest
from fp_i03_time.calendar import snapshot
from fp_i03_time.enums import CalendarSegment
from fp_i03_time.time_math import epoch_ms

UTC=timezone.utc

@pytest.mark.parametrize("base_iso,before,at",[
    ("2026-07-12T22:00:00+00:00",CalendarSegment.WEEKEND_CLOSED,CalendarSegment.A),
    ("2026-07-13T08:00:00+00:00",CalendarSegment.A,CalendarSegment.L),
    ("2026-07-13T13:30:00+00:00",CalendarSegment.L,CalendarSegment.N),
    ("2026-07-13T21:00:00+00:00",CalendarSegment.N,CalendarSegment.DAILY_GAP),
    ("2026-07-13T22:00:00+00:00",CalendarSegment.DAILY_GAP,CalendarSegment.A),
    ("2026-07-17T21:00:00+00:00",CalendarSegment.N,CalendarSegment.WEEKEND_CLOSED),
])
def test_each_boundary_is_half_open(base_iso,before,at):
    point=datetime.fromisoformat(base_iso)
    assert snapshot(epoch_ms(point-timedelta(milliseconds=1))).segment is before
    assert snapshot(epoch_ms(point)).segment is at
