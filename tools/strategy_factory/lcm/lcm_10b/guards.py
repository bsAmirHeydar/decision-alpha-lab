from __future__ import annotations
from dataclasses import dataclass
from .errors import CapabilityDeniedError
@dataclass(frozen=True,slots=True)
class CapabilityDecision:
    allowed:bool;code:str;reason:str
class CapabilityGuard:
    def __init__(self,policy:dict):
        self.policy=policy
        if policy.get("submission_capability_default") is not False:raise ValueError("LCM10B_GUARD_DEFAULT_MUST_BE_FALSE")
    def decide(self,capability:str,mode:str)->CapabilityDecision:
        if capability in {"SUBMIT_ORDER","MODIFY_POSITION","MODIFY_ORDER","CANCEL_ORDER","CLOSE_POSITION","LIVE_BROKER_ACCESS"}:return CapabilityDecision(False,"LCM10B_CAPABILITY_DENIED","Broker mutation is unavailable in LCM-10B")
        if mode not in {"REFERENCE","DRY_RUN"}:return CapabilityDecision(False,"LCM10B_MODE_DENIED","Only reference and dry-run modes exist")
        return CapabilityDecision(capability in set(self.policy.get("dry_run_allowed_capabilities",[])),"LCM10B_REFERENCE_DECISION","Reference-only capability decision")
    def require(self,capability:str,mode:str)->None:
        d=self.decide(capability,mode)
        if not d.allowed:raise CapabilityDeniedError(f"{d.code}:{d.reason}")
