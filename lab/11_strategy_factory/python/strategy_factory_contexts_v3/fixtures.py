"""Golden source records and mutations for reference package conformance."""
from __future__ import annotations

def synthetic_records():
    base={"symbol":"EURUSD","timeframe_seconds":60,"signal_bar_open_ms":1710000000000,"event_time_ms":1710000059999,"known_time_ms":1710000060000,"confirmation_time_ms":1710000060000,"observation_cut_ms":1710000060000,"decision_time_ms":1710000060001,"prior_high":1.1000,"prior_low":1.0980,"atr":0.0010,"spread_points":12.0,"session":"london","trading_day":"2024-03-09","source_event_id":"evt.synthetic.001","close":1.1010}
    inside=dict(base,source_event_id="evt.synthetic.none",signal_bar_open_ms=1710000060000,event_time_ms=1710000119999,known_time_ms=1710000120000,confirmation_time_ms=1710000120000,observation_cut_ms=1710000120000,decision_time_ms=1710000120001,close=1.0990)
    short=dict(base,source_event_id="evt.synthetic.002",signal_bar_open_ms=1710000120000,event_time_ms=1710000179999,known_time_ms=1710000180000,confirmation_time_ms=1710000180000,observation_cut_ms=1710000180000,decision_time_ms=1710000180001,close=1.0970,session="new_york")
    return [base,inside,short]

def synthetic_future_mutations():
    return [{"base_record_index":0,"mutation_time_ms":1710000120000,"changes":{"future_close":1.2000,"future_high":1.2500}}]

def exp0017_records():
    return [{"canonical_event_id":"sf20_evt_001","event_time_ms":1711000000000,"known_time_ms":1711000001000,"confirmation_time_ms":1711000001000,"observation_cut_ms":1711000001000,"decision_time_ms":1711000001001,"hunter_symbol":"US100","clean_symbol":"US500","group_minutes":60,"direction":"short","hunter_reference_price":18000.0,"clean_reference_price":5200.0,"hunter_current_extreme":18025.0,"clean_current_extreme":5201.0,"trading_day":"2024-03-21","current_cycle_start_ms":1710997200000,"parent_event_id":"sf20_parent_001"}]
