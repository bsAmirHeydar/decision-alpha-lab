from dataclasses import replace

import pytest

from fp_i02_kernel.contracts import ReferenceSideKey, ReferenceSideRecord, SymbolPair, WindowKey, WindowRecord
from fp_i02_kernel.enums import DataState, PriceSide, ReferenceState, WindowKind, WindowScope
from fp_i02_kernel.errors import FPI02Error
from fp_i02_kernel.golden import golden_reference_key, golden_window_key


def test_symbol_pair_is_order_invariant_for_pair_id():
    assert SymbolPair("SPXUSD", "NDXUSD").pair_id == SymbolPair("NDXUSD", "SPXUSD").pair_id


def test_symbol_pair_rejects_same_symbol():
    with pytest.raises(FPI02Error):
        SymbolPair("SPXUSD", "SPXUSD")


def test_window_id_is_deterministic_and_revision_bearing():
    key = golden_window_key()
    assert key.window_id == golden_window_key().window_id
    changed = replace(key, data_revision="REV-2")
    assert changed.window_id != key.window_id


def test_empty_or_inverted_window_is_rejected():
    key = golden_window_key()
    with pytest.raises(FPI02Error):
        replace(key, end_utc_ms=key.start_utc_ms)


def test_prior_calendar_window_requires_positive_offset():
    key = golden_window_key()
    with pytest.raises(FPI02Error):
        replace(key, kind=WindowKind.N, scope=WindowScope.EXACT_PRIOR_CALENDAR_OFFSET, calendar_offset=0)


def test_complete_window_requires_two_symbol_maps_and_bars():
    key = golden_window_key()
    record = WindowRecord(
        key,
        DataState.COMPLETE,
        {"SPXUSD": 6250.0, "NDXUSD": 22500.0},
        {"SPXUSD": 6200.0, "NDXUSD": 22300.0},
        {"SPXUSD": 600, "NDXUSD": 600},
        "c" * 64,
        True,
    )
    assert len(record.record_hash) == 64
    with pytest.raises(FPI02Error):
        replace(record, bar_count_by_symbol={"SPXUSD": 0, "NDXUSD": 600})


def test_reference_side_is_symbol_local_and_side_specific():
    high = golden_reference_key()
    low = replace(high, side=PriceSide.LOW, price=22000.0)
    other = replace(high, symbol="SPXUSD", price=6250.0)
    assert len({high.reference_side_id, low.reference_side_id, other.reference_side_id}) == 3


def test_reference_state_requires_event_lineage():
    key = golden_reference_key()
    with pytest.raises(FPI02Error):
        ReferenceSideRecord(key, ReferenceState.HUNTER_SEEN)
    with pytest.raises(FPI02Error):
        ReferenceSideRecord(key, ReferenceState.CONSUMED_BY_PROTECTED_TOUCH)
    assert ReferenceSideRecord(key, ReferenceState.HUNTER_SEEN, first_hunter_event_id="evt").state is ReferenceState.HUNTER_SEEN
