from __future__ import annotations
import re
from typing import Any
from .policies import load_policy
from .types import Finding,Severity

class AmbiguityAnalyzer:
    def __init__(self):
        p=load_policy("ambiguity_policy"); self.tokens={x["token"].lower():x for x in p["vague_terms"]}; self.placeholder=re.compile(p["placeholder_regex"],re.I); self.min_rule_chars=int(p["minimum_rule_characters"])
    def analyze(self,package:dict[str,Any])->dict[str,Any]:
        findings=[]
        def walk(v:Any,path:str):
            if isinstance(v,dict):
                for k,x in v.items():
                    if k.startswith("_"):continue
                    walk(x,f"{path}.{k}" if path else k)
            elif isinstance(v,list):
                for i,x in enumerate(v):walk(x,f"{path}.{i}")
            elif isinstance(v,str):
                text=v.strip(); low=text.lower()
                if self.placeholder.search(text): findings.append(Finding("ACL02_PLACEHOLDER_PRESENT",Severity.BLOCKER,path,"placeholder or unresolved drafting token found","replace it with a precise observable definition"))
                for token,rule in self.tokens.items():
                    if re.search(r"(?<![A-Za-z0-9_])"+re.escape(token)+r"(?![A-Za-z0-9_])",low):
                        findings.append(Finding("ACL02_VAGUE_TERM",Severity.ERROR if rule["blocking"] else Severity.WARNING,path,f"vague term: {token}",rule["remediation"],{"token":token}))
                if any(x in path for x in ("rule","definition","observable","invalidation","confirmation")) and text and len(text)<self.min_rule_chars:
                    findings.append(Finding("ACL02_RULE_TOO_SHORT",Severity.WARNING,path,"rule is too short to establish deterministic semantics","state observable inputs, comparison, time boundary and unknown behavior"))
        walk(package,"")
        # contradictory terminal/non-goal declarations
        states=set(package.get("state_machine",{}).get("states",[])); terminals=set(package.get("state_machine",{}).get("terminal_states",[]))
        if not terminals.issubset(states): findings.append(Finding("ACL02_TERMINAL_STATE_UNDECLARED",Severity.BLOCKER,"state_machine.terminal_states","terminal state not present in states","declare every terminal state"))
        scope=package.get("scope",{}); overlap=set(scope.get("goals",[])) & set(scope.get("non_goals",[]))
        if overlap: findings.append(Finding("ACL02_GOAL_NON_GOAL_CONFLICT",Severity.BLOCKER,"scope",f"goals and non-goals overlap: {sorted(overlap)}","separate intended behavior from exclusions"))
        return {"finding_count":len(findings),"blocking_count":sum(f.severity in {Severity.BLOCKER,Severity.ERROR} for f in findings),"findings":[f.to_dict() for f in findings]}
