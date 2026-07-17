from __future__ import annotations
from datetime import datetime
from pathlib import Path
from typing import Any
from .canonical import digest_object,stable_id
from .io import load_json
from .errors import ReplayError

def _parse_time(value:str)->datetime:
    return datetime.fromisoformat(value.replace("Z","+00:00"))

def compile_golden_cases(context_root:Path,package:dict[str,Any],detector_ir:dict[str,Any])->list[dict[str,Any]]:
    cases=[]
    for ex in sorted(package["examples"].get("examples",[]),key=lambda x:x["example_id"]):
        payload=load_json(context_root/ex["fixture_ref"])
        events=payload.get("events",[])
        case={"schema_version":"1.0.0","case_id":stable_id("GOLD",package["manifest"]["context_id"],ex["example_id"]),"example_id":ex["example_id"],"kind":ex["kind"],"context_id":package["manifest"]["context_id"],"initial_state":detector_ir["initial_state"],"events":events,"expected_terminal_state":payload.get("expected_terminal_state"),"expected_classification":ex["expected_classification"],"source_fixture":ex["fixture_ref"]}
        cases.append({**case,"case_digest":digest_object(case)})
    return cases

def replay_case(detector_ir:dict[str,Any],known_time_ir:dict[str,Any],case:dict[str,Any])->dict[str,Any]:
    state=case["initial_state"]; trace=[]; last_known=None
    for idx,event in enumerate(case.get("events",[])):
        known=_parse_time(event["known_time"]); decision=_parse_time(event["decision_time"])
        if known>decision: raise ReplayError("known_time exceeds decision_time")
        if last_known is not None and known<last_known: raise ReplayError("known_time regressed")
        last_known=known
        candidates=[t for t in detector_ir["transitions"] if t["from_state"]==state and t["event"]==event["event"]]
        candidates.sort(key=lambda t:(t["priority"],t["transition_id"]))
        selected=None
        for t in candidates:
            result=event.get("guard_results",{}).get(t["transition_id"],event.get("guard_result"))
            if result is True: selected=t; break
            if result is None and t["unknown_guard_policy"] not in {"REJECT","ABSTAIN"}: raise ReplayError("unknown guard policy is unsafe")
        before=state
        if selected is not None: state=selected["to_state"]
        trace.append({"index":idx,"event":event["event"],"known_time":event["known_time"],"decision_time":event["decision_time"],"state_before":before,"state_after":state,"transition_id":selected["transition_id"] if selected else None})
    expected=case.get("expected_terminal_state")
    passed=expected is None or state==expected
    body={"schema_version":"1.0.0","case_id":case["case_id"],"passed":passed,"final_state":state,"expected_terminal_state":expected,"trace":trace}
    return {**body,"result_digest":digest_object(body)}

def run_golden_replay(detector_ir:dict[str,Any],known_time_ir:dict[str,Any],cases:list[dict[str,Any]])->dict[str,Any]:
    results=[]
    for case in cases:
        try: results.append(replay_case(detector_ir,known_time_ir,case))
        except Exception as e: results.append({"schema_version":"1.0.0","case_id":case["case_id"],"passed":False,"error":type(e).__name__,"message":str(e),"trace":[]})
    body={"schema_version":"1.0.0","case_count":len(cases),"passed_count":sum(1 for r in results if r.get("passed")),"failed_count":sum(1 for r in results if not r.get("passed")),"results":results}
    return {**body,"replay_digest":digest_object(body)}
