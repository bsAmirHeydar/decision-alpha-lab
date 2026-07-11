from strategy_factory_research.models import ResearchMetrics
from strategy_factory_research.differential import *
from strategy_factory_research.enums import DifferentialStatus
def test_exact():
 m=ResearchMetrics(total_net_r=1,fill_rate=.5,maximum_drawdown_r=2,filled_count=10);assert compare_metrics(m,m).status==DifferentialStatus.MATCH
def test_mismatch():
 a=ResearchMetrics(total_net_r=1,fill_rate=.5,maximum_drawdown_r=2,filled_count=10);b=ResearchMetrics(total_net_r=4,fill_rate=.5,maximum_drawdown_r=2,filled_count=10);assert compare_metrics(a,b).status==DifferentialStatus.MISMATCH
