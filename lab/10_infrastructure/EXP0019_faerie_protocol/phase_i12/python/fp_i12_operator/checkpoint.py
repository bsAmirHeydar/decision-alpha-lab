from .contracts import *
from .canonical import sha256,stable_id
from .errors import FPI12Error

def build_checkpoint(config,prefs,alert_state,last_snapshot_hash):
 payload={'version':CHECKPOINT_VERSION,'instance_id':config.instance_id,'config_hash':config.config_hash,'preferences':prefs,'alert_state':alert_state,'last_snapshot_hash':last_snapshot_hash}
 return OperatorCheckpoint(stable_id('FPUXCKPT',payload),CHECKPOINT_VERSION,config.instance_id,config.config_hash,prefs,alert_state,last_snapshot_hash,sha256(payload))
def validate_checkpoint(cp,config):
 if cp.version!=CHECKPOINT_VERSION:raise FPI12Error('FP_UX_CKPT_VERSION_MISMATCH','checkpoint version mismatch')
 if cp.instance_id!=config.instance_id:raise FPI12Error('FP_UX_CKPT_INSTANCE_MISMATCH','checkpoint instance mismatch')
 if cp.config_hash!=config.config_hash:raise FPI12Error('FP_UX_CKPT_CONFIG_MISMATCH','checkpoint config mismatch')
 payload={'version':cp.version,'instance_id':cp.instance_id,'config_hash':cp.config_hash,'preferences':cp.preferences,'alert_state':cp.alert_state,'last_snapshot_hash':cp.last_snapshot_hash}
 if sha256(payload)!=cp.payload_hash:raise FPI12Error('FP_UX_CKPT_PAYLOAD_MISMATCH','checkpoint corrupted')
 return True
