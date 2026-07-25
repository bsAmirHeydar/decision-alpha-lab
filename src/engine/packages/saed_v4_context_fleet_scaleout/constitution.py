from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer
from .errors import ConstitutionError
from .canonical import content_hash,seal
def freeze_constitution(v:dict)->dict:
 exact(v,["constitution_id","version","clauses","immutable_cell_identity","tenant_isolation_required","no_mutable_global_state","idempotent_side_effects_required","journal_every_transition","fail_closed_required","baseline_preservation_required","automatic_live_promotion_allowed","cross_tenant_routing_allowed","live_order_submission_allowed","capital_activation_allowed","production_authorization_allowed","research_only"])
 for k in ["immutable_cell_identity","tenant_isolation_required","no_mutable_global_state","idempotent_side_effects_required","journal_every_transition","fail_closed_required","baseline_preservation_required","research_only"]:
  if v[k] is not True:raise ConstitutionError(f"{k} must be true")
 for k in ["automatic_live_promotion_allowed","cross_tenant_routing_allowed","live_order_submission_allowed","capital_activation_allowed","production_authorization_allowed"]:
  if v[k] is not False:raise ConstitutionError(f"{k} must be false")
 clauses=list_of(v["clauses"],"clauses",64);unique(clauses,"clause_id","clauses")
 for c in clauses:exact(c,["clause_id","priority","requirement","failure_action","evidence_required"]);integer(c["priority"],"priority",1)
 x=deepcopy(v);x["clauses"]=sorted(clauses,key=lambda z:(z["priority"],z["clause_id"]));x["constitution_hash"]=content_hash(x);return x
def authority_boundary()->dict:
 return seal({"phase":"SAED_V4_40","may_register_context_cells":True,"may_compile_fleet_manifest":True,"may_simulate_placement":True,"may_simulate_rollout":True,"may_route_synthetic_occurrences":True,"may_quarantine_cells":True,"may_generate_mql5_fleet_mirror":True,"may_submit_live_order":False,"may_activate_capital":False,"may_auto_promote_live":False,"may_cross_tenant_route":False,"may_mutate_immutable_runtime":False,"may_mutate_ucee":False,"may_claim_external_scale_evidence_without_attachment":False,"may_claim_production_authorization":False,"failure_action":"ABSTAIN_QUARANTINE_PRESERVE_BASELINE_AND_ESCALATE","research_only":True},"v440_authority","boundary_id","boundary_hash")
