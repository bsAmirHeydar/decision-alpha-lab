from .canonical import canonical_sha256,stable_id
from .constants import CHECKPOINT_VERSION
from .contracts import LedgerCheckpoint,CheckpointValidation
from .enums import CheckpointDecision

def create_checkpoint(snapshot,source_revision_id,created_utc_ms):
    p={"checkpoint_version":CHECKPOINT_VERSION,"config_hash":snapshot.config_hash,"chain_head_hash":snapshot.chain_head_hash,"event_count":len(snapshot.events),"snapshot_hash":snapshot.snapshot_hash,"source_revision_id":source_revision_id,"created_utc_ms":created_utc_ms}
    h=canonical_sha256(p); return LedgerCheckpoint(stable_id("FPCK",p),CHECKPOINT_VERSION,snapshot.config_hash,snapshot.chain_head_hash,len(snapshot.events),snapshot,source_revision_id,created_utc_ms,h)

def validate_checkpoint(cp,expected_config_hash,expected_chain_head_hash):
    decision=CheckpointDecision.ACCEPT; reason="FP_LDG_CHECKPOINT_ACCEPTED"
    if cp.checkpoint_version!=CHECKPOINT_VERSION: decision=CheckpointDecision.REJECT_VERSION; reason="FP_LDG_CHECKPOINT_VERSION_MISMATCH"
    elif cp.config_hash!=expected_config_hash: decision=CheckpointDecision.REJECT_CONFIG; reason="FP_LDG_CHECKPOINT_CONFIG_MISMATCH"
    elif cp.chain_head_hash!=expected_chain_head_hash: decision=CheckpointDecision.REJECT_CHAIN_HEAD; reason="FP_LDG_CHECKPOINT_CHAIN_HEAD_MISMATCH"
    else:
        p={"checkpoint_version":cp.checkpoint_version,"config_hash":cp.snapshot.config_hash,"chain_head_hash":cp.snapshot.chain_head_hash,"event_count":len(cp.snapshot.events),"snapshot_hash":cp.snapshot.snapshot_hash,"source_revision_id":cp.source_revision_id,"created_utc_ms":cp.created_utc_ms}
        if canonical_sha256(p)!=cp.payload_hash: decision=CheckpointDecision.REJECT_HASH; reason="FP_LDG_CHECKPOINT_PAYLOAD_HASH_MISMATCH"
    v={"decision":decision.value,"checkpoint_id":cp.checkpoint_id,"reason_code":reason,"expected_config_hash":expected_config_hash,"observed_config_hash":cp.config_hash,"expected_chain_head_hash":expected_chain_head_hash,"observed_chain_head_hash":cp.chain_head_hash}
    h=canonical_sha256(v); return CheckpointValidation(stable_id("FPCV",v),decision,cp.checkpoint_id,reason,expected_config_hash,cp.config_hash,expected_chain_head_hash,cp.chain_head_hash,h)
