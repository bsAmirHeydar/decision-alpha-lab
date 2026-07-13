from __future__ import annotations
from .canonical import canonical_sha256,stable_id
from .contracts import RelationEngineCheckpoint
from .constants import CHECKPOINT_VERSION
from .errors import FPI06Error

def create_checkpoint(config,snapshot,compiler_report,created_utc_ms):
    payload={'config':config.config_hash,'source_revision':snapshot.source_revision_id,'compiler':compiler_report.evidence_hash,'snapshot':snapshot.semantic_hash,'created':created_utc_ms}
    ph=canonical_sha256(payload)
    return RelationEngineCheckpoint(stable_id('FPRELCP',payload,32),CHECKPOINT_VERSION,config.config_hash,snapshot.source_revision_id,compiler_report.evidence_hash,snapshot.semantic_hash,ph,created_utc_ms)
def validate_checkpoint(checkpoint,config,source_revision_id,compiler_report_hash,payload):
    if checkpoint.checkpoint_version!=CHECKPOINT_VERSION:return False,'FP_HRC_CHECKPOINT_VERSION_MISMATCH'
    if checkpoint.config_hash!=config.config_hash:return False,'FP_HRC_CHECKPOINT_CONFIG_MISMATCH'
    if checkpoint.source_revision_id!=source_revision_id:return False,'FP_HRC_CHECKPOINT_REVISION_MISMATCH'
    if checkpoint.compiler_report_hash!=compiler_report_hash:return False,'FP_HRC_CHECKPOINT_COMPILER_MISMATCH'
    if canonical_sha256(payload)!=checkpoint.payload_hash:return False,'FP_HRC_CHECKPOINT_PAYLOAD_CORRUPT'
    return True,'FP_HRC_CHECKPOINT_VALID'
