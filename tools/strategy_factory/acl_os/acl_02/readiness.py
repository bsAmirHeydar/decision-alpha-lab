from __future__ import annotations
from .canonical import digest_object
from .types import IntakeDecision,ReadinessState

def build_readiness(context_id:str,completeness:dict,ambiguity:dict,clock:dict,semantic:dict,security:dict,schema_findings:list,authority:dict)->dict:
    blocking=[];warnings=[]
    sources=[completeness,ambiguity,clock,semantic,security,authority]
    for source in sources:
        for f in source.get("findings",[]):
            (blocking if f["severity"] in {"BLOCKER","ERROR"} else warnings).append(f)
    blocking.extend(schema_findings)
    if blocking: decision=IntakeDecision.NEEDS_INPUT; state=ReadinessState.DRAFT_CONTEXT
    elif ambiguity.get("finding_count",0)>0 or warnings: decision=IntakeDecision.NEEDS_REVIEW; state=ReadinessState.SEMANTIC_REVIEW_REQUIRED
    else: decision=IntakeDecision.ACCEPT_FOR_SEMANTIC_REVIEW; state=ReadinessState.INTAKE_COMPLETE
    stages={
      "intake_complete":{"ready":not blocking,"blockers":blocking},
      "semantic_review":{"ready":not blocking,"manual_approval_required":True},
      "context_compile":{"ready":False,"reason_codes":["ACL03_CONTEXT_COMPILER_REQUIRED"]},
      "research_entry":{"ready":False,"reason_codes":["ACL05_IMMUTABLE_BATCH_REQUIRED"]},
      "live_activation":{"ready":False,"reason_codes":["ACL11_RUNTIME_PARITY_REQUIRED","ACL12_SECURITY_HARDENING_REQUIRED","ACL14_CAPITAL_AUTHORIZATION_REQUIRED"]}}
    body={"context_id":context_id,"decision":decision.value,"highest_state":state.value,"completeness_score":completeness["overall_score"],"blocking_count":len(blocking),"warning_count":len(warnings),"blocking_findings":blocking,"warning_findings":warnings,"stages":stages,"claim_ceiling":"SEMANTIC_INTAKE_REFERENCE_ONLY","live_order_submission_allowed":False,"capital_activation_allowed":False}
    return {**body,"report_digest":digest_object(body)}
