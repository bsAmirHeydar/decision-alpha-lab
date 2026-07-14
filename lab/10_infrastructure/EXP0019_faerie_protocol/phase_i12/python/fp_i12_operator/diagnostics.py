from .contracts import *
from .canonical import sha256,stable_id

def build_diagnostic(config,panel,filtered,alert_state,exports,reason_codes=()):
 health=OperatorHealth.READY
 reasons=set(reason_codes)
 if config.open_decision_state=='UNSET':health=OperatorHealth.DEGRADED;reasons.add('FP_UX_OPEN_DECISION_UNSET')
 if panel.state is PanelState.HIDDEN:reasons.add('FP_UX_PANEL_HIDDEN')
 last_export_hash=exports[-1].content_hash if exports else sha256('')
 payload={'health':health.value,'panel_hash':panel.panel_hash,'filter_hash':filtered.filter_hash,'alert_state_hash':alert_state.state_hash,'last_export_hash':last_export_hash,'reasons':sorted(reasons)}
 return OperatorDiagnostic(stable_id('FPUXDIAG',payload),health,panel.panel_hash,filtered.filter_hash,alert_state.state_hash,last_export_hash,tuple(sorted(reasons)),sha256(payload))
