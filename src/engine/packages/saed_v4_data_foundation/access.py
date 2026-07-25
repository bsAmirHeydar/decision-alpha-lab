from __future__ import annotations
from dataclasses import dataclass
from .enums import DataRole,AccessOperation
from .partitions import assert_role_operation
from .errors import AccessDenied,RoleViolation
@dataclass(frozen=True)
class DataPrincipal:
    principal_id:str; allowed_roles:tuple[DataRole,...]; allowed_operations:tuple[AccessOperation,...]
class DataAccessPolicy:
    def authorize(self,principal:DataPrincipal,role:DataRole,operation:AccessOperation)->bool:
        if role not in principal.allowed_roles or operation not in principal.allowed_operations: raise AccessDenied(f'{principal.principal_id} lacks {operation.value} on {role.value}')
        try: assert_role_operation(role,operation)
        except RoleViolation as e: raise AccessDenied(str(e)) from e
        return True
