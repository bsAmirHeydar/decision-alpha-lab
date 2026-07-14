import pytest
from saed_v4_data_foundation.enums import DataRole,AccessOperation
from saed_v4_data_foundation.partitions import assert_role_operation,assert_derivation_flow
from saed_v4_data_foundation.access import DataAccessPolicy,DataPrincipal
from saed_v4_data_foundation.errors import RoleViolation,AccessDenied
@pytest.mark.parametrize('role',[DataRole.LOCKED_FINAL,DataRole.PROSPECTIVE,DataRole.SHADOW,DataRole.MICRO_LIVE,DataRole.LIVE,DataRole.EXTERNAL_ACTUAL])
def test_protected_cannot_train(role):
 with pytest.raises(RoleViolation): assert_role_operation(role,AccessOperation.TRAIN)
def test_synthetic_cannot_promote():
 with pytest.raises(RoleViolation): assert_role_operation(DataRole.SYNTHETIC_STRESS,AccessOperation.PROMOTE)
def test_static_cannot_promote():
 with pytest.raises(RoleViolation): assert_role_operation(DataRole.EXTERNAL_STATIC,AccessOperation.PROMOTE)
def test_development_can_train(): assert_role_operation(DataRole.DEVELOPMENT,AccessOperation.TRAIN) is None
def test_backward_flow_rejected():
 with pytest.raises(RoleViolation): assert_derivation_flow(DataRole.LOCKED_FINAL,DataRole.DEVELOPMENT)
def test_forward_flow_allowed(): assert_derivation_flow(DataRole.DEVELOPMENT,DataRole.LOCKED_FINAL) is None
def test_access_allow():
 p=DataPrincipal('r',(DataRole.DEVELOPMENT,),(AccessOperation.TRAIN,)); assert DataAccessPolicy().authorize(p,DataRole.DEVELOPMENT,AccessOperation.TRAIN)
def test_access_principal_denied():
 p=DataPrincipal('r',(DataRole.DEVELOPMENT,),(AccessOperation.READ,))
 with pytest.raises(AccessDenied): DataAccessPolicy().authorize(p,DataRole.DEVELOPMENT,AccessOperation.TRAIN)
def test_access_role_policy_denied():
 p=DataPrincipal('r',(DataRole.LIVE,),(AccessOperation.TRAIN,))
 with pytest.raises(AccessDenied): DataAccessPolicy().authorize(p,DataRole.LIVE,AccessOperation.TRAIN)
