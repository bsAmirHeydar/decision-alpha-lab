import pytest
from saed_v4_conformal_ood_selective_control.canonical import content_hash
from saed_v4_conformal_ood_selective_control.service import run
def test_certificate(outputs):
    certificate = outputs['certificate']; assert certificate['accepted_for_conformal_ood_selective_research'] and all(certificate['gates'].values())
    assert not any(certificate['authority_boundary']['authority'].values()) and certificate['conditional_coverage_claim'] is False
def test_handoff(outputs):
    handoff = outputs['handoff']; assert handoff['next_phase'] == 'SAED_V4_25' and all(handoff['entry_gates'].values()) and not any(handoff['authority'].values())
def test_deterministic(config, upstream, records, outputs): assert content_hash(run(config, upstream, records)) == content_hash(outputs)
@pytest.mark.parametrize('key', ['hidden_evaluation_queries','protected_evidence_exposures','runtime_compilations','order_submissions'])
def test_exposure_zero(outputs, key): assert outputs['exposure_ledger'][key] == 0
