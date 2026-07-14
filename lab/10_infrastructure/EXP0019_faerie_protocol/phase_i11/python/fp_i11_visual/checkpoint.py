from dataclasses import dataclass
from .canonical import canonical_sha256,require_hash,require_id
@dataclass(frozen=True,slots=True)
class ProjectionCheckpoint:
 version:str; instance_id:str; config_hash:str; source_snapshot_hash:str; inventory_hash:str; object_ids:tuple[str,...]; created_at:int; payload_hash:str
 def valid(self,instance_id,config_hash): return self.version=='1.0.0' and self.instance_id==instance_id and self.config_hash==config_hash and self.payload_hash==canonical_sha256({'version':self.version,'instance_id':self.instance_id,'config_hash':self.config_hash,'source_snapshot_hash':self.source_snapshot_hash,'inventory_hash':self.inventory_hash,'object_ids':self.object_ids,'created_at':self.created_at})
def build_checkpoint(instance_id,config_hash,source_snapshot_hash,inventory,created_at):
 payload={'version':'1.0.0','instance_id':instance_id,'config_hash':config_hash,'source_snapshot_hash':source_snapshot_hash,'inventory_hash':inventory.inventory_hash,'object_ids':tuple(x.object_id for x in inventory.objects),'created_at':created_at}
 return ProjectionCheckpoint(**payload,payload_hash=canonical_sha256(payload))
