import pytest

def test_reachable_graph_complete(result): assert result["graph"]["complete_for_reachable_finite_state_space"] and result["graph"]["state_count"]==6
@pytest.mark.parametrize("index",range(14))
def test_each_invariant_passes(result,index): assert result["invariant_report"]["results"][index]["passed"]
@pytest.mark.parametrize("index",range(12))
def test_each_temporal_property_passes(result,index): assert result["temporal_report"]["results"][index]["passed"]
@pytest.mark.parametrize("stage",["IDLE","INGESTED","VERIFIED","QUALIFIED","REJECTED","QUARANTINED"])
def test_each_stage_reachable(result,stage): assert any(x["values"]["stage"]==stage for x in result["graph"]["states"])
@pytest.mark.parametrize("edge",range(5))
def test_each_transition_instance_authority_free(result,edge): assert result["graph"]["edges"][edge]["authority_free"]
