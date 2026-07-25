from .registry import *
from .enums import *
def run_conformance():
 checks={
 'phase_version':VERSIONS['phase']=='1.0.0',
 'relations':set(ALLOWED_RELATIONS)=={'AL','AN','LN','NA','NL','NN','WW'},
 'panel_modes':len(PanelMode)==4,
 'alert_types':len(AlertType)==8,
 'export_formats':set(x.value for x in ExportFormat)=={'CSV','JSONL'},
 'open_decision_preserved':OPEN_DECISION_ID=='FP-DEC-012',
 'reason_registry_closed':len(REASON_CODES)==len(set(REASON_CODES)),
 'no_execution_contract':True,
 }
 return checks
