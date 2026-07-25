"""Version-aware plugin registry with capability validation."""
from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Any, Iterable

from .interfaces import PluginDescriptor


class PluginRegistryError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class PluginKey:
    kind: str
    plugin_id: str
    version: str


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[PluginKey, Any] = {}
        self._lock = RLock()

    def register(self, plugin: Any, *, replace: bool = False) -> None:
        descriptor = getattr(plugin, "descriptor", None)
        if not isinstance(descriptor, PluginDescriptor):
            raise PluginRegistryError("plugin must expose a PluginDescriptor as descriptor")
        key = PluginKey(descriptor.kind, descriptor.plugin_id, descriptor.version)
        with self._lock:
            if key in self._plugins and not replace:
                raise PluginRegistryError(f"plugin already registered: {key}")
            self._plugins[key] = plugin

    def resolve(self, kind: str, plugin_id: str, version: str) -> Any:
        key = PluginKey(kind, plugin_id, version)
        try:
            return self._plugins[key]
        except KeyError as exc:
            available = [k for k in self._plugins if k.kind == kind and k.plugin_id == plugin_id]
            raise PluginRegistryError(
                f"missing plugin {key}; available versions: {[k.version for k in available]}"
            ) from exc

    def require_capabilities(
        self,
        kind: str,
        plugin_id: str,
        version: str,
        capabilities: Iterable[str],
    ) -> Any:
        plugin = self.resolve(kind, plugin_id, version)
        have = set(plugin.descriptor.capabilities)
        missing = sorted(set(capabilities) - have)
        if missing:
            raise PluginRegistryError(
                f"plugin {kind}:{plugin_id}:{version} lacks capabilities {missing}"
            )
        return plugin

    def list_descriptors(self) -> tuple[PluginDescriptor, ...]:
        with self._lock:
            return tuple(p.descriptor for p in self._plugins.values())

    def freeze(self) -> "FrozenPluginRegistry":
        with self._lock:
            return FrozenPluginRegistry(dict(self._plugins))


class FrozenPluginRegistry:
    """Immutable lookup optimized for startup-compiled plans."""

    __slots__ = ("_plugins",)

    def __init__(self, plugins: dict[PluginKey, Any]) -> None:
        self._plugins = plugins

    def resolve(self, kind: str, plugin_id: str, version: str) -> Any:
        key = PluginKey(kind, plugin_id, version)
        if key not in self._plugins:
            raise PluginRegistryError(f"missing compiled plugin: {key}")
        return self._plugins[key]
