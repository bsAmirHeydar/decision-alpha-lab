import pytest

def test_decision_count(outputs): assert len(outputs['selective_decisions']) == 60
@pytest.mark.parametrize('index', range(40))
def test_decision_fail_closed(outputs, index):
    decision = outputs['selective_decisions'][index]
    assert decision['accepted'] != decision['abstained']
    assert decision['selected_action'] == (decision['candidate_action'] if decision['accepted'] else 'skip')
    assert decision['uses_realized_outcome'] is False
    assert decision['promotion_eligible'] is False and decision['runtime_executable'] is False
@pytest.mark.parametrize('index', range(10))
def test_frontier_rows(outputs, index):
    row = outputs['coverage_risk_frontier']['rows'][index]
    assert 0 <= row['coverage'] <= 1 and 0 <= row['selective_risk'] <= 1
    assert 0 <= row['selective_risk_lower'] <= 1 and 0 <= row['selective_risk_upper'] <= 1
    assert row['bootstrap_draws'] == 300 and 'monotone_risk_upper' in row
def test_abstention_policy(outputs):
    policy = outputs['abstention_policy']; assert policy['safe_action'] == 'skip' and policy['research_only']
