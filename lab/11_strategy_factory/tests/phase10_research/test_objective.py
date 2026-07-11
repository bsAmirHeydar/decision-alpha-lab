from strategy_factory_research.models import *
from strategy_factory_research.objective import evaluate_objective
from strategy_factory_research.enums import *
def m(**kw):
 d=dict(unique_event_count=50,filled_count=40,fill_rate=.8,expectancy_r=.2,maximum_drawdown_r=2,standard_deviation_r=1,best_trade_share=.2)
 d.update(kw)
 return ResearchMetrics(**d)
def test_accept():assert evaluate_objective(m(),ObjectiveConfig()).status==PassStatus.VALID
def test_min_sample():assert evaluate_objective(m(unique_event_count=2),ObjectiveConfig()).status==PassStatus.REJECTED_MIN_SAMPLE
