import pytest
from saed_v4_self_supervised_pretraining.authority import AUTHORITY,assert_reference_authority,boundary_record
from saed_v4_self_supervised_pretraining.errors import AuthorityError

def test_reference_training_allowed():assert AUTHORITY['train_reference_synthetic_encoder']
def test_execution_denied():assert not AUTHORITY['send_order'] and not AUTHORITY['activate_runtime']
def test_forbidden_authority_rejected():
 with pytest.raises(AuthorityError):assert_reference_authority({'send_order':True})
def test_unknown_authority_rejected():
 with pytest.raises(AuthorityError):assert_reference_authority({'invented':True})
def test_boundary_reference_only():assert boundary_record()['authority']=='reference_synthetic_only'
