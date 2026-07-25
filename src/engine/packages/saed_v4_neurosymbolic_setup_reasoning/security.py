from __future__ import annotations
THREATS={
 'dynamic_code_injection':'reject','ontology_expansion':'reject','future_fact_injection':'reject','rule_hash_substitution':'quarantine',
 'proof_elision':'reject','manual_doctrine_override':'reject','neural_symbolic_disagreement':'abstain','protected_evidence_access':'stop_family',
 'runtime_authority_escalation':'reject','execution_api_access':'reject'
}
def threat_response(name):return THREATS.get(name,'quarantine')
