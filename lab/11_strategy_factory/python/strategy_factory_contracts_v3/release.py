"""Frozen contract-release manifest and evidence verification."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable,Mapping
from .hashing import canonical_sha256
from .schema import SchemaRegistry
from .time_model import UtcInstant
from .validation import require_sha256,require_safe_identifier

@dataclass(frozen=True,slots=True)
class ArtifactDigest:
    path:str
    sha256:str
    media_type:str
    byte_count:int

    def __post_init__(self)->None:
        if not self.path or self.path.startswith("/") or ".." in self.path.split("/"): raise ValueError("artifact path must be repository-relative")
        require_sha256(self.sha256,"artifact.sha256")
        require_safe_identifier(self.media_type,"artifact.media_type")
        if self.byte_count<0:raise ValueError("byte_count cannot be negative")

@dataclass(frozen=True,slots=True)
class ContractReleaseManifest:
    release_id:str
    contract_version:str
    created_at:UtcInstant
    semantic_owner:str
    registry_entries:tuple[Mapping[str,str],...]
    artifacts:tuple[ArtifactDigest,...]
    compatibility_policy_version:str
    migration_registry_version:str
    prior_release_id:str|None=None

    def __post_init__(self)->None:
        require_safe_identifier(self.release_id,"release_id")
        require_safe_identifier(self.contract_version,"contract_version")
        require_safe_identifier(self.semantic_owner,"semantic_owner")
        if not self.registry_entries:raise ValueError("release requires registry entries")

    @property
    def material(self)->dict[str,object]:
        return {
            "artifacts":[{"byte_count":a.byte_count,"media_type":a.media_type,"path":a.path,"sha256":a.sha256} for a in sorted(self.artifacts,key=lambda item:item.path)],
            "compatibility_policy_version":self.compatibility_policy_version,
            "contract_version":self.contract_version,
            "created_at":self.created_at.material(),
            "migration_registry_version":self.migration_registry_version,
            "prior_release_id":self.prior_release_id,
            "registry_entries":list(self.registry_entries),
            "release_id":self.release_id,
            "semantic_owner":self.semantic_owner,
        }

    @property
    def manifest_sha256(self)->str:return canonical_sha256(self.material)


def build_release_manifest(*,release_id:str,created_at:UtcInstant,schemas:SchemaRegistry,artifacts:Iterable[ArtifactDigest],prior_release_id:str|None=None)->ContractReleaseManifest:
    return ContractReleaseManifest(release_id,"3.0.0",created_at,"strategy_factory_contracts",tuple(schemas.manifest()),tuple(artifacts),"1.0.0","1.0.0",prior_release_id)
