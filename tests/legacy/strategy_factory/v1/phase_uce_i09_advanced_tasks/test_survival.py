from strategy_factory_advanced_tasks_v3.golden import survival_observations
from strategy_factory_advanced_tasks_v3.survival import DiscreteHazardModel,survival_metrics

def test_survival_and_competing_risk_are_monotone_and_bounded():
 obs=survival_observations();m=DiscreteHazardModel((60000,120000,180000,240000,360000)).fit(obs);c=m.curve();assert all(a>=b for a,b in zip(c.survival,c.survival[1:]));cr=m.competing_curve();assert all(0<=x<=1 for row in cr.cumulative_incidence for x in row);curves={o.row_id:m.curve(o.row_id) for o in obs};r=survival_metrics(obs,{o.row_id:1/o.duration_ms for o in obs},curves,m.horizons);assert 0<=r.concordance_index<=1
