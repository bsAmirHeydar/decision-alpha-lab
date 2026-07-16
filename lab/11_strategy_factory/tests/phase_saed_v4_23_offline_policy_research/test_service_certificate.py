import pytest
from saed_v4_offline_policy_research.service import run

def test_reference_run(config,upstream,dataset,baseline):
    o=run(config,upstream,dataset,baseline);assert o['certificate']['accepted_for_offline_policy_research'] and o['handoff']['next_phase']=='SAED_V4_24'
def test_deterministic(config,upstream,dataset,baseline):assert run(config,upstream,dataset,baseline)['replay_receipt']['replay_hash']==run(config,upstream,dataset,baseline)['replay_receipt']['replay_hash']
@pytest.mark.parametrize('field',['promotion_authority','runtime_executable','production_authority','real_alpha_claim','prospective_success_claim'])
def test_certificate_denials(config,upstream,dataset,baseline,field):assert run(config,upstream,dataset,baseline)['certificate'][field] is False
@pytest.mark.parametrize('field',['decision','execution','production','promotion','risk_allocation','runtime'])
def test_handoff_denials(config,upstream,dataset,baseline,field):assert run(config,upstream,dataset,baseline)['handoff']['authority'][field] is False
def test_exposure_zero(config,upstream,dataset,baseline):
    x=run(config,upstream,dataset,baseline)['exposure_ledger'];assert x['hidden_evaluation_queries']==0 and x['protected_evidence_exposures']==0 and x['order_submissions']==0
