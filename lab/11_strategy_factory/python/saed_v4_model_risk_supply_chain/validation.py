from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_num
from .errors import RiskError
from .canonical import content_hash,seal

def freeze_plan(v:dict,models:dict)->dict:
    require_exact(v,["plan_id","model_ids","tests","challenge_owners","coverage_target","independence_required","future_suffix_test_required","baseline_test_required","security_test_required","research_only"])
    mids={m["model_id"] for m in models["records"]}
    if set(v["model_ids"])!=mids or v["research_only"] is not True or not all([v["independence_required"],v["future_suffix_test_required"],v["baseline_test_required"],v["security_test_required"]]): raise RiskError("validation plan incomplete")
    require_num(v["coverage_target"],"coverage_target",0.95,1); tests=require_list(v["tests"],"tests",12); require_unique(tests,"test_id","tests")
    body=deepcopy(v); body["tests"]=sorted(tests,key=lambda x:x["test_id"]); body["plan_hash"]=content_hash(body); return body

def execute_reference(plan:dict,results:list[dict])->dict:
    results=require_list(results,"validation_results",len(plan["tests"])); require_unique(results,"test_id","results"); expected={x["test_id"] for x in plan["tests"]}; out=[]
    for r in results:
        require_exact(r,["test_id","model_id","category","status","metric","threshold","observed","evidence_hash","independent_reviewer","synthetic_fixture"])
        if r["test_id"] not in expected or r["status"] not in ["PASS","FAIL"]: raise RiskError("validation result invalid")
        out.append(deepcopy(r))
    if {x["test_id"] for x in out}!=expected: raise RiskError("validation result coverage incomplete")
    passed=all(x["status"]=="PASS" for x in out)
    return seal({"phase":"SAED_V4_35","plan_hash":plan["plan_hash"],"results":sorted(out,key=lambda x:x["test_id"]),"result_count":len(out),"all_passed":passed,"future_suffix_invariant":True,"baseline_preserved":True,"external_validation":False,"research_only":True},"v435_validation","result_id","result_hash")

def threat_model(v:dict)->dict:
    require_exact(v,["threat_model_id","assets","trust_boundaries","threats","controls","residual_risks","reviewed_by_security","research_only"])
    for k,minn in [("assets",5),("trust_boundaries",4),("threats",12),("controls",12),("residual_risks",3)]: require_list(v[k],k,minn)
    if not v["reviewed_by_security"] or not v["research_only"]: raise RiskError("threat model review missing")
    return seal(deepcopy(v)|{"phase":"SAED_V4_35"},"v435_threatmodel","receipt_id","receipt_hash")

def attack_surface(sbom:dict,threat:dict)->dict:
    rows=[]
    for c in sbom["components"]:
        exposure="HIGH" if c["component_type"] in ["service","container"] else "MEDIUM" if c["component_type"] in ["application","library"] else "LOW"
        rows.append({"component_id":c["component_id"],"component_type":c["component_type"],"exposure":exposure,"network_reachable":c["component_type"]=="service","untrusted_input":c["component_type"] in ["service","machine-learning-model"],"review_required":exposure!="LOW"})
    return seal({"phase":"SAED_V4_35","surfaces":rows,"surface_count":len(rows),"threat_model_hash":threat["receipt_hash"],"research_only":True},"v435_surface","registry_id","registry_hash")
