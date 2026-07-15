import pytest
from saed_v4_graph_hypergraph_models.contracts import GraphSpec,CandidateSpec
from saed_v4_graph_hypergraph_models.graph_compiler import compile_graph
from saed_v4_graph_hypergraph_models.perturbation import future_suffix_audit,node_order_audit
@pytest.mark.parametrize('idx',range(6))
def test_future_suffix(inputs,idx):
 s=GraphSpec.from_mapping(inputs['spec']);c=CandidateSpec.from_mapping(inputs['candidates'][idx]);g=compile_graph(inputs['graph'],inputs['snapshots'],inputs['distill'],s,inputs['graph']['known_as_of']);assert future_suffix_audit(inputs['graph'],g,s,c,compile_graph,inputs['snapshots'],inputs['distill'])['passed']
@pytest.mark.parametrize('idx',range(6))
def test_order_invariance(inputs,idx):
 s=GraphSpec.from_mapping(inputs['spec']);c=CandidateSpec.from_mapping(inputs['candidates'][idx]);g=compile_graph(inputs['graph'],inputs['snapshots'],inputs['distill'],s,inputs['graph']['known_as_of']);assert node_order_audit(g,s,c)['passed']
