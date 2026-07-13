from __future__ import annotations
from dataclasses import dataclass
from .canonical import canonical_sha256,stable_id,require_sha256,require_semver
from .errors import FPI08Error
@dataclass(frozen=True,slots=True)
class WWCheckpoint:
    checkpoint_id:str; checkpoint_version:str; config_hash:str; snapshot_hash:str; active_stack_hash:str; source_revision_id:str; created_utc_ms:int; payload_hash:str
    def __post_init__(self):
        require_semver(self.checkpoint_version,"checkpoint_version");require_sha256(self.config_hash,"config_hash");require_sha256(self.snapshot_hash,"snapshot_hash");require_sha256(self.active_stack_hash,"active_stack_hash");require_sha256(self.payload_hash,"payload_hash")
def create_checkpoint(snapshot):
    mat={"version":"1.0.0","config":snapshot.config_hash,"snapshot":snapshot.snapshot_hash,"stack":snapshot.active_stack.stack_hash,"revision":snapshot.source_revision_id,"created":snapshot.created_utc_ms}
    return WWCheckpoint(stable_id("FPWWCP",mat,32),"1.0.0",snapshot.config_hash,snapshot.snapshot_hash,snapshot.active_stack.stack_hash,snapshot.source_revision_id,snapshot.created_utc_ms,canonical_sha256(mat))
def validate_checkpoint(cp,snapshot):
    if cp.config_hash!=snapshot.config_hash: raise FPI08Error("FP_WRC_CHECKPOINT_CONFIG_MISMATCH","checkpoint config mismatch")
    if cp.snapshot_hash!=snapshot.snapshot_hash or cp.active_stack_hash!=snapshot.active_stack.stack_hash: raise FPI08Error("FP_WRC_CHECKPOINT_PAYLOAD_MISMATCH","checkpoint payload mismatch")
    return True
