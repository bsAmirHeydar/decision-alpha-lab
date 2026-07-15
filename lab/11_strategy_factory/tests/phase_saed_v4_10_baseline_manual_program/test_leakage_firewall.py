import pytest
from saed_v4_baseline_manual.compiler import compile_program
from saed_v4_baseline_manual.errors import LeakageError,ContractError

def test_outcome_feature_rejected(load,upstream):
 v,_,l,_=upstream;p=load('lab/11_strategy_factory/examples/saed_v4_10/negative/unknown_feature.json')
 with pytest.raises(LeakageError):compile_program(p,v,l)
def test_unknown_node_rejected(load,upstream):
 v,_,l,_=upstream;p=load('lab/11_strategy_factory/examples/saed_v4_10/negative/unknown_node.json')
 with pytest.raises(ContractError):compile_program(p,v,l)
def test_non_abstain_fallback_rejected(load,upstream):
 v,_,l,_=upstream;p=load('lab/11_strategy_factory/examples/saed_v4_10/negative/non_abstain_fallback.json')
 with pytest.raises(ContractError):compile_program(p,v,l)
