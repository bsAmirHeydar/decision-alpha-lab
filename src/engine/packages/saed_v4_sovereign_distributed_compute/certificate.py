from __future__ import annotations
from .canonical import content_hash,seal

def evidence_bundle(items:dict)->dict:
    entries=[]
    for k,v in sorted(items.items()): entries.append({"artifact_key":k,"artifact_hash":content_hash(v)})
    return seal({"phase":"SAED_V4_34","entries":entries,"entry_count":len(entries),"complete":True,"research_only":True},"v434_bundle","bundle_id","bundle_hash")
def certificate(items:dict)->dict:
    return seal({"phase":"SAED_V4_34","title":"Sovereign Distributed Compute","version":"1.0.0","status":"accepted_reference","upstream_verified":items["upstream"]["verified"],"contracts_closed":items["contract_closure"]["closure_passed"],"deterministic_replay":items["replay"]["deterministic"],"future_suffix_invariant":items["known_time"]["future_suffix_invariant"],"resource_budget_passed":items["usage"]["all_within_budget"],"locality_passed":items["locality"]["all_locality_satisfied"],"recovery_reference_passed":items["recovery"]["all_recovered"],"evidence_quorum_met":items["quorum"]["threshold_met"],"ucee_compatibility":items["ucee"]["compatibility_passed"],"baseline_preserved":True,"promotion_authority":False,"execution_authority":False,"production_authorization":False,"claim_ceiling":"synthetic_deterministic_reference_only","research_only":True},"v434_certificate","certificate_id","certificate_hash")
def handoff(cert:dict)->dict:
    return seal({"phase":"SAED_V4_34","next_phase":"SAED_V4_35","certificate_id":cert["certificate_id"],"certificate_hash":cert["certificate_hash"],"immutable_inputs":["compute constitution","domain registry","node registry","workload DAG","resource budget","execution transcript","recovery transcript","exposure ledger","provenance graph"],"entry_gates":["verify V4-34 hashes","freeze model and dependency identities","freeze provenance and SBOM boundaries","approve model-risk and supply-chain review budgets","preserve UCEE authority"],"authority_granted":False,"production_authorized":False,"research_only":True},"v434_handoff","handoff_id","handoff_hash")
