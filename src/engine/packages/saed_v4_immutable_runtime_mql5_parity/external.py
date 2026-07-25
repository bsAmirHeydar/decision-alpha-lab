from __future__ import annotations
from copy import deepcopy
from .contracts import exact,enum,sha256
from .errors import ExternalEvidenceError
from .canonical import seal
STATUSES={"PASSED","FAILED","PENDING_EXTERNAL","NOT_APPLICABLE"}

def freeze_external_evidence(items:list[dict])->dict:
 required={"PYTHON_REFERENCE","MQL5_STATIC_VALIDATION","METAEDITOR_COMPILE","TERMINAL_VECTOR_REPLAY","CROSS_RUNTIME_STATE_REPLAY","WINDOWS_DLL_BOUNDARY","BROKER_ROUTE_GUARD"}
 by={x.get("evidence_type"):x for x in items}
 if set(by)!=required:raise ExternalEvidenceError(f"external evidence matrix mismatch: {sorted(set(by)^required)}")
 out=[]
 for typ in sorted(required):
  x=by[typ]; exact(x,["evidence_id","evidence_type","status","environment","artifact_hash","observed_at","independent_reviewer","actual_external_evidence","notes"]); enum(x["status"],STATUSES,"status"); sha256(x["artifact_hash"],"artifact_hash")
  if typ in {"METAEDITOR_COMPILE","TERMINAL_VECTOR_REPLAY","CROSS_RUNTIME_STATE_REPLAY","WINDOWS_DLL_BOUNDARY"} and x["status"]=="PASSED" and x["actual_external_evidence"] is not True:raise ExternalEvidenceError("cannot pass external gate without actual evidence")
  out.append(deepcopy(x))
 external_complete=all(x["status"]=="PASSED" for x in out if x["evidence_type"] in {"METAEDITOR_COMPILE","TERMINAL_VECTOR_REPLAY","CROSS_RUNTIME_STATE_REPLAY","WINDOWS_DLL_BOUNDARY"})
 return seal({"phase":"SAED_V4_38","items":out,"external_runtime_evidence_complete":external_complete,"actual_metaeditor_compile_passed":by["METAEDITOR_COMPILE"]["status"]=="PASSED" and by["METAEDITOR_COMPILE"]["actual_external_evidence"] is True,"actual_terminal_parity_passed":by["TERMINAL_VECTOR_REPLAY"]["status"]=="PASSED" and by["TERMINAL_VECTOR_REPLAY"]["actual_external_evidence"] is True,"research_only":True},"v438_external","matrix_id","matrix_hash")
