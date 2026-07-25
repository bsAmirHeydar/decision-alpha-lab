import json,pytest
from saed_v4_sequence_state_space.embeddings import FrozenEmbeddingTable
from saed_v4_sequence_state_space.sequence import compile_points,compile_sequences
from saed_v4_sequence_state_space.contracts import CandidateSpec
from saed_v4_sequence_state_space.models import build_model
from saed_v4_sequence_state_space.streaming import batch_streaming_parity,chunked_parity

def seq(upstream):return compile_sequences(compile_points(upstream[0],FrozenEmbeddingTable(upstream[1],upstream[4]['encoder_checkpoint_hash'])),16)[0]
@pytest.mark.parametrize('architecture',['ema_recurrent','causal_convolution','diagonal_ssm','selective_ssm','local_causal_attention','hybrid_ssm_attention'])
def test_batch_streaming_parity(upstream,architecture):
 m=build_model(CandidateSpec('p_'+architecture,architecture,11,10,16,True),12);assert batch_streaming_parity(m,seq(upstream))['passed']
@pytest.mark.parametrize('architecture',['ema_recurrent','causal_convolution','diagonal_ssm','selective_ssm','local_causal_attention','hybrid_ssm_attention'])
def test_chunk_parity(upstream,architecture):
 m=build_model(CandidateSpec('c_'+architecture,architecture,13,10,16,True),12);assert chunked_parity(m,seq(upstream),2)['passed']
