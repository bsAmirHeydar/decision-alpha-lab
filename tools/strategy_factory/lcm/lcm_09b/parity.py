from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id

def compare_traces(*,setup_id:str,legacy:list[dict[str,Any]]|None,canonical:list[dict[str,Any]]|None,blockers:list[str])->dict[str,Any]:
    if blockers:
        status="BLOCKED";mismatches=[];reasons=sorted(set(blockers+["LCM09B_PARITY_NOT_EXECUTED_WHILE_BLOCKED"]))
    elif legacy is None or canonical is None:
        status="UNKNOWN";mismatches=[];reasons=["LCM09B_GOLDEN_TRACE_UNAVAILABLE"]
    else:
        keys=("sequence","decision_state","reason_codes","observed_at","available_at")
        mismatches=[]
        if len(legacy)!=len(canonical):mismatches.append({"dimension":"EVENT_COUNT","legacy":len(legacy),"canonical":len(canonical)})
        for i,(a,b) in enumerate(zip(legacy,canonical)):
            for key in keys:
                if a.get(key)!=b.get(key):mismatches.append({"dimension":key,"index":i,"legacy":a.get(key),"canonical":b.get(key)})
        status="PASS" if not mismatches else "FAIL";reasons=[] if status=="PASS" else ["LCM09B_HARD_DECISION_MISMATCH"]
    body={"schema_version":"1.0.0","parity_id":stable_id("SETUPPARITY",setup_id,status,digest_object(mismatches)),"setup_id":setup_id,"parity_status":status,"legacy_event_count":0 if legacy is None else len(legacy),"canonical_event_count":0 if canonical is None else len(canonical),"mismatches":mismatches,"reason_codes":reasons,"hard_mismatch_count":len(mismatches),"aggregate_success_cannot_override":True}
    return {**body,"parity_digest":digest_object(body)}
