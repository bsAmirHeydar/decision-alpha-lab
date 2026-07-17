from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from .canonical import digest_object
from .types import Finding,Severity

ALLOWED_ACTION="ACL03_COMPILE_CONTEXT"

def _finding(code,severity,path,message,remediation,**details): return Finding(code,severity,path,message,remediation,details).to_dict()

def validate_prerequisites(package:dict[str,Any],source_snapshot:dict[str,Any],authority_permit:dict|None,semantic_approval:dict|None,acl02_readiness:dict|None)->dict[str,Any]:
    f=[]; manifest=package["manifest"]
    if authority_permit is None: f.append(_finding("ACL03_AUTHORITY_PERMIT_MISSING",Severity.BLOCKER,"authority_permit","ACL-00 compiler permit is absent","obtain a subject-bound ACL03_COMPILE_CONTEXT permit"))
    else:
        if authority_permit.get("decision")!="ALLOW": f.append(_finding("ACL03_AUTHORITY_DENIED",Severity.BLOCKER,"authority_permit.decision","authority decision is not ALLOW","obtain an approved permit"))
        if authority_permit.get("action")!=ALLOWED_ACTION: f.append(_finding("ACL03_AUTHORITY_ACTION_MISMATCH",Severity.BLOCKER,"authority_permit.action","permit action mismatch","request exact ACL03_COMPILE_CONTEXT authority"))
        if authority_permit.get("subject_artifact_id")!=manifest.get("artifact_id"): f.append(_finding("ACL03_AUTHORITY_SUBJECT_MISMATCH",Severity.BLOCKER,"authority_permit.subject_artifact_id","permit is not bound to this Context","issue a subject-bound permit"))
        if authority_permit.get("live_order_submission_allowed") or authority_permit.get("capital_activation_allowed"): f.append(_finding("ACL03_ILLEGAL_CAPITAL_AUTHORITY",Severity.BLOCKER,"authority_permit","compiler permit cannot carry trading authority","reissue a non-trading permit"))
    if semantic_approval is None: f.append(_finding("ACL03_SEMANTIC_APPROVAL_MISSING",Severity.BLOCKER,"semantic_approval","semantic approval is absent","record semantic owner and independent reviewer approval"))
    else:
        if semantic_approval.get("decision")!="APPROVE": f.append(_finding("ACL03_SEMANTIC_APPROVAL_DENIED",Severity.BLOCKER,"semantic_approval.decision","semantic approval is not APPROVE","resolve semantic review findings"))
        if semantic_approval.get("subject_artifact_id")!=manifest.get("artifact_id"): f.append(_finding("ACL03_SEMANTIC_SUBJECT_MISMATCH",Severity.BLOCKER,"semantic_approval.subject_artifact_id","semantic approval is for another artifact","approve the exact Context artifact"))
        if semantic_approval.get("source_snapshot_digest")!=source_snapshot.get("snapshot_digest"): f.append(_finding("ACL03_SOURCE_CHANGED_AFTER_APPROVAL",Severity.BLOCKER,"semantic_approval.source_snapshot_digest","approved source snapshot differs from compiler source","obtain approval for the frozen source"))
        roles=set(semantic_approval.get("approver_roles",[]))
        if not {"semantic_owner","independent_reviewer"}.issubset(roles): f.append(_finding("ACL03_SEPARATION_OF_DUTIES_MISSING",Severity.BLOCKER,"semantic_approval.approver_roles","required semantic owner and independent reviewer roles are absent","add independent approval roles"))
    if acl02_readiness is None: f.append(_finding("ACL03_ACL02_READINESS_MISSING",Severity.BLOCKER,"acl02_readiness","ACL-02 readiness evidence is absent","attach the exact ACL-02 readiness report"))
    else:
        if acl02_readiness.get("context_id")!=manifest.get("context_id"): f.append(_finding("ACL03_READINESS_CONTEXT_MISMATCH",Severity.BLOCKER,"acl02_readiness.context_id","readiness report belongs to another Context","attach matching readiness evidence"))
        if acl02_readiness.get("blocking_count",1)!=0: f.append(_finding("ACL03_ACL02_BLOCKERS_OPEN",Severity.BLOCKER,"acl02_readiness.blocking_count","ACL-02 blockers remain open","resolve all intake blockers"))
        if acl02_readiness.get("highest_state") not in {"INTAKE_COMPLETE","SEMANTICALLY_VALIDATED","SEMANTIC_REVIEW_REQUIRED"}: f.append(_finding("ACL03_ACL02_STATE_INSUFFICIENT",Severity.BLOCKER,"acl02_readiness.highest_state","ACL-02 state is insufficient for compilation","complete ACL-02 intake and semantic approval"))
    return {"passed":not f,"findings":f,"binding_digest":digest_object({"manifest_artifact_id":manifest.get("artifact_id"),"source_snapshot_digest":source_snapshot.get("snapshot_digest"),"authority_permit":authority_permit,"semantic_approval":semantic_approval,"acl02_report_digest":(acl02_readiness or {}).get("report_digest")})}
