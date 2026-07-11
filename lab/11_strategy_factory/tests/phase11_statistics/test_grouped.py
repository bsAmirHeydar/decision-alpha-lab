from strategy_factory_statistics.models import StatisticalSample
from strategy_factory_statistics.grouped import GroupedStatisticsEngine,group_key
import pytest

def s(i,r,filled=True,session='ny'):
    return StatisticalSample(f's{i}',f'o{i}',f'c{i}',f'e{i}',f'cl{i//2}','st','EURUSD','long',session,2026,7,4,f'session={session}',filled,False,r,2,1,60)
def test_all_group_summary():
    x=GroupedStatisticsEngine().summarize([s(0,1),s(1,-1),s(2,2),s(3,0)])
    assert len(x)==1 and x[0].sample_count==4 and x[0].unique_cluster_count==2
def test_session_groups_are_sorted():
    x=GroupedStatisticsEngine().summarize([s(0,1,session='ny'),s(1,1,session='ldn')],('session_id',))
    assert [z.group_key for z in x]==['session_id=ldn','session_id=ny']
def test_no_fill_is_not_return():
    x=GroupedStatisticsEngine().summarize([s(0,100,False),s(1,1,True)])[0]
    assert x.filled_count==1 and x.mean_net_r==1
def test_unsupported_dimension_rejected():
    with pytest.raises(ValueError): GroupedStatisticsEngine().summarize([s(0,1)],('future_label',))
def test_summary_hash_deterministic():
    rows=[s(0,1),s(1,-1)]
    a=GroupedStatisticsEngine().summarize(rows)[0];b=GroupedStatisticsEngine().summarize(rows)[0]
    assert a.summary_hash==b.summary_hash
