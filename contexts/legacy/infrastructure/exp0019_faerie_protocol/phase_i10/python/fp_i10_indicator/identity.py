from .canonical import stable_id,canonical_sha256
from .contracts import IndicatorConfig,InstanceIdentity
from .constants import INDICATOR_PRODUCT_ID

def build_instance_identity(config:IndicatorConfig, chart_id:int, terminal_instance_id:str, program_name:str=INDICATOR_PRODUCT_ID)->InstanceIdentity:
    payload={'chart_id':chart_id,'terminal_instance_id':terminal_instance_id,'program_name':program_name,'pair_id':config.pair_id,'context_epoch':config.context_epoch,'config_hash':config.config_hash}
    instance_id=stable_id('FPINST',payload)
    namespace=f'FP19::{instance_id}::'
    checkpoint_key=f'FP19_CHECKPOINT::{instance_id}'
    identity_hash=canonical_sha256({**payload,'instance_id':instance_id,'object_namespace':namespace,'checkpoint_key':checkpoint_key})
    return InstanceIdentity(instance_id,chart_id,terminal_instance_id,program_name,config.pair_id,config.context_epoch,config.config_hash,namespace,checkpoint_key,identity_hash)
