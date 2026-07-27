import pytest
from strategy_factory_market import BarCache, TickCache, TickSnapshot
from .helpers import bar

def test_tick_cache_rejects_out_of_order_tick() -> None:
    cache = TickCache()
    cache.put(TickSnapshot("#NQ", 1000, 1000, 10.0, 10.25, 10.0, 1))
    with pytest.raises(ValueError):
        cache.put(TickSnapshot("#NQ", 999, 1001, 10.0, 10.25, 10.0, 1))

def test_tick_cache_stale_fails_closed() -> None:
    cache = TickCache()
    cache.put(TickSnapshot("#NQ", 1000, 1000, 10.0, 10.25, 10.0, 1))
    with pytest.raises(RuntimeError, match="stale"):
        cache.get("#NQ", 7000, 5000)

def test_bar_series_insert_replace_duplicate_and_generation() -> None:
    cache = BarCache()
    first = bar()
    assert cache.upsert(first) == "inserted"
    assert cache.upsert(first) == "duplicate"
    changed = bar(close_price=101.5)
    assert cache.upsert(changed) == "replaced"
    series = cache.get("#NQ", 60)
    assert series.generation == 2
    assert series.latest.close_price == 101.5

def test_bar_gap_is_persistent() -> None:
    cache = BarCache()
    cache.upsert(bar(open_ms=1_000_000))
    result = cache.upsert(bar(open_ms=1_000_000 + 120_000))
    assert result == "gap_inserted"
    assert cache.get("#NQ", 60).has_gap

def test_bar_capacity_is_bounded() -> None:
    series = BarCache().ensure("#NQ", 60, capacity=2)
    for i in range(3):
        series.upsert(bar(open_ms=1_000_000 + i * 60_000))
    assert len(series.bars) == 2
