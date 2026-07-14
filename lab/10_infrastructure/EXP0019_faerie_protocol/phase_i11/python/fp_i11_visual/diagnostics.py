from dataclasses import dataclass
from .canonical import canonical_sha256
@dataclass(frozen=True,slots=True)
class ProjectionDiagnostic:
 projection_id:str; source_snapshot_hash:str; object_count:int; create_count:int; update_count:int; delete_count:int; unchanged_count:int; degraded:bool; reason_codes:tuple[str,...]; generated_at:int; diagnostic_hash:str
def build_diagnostic(result,generated_at):
 d={'projection_id':result.projection_id,'source_snapshot_hash':result.snapshot_hash,'object_count':result.object_count,'create_count':len(result.dirty_set.creates),'update_count':len(result.dirty_set.updates),'delete_count':len(result.dirty_set.deletes),'unchanged_count':len(result.dirty_set.unchanged),'degraded':result.degraded,'reason_codes':result.reason_codes,'generated_at':generated_at}
 return ProjectionDiagnostic(**d,diagnostic_hash=canonical_sha256(d))
