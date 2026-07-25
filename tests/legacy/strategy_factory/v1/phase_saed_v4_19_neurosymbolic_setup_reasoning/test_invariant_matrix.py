import pytest
from saed_v4_neurosymbolic_setup_reasoning.security import threat_response

@pytest.mark.parametrize('threat,expected',[
 ('dynamic_code_injection','reject'),('ontology_expansion','reject'),('future_fact_injection','reject'),('rule_hash_substitution','quarantine'),('proof_elision','reject'),('manual_doctrine_override','reject'),('neural_symbolic_disagreement','abstain'),('protected_evidence_access','stop_family'),('runtime_authority_escalation','reject'),('execution_api_access','reject')])
def test_threat_matrix(threat,expected):assert threat_response(threat)==expected
@pytest.mark.parametrize('artifact',[ 'GOLDEN_REASONING_TRACE.JSON','GOLDEN_SOFT_LOGIC_REPORT.JSON','GOLDEN_CONSTRAINT_PROJECTION.JSON','GOLDEN_PROOF_ENVELOPE.JSON','GOLDEN_FACT_CONTRADICTION_AUDIT.JSON','GOLDEN_DECISION_CONTRADICTION_AUDIT.JSON','GOLDEN_BOUNDED_SYNTHESIS_REPORT.JSON','GOLDEN_COUNTEREXAMPLE_REPORT.JSON','GOLDEN_MUTATION_COUNTEREXAMPLE_REPORT.JSON','GOLDEN_SYMBOLIC_REGRESSION_REPORT.JSON','GOLDEN_NEURAL_SYMBOLIC_DISAGREEMENT.JSON','GOLDEN_MDL_SCORECARD.JSON','GOLDEN_BASELINE_PRESERVATION.JSON','GOLDEN_EXPOSURE_LEDGER.JSON','GOLDEN_AUTHORITY_BOUNDARY.JSON','GOLDEN_UPSTREAM_VALIDATION.JSON','GOLDEN_CLAIM_TIER_REPORT.JSON','GOLDEN_SECURITY_REVIEW.JSON','GOLDEN_MODEL_RISK_DOSSIER.JSON','GOLDEN_INTEGRITY_RECEIPT.JSON','GOLDEN_PROVENANCE_GRAPH.JSON','GOLDEN_PROOF_REGISTRY.JSON','GOLDEN_REPLAY_BUNDLE.JSON','V4_19_TO_V4_20_HANDOFF.JSON'])
def test_artifact_nonempty(root,art,artifact):assert (root/art/artifact).stat().st_size>20
@pytest.mark.parametrize('claim',[ 'decision_authority','promotion_authority','runtime_authority','execution_authority','production_authority','real_mechanism_claim_authority','production_treatment_selection_authority'])
def test_authority_false(load,art,claim):assert load(art+'/GOLDEN_AUTHORITY_BOUNDARY.JSON')[claim] is False
