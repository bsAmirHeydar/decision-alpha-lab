from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
from typing import Any
from .approvals import ApprovalEvaluator
from .audit import AuditLedger
from .authority import AuthorityEvaluator
from .canonical import StructuralSignatureVerifier,digest_object,SignatureVerifier
from .catalogs import PolicyBundle
from .claims import ClaimCeilingEvaluator
from .evidence import EvidenceEvaluator
from .errors import ConcurrencyError
from .lifecycle import LifecycleEvaluator
from .security import SecurityHookEvaluator
from .store import InMemoryStateStore
from .types import ApprovalRecord,Decision,EvidenceRecord,Reason,SecurityControlResult,TransitionDecision,TransitionRequest,WaiverRecord
from .waivers import WaiverEvaluator

@dataclass(frozen=True,slots=True)
class EvaluationBundle:
    request:TransitionRequest
    evidence:tuple[EvidenceRecord,...]=()
    approvals:tuple[ApprovalRecord,...]=()
    security_results:tuple[SecurityControlResult,...]=()
    waiver:WaiverRecord|None=None

class ACL00ControlPlane:
    def __init__(self,policy_bundle:PolicyBundle|None=None,signature_verifier:SignatureVerifier|None=None,state_store:InMemoryStateStore|None=None,audit_ledger:AuditLedger|None=None):
        self.policies=policy_bundle or PolicyBundle.load(); self.verifier=signature_verifier or StructuralSignatureVerifier(); self.store=state_store or InMemoryStateStore(); self.audit=audit_ledger or AuditLedger()
        self.lifecycle=LifecycleEvaluator(self.policies); self.authority=AuthorityEvaluator(self.policies); self.evidence=EvidenceEvaluator(); self.approvals=ApprovalEvaluator(self.verifier); self.security=SecurityHookEvaluator(); self.claims=ClaimCeilingEvaluator(); self.waivers=WaiverEvaluator(self.verifier,self.policies.documents["waiver_policy"])

    def evaluate(self,bundle:EvaluationBundle,now:datetime|None=None,commit:bool=False)->TransitionDecision:
        now=(now or datetime.now(timezone.utc)).astimezone(timezone.utc); req=bundle.request
        req_dict=req.to_dict(); req_digest=digest_object({k:v for k,v in req_dict.items() if k!="metadata"} | {"metadata":{k:v for k,v in req.metadata.items() if k!="request_digest"}})
        reasons=[]
        if req.metadata.get("request_digest")!=req_digest: reasons.append(Reason("REQUEST_DIGEST_MISMATCH","Request digest is absent or does not bind the exact request.","REQUEST_INTEGRITY",False,{"computed":req_digest}))
        transition_policy,life_reasons=self.lifecycle.policy_for(req); reasons.extend(life_reasons)
        if transition_policy:
            reasons.extend(self.authority.evaluate_requester(req.requested_by,transition_policy,req.tenant_id))
            ev_key=transition_policy.get("evidence_policy","default")
            reasons.extend(self.evidence.evaluate(req,list(bundle.evidence),self.policies.documents["evidence_requirements"]["policies"].get(ev_key,{}),now))
            ap_key=transition_policy.get("approval_policy","none")
            reasons.extend(self.approvals.evaluate(req,list(bundle.approvals),self.policies.documents["approval_policy"]["policies"].get(ap_key,{}),now))
            sec_key=transition_policy.get("security_policy","base")
            reasons.extend(self.security.evaluate(req,list(bundle.security_results),self.policies.documents["security_hook_policy"]["policies"].get(sec_key,{}),now))
            reasons.extend(self.claims.evaluate(req,transition_policy))
        reasons,waived=self.waivers.apply(req,reasons,bundle.waiver,now)
        decision=Decision.ALLOW if not reasons else Decision.DENY
        revision=req.expected_revision
        if decision==Decision.ALLOW and commit:
            try: revision=self.store.compare_and_set(req.subject_ref.artifact_id,req.tenant_id,req.expected_revision,req.from_state,req.to_state).revision
            except ConcurrencyError as exc:
                reasons.append(Reason("OPTIMISTIC_CONCURRENCY_FAILURE",str(exc),"STATE_REVISION",False)); decision=Decision.DENY
        next_actions=self.authority.allowed_actions(req.requested_by,req.to_state.value if decision==Decision.ALLOW else req.from_state.value)
        out=TransitionDecision("1.0.0",f"DEC_{req.transition_id}",req.transition_id,req.subject_ref,req.from_state,req.to_state,decision,tuple(reasons),((bundle.waiver.waiver_id,) if bundle.waiver and waived else ()),tuple(x.evidence_id for x in bundle.evidence),tuple(x.approval_id for x in bundle.approvals),tuple(x.control_id for x in bundle.security_results),now,self.policies.digest,next_actions,revision,False,False)
        self.audit.append("ACL00_TRANSITION_DECISION",req.tenant_id,req.subject_ref.artifact_id,req.requested_by.actor_id,out.to_dict(),now,{"committed":commit and decision==Decision.ALLOW})
        return out

    def allowed_next_actions(self,actor,state:str)->tuple[str,...]: return self.authority.allowed_actions(actor,state)
