import pytest
from saed_v4_sequence_state_space.embeddings import FrozenEmbeddingTable
from saed_v4_sequence_state_space.errors import IntegrityError

def test_binding(upstream):
 t=FrozenEmbeddingTable(upstream[1],upstream[4]['encoder_checkpoint_hash']);b=t.binding();assert b['frozen'] and b['trainable_parameters']==0 and b['dimension']==12
def test_unknown_token_is_zero(upstream):
 t=FrozenEmbeddingTable(upstream[1],upstream[4]['encoder_checkpoint_hash']);assert t.token('DOES_NOT_EXIST')==(0.0,)*12
def test_bad_hash(upstream):
 with pytest.raises(IntegrityError):FrozenEmbeddingTable(upstream[1],'0'*64)
