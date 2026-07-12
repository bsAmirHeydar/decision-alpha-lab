"""Evidence-preserving bridge from SF01 identities to UCEE v3 identities."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Mapping
from .enums import IdentityKind
from .hashing import canonical_sha256
from .identity import IdentityKey
from .schema import SchemaId
from .time_model import UtcInstant
from .validation import require_safe_identifier

@dataclass(frozen=True,slots=True)
class LegacyBridgeRecord:
    legacy_contract_id:str
    legacy_schema_id:str
    legacy_entity_id:str
    legacy_payload_sha256:str
    v3_entity_id:str
    v3_identity_sha256:str
    bridged_at:UtcInstant
    bridge_version:str="1.0.0"


def bridge_sf01(*,legacy_contract_id:str,legacy_schema:SchemaId,legacy_entity_id:str,legacy_payload:Mapping[str,Any],target_kind:IdentityKind,semantic_namespace:str,semantic_version:str,owner_id:str,extra_dimensions:Mapping[str,Any]|None=None,bridged_at:UtcInstant)->tuple[IdentityKey,LegacyBridgeRecord]:
    require_safe_identifier(legacy_contract_id,"legacy_contract_id")
    require_safe_identifier(legacy_entity_id,"legacy_entity_id")
    dimensions={
        "legacy_contract_id":legacy_contract_id,
        "legacy_entity_id":legacy_entity_id,
        "legacy_payload_sha256":canonical_sha256(legacy_payload),
        "legacy_schema_id":legacy_schema.exact_key,
    }
    dimensions.update(dict(extra_dimensions or {}))
    identity=IdentityKey(target_kind,semantic_namespace,semantic_version,owner_id,dimensions)
    record=LegacyBridgeRecord(
        legacy_contract_id=legacy_contract_id,
        legacy_schema_id=legacy_schema.exact_key,
        legacy_entity_id=legacy_entity_id,
        legacy_payload_sha256=dimensions["legacy_payload_sha256"],
        v3_entity_id=identity.stable_id,
        v3_identity_sha256=identity.evidence_sha256,
        bridged_at=bridged_at,
    )
    return identity,record
