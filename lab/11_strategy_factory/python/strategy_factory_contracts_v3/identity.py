"""Immutable identity material and stable UCEE v3 identifiers."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .codec import canonical_json
from .enums import IdentityKind
from .errors import IdentityError
from .hashing import canonical_id_digest, canonical_sha256
from .validation import require_safe_identifier
from .version import ID_PREFIX

@dataclass(frozen=True, slots=True)
class IdentityKey:
    kind: IdentityKind
    semantic_namespace: str
    semantic_version: str
    owner_id: str
    dimensions: Mapping[str, Any]

    def __post_init__(self) -> None:
        require_safe_identifier(self.semantic_namespace, "semantic_namespace")
        require_safe_identifier(self.semantic_version, "semantic_version")
        require_safe_identifier(self.owner_id, "owner_id")
        if not self.dimensions:
            raise IdentityError("empty_identity_dimensions", "identity dimensions may not be empty")
        forbidden={"created_at", "updated_at", "wall_clock", "process_id", "random", "uuid"}
        collisions=forbidden.intersection(self.dimensions)
        if collisions:
            raise IdentityError("mutable_identity_dimension", "identity contains mutable or non-deterministic fields", {"fields": sorted(collisions)})

    def material(self) -> dict[str, Any]:
        return {
            "contract_release":"3.0.0",
            "dimensions":dict(self.dimensions),
            "kind":self.kind.value,
            "owner_id":self.owner_id,
            "semantic_namespace":self.semantic_namespace,
            "semantic_version":self.semantic_version,
        }

    @property
    def canonical_material(self) -> str:
        return canonical_json(self.material())

    @property
    def stable_id(self) -> str:
        return f"{ID_PREFIX}_{self.kind.value}_{canonical_id_digest(self.material())}"

    @property
    def evidence_sha256(self) -> str:
        return canonical_sha256(self.material())


def build_identity(kind: IdentityKind | str, *, namespace: str, version: str, owner_id: str, **dimensions: Any) -> IdentityKey:
    try:
        normalized_kind=kind if isinstance(kind, IdentityKind) else IdentityKind(kind)
    except ValueError as exc:
        raise IdentityError("unknown_identity_kind", "identity kind is not registered", {"kind": str(kind)}) from exc
    return IdentityKey(normalized_kind, namespace, version, owner_id, dimensions)
