from datetime import date
from dataclasses import replace
from fp_i02_kernel.enums import WindowKind
from fp_i03_time.contracts import TimeKernelConfig
from fp_i05_reference.golden import golden_completed_n_window
from fp_i05_reference.window_builder import descriptor_for_session,descriptor_for_week,aggregate_pair_window
from fp_i05_reference.enums import WindowBuildState,PairWindowHealth

def test_session_descriptor_uses_i03_calendar():
 tc=TimeKernelConfig();d=descriptor_for_session('PAIR',date(2026,7,13),WindowKind.A,tc.config_hash)
 assert d.expected_minutes==600 and d.end_utc_ms>d.start_utc_ms

def test_london_expected_minutes():
 tc=TimeKernelConfig();d=descriptor_for_session('PAIR',date(2026,7,13),WindowKind.L,tc.config_hash)
 assert d.expected_minutes==330

def test_new_york_expected_minutes():
 tc=TimeKernelConfig();d=descriptor_for_session('PAIR',date(2026,7,13),WindowKind.N,tc.config_hash)
 assert d.expected_minutes==450

def test_week_expected_minutes_excludes_daily_gaps():
 tc=TimeKernelConfig();d=descriptor_for_week('PAIR',date(2026,7,12),tc.config_hash)
 assert d.expected_minutes==6900

def test_complete_window_aggregates_symbol_local_extremes():
 cfg,result,desc,agg,refs=golden_completed_n_window()
 assert agg.completed and agg.health is PairWindowHealth.READY
 assert agg.left.high!=agg.right.high
 assert agg.left.high_utc_ms>=desc.start_utc_ms

def test_active_window_is_not_complete():
 cfg,result,desc,agg,refs=golden_completed_n_window()
 active=aggregate_pair_window(desc,result.rows,agg.left.canonical_symbol,agg.right.canonical_symbol,desc.start_utc_ms+60_000,result.revision.revision_id)
 assert active.left.state is WindowBuildState.ACTIVE and not active.completed

def test_missing_row_degrades_window():
 cfg,result,desc,agg,refs=golden_completed_n_window()
 rows=tuple(r for i,r in enumerate(result.rows) if i!=10)
 partial=aggregate_pair_window(desc,rows,agg.left.canonical_symbol,agg.right.canonical_symbol,desc.end_utc_ms,result.revision.revision_id)
 assert partial.health is PairWindowHealth.DEGRADED

def test_same_input_same_window_hash():
 cfg,result,desc,agg,refs=golden_completed_n_window()
 again=aggregate_pair_window(desc,result.rows,agg.left.canonical_symbol,agg.right.canonical_symbol,desc.end_utc_ms,result.revision.revision_id)
 assert again.semantic_hash==agg.semantic_hash and again.pair_window_id==agg.pair_window_id
