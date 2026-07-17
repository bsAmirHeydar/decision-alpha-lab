from __future__ import annotations
import re
from typing import Any
from .canonical import digest_object,stable_id
from .types import Finding,Severity

TOKEN=re.compile(r"[A-Za-z_][A-Za-z0-9_.]*")
FORBIDDEN=("__import__","eval(","exec(","OrderSend(","CTrade","subprocess","socket.","requests.","open(")

def compile_detector_ir(package:dict[str,Any])->tuple[dict[str,Any],list[dict[str,Any]]]:
    sm=package["state_machine"]; cid=package["manifest"]["context_id"]; cv=package["manifest"]["context_version"]
    findings=[]; transitions=[]; seen=set()
    for raw in sorted(sm.get("transitions",[]),key=lambda x:(x.get("from",""),int(x.get("priority",0)),x.get("event",""),x.get("to",""))):
        guard=str(raw.get("guard","")).strip()
        if any(tok in guard for tok in FORBIDDEN): findings.append(Finding("ACL03_FORBIDDEN_GUARD_TOKEN",Severity.BLOCKER,"state_machine.transitions.guard","guard contains a forbidden executable token","rewrite the guard in declarative DSL",{"guard":guard}).to_dict())
        tid=stable_id("TR",cid,cv,str(raw.get("from")),str(raw.get("to")),str(raw.get("event")),guard,str(raw.get("priority",0)))
        if tid in seen: findings.append(Finding("ACL03_DUPLICATE_TRANSITION",Severity.BLOCKER,"state_machine.transitions","duplicate canonical transition","remove duplicate transition",{"transition_id":tid}).to_dict())
        seen.add(tid)
        identifiers=sorted({t for t in TOKEN.findall(guard) if t.lower() not in {"and","or","not","true","false","at","completed","bar"}})
        transitions.append({"transition_id":tid,"from_state":raw["from"],"to_state":raw["to"],"event":raw["event"],"guard_dsl":guard,"guard_identifiers":identifiers,"priority":int(raw.get("priority",0)),"unknown_guard_policy":raw.get("unknown_guard_policy","REJECT")})
    body={"schema_version":"1.0.0","ir_version":"1.0.0","context_id":cid,"context_version":cv,"initial_state":sm["initial_state"],"states":sorted(sm["states"]),"terminal_states":sorted(sm["terminal_states"]),"unknown_state":sm["unknown_state"],"determinism_policy":sm["determinism_policy"],"transitions":transitions,"execution_model":"DECLARATIVE_EVENT_GUARD_IR","generated_code_allowed":False}
    return {**body,"detector_ir_digest":digest_object(body)},findings
