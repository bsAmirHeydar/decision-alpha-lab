"""Explicit directional schema migration graph with cryptographic evidence."""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Mapping
from .enums import MigrationMode
from .errors import MigrationError
from .hashing import canonical_sha256
from .schema import SchemaId, SchemaRegistry
from .time_model import UtcInstant
from .validation import require_safe_identifier

MigrationFunction=Callable[[Mapping[str,Any]],Mapping[str,Any]]

@dataclass(frozen=True,slots=True)
class MigrationEdge:
    migration_id:str
    source:SchemaId
    destination:SchemaId
    source_semantic_hash:str
    destination_semantic_hash:str
    mode:MigrationMode
    transformer:MigrationFunction

    def __post_init__(self)->None:
        require_safe_identifier(self.migration_id,"migration_id")
        if self.source.family_key != self.destination.family_key:
            raise MigrationError("cross_family_migration","schema migrations must remain within one schema family")
        if self.destination.version <= self.source.version:
            raise MigrationError("non_monotonic_migration","destination version must be greater than source version")

@dataclass(frozen=True,slots=True)
class MigrationEvidence:
    migration_path:tuple[str,...]
    source_schema:str
    destination_schema:str
    source_payload_sha256:str
    destination_payload_sha256:str
    applied_at:UtcInstant
    mode_chain:tuple[str,...]

class MigrationRegistry:
    def __init__(self,schema_registry:SchemaRegistry,edges:Iterable[MigrationEdge]=())->None:
        self.schemas=schema_registry
        self._edges:dict[str,MigrationEdge]={}
        self._from:dict[str,list[MigrationEdge]]={}
        for edge in edges:self.register(edge)

    def register(self,edge:MigrationEdge)->None:
        if edge.migration_id in self._edges: raise MigrationError("duplicate_migration","migration_id is already registered",{"migration_id":edge.migration_id})
        source=self.schemas.resolve_exact(edge.source)
        destination=self.schemas.resolve_exact(edge.destination)
        if source.semantic_hash!=edge.source_semantic_hash or destination.semantic_hash!=edge.destination_semantic_hash:
            raise MigrationError("migration_semantic_hash_mismatch","edge hashes do not match schema registry")
        self._edges[edge.migration_id]=edge
        self._from.setdefault(edge.source.exact_key,[]).append(edge)
        self._from[edge.source.exact_key].sort(key=lambda item:item.destination.exact_key)

    def find_path(self,source:SchemaId,destination:SchemaId)->tuple[MigrationEdge,...]:
        if source.exact_key==destination.exact_key:return ()
        queue=deque([(source.exact_key,())])
        visited={source.exact_key}
        while queue:
            current,path=queue.popleft()
            for edge in self._from.get(current,[]):
                candidate=path+(edge,)
                if edge.destination.exact_key==destination.exact_key:return candidate
                if edge.destination.exact_key not in visited:
                    visited.add(edge.destination.exact_key);queue.append((edge.destination.exact_key,candidate))
        raise MigrationError("migration_path_missing","no explicit migration path exists",{"source":source.exact_key,"destination":destination.exact_key})

    def migrate(self,payload:Mapping[str,Any],source:SchemaId,destination:SchemaId,*,applied_at:UtcInstant)->tuple[Mapping[str,Any],MigrationEvidence]:
        path=self.find_path(source,destination)
        current=dict(payload)
        source_hash=canonical_sha256(current)
        for edge in path:
            current=dict(edge.transformer(current))
        destination_hash=canonical_sha256(current)
        evidence=MigrationEvidence(
            migration_path=tuple(edge.migration_id for edge in path),
            source_schema=source.exact_key,destination_schema=destination.exact_key,
            source_payload_sha256=source_hash,destination_payload_sha256=destination_hash,
            applied_at=applied_at,mode_chain=tuple(edge.mode.value for edge in path),
        )
        return current,evidence
