import numpy as np, pytest
from strategy_factory_promotion_v3.uncertainty import *
from strategy_factory_promotion_v3.errors import PromotionError
from strategy_factory_promotion_v3.golden import golden_returns

def test_ess_is_bounded():
    v=golden_returns(); ess=effective_sample_size(v); assert 1<=ess<=len(v)
def test_positive_autocorrelation_reduces_ess():
    rng=np.random.default_rng(3); x=np.zeros(200)
    for i in range(1,len(x)): x[i]=.9*x[i-1]+rng.normal()
    assert effective_sample_size(x)<len(x)/2
def test_block_bootstrap_is_deterministic():
    a=moving_block_bootstrap(golden_returns(),block_size=4,iterations=200,seed=11); b=moving_block_bootstrap(golden_returns(),block_size=4,iterations=200,seed=11); assert a==b
def test_block_bootstrap_interval_contains_estimate():
    r=moving_block_bootstrap(golden_returns(),block_size=4,iterations=200); assert r['lower']<=r['estimate']<=r['upper']
def test_cluster_bootstrap_counts_clusters():
    v=golden_returns(30); c=[f"c{i//3}" for i in range(30)]; assert cluster_bootstrap(v,c,iterations=200)['cluster_count']==10
def test_paired_bootstrap_detects_positive_uplift():
    r=paired_block_bootstrap(golden_returns(40),[0.01]*40,block_size=3,iterations=200); assert r['lower']>0
def test_subgroup_uncertainty_is_sorted_and_complete():
    v=golden_returns(20); g=['b' if i%2 else 'a' for i in range(20)]; assert list(subgroup_uncertainty(v,g,iterations=200))==['a','b']
def test_sequential_confidence_uses_all_looks(): assert [x['look'] for x in sequential_confidence(golden_returns(40),(10,20,40),iterations=200)]==[10,20,40]
def test_invalid_block_size_fails_closed():
    with pytest.raises(PromotionError): moving_block_bootstrap([1,2,3],block_size=4,iterations=200)
def test_uncertainty_report_carries_evidence_hash(): assert len(build_uncertainty_report(golden_returns(),report_name='x',iterations=200).evidence_hash)==64
