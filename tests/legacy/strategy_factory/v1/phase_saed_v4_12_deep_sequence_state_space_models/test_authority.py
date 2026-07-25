import pytest
from saed_v4_sequence_state_space.authority import AUTHORITY,assert_authority,boundary_record
from saed_v4_sequence_state_space.errors import AuthorityError
@pytest.mark.parametrize('key',[k for k,v in AUTHORITY.items() if not v])
def test_forbidden_authority_fails(key):
 with pytest.raises(AuthorityError):assert_authority({key:True})
def test_boundary_has_no_execution():
 b=boundary_record();assert not b['decision_authority'] and not b['runtime_authority'] and not b['execution_authority']
