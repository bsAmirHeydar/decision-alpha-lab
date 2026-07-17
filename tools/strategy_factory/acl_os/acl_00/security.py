from __future__ import annotations
from datetime import datetime
from .types import SecurityControlResult,SecurityStatus,Reason,TransitionRequest

class SecurityHookEvaluator:
    def evaluate(self,request:TransitionRequest,results:list[SecurityControlResult],policy:dict,now:datetime)->list[Reason]:
        reasons=[]; by_id={x.control_id:x for x in results}
        for control_id in policy.get("required_controls",[]):
            item=by_id.get(control_id)
            if item is None:
                reasons.append(Reason("SECURITY_CONTROL_MISSING",f"Required security control {control_id} is absent.",f"SECURITY_{control_id}",False)); continue
            if item.subject_ref.artifact_id!=request.subject_ref.artifact_id:
                reasons.append(Reason("SECURITY_SUBJECT_MISMATCH",f"Security result {control_id} targets another subject.",f"SECURITY_{control_id}",False)); continue
            if item.expires_at<=now:
                reasons.append(Reason("SECURITY_CONTROL_EXPIRED",f"Security control {control_id} expired.",f"SECURITY_{control_id}",False)); continue
            if item.evaluated_at>now:
                reasons.append(Reason("SECURITY_CONTROL_FROM_FUTURE",f"Security control {control_id} is future-dated.",f"SECURITY_{control_id}",False)); continue
            if item.status!=SecurityStatus.PASS:
                reasons.append(Reason("SECURITY_CONTROL_NOT_PASS",f"Security control {control_id} status is {item.status.value}.",f"SECURITY_{control_id}",False,{"status":item.status.value,"severity":item.severity.value}))
        unknown=set(by_id)-set(policy.get("known_controls",policy.get("required_controls",[])))
        if unknown and policy.get("reject_unknown_controls",True):
            reasons.append(Reason("UNKNOWN_SECURITY_CONTROL",f"Unknown security controls supplied: {sorted(unknown)}","SECURITY_CONTROL_CATALOG",False))
        return reasons
