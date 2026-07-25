def test_heavy_tail_benchmark(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_16/GOLDEN_HEAVY_TAIL_BENCHMARK.JSON');assert x['passed'] and x['minimum']<-5 and x['maximum']>10 and x['lower_tail_expected_shortfall']<=x['lower_tail_var']
def test_best_trade_removal(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_16/GOLDEN_BEST_TRADE_REMOVAL.JSON');assert x['passed'] and x['best_trade_dependence_detected']
def test_tail_event_holdout(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_16/GOLDEN_TAIL_EVENT_HOLDOUT.JSON');assert x['passed'] and x['tail_event_count']>0 and x['holdout_is_explicit']
def test_competing_event_swap(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_16/GOLDEN_COMPETING_EVENT_SWAP.JSON');assert x['passed'] and x['mutation_detected']
def test_informative_censoring_sensitivity(load):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_16/GOLDEN_INFORMATIVE_CENSORING_SENSITIVITY.JSON');assert x['passed'] and x['directionally_ordered'] and x['factors']==[0.5,1.0,2.0]
