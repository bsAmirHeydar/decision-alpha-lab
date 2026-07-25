import copy,pytest
from saed_v4_foundation_model_adapters.validation import validate_upstream
from saed_v4_foundation_model_adapters.errors import IntegrityError

def args(i):return [i['v413_handoff'],i['v413_registry'],i['v413_embeddings'],i['v413_graph'],i['v413_tournament']]
def test_upstream_valid(inputs):assert validate_upstream(*args(inputs))['passed']
@pytest.mark.parametrize('target,field',[('v413_handoff','graph_checkpoint_registry_hash'),('v413_handoff','compiled_graph_hash'),('v413_tournament','reference_champion_id')])
def test_upstream_mutation_rejected(inputs,target,field):
 i=copy.deepcopy(inputs);i[target][field]='bad'
 with pytest.raises(IntegrityError):validate_upstream(*args(i))
def test_authority_widening_rejected(inputs):
 i=copy.deepcopy(inputs);i['v413_handoff']['authority']['predict_outcomes']=True
 with pytest.raises(IntegrityError):validate_upstream(*args(i))
