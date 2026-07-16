import pytest

@pytest.mark.parametrize('artifact,key,count',[
 ('GOLDEN_PROPENSITY_SENSITIVITY.JSON','runs',5),('GOLDEN_HIDDEN_CONFOUNDER_SENSITIVITY.JSON','runs',6),('GOLDEN_COST_STRESS.JSON','runs',4),('GOLDEN_TRANSPORT_REPORT.JSON','environments',4)])
def test_sensitivity_counts(load,art,artifact,key,count):assert len(load(f'{art}/{artifact}')[key])==count

def test_transport_no_claim(load,art):assert not load(f'{art}/GOLDEN_TRANSPORT_REPORT.JSON')['transport_claim']

def test_tournament_baselines_preserved(load,art):
 t=load(f'{art}/GOLDEN_POLICY_TOURNAMENT.JSON');assert t['baseline_preserved'] and t['manual_fallback_preserved'] and not t['production_promotion_allowed']

def test_champion_exists(load,art):
 t=load(f'{art}/GOLDEN_POLICY_TOURNAMENT.JSON');assert t['reference_champion_id'] in {x['policy_id'] for x in t['candidates']}

@pytest.mark.parametrize('case',range(6))
def test_fail_closed_cases(load,art,case):assert load(f'{art}/GOLDEN_FAIL_CLOSED_AUDITS.JSON')['cases'][case]['passed']

def test_estimator_scorecard_preserves_baseline(load,art):
 x=load(f'{art}/GOLDEN_ESTIMATOR_SCORECARD.JSON');assert x['baseline_preserved'] and len(x['methods'])==5
