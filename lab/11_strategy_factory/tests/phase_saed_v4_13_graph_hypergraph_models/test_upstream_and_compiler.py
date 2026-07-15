import copy,pytest
from saed_v4_graph_hypergraph_models.validation import validate_upstream
from saed_v4_graph_hypergraph_models.graph_compiler import compile_graph
from saed_v4_graph_hypergraph_models.contracts import GraphSpec
from saed_v4_graph_hypergraph_models.errors import IntegrityError,CausalityError,TopologyError,ContaminationError

def test_upstream(inputs):assert validate_upstream(inputs['graph'],inputs['receipt'],inputs['handoff'],inputs['registry'],inputs['distill'])['passed']
def test_bad_registry(inputs):
 x=copy.deepcopy(inputs['registry']);x['registry_hash']='0'*64
 with pytest.raises(IntegrityError):validate_upstream(inputs['graph'],inputs['receipt'],inputs['handoff'],x,inputs['distill'])
def test_compiler_counts(inputs):
 g=compile_graph(inputs['graph'],inputs['snapshots'],inputs['distill'],GraphSpec.from_mapping(inputs['spec']),inputs['graph']['known_as_of']);assert len(g['nodes'])==95 and len(g['hyperedges'])==63 and g['frozen']
def test_future_node_rejected(inputs):
 x=copy.deepcopy(inputs['graph']);x['nodes'][0]['known_time']='2027-01-01T00:00:00Z'
 with pytest.raises(CausalityError):compile_graph(x,inputs['snapshots'],inputs['distill'],GraphSpec.from_mapping(inputs['spec']),inputs['graph']['known_as_of'])
def test_dangling_member(inputs):
 x=copy.deepcopy(inputs['graph']);x['edges'][0]['member_node_ids'][0]='missing'
 with pytest.raises(TopologyError):compile_graph(x,inputs['snapshots'],inputs['distill'],GraphSpec.from_mapping(inputs['spec']),inputs['graph']['known_as_of'])
def test_forbidden_label(inputs):
 x=copy.deepcopy(inputs['graph']);x['nodes'][0]['attributes']['outcome']=1
 with pytest.raises(ContaminationError):compile_graph(x,inputs['snapshots'],inputs['distill'],GraphSpec.from_mapping(inputs['spec']),inputs['graph']['known_as_of'])
