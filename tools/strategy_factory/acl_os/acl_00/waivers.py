from __future__ import annotations
from datetime import datetime
from .canonical import SignatureVerifier
from .types import WaiverRecord,Reason,TransitionRequest,ApprovalDisposition

class WaiverEvaluator:
    def __init__(self,verifier:SignatureVerifier,policy:dict): self.verifier=verifier; self.policy=policy

    def apply(self,request:TransitionRequest,reasons:list[Reason],waiver:WaiverRecord|None,now:datetime)->tuple[list[Reason],tuple[str,...]]:
        if waiver is None: return reasons,()
        extra=[]
        if waiver.transition_id!=request.transition_id: extra.append(Reason("WAIVER_TRANSITION_MISMATCH","Waiver targets another transition.","WAIVER_BINDING",False))
        if waiver.subject_ref.artifact_id!=request.subject_ref.artifact_id: extra.append(Reason("WAIVER_SUBJECT_MISMATCH","Waiver targets another subject.","WAIVER_BINDING",False))
        if waiver.expires_at<=now: extra.append(Reason("WAIVER_EXPIRED","Waiver expired.","WAIVER_FRESHNESS",False))
        if not waiver.compensating_controls: extra.append(Reason("WAIVER_COMPENSATING_CONTROL_MISSING","Waiver requires compensating controls.","WAIVER_COMPENSATION",False))
        nonwaivable=set(self.policy.get("nonwaivable_policy_ids",[]))
        requested=set(waiver.waived_policy_ids)
        blocked=sorted(requested&nonwaivable)
        if blocked: extra.append(Reason("NONWAIVABLE_POLICY_REQUESTED",f"Policies cannot be waived: {blocked}","WAIVER_NONWAIVABLE",False))
        held={r for ap in waiver.approvals if ap.disposition==ApprovalDisposition.APPROVE for r in [ap.role]}
        required=set(self.policy.get("required_approval_roles",[]))
        if not required.issubset(held): extra.append(Reason("WAIVER_APPROVAL_MISSING",f"Waiver approvals missing roles: {sorted(required-held)}","WAIVER_APPROVAL",False))
        if not self.verifier.verify({"waiver_id":waiver.waiver_id,"transition_id":waiver.transition_id,"policies":list(waiver.waived_policy_ids)},waiver.signature,waiver.issued_by.actor_id): extra.append(Reason("WAIVER_SIGNATURE_INVALID","Waiver signature is invalid.","WAIVER_SIGNATURE",False))
        if extra: return reasons+extra,()
        remaining=[]; applied=[]
        for reason in reasons:
            if reason.policy_id in requested and reason.waivable:
                applied.append(reason.policy_id or "")
            else: remaining.append(reason)
        return remaining,tuple(sorted(set(applied)))
