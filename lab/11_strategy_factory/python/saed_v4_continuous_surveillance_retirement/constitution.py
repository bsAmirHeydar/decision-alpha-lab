from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer
from .errors import ConstitutionError
from .canonical import content_hash,seal
def freeze_constitution(v:dict)->dict:
 exact(v,["constitution_id","version","clauses","known_time_only","complete_coverage_required","immutable_observation_ledger","baseline_preservation_required","two_person_retirement_required","retirement_tombstones_immutable","reinstatement_without_requalification_allowed","silent_threshold_change_allowed","automatic_live_authority_allowed","cross_tenant_action_allowed","live_order_submission_allowed","capital_activation_allowed","production_authorization_allowed","research_only"])
 for k in ["known_time_only","complete_coverage_required","immutable_observation_ledger","baseline_preservation_required","two_person_retirement_required","retirement_tombstones_immutable","research_only"]:
  if v[k] is not True:raise ConstitutionError(f"{k} must be true")
 for k in ["reinstatement_without_requalification_allowed","silent_threshold_change_allowed","automatic_live_authority_allowed","cross_tenant_action_allowed","live_order_submission_allowed","capital_activation_allowed","production_authorization_allowed"]:
  if v[k] is not False:raise ConstitutionError(f"{k} must be false")
 clauses=list_of(v["clauses"],"clauses",80);unique(clauses,"clause_id","clauses")
 for c in clauses:exact(c,["clause_id","priority","requirement","failure_action","evidence_required"]);integer(c["priority"],"priority",1)
 x=deepcopy(v);x["clauses"]=sorted(clauses,key=lambda z:(z["priority"],z["clause_id"]));x["clauses_hash"]=content_hash(x["clauses"]);return seal(x,"v441_constitution","frozen_constitution_id","frozen_constitution_hash")
def authority_boundary()->dict:
 return seal({"phase":"SAED_V4_41","may_ingest_synthetic_surveillance":True,"may_detect_drift":True,"may_open_reference_incidents":True,"may_restrict_reference_routes":True,"may_quarantine_reference_cells":True,"may_compile_retirement_candidates":True,"may_retire_synthetic_reference_cells":True,"may_archive_reference_evidence":True,"may_generate_mql5_surveillance_mirror":True,"may_reinstate_without_new_qualification":False,"may_change_thresholds_silently":False,"may_cross_tenant_action":False,"may_submit_live_order":False,"may_activate_capital":False,"may_mutate_immutable_runtime":False,"may_mutate_ucee":False,"may_claim_external_surveillance_evidence_without_attachment":False,"may_claim_production_authorization":False,"failure_action":"ABSTAIN_RESTRICT_QUARANTINE_RETIRE_PRESERVE_BASELINE_AND_ESCALATE","research_only":True},"v441_authority","boundary_id","boundary_hash")
