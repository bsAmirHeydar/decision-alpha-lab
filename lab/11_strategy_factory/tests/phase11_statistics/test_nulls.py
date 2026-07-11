from strategy_factory_statistics.models import StatisticalSample,MatchedNullSpec
from strategy_factory_statistics.enums import NullMethod,ReportStatus
from strategy_factory_statistics.nulls import MatchedNullEngine,compare_matched_pairs

def s(i,cl,r,stratum='x'):return StatisticalSample(f's{i}',f'o{i}',f'c{i}',f'e{i}',cl,'st','EURUSD','long','ny',2026,7,4,stratum,True,False,r,1,1,60)
def spec():return MatchedNullSpec('n','1',NullMethod.EXACT_STRATIFIED_CYCLIC,17,1,1,True,('session_id',)).with_hash()
def test_exact_matching_different_cluster():
    obs=[s(1,'a',1)];ctl=[s(2,'a',0),s(3,'b',0)]
    a=MatchedNullEngine(spec()).assign(obs,ctl)
    assert len(a)==1 and a[0].control_cluster_id=='b'
def test_reuse_cap_is_enforced():
    obs=[s(1,'a',1),s(2,'b',1),s(3,'c',1)];ctl=[s(9,'z',0)]
    a=MatchedNullEngine(spec()).assign(obs,ctl)
    assert len(a)==1
def test_unmatched_comparison():
    x=compare_matched_pairs([],[],[],'n')
    assert x.status==ReportStatus.UNMATCHED
def test_positive_uplift():
    obs=[s(1,'a',1),s(2,'b',2)];ctl=[s(3,'c',0),s(4,'d',0)]
    a=MatchedNullEngine(spec()).assign(obs,ctl);x=compare_matched_pairs(obs,ctl,a,spec().null_hash)
    assert x.uplift_r>0 and x.matched_count==2
