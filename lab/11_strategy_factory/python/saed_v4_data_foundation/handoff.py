from __future__ import annotations
from .models import TwinSeedPackage,DatasetSnapshot
from .canonical import stable_id
from .errors import IntegrityViolation

def build_twin_seed(context_specification_artifact_id:str,snapshots:list[DatasetSnapshot],schema_versions:dict[str,str],lineage_root:str,known_as_of:str,constitution_hash:str,limitations=())->TwinSeedPackage:
    if not context_specification_artifact_id: raise IntegrityViolation('context specification artifact is required')
    if not snapshots: raise IntegrityViolation('at least one sovereign snapshot is required')
    payload={'context_specification_artifact_id':context_specification_artifact_id,'snapshot_ids':sorted(s.snapshot_id for s in snapshots),'schema_versions':dict(sorted(schema_versions.items())),'lineage_root':lineage_root,'known_as_of':known_as_of,'constitution_hash':constitution_hash,'limitations':tuple(limitations)}
    return TwinSeedPackage(stable_id('twinseed',payload),context_specification_artifact_id,tuple(payload['snapshot_ids']),payload['schema_versions'],lineage_root,known_as_of,constitution_hash,tuple(limitations))
