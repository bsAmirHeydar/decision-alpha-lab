from __future__ import annotations
from strategy_factory_contracts.records import BarRecord
from strategy_factory_contracts.time import MarketTimestamp

def ts(value: int) -> MarketTimestamp:
    return MarketTimestamp(value, "UTC", 0, "fixture")

def bar(
    symbol: str = "#NQ",
    timeframe_seconds: int = 60,
    open_ms: int = 1_000_000,
    open_price: float = 100.0,
    high_price: float = 102.0,
    low_price: float = 99.0,
    close_price: float = 101.0,
) -> BarRecord:
    return BarRecord(
        symbol=symbol,
        timeframe_seconds=timeframe_seconds,
        open_time=ts(open_ms),
        close_time=ts(open_ms + timeframe_seconds * 1000),
        open_price=open_price,
        high_price=high_price,
        low_price=low_price,
        close_price=close_price,
        tick_volume=100,
        real_volume=0,
        bid_close=close_price,
        ask_close=close_price + 0.25,
        spread_points=1.0,
        source_id="fixture",
        source_bar_id=f"bar_{timeframe_seconds}_{open_ms}",
    )
