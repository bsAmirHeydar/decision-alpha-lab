from __future__ import annotations
from .canonical import content_hash,seal

def evidence_bundle(e:dict)->dict:
    keys=["upstream","constitution","authority","models","datasets","dependencies","tools","runtimes","services","sbom","dependency_graph","license_policy","license_review","vulnerability_catalog","vulnerability_review","build_provenance","signatures","reproducible_build","tamper_evidence","model_cards","data_cards","tiering","scorecards","validation_plan","validation_results","threat_model","attack_surface","three_lines","committee","audit","governance_ledger","exceptions","waivers","quarantine","incident_plan","recall_plan","baseline","ucee","external_boundary","eligibility","limitations","independent_reproduction","replay"]
    refs=[{"artifact":k,"artifact_hash":content_hash(e[k])} for k in keys]
    return seal({"phase":"SAED_V4_35","references":refs,"reference_count":len(refs),"complete":True,"research_only":True},"v435_evidence","bundle_id","bundle_hash")

def certificate(e:dict)->dict:
    eligible=e["eligibility"]["reference_release_eligible"] and e["replay"]["deterministic"] and e["independent_reproduction"]["exact_match"]
    return seal({"phase":"SAED_V4_35","reference_accepted":eligible,"status":"ACCEPTED_REFERENCE" if eligible else "REJECTED","claim_ceiling":"synthetic_deterministic_reference_only","evidence_bundle_hash":e["evidence_bundle"]["bundle_hash"],"production_authorized":False,"runtime_activation_allowed":False,"live_trading_authority":False,"research_only":True},"v435_certificate","certificate_id","certificate_hash")

def handoff(cert:dict,sbom:dict,scorecards:dict,ledger:dict)->dict:
    return seal({"phase":"SAED_V4_35","next_phase":"SAED_V4_36","certificate_hash":cert["certificate_hash"],"sbom_hash":sbom["sbom_hash"],"risk_scorecard_hash":scorecards["registry_hash"],"governance_ledger_hash":ledger["ledger_hash"],"handoff_scope":"immutable research-memory inputs only","authority_granted":False,"production_authorized":False,"research_only":True},"v435_handoff","handoff_id","handoff_hash")
