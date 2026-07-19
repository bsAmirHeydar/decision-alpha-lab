from __future__ import annotations
from .canonical import content_id, digest_object
from .constants import PILOT_IDENTITY_ID
from .registries import PILOT_GATES


def _gate(gate_id: str, passed: bool, reason: str, evidence=None, non_compensatory: bool=True):
    return {"gate_id":gate_id,"passed":bool(passed),"non_compensatory":non_compensatory,"reason_code":reason,"evidence":evidence or []}


def evaluate(record: dict) -> dict:
    caps=record["static_profile"].get("capabilities",{})
    language=record.get("source_language")
    gates=[
      _gate("SOURCE_EXISTS",record["source_exists"],"PASS" if record["source_exists"] else "SOURCE_MISSING",[record["source_artifact_path"]]),
      _gate("PACKAGE_CONTEXT_GRANULARITY",record["granularity_class"]=="PACKAGE_CONTEXT","PASS" if record["granularity_class"]=="PACKAGE_CONTEXT" else "NOT_A_PACKAGE_CONTEXT",[record["granularity_class"]]),
      _gate("NOT_PROTECTED_PLATFORM",not record["protected_platform_asset"],"PASS" if not record["protected_platform_asset"] else "PROTECTED_PLATFORM"),
      _gate("NOT_SECURITY_SENSITIVE",not record["security_sensitive"],"PASS" if not record["security_sensitive"] else "SECURITY_REVIEW_REQUIRED"),
      _gate("NO_DIRECT_ORDER_AUTHORITY",not bool(caps.get("order_api")),"PASS" if not caps.get("order_api") else "DIRECT_ORDER_AUTHORITY"),
      _gate("NO_NETWORK_OR_DYNAMIC_EXECUTION",not bool(caps.get("network_api") or caps.get("dynamic_exec")),"PASS" if not (caps.get("network_api") or caps.get("dynamic_exec")) else "NETWORK_OR_DYNAMIC_EXECUTION"),
      _gate("NO_UNSTABLE_RANDOMNESS",not bool(caps.get("randomness")),"PASS" if not caps.get("randomness") else "UNSTABLE_RANDOMNESS"),
      _gate("NO_CURRENT_BAR_OR_FUTURE_AWARENESS",not bool(caps.get("current_bar")),"PASS" if not caps.get("current_bar") else "CURRENT_BAR_OR_FUTURE_AWARENESS"),
      _gate("NO_IDENTITY_COLLISION",not record["identity_collision"],"PASS" if not record["identity_collision"] else "IDENTITY_COLLISION"),
      _gate("OWNER_ROLE_BOUND",record["owner_state"]["role_binding_exists"],"PASS" if record["owner_state"]["role_binding_exists"] else "HUMAN_OWNER_ROLE_PENDING",[record["owner_state"].get("semantic_owner_role")]),
      _gate("ARCHITECT_APPROVED_SELECTION_POLICY",record["identity_id"]==PILOT_IDENTITY_ID,"PASS" if record["identity_id"]==PILOT_IDENTITY_ID else "REJECTED_TIE_BREAK",["LCM_ROADMAP_R1_BALANCED_PARTITION","EXPLICIT_ARCHITECT_DIRECTION_TO_PROCEED_AFTER_LCM07"]),
      _gate("DOCUMENTATION_EVIDENCE_PRESENT",len(record["documentation_evidence"])>=2,"PASS" if len(record["documentation_evidence"])>=2 else "DOCUMENTATION_EVIDENCE_INSUFFICIENT",record["documentation_evidence"]),
      _gate("BOUNDED_PACKAGE_SURFACE",record["static_profile"]["package_file_count"]<=20 and record["static_profile"]["line_count"]<=1200,"PASS" if record["static_profile"]["package_file_count"]<=20 and record["static_profile"]["line_count"]<=1200 else "PACKAGE_SURFACE_UNBOUNDED",[record["static_profile"]["package_file_count"],record["static_profile"]["line_count"]]),
      _gate("REFERENCE_RUNTIME_AVAILABLE",language=="PYTHON","PASS" if language=="PYTHON" else "MQL5_RUNTIME_UNAVAILABLE",[language]),
      _gate("ROLLBACK_SAFE_SOURCE_BOUNDARY",True,"PASS",["NO_SOURCE_MOVE","NO_SOURCE_DELETE","NO_CONSUMER_SWITCH"]),
    ]
    hard_pass=all(g["passed"] for g in gates if g["non_compensatory"])
    evaluation={"schema_version":"1.0.0","evaluation_id":content_id("PILOTEVAL",record["identity_id"]),"identity_id":record["identity_id"],"source_artifact_path":record["source_artifact_path"],"risk_class":record["risk_class"],"aggregate_risk_score":record["aggregate_risk_score"],"gates":gates,"eligible":hard_pass,"selected":False,"selection_rank":None,"evaluation_digest":None}
    evaluation["evaluation_digest"]=digest_object(evaluation,"evaluation_digest")
    return evaluation


def select(records: list[dict]):
    evaluations=[evaluate(r) for r in records]
    eligible=[e for e in evaluations if e["eligible"]]
    eligible.sort(key=lambda e:(e["risk_class"]!="LOW",e["aggregate_risk_score"],e["identity_id"]))
    selected=eligible[0] if eligible else None
    if selected:
        selected["selected"]=True; selected["selection_rank"]=1; selected["evaluation_digest"]=digest_object(selected,"evaluation_digest")
    for index,e in enumerate(eligible[1:],start=2):
        e["selection_rank"]=index;e["evaluation_digest"]=digest_object(e,"evaluation_digest")
    return evaluations, selected
