from dataclasses import replace
from fp_i03_time.calendar import build_session, snapshot
from fp_i03_time.contracts import TimeKernelConfig
from fp_i03_time.enums import CalendarSegment, LocalResolutionPolicy
from fp_i03_time.golden import utc_ms


def test_same_input_same_semantic_ids():
    first=snapshot(utc_ms("2026-07-13T12:00:00Z"))
    second=snapshot(utc_ms("2026-07-13T12:00:00Z"))
    assert first.snapshot_id==second.snapshot_id
    assert first.trading_day.window_id==second.trading_day.window_id
    assert first.session.window_id==second.session.window_id
    assert first.week.window_id==second.week.window_id


def test_config_policy_change_changes_config_and_snapshot_identity():
    base=TimeKernelConfig()
    changed=replace(base,ambiguous_start_policy=LocalResolutionPolicy.LATEST)
    assert base.config_hash!=changed.config_hash
    first=snapshot(utc_ms("2026-07-13T12:00:00Z"),base)
    second=snapshot(utc_ms("2026-07-13T12:00:00Z"),changed)
    assert first.snapshot_id!=second.snapshot_id


def test_session_window_id_not_chart_timeframe_dependent():
    first=build_session(__import__('datetime').date(2026,7,13),CalendarSegment.L)[0]
    second=build_session(__import__('datetime').date(2026,7,13),CalendarSegment.L)[0]
    assert first.window_id==second.window_id
