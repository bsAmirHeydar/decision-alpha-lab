import pytest
from saed_v4_graph_hypergraph_models.contracts import GraphSpec,CandidateSpec
from saed_v4_graph_hypergraph_models.graph_compiler import compile_graph
from saed_v4_graph_hypergraph_models.models import encode
@pytest.fixture(scope='module')
def compiled(inputs):return compile_graph(inputs['graph'],inputs['snapshots'],inputs['distill'],GraphSpec.from_mapping(inputs['spec']),inputs['graph']['known_as_of'])
@pytest.mark.parametrize('idx',range(6))
def test_model_determinism(inputs,compiled,idx):
 s=GraphSpec.from_mapping(inputs['spec']);c=CandidateSpec.from_mapping(inputs['candidates'][idx]);a=encode(compiled,s,c);b=encode(compiled,s,c);assert a['embedding_hash']==b['embedding_hash'] and a['node_count']==95
@pytest.mark.parametrize('idx',range(6))
def test_embedding_width(inputs,compiled,idx):
 s=GraphSpec.from_mapping(inputs['spec']);c=CandidateSpec.from_mapping(inputs['candidates'][idx]);a=encode(compiled,s,c);assert all(len(v)==8 for v in a['embeddings'].values())
