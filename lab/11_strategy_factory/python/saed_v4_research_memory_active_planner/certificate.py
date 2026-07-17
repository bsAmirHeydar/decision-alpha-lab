from __future__ import annotations
from .canonical import content_hash,seal,merkle_root

def evidence_bundle(e:dict)->dict:
    keys=["upstream","constitution","authority","memory","negative_knowledge","supersession","evidence","lineage","evidence_coverage","claims","contradictions","knowledge_state","retrieval_index","retrieval_receipt","gaps","coverage_matrix","budgets","availability","risk_findings","weights","scorecard","plan","schedule","governance_policy","review","governance_ledger","baseline","external_boundary","limitations","reproduction","replay"]
    hashes=[content_hash(e[k]) for k in keys]
    return seal({"phase":"SAED_V4_36","artifact_keys":keys,"artifact_hashes":hashes,"artifact_count":len(keys),"merkle_root":merkle_root(hashes),"complete":True,"research_only":True},"v436_bundle","bundle_id","bundle_hash")

def certificate(e:dict)->dict:
    accepted=all([e["memory"]["append_only"],e["negative_knowledge"]["record_count"]>0,e["evidence_coverage"]["covered"],e["plan"]["selected_count"]>0,e["review"]["reference_agenda_accepted"],e["replay"]["deterministic"],e["reproduction"]["exact_match"]])
    return seal({"phase":"SAED_V4_36","version":"1.0.0","reference_accepted":accepted,"research_memory_accepted":accepted,"reference_agenda_accepted":accepted,"experiments_executed":0,"automatic_execution_authorized":False,"treatment_selection_authorized":False,"capital_allocation_authorized":False,"runtime_activation_allowed":False,"production_authorized":False,"live_trading_authority":False,"claim_ceiling":"synthetic_deterministic_research_memory_and_agenda_reference_only","evidence_bundle_hash":e["evidence_bundle"]["bundle_hash"],"research_only":True},"v436_certificate","certificate_id","certificate_hash")

def handoff(cert:dict,memory:dict,plan:dict,knowledge:dict,risk:dict)->dict:
    return seal({"phase":"SAED_V4_36","next_phase":"SAED_V4_37","certificate_hash":cert["certificate_hash"],"memory_store_hash":memory["memory_store_hash"],"plan_hash":plan["plan_hash"],"knowledge_state_hash":knowledge["state_hash"],"risk_register_hash":risk["register_hash"],"transferred_artifacts":["immutable research memory identity","negative knowledge registry","evidence coverage matrix","bounded human-reviewed research agenda","risk and budget constraints"],"authority_granted":False,"capital_authority_granted":False,"execution_authority_granted":False,"production_authorized":False,"research_only":True},"v436_handoff","handoff_id","handoff_hash")
