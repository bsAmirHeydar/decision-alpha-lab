import pytest
from saed_v4_sequence_state_space.embeddings import FrozenEmbeddingTable
from saed_v4_sequence_state_space.sequence import compile_points,compile_sequences
from saed_v4_sequence_state_space.validation import validate_candidates
from saed_v4_sequence_state_space.models import build_model
from saed_v4_sequence_state_space.ablation import future_suffix_audit
from saed_v4_sequence_state_space.contamination import audit

def get(upstream):return compile_sequences(compile_points(upstream[0],FrozenEmbeddingTable(upstream[1],upstream[4]['encoder_checkpoint_hash'])),16)
def test_contamination(upstream):assert audit(get(upstream))['passed']
@pytest.mark.parametrize('idx',range(6))
def test_future_suffix(upstream,config,idx):
 c=validate_candidates(config[1])[idx];m=build_model(c,12);assert future_suffix_audit(m,get(upstream)[0])['passed']
