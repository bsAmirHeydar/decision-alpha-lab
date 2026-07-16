def test_distribution_predictions_complete(load):
 p=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_DISTRIBUTIONAL_PREDICTIONS.JSON');assert p['candidate_count']==5 and p['prediction_count']==240 and len(p['quantile_levels'])==9
def test_quantiles_monotone(load):
 p=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_DISTRIBUTIONAL_PREDICTIONS.JSON');assert all(all(a<=b for a,b in zip(x['monotone_quantiles'],x['monotone_quantiles'][1:])) for x in p['items'])
def test_crossing_audit(load):
 a=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_QUANTILE_CROSSING_AUDIT.JSON');assert a['all_monotone_after_projection'] and a['crossing_after_count']==0
def test_zero_mass_explicit(load):
 p=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_DISTRIBUTIONAL_PREDICTIONS.JSON');assert 0<p['empirical_zero_mass_probability']<1 and all(0<=x['zero_mass_probability']<=1 for x in p['items'])
def test_non_authoritative(load):
 p=load('lab/11_strategy_factory/artifacts/saed_v4_16/GOLDEN_DISTRIBUTIONAL_PREDICTIONS.JSON');assert not any(x['production_eligible'] for x in p['items'])
