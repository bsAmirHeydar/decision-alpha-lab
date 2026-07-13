"""Exact-version frozen registry for UCE-I10 algorithm descriptors."""

from __future__ import annotations

from dataclasses import asdict

from .canonical import canonical_sha256, stable_id
from .catalog import CATALOG
from .contracts import DeepAlgorithmDescriptor, DeepRegistrySnapshot
from .errors import DeepViewError


class DeepAlgorithmRegistry:
    def __init__(self, descriptors=CATALOG) -> None:
        self._items: dict[str, DeepAlgorithmDescriptor] = {}
        self._frozen = False
        for descriptor in descriptors:
            self.register(descriptor)

    def register(self, descriptor: DeepAlgorithmDescriptor) -> None:
        if self._frozen:
            raise DeepViewError("deep_registry_frozen", "cannot mutate a frozen deep registry")
        if descriptor.key in self._items:
            raise DeepViewError("duplicate_deep_algorithm", "algorithm key is already registered", {"key": descriptor.key})
        self._items[descriptor.key] = descriptor

    def freeze(self) -> "DeepAlgorithmRegistry":
        self._frozen = True
        return self

    @property
    def frozen(self) -> bool:
        return self._frozen

    def resolve_exact(self, key: str) -> DeepAlgorithmDescriptor:
        try:
            return self._items[key]
        except KeyError as exc:
            raise DeepViewError("deep_algorithm_not_found", "exact algorithm key is not registered", {"key": key}) from exc

    def snapshot(self) -> DeepRegistrySnapshot:
        descriptors = tuple(self._items[key] for key in sorted(self._items))
        evidence_hash = canonical_sha256([asdict(descriptor) for descriptor in descriptors])
        return DeepRegistrySnapshot(
            stable_id("ucedeepreg", evidence_hash),
            descriptors,
            self._frozen,
            evidence_hash,
        )
