import copy,pytest
from saed_v4_sequence_state_space.embeddings import FrozenEmbeddingTable
from saed_v4_sequence_state_space.sequence import compile_points,compile_sequences
from saed_v4_sequence_state_space.errors import CausalityError

def _table(upstream):return FrozenEmbeddingTable(upstream[1],upstream[4]['encoder_checkpoint_hash'])
def test_compile(upstream):
 p=compile_points(upstream[0],_table(upstream));s=compile_sequences(p,16);assert len(p)==22 and len(s)==5 and {x.split for x in s}=={'train','validation','test'}
@pytest.mark.parametrize('token',['OUTCOME::win','EXECUTION_RESULT::fill','CONTEXT_ID::x','RECORD_ID::x'])
def test_forbidden_tokens(upstream,token):
 d=copy.deepcopy(upstream[0]);d['streams'][0]['tokens'].append(token)
 with pytest.raises(CausalityError):compile_points(d,_table(upstream))
def test_known_time_violation(upstream):
 d=copy.deepcopy(upstream[0]);d['streams'][0]['known_time']='2020-01-01T00:00:00Z'
 with pytest.raises(CausalityError):compile_points(d,_table(upstream))
