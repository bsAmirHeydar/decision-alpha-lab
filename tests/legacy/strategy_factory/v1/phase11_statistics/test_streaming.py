import math, pytest
from strategy_factory_statistics.streaming import OnlineMoments,DrawdownTracker,BoundedQuantileSketch,DistributionAccumulator

def test_online_moments_reference():
    m=OnlineMoments();[m.add(x) for x in [1,2,3,4]]
    assert m.count==4 and m.mean==2.5 and round(m.variance,6)==round(5/3,6)
def test_online_moments_rejects_nonfinite():
    with pytest.raises(ValueError): OnlineMoments().add(float('nan'))
def test_drawdown_reference():
    d=DrawdownTracker();[d.add(x) for x in [1,-2,1,-3,4]]
    assert d.maximum_drawdown==4
def test_quantiles_reference():
    q=BoundedQuantileSketch(16);[q.add(x) for x in range(10)]
    assert q.quantile(.5)==4.5
def test_distribution_profit_factor():
    a=DistributionAccumulator(16);[a.add(x) for x in [2,-1,1,-1]]
    assert a.profit_factor==1.5
