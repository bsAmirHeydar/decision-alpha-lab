import pytest
from saed_v4_outcome_cube.authority import assert_operation,AUTHORITY_BOUNDARY
from saed_v4_outcome_cube.errors import AuthorityError
def test_prohibited_operations():
 for op in ('train_model','select_treatment','allocate_risk','activate_runtime','send_order','mutate_action_lattice'):
  with pytest.raises(AuthorityError):assert_operation(op)
def test_allowed_boundary_is_bounded():assert AUTHORITY_BOUNDARY['build_executable_path_outcome_cube'] and not AUTHORITY_BOUNDARY['network_access']
