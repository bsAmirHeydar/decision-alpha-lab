import json,copy,pytest
from saed_v4_generative_path_stress_lab.service import run_reference,future_suffix_invariance

def test_reference_deterministic(config,upstream,paths,policy):assert run_reference(config,upstream,paths,policy)==run_reference(config,upstream,paths,policy)
def test_certificate_denials(config,upstream,paths,policy):
    c=run_reference(config,upstream,paths,policy)['certificate'];assert c['positive_alpha_evidence'] is False and c['promotion_authority'] is False and c['runtime_executable'] is False and c['production_authority'] is False
@pytest.mark.parametrize('field',['decision','execution','promotion','production','risk_allocation','runtime'])
def test_handoff_authority_denied(config,upstream,paths,policy,field):assert run_reference(config,upstream,paths,policy)['handoff']['authority'][field] is False
def test_future_suffix_invariance(config,upstream,paths,policy):assert future_suffix_invariance(config,upstream,paths,policy)['passed']
def test_zero_protected_budget(config,upstream,paths,policy):
    b=run_reference(config,upstream,paths,policy)['budget_snapshot'];assert b['hidden_evaluation_queries']==0 and b['protected_evidence_exposures']==0
def test_claim_tier(config,upstream,paths,policy):assert run_reference(config,upstream,paths,policy)['claim_tier_report']['synthetic_positive_evidence_allowed'] is False
