from datetime import datetime, timezone

import pytest

from strategy_factory.context import MappingFeatureProvider, compile_feature_graph, ContextGraphError
from strategy_factory.plugins import PluginDescriptor


def provider(pid, outputs, deps=()):
    return MappingFeatureProvider(
        descriptor=PluginDescriptor(pid, "1", "feature_provider"),
        feature_names=tuple(outputs),
        dependencies=tuple(deps),
        compute_fn=lambda event, resolved, market: {name: 1.0 for name in outputs},
    )


def test_feature_graph_orders_dependencies():
    a = provider("a", ["a"])
    b = provider("b", ["b"], ["a"])
    graph = compile_feature_graph([b, a])
    assert [p.descriptor.plugin_id for p in graph.ordered_providers] == ["a", "b"]


def test_feature_graph_rejects_duplicate_output():
    with pytest.raises(ContextGraphError):
        compile_feature_graph([provider("a", ["x"]), provider("b", ["x"])])


def test_feature_graph_rejects_cycle():
    a = provider("a", ["a"], ["b"])
    b = provider("b", ["b"], ["a"])
    with pytest.raises(ContextGraphError):
        compile_feature_graph([a, b])
