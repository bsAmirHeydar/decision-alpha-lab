import pytest

from strategy_factory.plugins import PluginDescriptor, PluginRegistry, PluginRegistryError


class Dummy:
    descriptor = PluginDescriptor("dummy", "1", "test", capabilities=("x",))


def test_plugin_registry_freezes_and_resolves():
    registry = PluginRegistry()
    dummy = Dummy()
    registry.register(dummy)
    assert registry.resolve("test", "dummy", "1") is dummy
    assert registry.freeze().resolve("test", "dummy", "1") is dummy


def test_plugin_registry_rejects_duplicate():
    registry = PluginRegistry()
    registry.register(Dummy())
    with pytest.raises(PluginRegistryError):
        registry.register(Dummy())


def test_plugin_capability_validation():
    registry = PluginRegistry()
    registry.register(Dummy())
    assert registry.require_capabilities("test", "dummy", "1", ["x"])
    with pytest.raises(PluginRegistryError):
        registry.require_capabilities("test", "dummy", "1", ["missing"])
