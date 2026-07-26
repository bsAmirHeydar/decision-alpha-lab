import copy,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_03.detector_ir import compile_detector_ir
from src.engine.tooling.strategy_factory.acl_os.acl_03.known_time_ir import compile_known_time_ir
from src.engine.tooling.strategy_factory.acl_os.acl_03.feature_binding_ir import compile_feature_binding_ir

@pytest.mark.parametrize("priority",list(range(0,25)))
def test_transition_priority_is_preserved(package,priority):
    p=copy.deepcopy(package);p["state_machine"]["transitions"][0]["priority"]=priority;ir,f=compile_detector_ir(p);assert not f;assert any(x["priority"]==priority for x in ir["transitions"])

@pytest.mark.parametrize("skew",[0,1,2,5,10,25,50,100,250,500,1000])
def test_clock_skew_is_preserved(package,skew):
    p=copy.deepcopy(package);p["causal_clock"]["clock_skew_tolerance_ms"]=skew;ir,f=compile_known_time_ir(p);assert not f;assert ir["clock_skew_tolerance_ms"]==skew

@pytest.mark.parametrize("kind",["TABULAR","SEQUENCE","GRAPH","HYPERGRAPH","RASTER","EVENT_STREAM"])
def test_feature_kind_is_preserved(package,kind):
    p=copy.deepcopy(package);p["feature_views"]["views"][0]["kind"]=kind;ir,f=compile_feature_binding_ir(p);assert not f;assert ir["bindings"][0]["kind"]==kind
