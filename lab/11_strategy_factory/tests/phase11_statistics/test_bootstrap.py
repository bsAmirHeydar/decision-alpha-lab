from strategy_factory_statistics.models import StatisticalSample
from strategy_factory_statistics.bootstrap import cluster_bootstrap_mean_interval
import pytest

def s(i,cl,r):return StatisticalSample(f's{i}',f'o{i}',f'c{i}',f'e{i}',cl,'st','EURUSD','long','ny',2026,7,4,'x',True,False,r,1,1,60)
def test_cluster_bootstrap_deterministic():
    rows=[s(0,'a',1),s(1,'a',2),s(2,'b',-1),s(3,'c',1)]
    a=cluster_bootstrap_mean_interval(rows,iterations=200,seed=7)
    b=cluster_bootstrap_mean_interval(rows,iterations=200,seed=7)
    assert a.lower==b.lower and a.upper==b.upper and a.effective_sample_count==3
def test_cluster_bootstrap_rejects_too_few_iterations():
    with pytest.raises(ValueError): cluster_bootstrap_mean_interval([s(0,'a',1)],iterations=10)
