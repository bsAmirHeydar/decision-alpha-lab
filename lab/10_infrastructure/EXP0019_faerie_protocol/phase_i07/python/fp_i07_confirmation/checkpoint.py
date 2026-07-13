from .canonical import canonical_sha256,stable_id
from .constants import CHECKPOINT_VERSION
from .contracts import ConfirmationCheckpoint
from .errors import FPI07Error

def build_checkpoint(config,pending,results,last_processed_close_utc_ms,source_revision_id):
    pending=tuple(sorted(pending,key=lambda p:p.pending_id));results=tuple(sorted(results,key=lambda r:r.result_id))
    material={"version":CHECKPOINT_VERSION,"config":config.config_hash,"pending":[p.pending_hash for p in pending],"results":[r.result_hash for r in results],"last":last_processed_close_utc_ms,"revision":source_revision_id}
    return ConfirmationCheckpoint(stable_id("FPCONFCP",material,32),CHECKPOINT_VERSION,config.config_hash,pending,results,last_processed_close_utc_ms,source_revision_id,canonical_sha256(material))
def validate_checkpoint(cp,config):
    if cp.checkpoint_version!=CHECKPOINT_VERSION: raise FPI07Error("FP_CRC_CHECKPOINT_VERSION_MISMATCH","checkpoint version mismatch")
    if cp.config_hash!=config.config_hash: raise FPI07Error("FP_CRC_CHECKPOINT_CONFIG_MISMATCH","checkpoint config mismatch")
    material={"version":cp.checkpoint_version,"config":cp.config_hash,"pending":[p.pending_hash for p in cp.pending],"results":[r.result_hash for r in cp.results],"last":cp.last_processed_close_utc_ms,"revision":cp.source_revision_id}
    if canonical_sha256(material)!=cp.payload_hash: raise FPI07Error("FP_CRC_CHECKPOINT_HASH_MISMATCH","checkpoint payload hash mismatch")
    return True
