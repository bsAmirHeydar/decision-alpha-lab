import pytest
from saed_v4_data_foundation.enums import DataRole,AccessOperation
from saed_v4_data_foundation.partitions import assert_role_operation
from saed_v4_data_foundation.errors import RoleViolation
CASES=[]
for role in DataRole:
 for op in AccessOperation:
  expected=not ((op in {AccessOperation.TRAIN,AccessOperation.TUNE} and role!=DataRole.DEVELOPMENT) or (op==AccessOperation.CALIBRATE and role!=DataRole.CALIBRATION) or (op==AccessOperation.SELECT and role!=DataRole.SELECTION_VALIDATION) or (op==AccessOperation.PROMOTE and role in {DataRole.SYNTHETIC_STRESS,DataRole.EXTERNAL_STATIC}))
  CASES.append((role,op,expected))
@pytest.mark.parametrize('role,op,expected',CASES)
def test_role_operation_matrix(role,op,expected):
 if expected: assert_role_operation(role,op)
 else:
  with pytest.raises(RoleViolation):assert_role_operation(role,op)
