from strategy_factory_research.models import *
from strategy_factory_research.selector import *
from strategy_factory_research.enums import *
def s(i,score):return PassSummary(i,"r","m","p",score,PassStatus.VALID,ResearchMetrics(unique_event_count=50,expectancy_r=.1).with_hash()).with_hash()
def test_top_n():
 c=SelectedPassCollector(SelectionPolicy(maximum_passes=2,minimum_unique_events=1));[c.consider(s(i,x)) for i,x in [(1,1),(2,3),(3,2)]];assert [x.public_id for x in c.items]==[2,3]
