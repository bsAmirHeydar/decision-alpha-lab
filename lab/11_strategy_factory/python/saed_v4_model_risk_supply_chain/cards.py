from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique
from .errors import CatalogError
from .canonical import seal

def model_cards(models:dict,cards:list[dict])->dict:
    cards=require_list(cards,"model_cards",len(models["records"])); require_unique(cards,"model_id","model_cards"); mids={m["model_id"] for m in models["records"]}; out=[]
    for c in cards:
        require_exact(c,["model_id","intended_use","prohibited_uses","training_scope","evaluation_scope","limitations","ethical_risks","known_failure_modes","owner_id","review_status"])
        if c["model_id"] not in mids or c["review_status"]!="reviewed-reference" or not c["prohibited_uses"] or not c["limitations"] or not c["known_failure_modes"]: raise CatalogError("model card incomplete")
        out.append(deepcopy(c))
    if {x["model_id"] for x in out}!=mids: raise CatalogError("model-card coverage incomplete")
    return seal({"phase":"SAED_V4_35","cards":sorted(out,key=lambda x:x["model_id"]),"coverage_complete":True,"research_only":True},"v435_modelcards","registry_id","registry_hash")

def data_cards(datasets:dict,cards:list[dict])->dict:
    cards=require_list(cards,"data_cards",len(datasets["records"])); require_unique(cards,"dataset_id","data_cards"); dids={d["dataset_id"] for d in datasets["records"]}; out=[]
    for c in cards:
        require_exact(c,["dataset_id","source_description","collection_window","known_time_policy","sampling_policy","missingness_policy","leakage_controls","privacy_class","license_review","limitations","review_status"])
        if c["dataset_id"] not in dids or c["review_status"]!="reviewed-reference" or c["known_time_policy"]!="STRICT": raise CatalogError("data card incomplete")
        out.append(deepcopy(c))
    if {x["dataset_id"] for x in out}!=dids: raise CatalogError("data-card coverage incomplete")
    return seal({"phase":"SAED_V4_35","cards":sorted(out,key=lambda x:x["dataset_id"]),"coverage_complete":True,"research_only":True},"v435_datacards","registry_id","registry_hash")
