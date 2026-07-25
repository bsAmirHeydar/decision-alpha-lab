from __future__ import annotations
from .enums import DataRole,AccessOperation
from .errors import RoleViolation
PROTECTED={DataRole.LOCKED_FINAL,DataRole.PROSPECTIVE,DataRole.SHADOW,DataRole.MICRO_LIVE,DataRole.LIVE,DataRole.EXTERNAL_ACTUAL}
TRAINABLE={DataRole.DEVELOPMENT}
CALIBRATABLE={DataRole.CALIBRATION}
SELECTABLE={DataRole.SELECTION_VALIDATION}
def assert_role_operation(role:DataRole,operation:AccessOperation)->None:
    if operation in {AccessOperation.TRAIN,AccessOperation.TUNE} and role not in TRAINABLE: raise RoleViolation(f'{role.value} cannot {operation.value}')
    if operation==AccessOperation.CALIBRATE and role not in CALIBRATABLE: raise RoleViolation(f'{role.value} cannot calibrate')
    if operation==AccessOperation.SELECT and role not in SELECTABLE: raise RoleViolation(f'{role.value} cannot select')
    if operation==AccessOperation.PROMOTE and role in {DataRole.SYNTHETIC_STRESS,DataRole.EXTERNAL_STATIC}: raise RoleViolation(f'{role.value} cannot positively promote')
def assert_derivation_flow(source:DataRole,target:DataRole)->None:
    order=[DataRole.DEVELOPMENT,DataRole.CALIBRATION,DataRole.SELECTION_VALIDATION,DataRole.LOCKED_FINAL,DataRole.PROSPECTIVE,DataRole.SHADOW,DataRole.MICRO_LIVE,DataRole.LIVE]
    if source in order and target in order and order.index(target)<order.index(source): raise RoleViolation('evidence cannot flow backward to a less protected role')
    if source in PROTECTED and target in {DataRole.DEVELOPMENT,DataRole.CALIBRATION,DataRole.SELECTION_VALIDATION}: raise RoleViolation('protected evidence cannot flow into adaptive roles')
