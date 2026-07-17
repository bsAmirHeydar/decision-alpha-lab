from __future__ import annotations
from collections import defaultdict
from typing import Any
from .path_access import get_path
from .policies import load_policy
from .types import Finding,SectionScore,Severity

def _present(v:Any)->bool:
    if v is None:return False
    if isinstance(v,str):return bool(v.strip())
    if isinstance(v,(list,dict,set,tuple)):return bool(v)
    return True

def evaluate_completeness(package:dict[str,Any])->dict[str,Any]:
    requirements=load_policy("requirement_catalog")["requirements"]
    required=defaultdict(float); earned=defaultdict(float); missing=defaultdict(list); findings=[]
    for r in requirements:
        sec=r["section"]; weight=float(r["weight"]); required[sec]+=weight
        value=get_path(package,r["path"],None); ok=_present(value)
        if ok: earned[sec]+=weight
        else:
            missing[sec].append(r["requirement_id"])
            sev=Severity.BLOCKER if r["blocking"] else Severity.WARNING
            findings.append(Finding("ACL02_REQUIRED_FIELD_MISSING" if r["blocking"] else "ACL02_RECOMMENDED_FIELD_MISSING",sev,r["path"],r["message"],r["remediation"],{"requirement_id":r["requirement_id"],"weight":weight}))
    scores=[]
    for sec in sorted(required):
        fs=[f for f in findings if f.path.startswith(sec+".") or f.path==sec]
        scores.append(SectionScore(sec,required[sec],earned[sec],sum(f.severity==Severity.BLOCKER for f in fs),sum(f.severity==Severity.WARNING for f in fs),missing[sec]).to_dict())
    total_req=sum(required.values());total_earned=sum(earned.values())
    return {"overall_score":round(total_earned/total_req,6) if total_req else 1.0,"sections":scores,"findings":[f.to_dict() for f in findings],"blocking_count":sum(f.severity==Severity.BLOCKER for f in findings)}
