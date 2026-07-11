"""Feature dependency graph and startup-time topological compilation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from ..plugins.interfaces import FeatureProvider


class ContextGraphError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class FeatureNode:
    provider_id: str
    version: str
    outputs: tuple[str, ...]
    dependencies: tuple[str, ...]
    required: bool
    ttl_seconds: float | None


@dataclass(frozen=True, slots=True)
class CompiledFeatureGraph:
    ordered_providers: tuple[FeatureProvider, ...]
    produced_by: Mapping[str, str]
    required_features: frozenset[str]


def compile_feature_graph(providers: Iterable[FeatureProvider]) -> CompiledFeatureGraph:
    providers = tuple(providers)
    produced_by: dict[str, str] = {}
    provider_by_id: dict[str, FeatureProvider] = {}
    for provider in providers:
        pid = provider.descriptor.plugin_id
        if pid in provider_by_id:
            raise ContextGraphError(f"duplicate feature provider id: {pid}")
        provider_by_id[pid] = provider
        for feature in provider.feature_names:
            if feature in produced_by:
                raise ContextGraphError(
                    f"feature {feature!r} produced by both {produced_by[feature]!r} and {pid!r}"
                )
            produced_by[feature] = pid

    dependencies_by_provider: dict[str, set[str]] = {pid: set() for pid in provider_by_id}
    reverse: dict[str, set[str]] = {pid: set() for pid in provider_by_id}
    for pid, provider in provider_by_id.items():
        for dependency_feature in provider.dependencies:
            owner = produced_by.get(dependency_feature)
            if owner is None:
                # Dependency may be supplied directly by the event/market state.
                continue
            if owner == pid:
                raise ContextGraphError(f"provider {pid!r} depends on its own feature {dependency_feature!r}")
            dependencies_by_provider[pid].add(owner)
            reverse[owner].add(pid)

    ready = sorted(pid for pid, deps in dependencies_by_provider.items() if not deps)
    ordered: list[str] = []
    while ready:
        pid = ready.pop(0)
        ordered.append(pid)
        for child in sorted(reverse[pid]):
            dependencies_by_provider[child].discard(pid)
            if not dependencies_by_provider[child] and child not in ready and child not in ordered:
                ready.append(child)
        ready.sort()

    if len(ordered) != len(provider_by_id):
        cycle_nodes = sorted(pid for pid, deps in dependencies_by_provider.items() if deps)
        raise ContextGraphError(f"feature dependency cycle detected among {cycle_nodes}")

    required = {
        feature
        for provider in providers
        if provider.required
        for feature in provider.feature_names
    }
    return CompiledFeatureGraph(
        ordered_providers=tuple(provider_by_id[pid] for pid in ordered),
        produced_by=produced_by,
        required_features=frozenset(required),
    )
