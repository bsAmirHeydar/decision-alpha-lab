import pytest
from saed_v4_graph_hypergraph_models.contracts import GraphSpec,CandidateSpec,ObjectiveSpec
from saed_v4_graph_hypergraph_models.graph_compiler import compile_graph
from saed_v4_graph_hypergraph_models.models import encode
from saed_v4_graph_hypergraph_models.objectives import evaluate
@pytest.mark.parametrize('idx',range(6))
def test_all_objectives(inputs,idx):
 s=GraphSpec.from_mapping(inputs['spec']);g=compile_graph(inputs['graph'],inputs['snapshots'],inputs['distill'],s,inputs['graph']['known_as_of']);c=CandidateSpec.from_mapping(inputs['candidates'][idx]);m=evaluate(g,encode(g,s,c),[ObjectiveSpec.from_mapping(x) for x in inputs['objectives']]);assert 0<=m['composite_score']<=1 and len(m['objectives'])==5 and not m['outcome_supervision']
