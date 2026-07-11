"""Small helpers for declaring plugins without framework coupling."""
from __future__ import annotations

from typing import Any, Callable, TypeVar

from .interfaces import PluginDescriptor

T = TypeVar("T")


def plugin(
    *,
    plugin_id: str,
    version: str,
    kind: str,
    deterministic: bool = True,
    thread_safe: bool = True,
    fast_path_safe: bool = True,
    capabilities: tuple[str, ...] = (),
) -> Callable[[T], T]:
    descriptor = PluginDescriptor(
        plugin_id=plugin_id,
        version=version,
        kind=kind,
        deterministic=deterministic,
        thread_safe=thread_safe,
        fast_path_safe=fast_path_safe,
        capabilities=capabilities,
    )

    def decorate(obj: T) -> T:
        setattr(obj, "descriptor", descriptor)
        return obj

    return decorate
