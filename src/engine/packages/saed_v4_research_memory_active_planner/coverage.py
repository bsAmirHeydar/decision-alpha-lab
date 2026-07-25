from __future__ import annotations
from copy import deepcopy
from .canonical import seal
from .contracts import require_exact,require_list,require_unique,require_num
from .errors import PlannerError

def freeze_gaps(items:list[dict],claims:dict,contradictions:dict)->dict:
    cids={x["claim_id"] for x in claims["claims"]}; items=require_list(items,"evidence_gaps",4); require_unique(items,"gap_id","evidence_gaps"); out=[]
    for x in items:
        require_exact(x,["gap_id","claim_id","dimension","severity","uncertainty","coverage","required_family","blocking","synthetic_fixture"])
        if x["claim_id"] not in cids: raise PlannerError("gap references unknown claim")
        require_num(x["uncertainty"],"uncertainty",0,1); require_num(x["coverage"],"coverage",0,1)
        out.append(deepcopy(x))
    return seal({"phase":"SAED_V4_36","gaps":sorted(out,key=lambda x:x["gap_id"]),"gap_count":len(out),"blocking_count":sum(x["blocking"] for x in out),"research_only":True},"v436_gaps","registry_id","registry_hash")

def coverage_matrix(gaps:dict,claims:dict)->dict:
    rows=[]
    for c in claims["claims"]:
        cg=[g for g in gaps["gaps"] if g["claim_id"]==c["claim_id"]]; rows.append({"claim_id":c["claim_id"],"dimensions":sorted({g["dimension"] for g in cg}),"mean_coverage":round(sum(g["coverage"] for g in cg)/len(cg),8) if cg else 1.0,"mean_uncertainty":round(sum(g["uncertainty"] for g in cg)/len(cg),8) if cg else 0.0,"blocking_gaps":sum(g["blocking"] for g in cg)})
    return seal({"phase":"SAED_V4_36","rows":rows,"claim_count":len(rows),"research_only":True},"v436_matrix","matrix_id","matrix_hash")
