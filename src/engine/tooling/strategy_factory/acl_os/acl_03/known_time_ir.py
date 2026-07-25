from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id
from .types import Finding,Severity

REQUIRED_ORDER=("event_time<=observation_time","observation_time<=known_time","known_time<=decision_time","decision_time<=maturity_time","maturity_time<=correction_time")

def compile_known_time_ir(package:dict[str,Any])->tuple[dict[str,Any],list[dict[str,Any]]]:
    c=package["causal_clock"]; findings=[]; order=tuple(c.get("required_order",[]))
    for relation in REQUIRED_ORDER:
        if relation not in order: findings.append(Finding("ACL03_CLOCK_ORDER_MISSING",Severity.BLOCKER,"causal_clock.required_order","required causal ordering relation is absent","declare the full causal partial order",{"relation":relation}).to_dict())
    guards=[]
    for relation in REQUIRED_ORDER:
        left,right=relation.split("<=")
        guards.append({"guard_id":stable_id("KTG",package["manifest"]["context_id"],relation),"left_clock":left,"operator":"<=","right_clock":right,"failure_action":"REJECT_EVENT"})
    source_guards=[]
    for src in package["data"].get("sources",[]):
        source_guards.append({"source_id":src["source_id"],"known_time_field":src["known_time_field"],"freshness_slo_ms":src["freshness_slo_ms"],"missingness_policy":src["missingness_policy"],"future_revision_allowed":False})
    body={"schema_version":"1.0.0","context_id":package["manifest"]["context_id"],"timezone":c["timezone"],"calendar_id":c["calendar_id"],"clock_skew_tolerance_ms":c["clock_skew_tolerance_ms"],"late_data_policy":c["late_data_policy"],"guards":guards,"source_guards":source_guards,"future_revision_allowed":False}
    return {**body,"known_time_ir_digest":digest_object(body)},findings
