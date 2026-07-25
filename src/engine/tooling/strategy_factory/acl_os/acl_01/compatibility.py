from __future__ import annotations
from dataclasses import dataclass
from .semver import satisfies, highest_satisfying, Version
from .types import ArtifactDescriptor, Reason

@dataclass(frozen=True,slots=True)
class CompatibilityRequirement:
    consumer_artifact_id:str
    provider_base_id:str
    version_constraint:str
    interface_id:str
    interface_version_constraint:str
    required_security_classification:str

class CompatibilityResolver:
    def __init__(self,policies): self.policy=policies.documents["compatibility_policy"]
    def resolve(self,requirement:CompatibilityRequirement,descriptors:dict[str,ArtifactDescriptor])->tuple[ArtifactDescriptor|None,list[Reason]]:
        ranks=self.policy["security_classification_ranks"]
        candidates=[]; reasons=[]
        for d in descriptors.values():
            if d.identity.base_id!=requirement.provider_base_id or d.status.value!="ACTIVE": continue
            if not satisfies(d.identity.version,requirement.version_constraint): continue
            interfaces=d.metadata.get("interfaces",{})
            offered=interfaces.get(requirement.interface_id)
            if not offered or not satisfies(offered,requirement.interface_version_constraint): continue
            if ranks.get(d.security_classification,-1)<ranks.get(requirement.required_security_classification,10**6): continue
            candidates.append(d)
        if not candidates:
            reasons.append(Reason("NO_COMPATIBLE_PROVIDER","No provider satisfies artifact, interface and security constraints.",{"provider_base_id":requirement.provider_base_id,"version_constraint":requirement.version_constraint}))
            return None,reasons
        candidates.sort(key=lambda d:Version.parse(d.identity.version),reverse=True)
        return candidates[0],reasons

    def validate_schema_evolution(self,old:ArtifactDescriptor,new:ArtifactDescriptor)->list[Reason]:
        reasons=[]; ov=Version.parse(old.identity.version); nv=Version.parse(new.identity.version)
        if nv.precedence_key()<=ov.precedence_key(): reasons.append(Reason("VERSION_NOT_MONOTONIC","New version must be greater than previous version.",{}))
        old_schema=old.metadata.get("schema_semver"); new_schema=new.metadata.get("schema_semver")
        if old_schema and new_schema:
            os=Version.parse(old_schema); ns=Version.parse(new_schema)
            breaking=bool(new.metadata.get("breaking_change",False))
            if breaking and ns.major<=os.major: reasons.append(Reason("BREAKING_SCHEMA_WITHOUT_MAJOR","Breaking schema change requires schema major increment.",{}))
            if not breaking and ns.major!=os.major: reasons.append(Reason("UNDECLARED_BREAKING_SCHEMA_CHANGE","Schema major changed without breaking_change declaration.",{}))
        return reasons
