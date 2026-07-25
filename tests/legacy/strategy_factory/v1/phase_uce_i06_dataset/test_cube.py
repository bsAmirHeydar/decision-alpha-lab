from decimal import Decimal as D
from strategy_factory_dataset_v3.golden import *
from strategy_factory_dataset_v3.cube import CounterfactualOutcomeCubeBuilder
from strategy_factory_dataset_v3.enums import OutcomeState

def test_cube_dimensions_and_determinism():
    a=golden_anchors(1)[0]; b=CounterfactualOutcomeCubeBuilder(); c1=b.build(a,golden_treatments(a),golden_path(a),golden_scenarios(),[300000]); c2=b.build(a,golden_treatments(a),golden_path(a),golden_scenarios(),[300000]); assert len(c1.cells)==4; assert c1.cube_hash==c2.cube_hash

def test_cost_stress_never_improves_same_path():
    a=golden_anchors(1)[0]; c=CounterfactualOutcomeCubeBuilder().build(a,golden_treatments(a),golden_path(a),golden_scenarios(),[300000]); by={}
    for x in c.cells: by[(x.treatment_id,x.scenario_key)]=x
    for t in golden_treatments(a): assert by[(t.treatment_id,'economics.stressed@1.0.0')].net_pnl_cash<=by[(t.treatment_id,'economics.baseline@1.0.0')].net_pnl_cash

def test_executable_side_long_and_short():
    b=CounterfactualOutcomeCubeBuilder()
    for a in (golden_anchors(2)[0],golden_anchors(2)[1]):
        c=b.build(a,golden_treatments(a),golden_path(a),golden_scenarios()[:1],[300000]); assert all(x.entry_price is not None for x in c.cells); assert all(x.path_hash==c.path_hash for x in c.cells)

def test_manual_and_ai_siblings_share_anchor():
    a=golden_anchors(1)[0]; c=CounterfactualOutcomeCubeBuilder().build(a,golden_treatments(a),golden_path(a),golden_scenarios()[:1],[300000]); assert {x.opportunity_id for x in c.cells}=={a.opportunity_id}
