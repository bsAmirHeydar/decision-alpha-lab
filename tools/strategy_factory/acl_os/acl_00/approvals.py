from __future__ import annotations
from collections import Counter
from datetime import datetime
from .canonical import SignatureVerifier
from .types import ApprovalRecord, ApprovalDisposition, Reason, TransitionRequest

class ApprovalEvaluator:
    def __init__(self,verifier:SignatureVerifier): self.verifier=verifier

    def evaluate(self,request:TransitionRequest,approvals:list[ApprovalRecord],policy:dict,now:datetime)->list[Reason]:
        reasons=[]; valid=[]; seen=set()
        for ap in approvals:
            if ap.approval_id in seen:
                reasons.append(Reason("DUPLICATE_APPROVAL","Duplicate approval ID.","APPROVAL_UNIQUENESS",False,{"approval_id":ap.approval_id})); continue
            seen.add(ap.approval_id)
            if ap.transition_id!=request.transition_id:
                reasons.append(Reason("APPROVAL_TRANSITION_MISMATCH",f"Approval {ap.approval_id} targets another transition.","APPROVAL_BINDING",False)); continue
            if ap.request_digest!=request.metadata.get("request_digest"):
                reasons.append(Reason("APPROVAL_DIGEST_MISMATCH",f"Approval {ap.approval_id} does not bind the exact request.","APPROVAL_BINDING",False)); continue
            if ap.approved_at>request.requested_at:
                # approvals may be created after request, but cannot be in the future relative to evaluation
                if ap.approved_at>now:
                    reasons.append(Reason("APPROVAL_FROM_FUTURE",f"Approval {ap.approval_id} is future-dated.","APPROVAL_CLOCK",False)); continue
            if ap.expires_at<=now:
                reasons.append(Reason("APPROVAL_EXPIRED",f"Approval {ap.approval_id} expired.","APPROVAL_FRESHNESS",False)); continue
            if ap.role not in ap.approver.roles:
                reasons.append(Reason("APPROVER_ROLE_NOT_HELD",f"Approver does not hold declared role {ap.role}.","APPROVAL_ROLE_BINDING",False)); continue
            if ap.disposition==ApprovalDisposition.REJECT:
                reasons.append(Reason("EXPLICIT_REJECTION",f"Approval {ap.approval_id} rejects the request.","APPROVAL_REJECTION",False)); continue
            if ap.disposition!=ApprovalDisposition.APPROVE: continue
            if not self.verifier.verify({"transition_id":ap.transition_id,"request_digest":ap.request_digest,"role":ap.role,"disposition":ap.disposition.value},ap.signature,ap.approver.actor_id):
                reasons.append(Reason("APPROVAL_SIGNATURE_INVALID",f"Approval {ap.approval_id} signature is invalid.","APPROVAL_SIGNATURE",False)); continue
            valid.append(ap)
        counts=Counter(x.role for x in valid)
        for role,count in policy.get("required_roles",{}).items():
            if counts[role]<int(count):
                reasons.append(Reason("REQUIRED_APPROVAL_MISSING",f"Need {count} approval(s) from {role}, found {counts[role]}.",f"APPROVAL_ROLE_{role}",False,{"role":role,"required":count,"found":counts[role]}))
        if policy.get("requester_cannot_approve",True) and any(x.approver.actor_id==request.requested_by.actor_id for x in valid):
            reasons.append(Reason("SELF_APPROVAL_FORBIDDEN","Requester cannot approve their own transition.","SOD_REQUESTER_APPROVER",False))
        if policy.get("distinct_approvers",False):
            ids=[x.approver.actor_id for x in valid]
            if len(ids)!=len(set(ids)): reasons.append(Reason("APPROVER_REUSE_FORBIDDEN","Required approvals must come from distinct actors.","SOD_DISTINCT_APPROVERS",False))
        if policy.get("distinct_roles",False):
            role_actor={}
            for x in valid:
                if x.approver.actor_id in role_actor and role_actor[x.approver.actor_id]!=x.role:
                    reasons.append(Reason("MULTI_ROLE_APPROVAL_FORBIDDEN","One actor cannot satisfy multiple independent approval roles.","SOD_DISTINCT_ROLES",False)); break
                role_actor[x.approver.actor_id]=x.role
        return reasons
