from __future__ import annotations
from dataclasses import dataclass,asdict
from typing import Mapping
from .canonical import content_hash,merkle_root
@dataclass(frozen=True)
class ArtifactBundle:
    bundle_id:str; manifest_hash:str; artifacts:Mapping[str,str]; lineage_root:str; schema_registry_hash:str; limitations:tuple[str,...]
    @property
    def bundle_hash(self): return content_hash(asdict(self))
def build_bundle(artifacts:Mapping[str,str],lineage_root:str,schema_registry_hash:str,limitations=())->ArtifactBundle:
    manifest_hash=merkle_root(f'{k}:{v}' for k,v in sorted(artifacts.items())); semantic={'manifest_hash':manifest_hash,'artifacts':dict(sorted(artifacts.items())),'lineage_root':lineage_root,'schema_registry_hash':schema_registry_hash,'limitations':tuple(limitations)}
    return ArtifactBundle('bundle_'+content_hash(semantic)[:24],manifest_hash,semantic['artifacts'],lineage_root,schema_registry_hash,tuple(limitations))
