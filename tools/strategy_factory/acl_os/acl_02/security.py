from __future__ import annotations
from .policies import load_policy
from .types import Finding,Severity

_ORDER={"PUBLIC":0,"INTERNAL":1,"CONFIDENTIAL":2,"RESTRICTED":3,"CROWN_JEWEL":4}

def classify_security(package:dict)->dict:
    policy=load_policy("security_classification_policy"); findings=[]; score=0; drivers=[]
    profile=package.get("security_profile",{}); declared=profile.get("classification","INTERNAL")
    for rule in policy["rules"]:
        path=rule["path"].split("."); cur=package
        for token in path:
            if not isinstance(cur,dict) or token not in cur:cur=None;break
            cur=cur[token]
        matched=(rule["operator"]=="truthy" and bool(cur)) or (rule["operator"]=="contains" and isinstance(cur,list) and rule["value"] in cur) or (rule["operator"]=="equals" and cur==rule.get("value"))
        if matched: score=max(score,int(rule["minimum_level"]));drivers.append(rule["rule_id"])
    inferred=next(k for k,v in _ORDER.items() if v==score)
    if _ORDER.get(declared,-1)<score:findings.append(Finding("ACL02_SECURITY_UNDERCLASSIFIED",Severity.BLOCKER,"security_profile.classification",f"declared {declared}, inferred minimum {inferred}","raise classification and apply mandatory controls",{"drivers":drivers}))
    required=set(policy["required_controls_by_level"][inferred]);actual=set(profile.get("required_controls",[]));missing=sorted(required-actual)
    if missing:findings.append(Finding("ACL02_SECURITY_CONTROLS_MISSING",Severity.BLOCKER,"security_profile.required_controls",f"missing controls: {missing}","add all controls required by inferred classification"))
    if profile.get("secrets",[]) and not profile.get("secret_reference_only",False):findings.append(Finding("ACL02_INLINE_SECRET_RISK",Severity.BLOCKER,"security_profile.secrets","secret-bearing Contexts must use references only","set secret_reference_only and remove inline values"))
    return {"declared_classification":declared,"inferred_minimum_classification":inferred,"drivers":drivers,"passed":not findings,"findings":[x.to_dict() for x in findings]}
