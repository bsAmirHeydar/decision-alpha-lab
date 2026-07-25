import pytest,copy
from tools.strategy_factory.lcm.lcm_06.adapter_contracts import build,verify
from tools.strategy_factory.lcm.lcm_06.errors import PolicyError
@pytest.mark.parametrize("kind",["CONTEXT","SETUP","TREATMENT","VISUALIZER"])
def test_adapter_types(kind):
    a=build("A",kind,"S","T");assert verify(a);assert not a["execution_authority"]
def test_unknown_adapter_rejected():
    with pytest.raises(PolicyError): build("A","EXECUTION","S","T")
def test_authority_escalation_rejected():
    a=build("A","CONTEXT","S","T");a["live_order_authority"]=True
    with pytest.raises(PolicyError): verify(a)

def test_adapter_digest_tamper_rejected():
    a=build("A","CONTEXT","S","T");a["source_identity_id"]="ALTERED"
    with pytest.raises(PolicyError): verify(a)

def test_adapter_reason_code_preservation_required():
    a=build("A","CONTEXT","S","T");a["reason_codes_preserved"]=False
    with pytest.raises(PolicyError): verify(a)
