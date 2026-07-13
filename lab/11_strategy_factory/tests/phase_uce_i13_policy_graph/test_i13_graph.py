from dataclasses import replace
import pytest
from strategy_factory_policy_v3.golden import *
from strategy_factory_policy_v3.graph import compile_graph
from strategy_factory_policy_v3.contracts import PolicyNodeSpec
from strategy_factory_policy_v3.enums import *
from strategy_factory_policy_v3.errors import PolicyError

def test_manual_graph_compiles(): assert compile_graph(golden_manual_graph()).topological_order[0]=='input'
def test_hybrid_graph_compiles_with_admission(): assert compile_graph(golden_hybrid_graph(),golden_admission()).topological_order[-1]=='output'
def test_hybrid_missing_admission_rejected():
    with pytest.raises(PolicyError):compile_graph(golden_hybrid_graph())
def test_manual_graph_rejects_ai_node():
    g=golden_hybrid_graph();
    with pytest.raises(PolicyError):compile_graph(replace(g,mode=PolicyMode.MANUAL_ONLY),golden_admission())
def test_cycle_rejected():
    g=golden_manual_graph(); nodes=list(g.nodes); nodes[0]=replace(nodes[0],dependencies=('output',))
    with pytest.raises(PolicyError,match='acyclic'):compile_graph(replace(g,nodes=tuple(nodes)))
def test_missing_dependency_rejected():
    g=golden_manual_graph(); nodes=list(g.nodes); nodes[1]=replace(nodes[1],dependencies=('missing',))
    with pytest.raises(PolicyError):compile_graph(replace(g,nodes=tuple(nodes)))
def test_wrong_authority_rejected():
    g=golden_manual_graph(); nodes=list(g.nodes); nodes[1]=replace(nodes[1],authority=Authority.MODEL)
    with pytest.raises(PolicyError):compile_graph(replace(g,nodes=tuple(nodes)))
def test_unknown_config_rejected():
    g=golden_manual_graph(); nodes=list(g.nodes); nodes[1]=replace(nodes[1],config={'x':1})
    with pytest.raises(PolicyError):compile_graph(replace(g,nodes=tuple(nodes)))
def test_unreachable_node_rejected():
    g=golden_manual_graph(); extra=PolicyNodeSpec('extra',NodeKind.FALLBACK,('input',),Authority.SYSTEM)
    with pytest.raises(PolicyError):compile_graph(replace(g,nodes=g.nodes+(extra,)))
def test_topological_order_deterministic(): assert compile_graph(golden_hybrid_graph(),golden_admission()).topological_order==compile_graph(golden_hybrid_graph(),golden_admission()).topological_order
def test_graph_support_cannot_exceed_promotion():
    g=golden_hybrid_graph()
    with pytest.raises(PolicyError): compile_graph(replace(g,supported_treatments=g.supported_treatments+('iceberg',)),golden_admission())
