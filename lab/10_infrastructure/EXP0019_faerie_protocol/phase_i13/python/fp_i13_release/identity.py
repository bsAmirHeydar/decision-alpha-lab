from .contracts import InstanceIdentity
from .canonical import sha256,stable_id,require_hash

def build_instance_identity(chart_id:int,terminal_path:str,pair_id:str,context_epoch:str,config_hash:str)->InstanceIdentity:
    require_hash(config_hash,'config_hash')
    terminal_path_hash=sha256({'terminal_path':terminal_path})
    core={'chart_id':int(chart_id),'terminal_path_hash':terminal_path_hash,'pair_id':pair_id,'context_epoch':context_epoch,'config_hash':config_hash}
    iid=stable_id('FPINST',core)
    short=sha256(core)[:16]
    return InstanceIdentity(iid,int(chart_id),terminal_path_hash,pair_id,context_epoch,config_hash,f'FP19::{short}::',f'FPCP::{short}',f'FP_AUDIT_{short}')
