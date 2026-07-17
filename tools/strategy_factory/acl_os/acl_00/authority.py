from __future__ import annotations
from .types import Actor, Reason
from .catalogs import PolicyBundle

class AuthorityEvaluator:
    def __init__(self,bundle:PolicyBundle): self.bundle=bundle

    def capabilities(self,actor:Actor)->set[str]:
        out=set()
        for role in actor.roles:
            spec=self.bundle.role(role)
            if spec: out.update(spec.get("capabilities",[]))
        return out

    def evaluate_requester(self,actor:Actor,transition_policy:dict,tenant_id:str)->list[Reason]:
        reasons=[]
        if actor.tenant_id!=tenant_id and "CROSS_TENANT_ADMIN" not in self.capabilities(actor):
            reasons.append(Reason("TENANT_MISMATCH","Requester tenant does not match the subject tenant.","AUTH_TENANT_ISOLATION",False))
        required=set(transition_policy.get("requester_capabilities",["PROPOSE_TRANSITION"]))
        missing=required-self.capabilities(actor)
        if missing:
            reasons.append(Reason("REQUESTER_NOT_AUTHORIZED",f"Missing requester capabilities: {sorted(missing)}","AUTH_REQUESTER_CAPABILITY",False,{"missing":sorted(missing)}))
        if actor.authentication_strength not in {"MFA","HARDWARE_MFA","WORKLOAD_IDENTITY"}:
            reasons.append(Reason("AUTHENTICATION_TOO_WEAK","Strong authentication is required.","AUTH_STRONG_AUTH",False))
        return reasons

    def allowed_actions(self,actor:Actor,state:str)->tuple[str,...]:
        caps=self.capabilities(actor); actions=self.bundle.documents["action_catalog"]["actions"]
        allowed=[]
        for aid,spec in actions.items():
            if state in spec.get("states",[]) and set(spec.get("required_capabilities",[])).issubset(caps): allowed.append(aid)
        return tuple(sorted(allowed))
