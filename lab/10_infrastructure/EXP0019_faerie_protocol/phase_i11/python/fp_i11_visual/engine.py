from .contracts import *
from .projectors import project_all
from .object_manager import ObjectManager
from .retention import retain_snapshot
from .canonical import stable_id,canonical_sha256
from .diagnostics import build_diagnostic
class VisualProjectionEngine:
 def __init__(self,config): self.config=config; self.manager=ObjectManager(config.instance_id); self.last_result=None
 def project(self,snapshot,layout):
  retained=retain_snapshot(snapshot,snapshot.generated_at,self.config.history_days)
  specs=project_all(retained,self.config,layout)
  degraded=False; reasons=[]
  if len(specs)>self.config.max_objects:
   degraded=True;reasons.append('FP_VIS_OBJECT_BUDGET_DEGRADED'); specs=specs[-self.config.max_objects:]
  dirty=self.manager.diff(specs,self.config.max_objects); inventory=self.manager.apply(dirty)
  payload={'snapshot_hash':snapshot.snapshot_hash,'dirty_hash':dirty.dirty_hash,'inventory_hash':inventory.inventory_hash,'degraded':degraded,'reason_codes':tuple(sorted(reasons))}
  result=ProjectionResult(stable_id('FPPROJ',payload),snapshot.snapshot_hash,specs,dirty,len(inventory.objects),degraded,tuple(sorted(reasons)),canonical_sha256(payload));self.last_result=result;return result
 def diagnostic(self): return build_diagnostic(self.last_result,self.last_result.specs[-1].anchor.time1 if self.last_result and self.last_result.specs else 0)
