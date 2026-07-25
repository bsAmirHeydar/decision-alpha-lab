from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id
from .errors import CapabilityDeniedError
from .execution_intent import validate_execution_intent
from .guards import CapabilityGuard
class DisabledExecutionAdapter:
    def __init__(self,contract:dict[str,Any],guard_policy:dict[str,Any]):
        if contract.get("submission_capability_default") is not False or contract.get("live_mode_allowed") is not False:raise ValueError("LCM10B_ADAPTER_MUST_DEFAULT_DISABLED")
        self.contract=contract;self.guard=CapabilityGuard(guard_policy)
    def dry_run(self,intent:dict[str,Any])->dict[str,Any]:
        v=validate_execution_intent(intent);decision=self.guard.decide("EMIT_DRY_RUN_RECORD","DRY_RUN")
        body={"schema_version":"1.0.0","adapter_id":self.contract["adapter_id"],"intent_id":intent.get("intent_id"),"intent_digest":intent.get("intent_digest"),"mode":"DRY_RUN","accepted_for_submission":False,"broker_api_invoked":False,"capability_decision":{"allowed":decision.allowed,"code":decision.code,"reason":decision.reason},"intent_validation":v,"result_status":"DRY_RUN_RECORDED" if v["passed"] and decision.allowed else "BLOCKED","rejection_reasons":[] if v["passed"] and decision.allowed else sorted({x["code"] for x in v["findings"]}|({decision.code} if not decision.allowed else set()))}
        body["result_id"]=stable_id("DRYRUN",body["adapter_id"],body["intent_digest"]);body["result_digest"]=digest_object(body,"result_digest");return body
    def submit(self,*args,**kwargs):raise CapabilityDeniedError("LCM10B_LIVE_AND_PAPER_SUBMISSION_UNAVAILABLE")
    def modify(self,*args,**kwargs):raise CapabilityDeniedError("LCM10B_BROKER_MUTATION_UNAVAILABLE")
    def cancel(self,*args,**kwargs):raise CapabilityDeniedError("LCM10B_BROKER_MUTATION_UNAVAILABLE")
    def close(self,*args,**kwargs):raise CapabilityDeniedError("LCM10B_BROKER_MUTATION_UNAVAILABLE")
