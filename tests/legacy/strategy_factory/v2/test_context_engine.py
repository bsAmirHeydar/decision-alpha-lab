from datetime import datetime, timedelta, timezone

from strategy_factory.context import IncrementalContextEngine, MappingFeatureProvider, compile_feature_graph
from strategy_factory.contracts import AnatomyEvent, Direction
from strategy_factory.plugins import PluginDescriptor


def event():
    t = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return AnatomyEvent("e", "s", "1", "X", Direction.LONG, t, t, t, 100.0, 99.0)


def test_context_engine_caches_same_generation():
    calls = {"n": 0}
    def compute(event, resolved, market):
        calls["n"] += 1
        return {"x": market["x"]}
    provider = MappingFeatureProvider(
        descriptor=PluginDescriptor("p", "1", "feature_provider"),
        feature_names=("x",),
        compute_fn=compute,
        ttl_seconds=10,
    )
    engine = IncrementalContextEngine(compile_feature_graph([provider]))
    t = event().confirmation_time_utc
    first = engine.build(event(), {"x": 2}, t, state_generation=1)
    second = engine.build(event(), {"x": 2}, t, state_generation=1)
    assert first.flat["x"] == 2
    assert second.cache_hits == 1
    assert calls["n"] == 1


def test_context_engine_recomputes_new_generation():
    calls = {"n": 0}
    provider = MappingFeatureProvider(
        descriptor=PluginDescriptor("p", "1", "feature_provider"),
        feature_names=("x",),
        compute_fn=lambda event, resolved, market: calls.__setitem__("n", calls["n"] + 1) or {"x": market["x"]},
    )
    engine = IncrementalContextEngine(compile_feature_graph([provider]))
    t = event().confirmation_time_utc
    engine.build(event(), {"x": 1}, t, state_generation=1)
    result = engine.build(event(), {"x": 3}, t, state_generation=2)
    assert result.flat["x"] == 3
    assert calls["n"] == 2
