from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,stable_id,hash_chain
from .contracts import require_exact,require_list,require_unique,require_enum
from .errors import AuthorityError

CAP_KEYS=["capability_id","description","allowed_roles","requires_human_checkpoint","requires_independent_roles","maximum_delegation_depth","denied_in_phase"]
FORBIDDEN={"promotion","runtime_activation","risk_allocation","order_submission","credential_access","production_release","online_learning","context_truth_mutation","evidence_role_mutation","counterexample_suppression","residual_risk_waiver"}
RESEARCH_CAPS={"propose_hypothesis","audit_data","challenge_statistics","implement_model","audit_causality","audit_execution","curate_evidence","schedule_task","request_review","block_candidate","approve_research_checkpoint","read_protected_evidence"}

def freeze_capabilities(items:list[dict],roles:dict)->dict:
    require_list(items,"capabilities",len(RESEARCH_CAPS)+len(FORBIDDEN)); require_unique(items,"capability_id","capabilities")
    role_ids={r["role_id"] for r in roles["roles"]}; normalized=[]
    for item in items:
        require_exact(item,CAP_KEYS,name="capability")
        cid=item["capability_id"]
        if cid not in RESEARCH_CAPS|FORBIDDEN: raise AuthorityError("unknown capability")
        if set(item["allowed_roles"])-role_ids: raise AuthorityError("unknown role in capability")
        if cid in FORBIDDEN:
            if item["allowed_roles"] or item["denied_in_phase"] is not True: raise AuthorityError("forbidden capability must be denied for all")
        else:
            if not item["allowed_roles"] or item["denied_in_phase"] is not False: raise AuthorityError("research capability incorrectly denied")
        if not isinstance(item["maximum_delegation_depth"],int) or not 0<=item["maximum_delegation_depth"]<=4: raise AuthorityError("delegation depth invalid")
        normalized.append(deepcopy(item))
    if {x["capability_id"] for x in items} != RESEARCH_CAPS|FORBIDDEN: raise AuthorityError("capability matrix incomplete")
    body={"phase":"SAED_V4_32","capabilities":sorted(normalized,key=lambda x:x["capability_id"]),"deny_by_default":True,"forbidden_capabilities":sorted(FORBIDDEN),"research_only":True}
    body["matrix_id"]=stable_id("v432_capability_matrix",body); body["matrix_hash"]=content_hash(body); return body

def authorize(agent:dict,capability_id:str,matrix:dict,checkpoint_ids:list[str]|None=None,independent_roles:list[str]|None=None)->dict:
    checkpoint_ids=checkpoint_ids or []; independent_roles=independent_roles or []
    rows={x["capability_id"]:x for x in matrix["capabilities"]}
    item=rows.get(capability_id)
    reason="allowed"; allowed=True
    if item is None: allowed=False; reason="deny_by_default"
    elif item["denied_in_phase"]: allowed=False; reason="constitutionally_forbidden"
    elif agent["role_id"] not in item["allowed_roles"]: allowed=False; reason="role_not_allowed"
    elif item["requires_human_checkpoint"] and not checkpoint_ids: allowed=False; reason="human_checkpoint_missing"
    elif item["requires_independent_roles"] and len(set(independent_roles))<2: allowed=False; reason="independent_roles_missing"
    event={"phase":"SAED_V4_32","agent_id":agent["agent_id"],"role_id":agent["role_id"],"capability_id":capability_id,"allowed":allowed,"reason":reason,"checkpoint_ids":sorted(checkpoint_ids),"independent_roles":sorted(set(independent_roles)),"research_only":True}
    event["decision_id"]=stable_id("v432_authorization",event); event["decision_hash"]=content_hash(event); return event

def separation_matrix(roles:dict)->dict:
    incompatible=[
      {"left":"hypothesis","right":"human_reviewer","reason":"proposal_review_separation"},
      {"left":"model_engineering","right":"statistical_adversary","reason":"builder_challenger_separation"},
      {"left":"model_engineering","right":"evidence_curator","reason":"builder_evidence_custody_separation"},
      {"left":"orchestrator","right":"human_reviewer","reason":"scheduler_approval_separation"},
      {"left":"data_audit","right":"model_engineering","reason":"data_builder_separation"},
      {"left":"leakage_sentinel","right":"model_engineering","reason":"sentinel_builder_separation"}
    ]
    body={"phase":"SAED_V4_32","incompatible_role_pairs":incompatible,"two_person_actions":["protected_evidence_access","research_checkpoint_approval","critical_waiver","incident_closure","constitution_amendment_proposal"],"self_approval_denied":True,"single_agent_quorum_denied":True,"research_only":True}
    body["matrix_id"]=stable_id("v432_separation_matrix",body); body["matrix_hash"]=content_hash(body); return body

def authority_boundary()->dict:
    authority={name:False for name in ["context_truth_mutation","evidence_role_mutation","promotion","runtime_activation","risk_allocation","execution","order_submission","credential_access","production_release","online_learning","live_trading","constitutional_self_amendment","counterexample_suppression","residual_risk_waiver"]}
    body={"phase":"SAED_V4_32","authority":authority,"research_actions_only":["propose","audit","implement","challenge","curate","request_review","block","approve_research_checkpoint"],"safe_action":"quarantine","agents_have_zero_live_authority":True,"ucee_authority_preserved":True,"research_only":True}
    body["boundary_id"]=stable_id("v432_authority_boundary",body); body["boundary_hash"]=content_hash(body); return body

def assert_zero(boundary:dict)->None:
    nonzero=[k for k,v in boundary["authority"].items() if v is not False]
    if nonzero: raise AuthorityError(f"nonzero authority {nonzero}")
