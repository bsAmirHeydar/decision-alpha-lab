from __future__ import annotations
from .types import Reason

class OwnershipEvaluator:
    def __init__(self,policies): self.policy=policies.documents["ownership_policy"]
    def validate_owner(self,owner_id:str,owners:dict,artifact_kind:str)->list[Reason]:
        if owner_id not in owners: return [Reason("OWNER_NOT_REGISTERED","Artifact owner is not registered.",{"owner_id":owner_id})]
        owner=owners[owner_id]; reasons=[]
        required=set(self.policy.get("required_roles_by_kind",{}).get(artifact_kind,[]))
        roles=set(owner.get("roles",[]))
        if not required<=roles: reasons.append(Reason("OWNER_ROLE_INSUFFICIENT","Owner lacks required artifact roles.",{"missing":sorted(required-roles)}))
        if owner.get("status")!="ACTIVE": reasons.append(Reason("OWNER_INACTIVE","Artifact owner is not active.",{"status":owner.get("status")}))
        return reasons
