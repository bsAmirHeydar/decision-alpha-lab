from datetime import datetime
import pytest
from fp_i03_time.calendar import classify_intraday_segment, trading_date_for_local
from fp_i03_time.enums import CalendarSegment

@pytest.mark.parametrize("local,segment,trading_date",[
    ("2026-07-12T17:59:59",CalendarSegment.DAILY_GAP,"2026-07-12"),
    ("2026-07-12T18:00:00",CalendarSegment.A,"2026-07-13"),
    ("2026-07-13T03:59:59",CalendarSegment.A,"2026-07-13"),
    ("2026-07-13T04:00:00",CalendarSegment.L,"2026-07-13"),
    ("2026-07-13T09:29:59",CalendarSegment.L,"2026-07-13"),
    ("2026-07-13T09:30:00",CalendarSegment.N,"2026-07-13"),
    ("2026-07-13T16:59:59",CalendarSegment.N,"2026-07-13"),
    ("2026-07-13T17:00:00",CalendarSegment.DAILY_GAP,"2026-07-13"),
    ("2026-07-13T17:59:59",CalendarSegment.DAILY_GAP,"2026-07-13"),
    ("2026-07-13T18:00:00",CalendarSegment.A,"2026-07-14"),
])
def test_intraday_half_open_boundaries(local,segment,trading_date):
    value=datetime.fromisoformat(local)
    assert classify_intraday_segment(value) is segment
    assert trading_date_for_local(value).isoformat()==trading_date
