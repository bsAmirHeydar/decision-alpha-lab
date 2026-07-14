from __future__ import annotations
from dataclasses import replace
from .contracts import *
from .preferences import default_preferences,normalize_preferences
from .filters import apply_filters
from .panel import build_panel,bind_panel_instance
from .alerts import AlertRouter,derive_alert_candidates
from .exporter import AuditExporter
from .actions import apply_action
from .diagnostics import build_diagnostic
from .canonical import stable_id,sha256
from .checkpoint import validate_checkpoint
class OperatorUXEngine:
 def __init__(self,config,checkpoint=None):
  self.config=config;self.previous=None;self.rebuild_requested=False;self.pending_export=False
  if checkpoint:
   validate_checkpoint(checkpoint,config);self.preferences=normalize_preferences(checkpoint.preferences);self.alerts=AlertRouter(config.instance_id,config.alerts,checkpoint.alert_state)
  else:self.preferences=default_preferences(config);self.alerts=AlertRouter(config.instance_id,config.alerts)
  self.exporter=AuditExporter(config.instance_id,config.export);self.last_output=None
 def action(self,request):
  result=apply_action(request,self.preferences);self.preferences=result.preferences;self.rebuild_requested|=result.rebuild_requested;self.pending_export|=result.export_requested
  if request.action is OperatorAction.ACK_ALERT:self.alerts.acknowledge(request.value)
  elif request.action is OperatorAction.ACK_ALL:self.alerts.acknowledge_all()
  return result
 def process(self,snapshot,now=None):
  now=snapshot.generated_at if now is None else now
  filtered=apply_filters(snapshot.items,self.preferences.filters,snapshot.computed_hash)
  panel=bind_panel_instance(build_panel(snapshot,filtered,self.preferences.panel,self.preferences.page),self.config.instance_id)
  events=tuple(self.alerts.route(c,now) for c in derive_alert_candidates(snapshot,self.previous))
  exports=[]
  if self.config.export.enabled and (self.config.export.auto_export_on_change or self.pending_export):
   for fmt in self.config.export.formats:exports.append(self.exporter.export(snapshot,fmt))
   self.pending_export=False
  alert_state=self.alerts.snapshot();diag=build_diagnostic(self.config,panel,filtered,alert_state,exports,('FP_REBUILD_REQUEST_RECORDED',) if self.rebuild_requested else ())
  payload={'snapshot_hash':snapshot.computed_hash,'panel_hash':panel.panel_hash,'filter_hash':filtered.result_hash,'alerts':[x.event_hash for x in events],'exports':[x.content_hash for x in exports],'preferences_hash':self.preferences.preferences_hash,'diagnostic_hash':diag.diagnostic_hash}
  out=OperatorOutput(stable_id('FPUXOUT',payload),snapshot.computed_hash,panel,filtered,events,tuple(exports),self.preferences,diag,sha256(payload));self.previous=snapshot;self.last_output=out;return out
