import copy,pytest
from saed_v4_sequence_state_space.validation import validate_upstream
from saed_v4_sequence_state_space.errors import IntegrityError

def test_upstream_valid(upstream):assert validate_upstream(upstream[4],upstream[2],upstream[1],upstream[3])['passed']
@pytest.mark.parametrize('which',['tokenizer_hash','encoder_checkpoint_hash','checkpoint_registry_hash'])
def test_upstream_hash_mutation_fails(upstream,which):
 h=copy.deepcopy(upstream[4]);h[which]='0'*64
 with pytest.raises(IntegrityError):validate_upstream(h,upstream[2],upstream[1],upstream[3])
