from strategy_factory_market import (
    BarCache, MultiSymbolSynchronizer, SyncRequirement, SyncStatus,
)
from helpers import bar

def requirements(skew: int = 0):
    return [
        SyncRequirement("NQ", 60, skew, 120_000),
        SyncRequirement("ES", 60, skew, 120_000),
    ]

def test_ready_when_close_times_match() -> None:
    cache = BarCache()
    cache.upsert(bar("NQ", open_ms=1_000_000))
    cache.upsert(bar("ES", open_ms=1_000_000))
    result = MultiSymbolSynchronizer().evaluate(cache, requirements(), 1_070_000)
    assert result.status is SyncStatus.READY
    assert result.ready_count == 2

def test_missing_series_fails_closed() -> None:
    cache = BarCache()
    cache.upsert(bar("NQ", open_ms=1_000_000))
    result = MultiSymbolSynchronizer().evaluate(cache, requirements(), 1_070_000)
    assert result.status is SyncStatus.MISSING_SERIES

def test_skew_exceeded() -> None:
    cache = BarCache()
    cache.upsert(bar("NQ", open_ms=1_000_000))
    cache.upsert(bar("ES", open_ms=1_060_000))
    result = MultiSymbolSynchronizer().evaluate(cache, requirements(skew=1_000), 1_130_000)
    assert result.status is SyncStatus.SKEW_EXCEEDED

def test_gap_is_not_ready() -> None:
    cache = BarCache()
    cache.upsert(bar("NQ", open_ms=1_000_000))
    cache.upsert(bar("NQ", open_ms=1_120_000))
    cache.upsert(bar("ES", open_ms=1_120_000))
    result = MultiSymbolSynchronizer().evaluate(cache, requirements(), 1_190_000)
    assert result.status is SyncStatus.GAP_DETECTED
