from .contracts import *
from .canonical import *
def create_checkpoint(config_hash,policy,ledger,quota_records=(),orders=(),fills=(),positions=()):
    payload={"version":CHECKPOINT_VERSION,"config":config_hash,"policy":policy.policy_hash,"ledger":ledger,"quota":quota_records,"orders":orders,"fills":fills,"positions":positions}
    return PaperCheckpoint(stable_id("FPCP",payload),CHECKPOINT_VERSION,config_hash,policy.policy_hash,tuple(ledger),tuple(quota_records),tuple(orders),tuple(fills),tuple(positions),sha256(payload))
def validate_checkpoint(cp,config_hash,policy):
    if cp.version!=CHECKPOINT_VERSION: return CheckpointValidation(CheckpointDisposition.REJECT_VERSION,("FP_PAPER_CHECKPOINT_VERSION_MISMATCH",))
    if cp.config_hash!=config_hash or cp.policy_hash!=policy.policy_hash: return CheckpointValidation(CheckpointDisposition.REJECT_CONFIG,("FP_PAPER_CHECKPOINT_CONFIG_MISMATCH",))
    payload={"version":cp.version,"config":cp.config_hash,"policy":cp.policy_hash,"ledger":cp.ledger,"quota":cp.quota_records,"orders":cp.orders,"fills":cp.fills,"positions":cp.positions}
    if sha256(payload)!=cp.payload_hash: return CheckpointValidation(CheckpointDisposition.REJECT_HASH,("FP_PAPER_CHECKPOINT_HASH_MISMATCH",))
    return CheckpointValidation(CheckpointDisposition.ACCEPTED,("FP_PAPER_CHECKPOINT_ACCEPTED",))
