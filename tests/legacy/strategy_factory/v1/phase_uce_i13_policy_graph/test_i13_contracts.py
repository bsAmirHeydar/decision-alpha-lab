import pytest
from dataclasses import replace
from strategy_factory_policy_v3.golden import *
from strategy_factory_policy_v3.contracts import *
from strategy_factory_policy_v3.enums import *
from strategy_factory_policy_v3.errors import PolicyError

def test_admission_hash_stable(): assert golden_admission().admission_hash==golden_admission().admission_hash
def test_invalid_signature_blocks_ai():
    a=replace(golden_admission(),signature_valid=False)
    with pytest.raises(PolicyError,match='signature'):a.assert_ai_usable(5000)
def test_challenge_not_ai_usable():
    with pytest.raises(PolicyError,match='promote'):replace(golden_admission(),outcome='challenge').assert_ai_usable(5000)
def test_occurrence_rejects_future_features():
    o=golden_occurrence()
    with pytest.raises(PolicyError):replace(o,feature_time_ms=o.known_time_ms+1)
def test_model_distribution_must_sum_one():
    with pytest.raises(PolicyError):replace(golden_output(),action_probabilities={'enter_long':.8,'no_action':.8})
def test_fallback_reasons_unique():
    f=golden_fallback()
    with pytest.raises(PolicyError):replace(f,rules=(f.rules[0],f.rules[0]))
def test_authority_matrix_complete():
    a=golden_authority(); assert len(a.precedence)==len(Authority)
def test_manual_policy_hash_changes_with_risk(): assert golden_manual().policy_hash!=replace(golden_manual(),risk_tier='low').policy_hash
def test_operator_override_requires_reason():
    with pytest.raises(PolicyError):OperatorOverride('ov:1','occ:1',OverrideKind.VETO,'op','',1,2,'a'*64)
def test_graph_hash_changes_with_node_config():
    g=golden_hybrid_graph(); nodes=list(g.nodes); nodes[3]=replace(nodes[3],config={'action':'enter_long','minimum_probability':.9}); assert g.graph_hash!=replace(g,nodes=tuple(nodes)).graph_hash
