from __future__ import annotations
from datetime import datetime,timezone
from .types import Finding,Severity

def validate_authority_binding(manifest:dict,permit:dict|None)->dict:
    findings=[]
    if permit is None:
        findings.append(Finding("ACL02_AUTHORITY_PERMIT_MISSING",Severity.BLOCKER,"authority_permit","ACL-00 semantic-intake permit is absent","obtain an ALLOW permit for ACL02_EVALUATE_CONTEXT"))
    else:
        if permit.get("decision")!="ALLOW":findings.append(Finding("ACL02_AUTHORITY_NOT_ALLOWED",Severity.BLOCKER,"authority_permit.decision","authority decision is not ALLOW","use an approved unexpired permit"))
        if permit.get("action")!="ACL02_EVALUATE_CONTEXT":findings.append(Finding("ACL02_AUTHORITY_ACTION_MISMATCH",Severity.BLOCKER,"authority_permit.action","permit action mismatch","request exact ACL02_EVALUATE_CONTEXT authority"))
        if permit.get("subject_artifact_id")!=manifest.get("artifact_id"):findings.append(Finding("ACL02_AUTHORITY_SUBJECT_MISMATCH",Severity.BLOCKER,"authority_permit.subject_artifact_id","permit does not bind this Context artifact","issue a subject-bound permit"))
        if permit.get("live_order_submission_allowed") or permit.get("capital_activation_allowed"):findings.append(Finding("ACL02_ILLEGAL_EXECUTION_AUTHORITY",Severity.BLOCKER,"authority_permit","ACL-02 permit must never allow trading or capital","reissue a non-trading semantic permit"))
    return {"passed":not findings,"findings":[x.to_dict() for x in findings]}
