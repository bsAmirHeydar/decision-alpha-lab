"""Frozen exact-version registry for UCE-I11 search adapters."""

from __future__ import annotations

from dataclasses import asdict

from .canonical import canonical_sha256, stable_id
from .contracts import SearchAdapterDescriptor, SearchRegistrySnapshot
from .enums import SearchKind
from .errors import ExperimentError


CATALOG = (
    SearchAdapterDescriptor("uce.search.baseline", "1.0.0", SearchKind.BASELINE, True, True, True, False, False),
    SearchAdapterDescriptor("uce.search.grid", "1.0.0", SearchKind.GRID, True, True, True, False, False),
    SearchAdapterDescriptor("uce.search.random", "1.0.0", SearchKind.RANDOM, True, True, True, False, False),
    SearchAdapterDescriptor("uce.search.halton", "1.0.0", SearchKind.QUASI_RANDOM, True, True, True, False, False),
    SearchAdapterDescriptor(
        "uce.search.tpe_reference",
        "1.0.0",
        SearchKind.TPE,
        True,
        True,
        True,
        False,
        False,
        limitations=("native reference uses a lightweight deterministic density ratio",),
    ),
    SearchAdapterDescriptor("uce.search.successive_halving", "1.0.0", SearchKind.SUCCESSIVE_HALVING, True, True, True, False, True),
    SearchAdapterDescriptor("uce.search.hyperband", "1.0.0", SearchKind.HYPERBAND, True, True, True, False, True),
    SearchAdapterDescriptor("uce.search.evolutionary_reference", "1.0.0", SearchKind.EVOLUTIONARY, True, True, True, False, False),
    SearchAdapterDescriptor("uce.search.pareto", "1.0.0", SearchKind.MULTI_OBJECTIVE, True, True, True, True, False),
    SearchAdapterDescriptor(
        "uce.search.optuna_tpe_adapter",
        "1.0.0",
        SearchKind.TPE,
        False,
        False,
        True,
        True,
        True,
        dependency_profile="optuna>=4",
        limitations=("determinism requires pinned dependency, sampler, storage, and worker count",),
    ),
)


class SearchRegistry:
    def __init__(self, descriptors=CATALOG) -> None:
        self._items: dict[str, SearchAdapterDescriptor] = {}
        self._frozen = False
        for descriptor in descriptors:
            self.register(descriptor)

    def register(self, descriptor: SearchAdapterDescriptor) -> None:
        if self._frozen:
            raise ExperimentError("search_registry_frozen", "cannot mutate a frozen search registry")
        if descriptor.key in self._items:
            raise ExperimentError("duplicate_search_adapter", "search adapter key is already registered", {"key": descriptor.key})
        self._items[descriptor.key] = descriptor

    def freeze(self) -> "SearchRegistry":
        self._frozen = True
        return self

    def resolve_exact(self, key: str) -> SearchAdapterDescriptor:
        try:
            return self._items[key]
        except KeyError as exc:
            raise ExperimentError("search_adapter_not_found", "exact search adapter key is not registered", {"key": key}) from exc

    def snapshot(self) -> SearchRegistrySnapshot:
        descriptors = tuple(self._items[key] for key in sorted(self._items))
        evidence_hash = canonical_sha256([asdict(descriptor) for descriptor in descriptors])
        return SearchRegistrySnapshot(stable_id("ucesearchreg", evidence_hash), descriptors, self._frozen, evidence_hash)
