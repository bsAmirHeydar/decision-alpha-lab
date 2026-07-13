from datetime import datetime,timezone
from fp_i03_time.contracts import TimeKernelConfig
from fp_i04_data.enums import ExpectedMinutePolicy
from fp_i04_data.synchronization import minute_axis

def ms(text): return int(datetime.fromisoformat(text).replace(tzinfo=timezone.utc).timestamp()*1000)

def test_all_requested_axis_emits_every_minute():
    axis,_=minute_axis(ms('2026-07-13T12:00:00'),ms('2026-07-13T12:05:00'),ExpectedMinutePolicy.ALL_REQUESTED_MINUTES,TimeKernelConfig())
    assert len(axis)==5

def test_trading_policy_excludes_daily_gap():
    # 17:00 NY in July = 21:00 UTC.
    axis,_=minute_axis(ms('2026-07-13T20:59:00'),ms('2026-07-13T21:02:00'),ExpectedMinutePolicy.NY_TRADING_SESSIONS_ONLY,TimeKernelConfig())
    assert len(axis)==1

def test_trading_policy_includes_exact_session_start():
    # 18:00 NY in July = 22:00 UTC.
    axis,_=minute_axis(ms('2026-07-13T21:59:00'),ms('2026-07-13T22:02:00'),ExpectedMinutePolicy.NY_TRADING_SESSIONS_ONLY,TimeKernelConfig())
    assert axis[-2:]==(ms('2026-07-13T22:00:00'),ms('2026-07-13T22:01:00'))
