from strategy_factory_research.models import *
from strategy_factory_research.frames import *
from strategy_factory_research.enums import *
def test_roundtrip():
 m=ResearchMetrics(outcome_count=10,filled_count=8,unique_event_count=10,unique_cluster_count=9,fill_rate=.8,expectancy_r=.2).with_hash();s=PassSummary(7,"run","man","par",1.2,PassStatus.VALID,m).with_hash();d=to_frame(s);r=from_frame("run","man","par",7,1.2,d);assert len(d)==24 and r.metrics.expectancy_r==.2
