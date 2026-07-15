import pytest
from saed_v4_sequence_state_space.validation import validate_sequence_spec,validate_candidates,validate_reset_policy
from saed_v4_sequence_state_space.errors import ContractError

def test_valid_contracts(config):
 s,c,r=config;assert validate_sequence_spec(s).causal;assert len(validate_candidates(c))==6;assert validate_reset_policy(r).fail_closed_on_corruption
@pytest.mark.parametrize('field',['input_dim','state_dim','max_context_steps','chunk_size','gap_reset_seconds'])
def test_invalid_sequence_limits(config,field):
 s=dict(config[0]);s[field]=0
 with pytest.raises(ContractError):validate_sequence_spec(s)
def test_unknown_architecture(config):
 c=[dict(config[1][0])];c[0]['architecture']='unknown'
 with pytest.raises(ContractError):validate_candidates(c)
