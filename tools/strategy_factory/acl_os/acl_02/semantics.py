from __future__ import annotations
from collections import Counter,defaultdict
from .types import Finding,Severity

def validate_semantics(package:dict)->dict:
    fs=[]
    manifest=package["manifest"]; cid=manifest.get("context_id","")
    if not cid.startswith("CTX_"): fs.append(Finding("ACL02_CONTEXT_ID_INVALID",Severity.BLOCKER,"manifest.context_id","context_id must start with CTX_","use canonical CTX_* identity"))
    owners=package["owners"]
    for role in ("semantic_owner","technical_owner","security_owner","capital_authority"):
        if not owners.get(role):fs.append(Finding("ACL02_OWNER_MISSING",Severity.BLOCKER,f"owners.{role}",f"{role} is missing","assign an accountable owner identity"))
    sm=package["state_machine"]; states=sm.get("states",[]); counts=Counter(states)
    dup=[x for x,n in counts.items() if n>1]
    if dup:fs.append(Finding("ACL02_DUPLICATE_STATE",Severity.BLOCKER,"state_machine.states",f"duplicate states: {dup}","remove duplicate state names"))
    if sm.get("initial_state") not in states:fs.append(Finding("ACL02_INITIAL_STATE_UNDECLARED",Severity.BLOCKER,"state_machine.initial_state","initial state is not declared","add it to states"))
    edges=defaultdict(set)
    for i,t in enumerate(sm.get("transitions",[])):
        a,b=t.get("from"),t.get("to")
        if a not in states or b not in states:fs.append(Finding("ACL02_TRANSITION_STATE_UNDECLARED",Severity.BLOCKER,f"state_machine.transitions.{i}","transition references undeclared state","declare both states"))
        key=(a,t.get("event"),t.get("priority",0))
        if b in edges[key]:fs.append(Finding("ACL02_DUPLICATE_TRANSITION",Severity.ERROR,f"state_machine.transitions.{i}","duplicate transition","deduplicate or define explicit precedence"))
        edges[key].add(b)
    occ=package["occurrence"]
    for name in ("start_rule","confirmation_rule","invalidation_rule","expiry_rule","deduplication_rule"):
        if not occ.get(name):fs.append(Finding("ACL02_OCCURRENCE_RULE_MISSING",Severity.BLOCKER,f"occurrence.{name}",f"{name} is missing","define deterministic occurrence semantics"))
    ex=package["examples"].get("examples",[]); kinds=Counter(x.get("kind") for x in ex)
    for kind in ("POSITIVE","NEGATIVE","AMBIGUOUS"):
        if kinds[kind]<1:fs.append(Finding("ACL02_EXAMPLE_CLASS_MISSING",Severity.BLOCKER,"examples.examples",f"no {kind} example declared","add at least one immutable fixture reference"))
    return {"passed":not any(x.severity==Severity.BLOCKER for x in fs),"findings":[x.to_dict() for x in fs]}
