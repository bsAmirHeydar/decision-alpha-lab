from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer
from .errors import ConstitutionError
from .canonical import content_hash,seal

def freeze_constitution(v:dict)->dict:
 exact(v,["constitution_id","version","clauses","research_only","immutable_bundle_required","deterministic_runtime_required","closed_abi_required","external_evidence_separation_required","automatic_order_submission_allowed","capital_activation_allowed","production_authorization_allowed"])
 for k in ["research_only","immutable_bundle_required","deterministic_runtime_required","closed_abi_required","external_evidence_separation_required"]:
  if v[k] is not True:raise ConstitutionError(f"{k} must be true")
 for k in ["automatic_order_submission_allowed","capital_activation_allowed","production_authorization_allowed"]:
  if v[k] is not False:raise ConstitutionError(f"{k} must be false")
 clauses=list_of(v["clauses"],"clauses",28); unique(clauses,"clause_id","clauses"); out=[]
 for c in clauses:
  exact(c,["clause_id","priority","requirement","failure_action","evidence_required"]); integer(c["priority"],"priority",1); out.append(deepcopy(c))
 x=deepcopy(v); x["clauses"]=sorted(out,key=lambda z:(z["priority"],z["clause_id"])); x["constitution_hash"]=content_hash(x); return x

def authority_boundary()->dict:
 return seal({"phase":"SAED_V4_38","research_only":True,"may_compile_immutable_bundle":True,"may_generate_mql5_source":True,"may_run_python_reference":True,"may_run_synthetic_mql5_emulator":True,"may_emit_parity_vectors":True,"may_accept_external_evidence":True,"may_send_order":False,"may_activate_capital":False,"may_mutate_ucee":False,"may_promote_model":False,"may_claim_metaeditor_compile_without_evidence":False,"may_claim_terminal_parity_without_evidence":False,"may_authorize_production":False,"live_trading_authority":False,"failure_action":"ABSTAIN_PRESERVE_BASELINE_AND_ESCALATE"},"v438_authority","boundary_id","boundary_hash")
