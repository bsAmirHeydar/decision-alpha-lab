import pytest
from strategy_factory_deep_views_v3.fusion import LateWeightedFusion,StackedFusion
from strategy_factory_deep_views_v3.enums import MissingViewPolicy
from strategy_factory_deep_views_v3.errors import DeepViewError
def test_late_and_stacked_fusion_are_bounded_and_deterministic():
    y=[float(i) for i in range(20)];pred={'a':[x+.1 for x in y],'b':[x-.2 for x in y]};late=LateWeightedFusion.fit(pred,y,MissingViewPolicy.GLOBAL_FALLBACK);p=late.predict('r',{'a':1.1,'b':.8});assert not p.abstained;assert abs(sum(p.view_weights.values())-1)<1e-12
    s1=StackedFusion.fit(pred,y);s2=StackedFusion.fit(pred,y);assert s1.state_hash==s2.state_hash
def test_missing_view_policies_fail_closed():
    y=[0.,1.,2.];pred={'a':[0.,1.,2.],'b':[0.,1.,2.]};m=LateWeightedFusion.fit(pred,y,MissingViewPolicy.REJECT)
    with pytest.raises(DeepViewError,match='missing'):m.predict('r',{'a':1.,'b':None})
