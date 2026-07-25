from strategy_factory_deep_views_v3.regime import RegimeModel,DistanceNoveltyModel,RegimeExpertGate
from strategy_factory_deep_views_v3.enums import RegimeGateDecision
def test_regime_gate_uses_global_for_sparse_regime_and_abstains_on_novelty():
    rows=[(float(i%3),float(i//3)) for i in range(30)];reg=RegimeModel.fit(rows,3);nov=DistanceNoveltyModel.fit(rows);gate=RegimeExpertGate(reg,nov,('e0','e1','e2'),100,.1,1.0)
    p=gate.predict('r0',rows[0]);assert p.decision is RegimeGateDecision.GLOBAL
    q=gate.predict('r1',(999.,999.));assert q.decision is RegimeGateDecision.ABSTAIN
