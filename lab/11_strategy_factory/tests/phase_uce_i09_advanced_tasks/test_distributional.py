from strategy_factory_advanced_tasks_v3.golden import quantile_values
from strategy_factory_advanced_tasks_v3.distributional import *
def test_quantiles_conformal_and_tail_summary():
 v=quantile_values();m=EmpiricalQuantileModel((.05,.25,.5,.75,.95)).fit(v);p=m.predict('r');assert p.monotone;state=fit_conformal_interval(v[:30],[m.values[2]]*30,.1);i=apply_conformal('r',m.values[2],state);assert i.lower<=i.upper;s=distributional_summary('r',v,.05,1.,-1.);assert s.conditional_value_at_risk<=s.value_at_risk
