from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer
from .errors import ConstitutionError
from .canonical import content_hash,seal

def freeze_constitution(v:dict)->dict:
 exact(v,["constitution_id","version","clauses","research_only","prospective_only","shadow_no_order_side_effects","micro_live_requires_external_authorization","baseline_preservation_required","kill_switch_required","two_person_control_required","automatic_order_submission_allowed","capital_activation_allowed","production_authorization_allowed"])
 for k in ["research_only","prospective_only","shadow_no_order_side_effects","micro_live_requires_external_authorization","baseline_preservation_required","kill_switch_required","two_person_control_required"]:
  if v[k] is not True:raise ConstitutionError(f"{k} must be true")
 for k in ["automatic_order_submission_allowed","capital_activation_allowed","production_authorization_allowed"]:
  if v[k] is not False:raise ConstitutionError(f"{k} must be false")
 clauses=list_of(v["clauses"],"clauses",48);unique(clauses,"clause_id","clauses");out=[]
 for c in clauses:
  exact(c,["clause_id","priority","requirement","failure_action","evidence_required"]);integer(c["priority"],"priority",1);out.append(deepcopy(c))
 x=deepcopy(v);x["clauses"]=sorted(out,key=lambda z:(z["priority"],z["clause_id"]));x["constitution_hash"]=content_hash(x);return x

def authority_boundary()->dict:
 return seal({"phase":"SAED_V4_39","research_only":True,"may_run_prospective_paper":True,"may_run_shadow":True,"may_build_order_intents":True,"may_reconcile_simulated_fills":True,"may_prepare_micro_live_plan":True,"may_accept_external_evidence":True,"may_generate_mql5_qualification_harness":True,"may_submit_live_order":False,"may_activate_capital":False,"may_self_authorize_micro_live":False,"may_bypass_kill_switch":False,"may_mutate_immutable_runtime":False,"may_mutate_ucee":False,"may_claim_actual_broker_qualification_without_evidence":False,"may_claim_production_authorization":False,"failure_action":"ABSTAIN_PRESERVE_BASELINE_KILL_AND_ESCALATE"},"v439_authority","boundary_id","boundary_hash")
