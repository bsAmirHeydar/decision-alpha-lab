from datetime import date
import pytest
from fp_i02_kernel.contracts import SymbolPair
from fp_i02_kernel.enums import WindowKind
from fp_i03_time.calendar import build_daily_gap, build_session, build_trading_day
from fp_i03_time.enums import CalendarSegment


def test_trading_day_is_18_to_17_ny_and_23_hours():
    window,evidence=build_trading_day(date(2026,7,13))
    assert window.start_ny_iso=="2026-07-12T18:00:00"
    assert window.end_ny_iso=="2026-07-13T17:00:00"
    assert window.elapsed_seconds==23*3600
    assert len(evidence)==2

@pytest.mark.parametrize("code,start,end,duration",[
    (CalendarSegment.A,"2026-07-12T18:00:00","2026-07-13T04:00:00",10*3600),
    (CalendarSegment.L,"2026-07-13T04:00:00","2026-07-13T09:30:00",5*3600+30*60),
    (CalendarSegment.N,"2026-07-13T09:30:00","2026-07-13T17:00:00",7*3600+30*60),
])
def test_session_bounds_and_duration(code,start,end,duration):
    window,evidence=build_session(date(2026,7,13),code)
    assert window.start_ny_iso==start
    assert window.end_ny_iso==end
    assert window.elapsed_seconds==duration
    assert len(evidence)==2


def test_daily_gap_is_exactly_one_hour():
    start,end,evidence=build_daily_gap(date(2026,7,13))
    assert end-start==3600*1000
    assert len(evidence)==2

@pytest.mark.parametrize("code,kind",[(CalendarSegment.A,WindowKind.A),(CalendarSegment.L,WindowKind.L),(CalendarSegment.N,WindowKind.N)])
def test_session_adapts_to_i02_window_key(code,kind):
    pair=SymbolPair("SPXUSD","NDXUSD")
    session=build_session(date(2026,7,13),code)[0]
    key=session.to_i02_window_key("FP-CONTEXT-001",pair.pair_id,"REV")
    assert key.kind is kind
    assert key.start_utc_ms==session.start_utc_ms
    assert key.end_utc_ms==session.end_utc_ms
    assert key.trading_day_id=="NYDAY-2026-07-13"
