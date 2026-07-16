def test_survival_predictions_complete(load):
 p=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_PREDICTIONS.JSON');assert p['candidate_count']==5 and p['prediction_count']==240 and len(p['horizons_seconds'])==5
def test_survival_monotone(load):
 p=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_PREDICTIONS.JSON');assert all(all(a>=b for a,b in zip(x['survival_probability'],x['survival_probability'][1:])) for x in p['items'])
def test_cumulative_incidence_monotone(load):
 p=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_PREDICTIONS.JSON');assert all(all(all(a<=b for a,b in zip(v,v[1:])) for v in x['cause_cumulative_incidence'].values()) for x in p['items'])
def test_competing_risk_simplex(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_COMPETING_RISK_SIMPLEX_AUDIT.JSON');assert a['all_simplex_valid'] and all(x['maximum_cumulative_incidence_sum']<=1+1e-12 for x in a['rows'])
def test_non_authoritative(load):
 p=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_SURVIVAL_PREDICTIONS.JSON');assert not any(x['production_eligible'] for x in p['items'])
