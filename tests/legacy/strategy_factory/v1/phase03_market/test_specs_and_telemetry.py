from strategy_factory_market import (
    DataQuality, MarketTelemetry, SymbolSpecCache, SymbolSpecSnapshot,
)

def spec(tick_size: float = 0.25, generation: int = 0) -> SymbolSpecSnapshot:
    return SymbolSpecSnapshot(
        symbol="#NQ", digits=2, point=0.01, tick_size=tick_size,
        tick_value=5.0, contract_size=1.0,
        volume_min=0.01, volume_max=100.0, volume_step=0.01,
        stops_level_points=0, freeze_level_points=0,
        filling_mode=0, order_mode=0, trade_mode=0,
        specification_generation=generation,
        observed_at_utc_milliseconds=1_000,
        quality=DataQuality.VALID,
    )

def test_spec_generation_changes_only_on_material_drift() -> None:
    cache = SymbolSpecCache()
    assert cache.put(spec()).specification_generation == 1
    assert cache.put(spec()).specification_generation == 1
    assert cache.put(spec(tick_size=0.5)).specification_generation == 2

def test_telemetry_is_monotonic_and_tracks_max_latency() -> None:
    telemetry = MarketTelemetry()
    telemetry.increment("tick_updates")
    telemetry.increment("tick_updates", 2)
    telemetry.refresh_latency(10)
    telemetry.refresh_latency(7)
    telemetry.refresh_latency(20)
    snapshot = telemetry.snapshot()
    assert snapshot.tick_updates == 3
    assert snapshot.last_refresh_latency_us == 20
    assert snapshot.maximum_refresh_latency_us == 20
