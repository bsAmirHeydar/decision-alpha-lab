import copy,pytest
from saed_v4_graph_hypergraph_models.contracts import GraphSpec,CandidateSpec,ObjectiveSpec
from saed_v4_graph_hypergraph_models.errors import ContractError

def test_graph_spec(inputs):assert GraphSpec.from_mapping(inputs['spec']).known_time_only
@pytest.mark.parametrize('candidate_idx',range(6))
def test_candidate_catalog(inputs,candidate_idx):assert CandidateSpec.from_mapping(inputs['candidates'][candidate_idx]).enabled
@pytest.mark.parametrize('objective_idx',range(5))
def test_objective_catalog(inputs,objective_idx):assert ObjectiveSpec.from_mapping(inputs['objectives'][objective_idx]).outcome_free
def test_unknown_graph_field(inputs):
 x=dict(inputs['spec']);x['unknown']=1
 with pytest.raises(ContractError):GraphSpec.from_mapping(x)
def test_unknown_architecture(inputs):
 x=dict(inputs['candidates'][0]);x['architecture']='unknown'
 with pytest.raises(ContractError):CandidateSpec.from_mapping(x)
