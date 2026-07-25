from __future__ import annotations
from itertools import combinations
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list
from .errors import EligibilityError

LAB_FIELDS=["lab_code","organization_id","operator_id","signing_key_id","environment_id","infrastructure_id","funding_source_id","originator_relation","mutable_state_group","declared_at","synthetic_fixture"]

def register_labs(values:list[dict],protocol:dict)->tuple[dict,dict]:
    require_list(values,"labs",protocol["minimum_labs"])
    labs=[]
    for value in values:
        require_exact(value,LAB_FIELDS,name="lab_registration")
        if value["synthetic_fixture"] is not True: raise EligibilityError("reference requires explicit synthetic fixture marker")
        if value["originator_relation"]!="none": raise EligibilityError("originator relation must be none")
        body=dict(value); body["lab_id"]=stable_id("v430_lab",body); body["registration_hash"]=content_hash(body); labs.append(body)
    required=protocol["required_independence_dimensions"]
    pairs=[]; all_independent=True
    for left,right in combinations(labs,2):
        checks={d:left[d]!=right[d] for d in required}
        eligible=all(checks.values()); all_independent &= eligible
        pair={"left_lab_id":left["lab_id"],"right_lab_id":right["lab_id"],"dimension_checks":checks,"independent":eligible}
        pair["pair_hash"]=content_hash(pair); pairs.append(pair)
    if len(labs)<protocol["minimum_labs"] or not all_independent: raise EligibilityError("minimum independent laboratory set not satisfied")
    registry={"phase":"SAED_V4_30","labs":labs,"eligible_lab_count":len(labs),"minimum_labs":protocol["minimum_labs"],"all_labs_eligible":True,"synthetic_fixture_only":True,"research_only":True}
    registry["registry_id"]=stable_id("v430_registry",registry); registry["registry_hash"]=content_hash(registry)
    matrix={"phase":"SAED_V4_30","required_dimensions":required,"pairs":pairs,"pair_count":len(pairs),"all_pairs_independent":True,"research_only":True}
    matrix["matrix_id"]=stable_id("v430_independence",matrix); matrix["matrix_hash"]=content_hash(matrix)
    return registry,matrix
