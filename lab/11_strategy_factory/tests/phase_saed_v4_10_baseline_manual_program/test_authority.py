import pytest
from saed_v4_baseline_manual.authority import boundary_record,assert_reference_authority
from saed_v4_baseline_manual.errors import AuthorityError

def test_authority_defaults_closed():
 x=boundary_record()['capabilities'];assert x['compile_manual_program'];assert not x['train_model'];assert not x['select_treatment'];assert not x['send_order']
def test_forbidden_authority_rejected():
 with pytest.raises(AuthorityError):assert_reference_authority({'send_order':True})
