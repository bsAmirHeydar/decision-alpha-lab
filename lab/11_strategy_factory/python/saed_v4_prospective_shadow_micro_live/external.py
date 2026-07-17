from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,enum,sha256
from .errors import ExternalEvidenceError
from .canonical import seal
STATUSES={"PASSED","FAILED","PENDING_EXTERNAL","NOT_APPLICABLE_APPROVED"}
def freeze_external_evidence(items:list[dict])->dict:
 xs=list_of(items,"external_evidence",12);unique(xs,"evidence_id","external_evidence");out=[]
 for x in xs:
  exact(x,["evidence_id","evidence_type","status","environment","artifact_hash","observed_at","independent_reviewer","actual_external_evidence","notes"]);enum(x["status"],STATUSES,"status");sha256(x["artifact_hash"],"artifact_hash")
  if x["status"]=="PASSED" and x["evidence_type"] in {"METAEDITOR_COMPILE","TERMINAL_VECTOR_REPLAY","CROSS_RUNTIME_STATE_REPLAY","DEMO_CONNECTIVITY","LIVE_CONNECTIVITY","PROSPECTIVE_PAPER_PERIOD","PROSPECTIVE_SHADOW_PERIOD","MICRO_LIVE_AUTHORIZATION","KEY_CUSTODY","BROKER_RECONCILIATION","KILL_SWITCH_LIVE_DRILL"} and x["actual_external_evidence"] is not True:raise ExternalEvidenceError("external pass requires actual evidence")
  out.append(deepcopy(x))
 by={x["evidence_type"]:x for x in out}
 required=["METAEDITOR_COMPILE","TERMINAL_VECTOR_REPLAY","CROSS_RUNTIME_STATE_REPLAY","DEMO_CONNECTIVITY","LIVE_CONNECTIVITY","PROSPECTIVE_PAPER_PERIOD","PROSPECTIVE_SHADOW_PERIOD","MICRO_LIVE_AUTHORIZATION","KEY_CUSTODY","BROKER_RECONCILIATION","KILL_SWITCH_LIVE_DRILL","INDEPENDENT_MODEL_RISK_APPROVAL"]
 if any(k not in by for k in required):raise ExternalEvidenceError("required external evidence types missing")
 return seal({"phase":"SAED_V4_39","items":sorted(out,key=lambda z:z["evidence_type"]),"actual_metaeditor_compile_passed":by["METAEDITOR_COMPILE"]["status"]=="PASSED" and by["METAEDITOR_COMPILE"]["actual_external_evidence"],"actual_terminal_parity_passed":by["TERMINAL_VECTOR_REPLAY"]["status"]=="PASSED" and by["TERMINAL_VECTOR_REPLAY"]["actual_external_evidence"],"actual_demo_connectivity_passed":by["DEMO_CONNECTIVITY"]["status"]=="PASSED" and by["DEMO_CONNECTIVITY"]["actual_external_evidence"],"actual_live_connectivity_passed":by["LIVE_CONNECTIVITY"]["status"]=="PASSED" and by["LIVE_CONNECTIVITY"]["actual_external_evidence"],"actual_prospective_paper_passed":by["PROSPECTIVE_PAPER_PERIOD"]["status"]=="PASSED" and by["PROSPECTIVE_PAPER_PERIOD"]["actual_external_evidence"],"actual_prospective_shadow_passed":by["PROSPECTIVE_SHADOW_PERIOD"]["status"]=="PASSED" and by["PROSPECTIVE_SHADOW_PERIOD"]["actual_external_evidence"],"actual_micro_live_authorized":by["MICRO_LIVE_AUTHORIZATION"]["status"]=="PASSED" and by["MICRO_LIVE_AUTHORIZATION"]["actual_external_evidence"],"research_only":True,"production_authorized":False},"v439_external","matrix_id","matrix_hash")
