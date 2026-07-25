from .contracts import IndicatorCheckpoint,CheckpointValidation
from .constants import CHECKPOINT_VERSION
from .canonical import canonical_sha256,stable_id
from .enums import CheckpointDisposition

def create_checkpoint(*,instance,composition,snapshot,last_processed_m1,lifecycle_sequence,source_revision_id):
    payload={'checkpoint_version':CHECKPOINT_VERSION,'instance_id':instance.instance_id,'config_hash':instance.config_hash,'composition_hash':composition.manifest_hash,'last_processed_m1':last_processed_m1,'lifecycle_sequence':lifecycle_sequence,'snapshot_hash':snapshot.snapshot_hash,'source_revision_id':source_revision_id}
    return IndicatorCheckpoint(stable_id('FPCKPT',payload),CHECKPOINT_VERSION,instance.instance_id,instance.config_hash,composition.manifest_hash,last_processed_m1,lifecycle_sequence,snapshot.snapshot_hash,source_revision_id,canonical_sha256(payload))

def validate_checkpoint(checkpoint,*,instance,composition):
    if checkpoint is None: disp=CheckpointDisposition.ABSENT; reasons=('FP_IND_CHECKPOINT_ABSENT',); accepted=False
    elif checkpoint.checkpoint_version!=CHECKPOINT_VERSION: disp=CheckpointDisposition.REJECT_VERSION; reasons=('FP_IND_CHECKPOINT_VERSION_MISMATCH',); accepted=False
    elif checkpoint.instance_id!=instance.instance_id: disp=CheckpointDisposition.REJECT_INSTANCE; reasons=('FP_IND_CHECKPOINT_INSTANCE_MISMATCH',); accepted=False
    elif checkpoint.config_hash!=instance.config_hash: disp=CheckpointDisposition.REJECT_CONFIG; reasons=('FP_IND_CHECKPOINT_CONFIG_MISMATCH',); accepted=False
    elif checkpoint.composition_hash!=composition.manifest_hash: disp=CheckpointDisposition.REJECT_HASH; reasons=('FP_IND_CHECKPOINT_COMPOSITION_MISMATCH',); accepted=False
    else:
        payload={'checkpoint_version':checkpoint.checkpoint_version,'instance_id':checkpoint.instance_id,'config_hash':checkpoint.config_hash,'composition_hash':checkpoint.composition_hash,'last_processed_m1':checkpoint.last_processed_m1,'lifecycle_sequence':checkpoint.lifecycle_sequence,'snapshot_hash':checkpoint.snapshot_hash,'source_revision_id':checkpoint.source_revision_id}
        if canonical_sha256(payload)!=checkpoint.payload_hash: disp=CheckpointDisposition.REJECT_HASH; reasons=('FP_IND_CHECKPOINT_PAYLOAD_MISMATCH',); accepted=False
        else: disp=CheckpointDisposition.RESTORED; reasons=('FP_IND_CHECKPOINT_RESTORED',); accepted=True
    material={'disposition':disp.value,'accepted':accepted,'reason_codes':reasons}
    return CheckpointValidation(disp,accepted,tuple(sorted(reasons)),canonical_sha256(material))
