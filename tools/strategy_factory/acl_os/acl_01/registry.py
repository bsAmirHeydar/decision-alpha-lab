from __future__ import annotations
from dataclasses import dataclass,field,asdict
from datetime import datetime,timezone
from typing import Any
from .canonical import digest_object
from .compatibility import CompatibilityRequirement,CompatibilityResolver
from .dependency import DependencyEdge,DependencyGraph
from .errors import RegistryError
from .identity import artifact_base
from .lineage import LineageEdge,LineageGraph
from .migrations import MigrationPlan,MigrationRegistry
from .ownership import OwnershipEvaluator
from .path_policy import PathPolicy
from .types import ArtifactDescriptor,Reason,RegistryStatus,RegistryMutationPermit
from ..acl_00.catalogs import PolicyBundle as ACL00PolicyBundle

@dataclass(slots=True)
class RepositoryRegistry:
    policies:Any
    artifacts:dict[str,ArtifactDescriptor]=field(default_factory=dict)
    aliases:dict[str,str]=field(default_factory=dict)
    owners:dict[str,dict]=field(default_factory=dict)
    schemas:dict[str,dict]=field(default_factory=dict)
    plugins:dict[str,dict]=field(default_factory=dict)
    dependencies:list[DependencyEdge]=field(default_factory=list)
    lineage:list[LineageEdge]=field(default_factory=list)
    migrations:list[MigrationPlan]=field(default_factory=list)
    revision:int=0
    paths:Any=field(init=False,repr=False)
    ownership:Any=field(init=False,repr=False)
    compat:Any=field(init=False,repr=False)
    dep_graph:Any=field(init=False,repr=False)
    lineage_graph:Any=field(init=False,repr=False)
    migration_registry:Any=field(init=False,repr=False)

    def __post_init__(self):
        self.paths=PathPolicy(self.policies); self.ownership=OwnershipEvaluator(self.policies); self.compat=CompatibilityResolver(self.policies); self.dep_graph=DependencyGraph(self.policies); self.lineage_graph=LineageGraph(self.policies); self.migration_registry=MigrationRegistry(self.policies)

    @property
    def digest(self)->str: return digest_object(self.snapshot())

    def snapshot(self)->dict:
        return {"schema_version":"1.0.0","revision":self.revision,"artifacts":{k:v.to_dict() for k,v in sorted(self.artifacts.items())},"aliases":dict(sorted(self.aliases.items())),"owners":dict(sorted(self.owners.items())),"schemas":dict(sorted(self.schemas.items())),"plugins":dict(sorted(self.plugins.items())),"dependencies":[x.to_dict() for x in sorted(self.dependencies,key=lambda e:(e.source_artifact_id,e.target_artifact_id,e.dependency_type))],"lineage":[x.to_dict() for x in sorted(self.lineage,key=lambda e:e.edge_id)],"migrations":[asdict(x) for x in sorted(self.migrations,key=lambda p:p.migration_id)],"live_order_submission_allowed":False,"capital_activation_allowed":False}

    def validate_permit(self,permit:RegistryMutationPermit,action:str,tenant_id:str,subject_id:str,now:datetime|None=None)->list[Reason]:
        now=(now or datetime.now(timezone.utc)).astimezone(timezone.utc); reasons=[]
        if permit.decision!="ALLOW": reasons.append(Reason("ACL00_DECISION_NOT_ALLOW","ACL-00 permit does not allow mutation.",{}))
        try:
            expected_policy_digest=ACL00PolicyBundle.load().digest
            if permit.policy_digest!=expected_policy_digest: reasons.append(Reason("ACL00_POLICY_DIGEST_MISMATCH","ACL-00 permit is bound to a non-current policy bundle.",{"expected":expected_policy_digest,"actual":permit.policy_digest}))
        except Exception as exc:
            reasons.append(Reason("ACL00_POLICY_UNAVAILABLE","ACL-00 policy bundle could not be loaded.",{"error":str(exc)}))
        if permit.action!=action: reasons.append(Reason("ACL00_ACTION_MISMATCH","ACL-00 permit action mismatch.",{"expected":action,"actual":permit.action}))
        if permit.tenant_id!=tenant_id: reasons.append(Reason("ACL00_TENANT_MISMATCH","ACL-00 permit tenant mismatch.",{}))
        if permit.subject_artifact_id not in {subject_id,"al://system/acl-os/repository-registry@1.0.0"}: reasons.append(Reason("ACL00_SUBJECT_MISMATCH","ACL-00 permit subject mismatch.",{}))
        if permit.issued_at>now: reasons.append(Reason("ACL00_PERMIT_NOT_YET_VALID","ACL-00 permit is not yet valid.",{}))
        if permit.expires_at<=now: reasons.append(Reason("ACL00_PERMIT_EXPIRED","ACL-00 permit is expired.",{}))
        if permit.live_order_submission_allowed or permit.capital_activation_allowed: reasons.append(Reason("ILLEGAL_LIVE_AUTHORITY_CLAIM","Repository permit cannot grant live or capital authority.",{}))
        return reasons

    def register_owner(self,owner_id:str,record:dict,permit:RegistryMutationPermit)->list[Reason]:
        reasons=self.validate_permit(permit,"REGISTER_OWNER",record.get("tenant_id","system"),"al://system/acl-os/repository-registry@1.0.0")
        if owner_id in self.owners: reasons.append(Reason("OWNER_ALREADY_REGISTERED","Owner ID already exists.",{"owner_id":owner_id}))
        if reasons:return reasons
        self.owners[owner_id]=record; self.revision+=1; return []

    def register_schema(self,schema_id:str,record:dict,permit:RegistryMutationPermit)->list[Reason]:
        reasons=self.validate_permit(permit,"REGISTER_SCHEMA",record.get("tenant_id","system"),"al://system/acl-os/repository-registry@1.0.0")
        if schema_id in self.schemas: reasons.append(Reason("SCHEMA_ALREADY_REGISTERED","Schema ID already exists.",{"schema_id":schema_id}))
        if reasons:return reasons
        self.schemas[schema_id]=record; self.revision+=1; return []

    def register_plugin(self,plugin_id:str,record:dict,permit:RegistryMutationPermit)->list[Reason]:
        reasons=self.validate_permit(permit,"REGISTER_PLUGIN",record.get("tenant_id","system"),"al://system/acl-os/repository-registry@1.0.0")
        if plugin_id in self.plugins: reasons.append(Reason("PLUGIN_ALREADY_REGISTERED","Plugin ID already exists.",{"plugin_id":plugin_id}))
        if not record.get("conformance_suite"): reasons.append(Reason("PLUGIN_CONFORMANCE_MISSING","Plugin requires a conformance suite.",{}))
        if reasons:return reasons
        self.plugins[plugin_id]=record; self.revision+=1; return []

    def register_artifact(self,d:ArtifactDescriptor,permit:RegistryMutationPermit)->list[Reason]:
        reasons=self.validate_permit(permit,"REGISTER_ARTIFACT",d.identity.tenant_id,d.identity.artifact_id)
        if d.identity.artifact_id in self.artifacts: reasons.append(Reason("ARTIFACT_ID_ALREADY_REGISTERED","Artifact identity already exists.",{"artifact_id":d.identity.artifact_id}))
        reasons.extend(self.paths.validate(d)); reasons.extend(self.ownership.validate_owner(d.owner_id,self.owners,d.identity.kind))
        if d.schema_id not in self.schemas: reasons.append(Reason("SCHEMA_NOT_REGISTERED","Artifact schema is not registered.",{"schema_id":d.schema_id}))
        kind_spec=self.policies.documents["artifact_kinds"]["kinds"].get(d.identity.kind)
        if not kind_spec: reasons.append(Reason("ARTIFACT_KIND_UNKNOWN","Artifact kind is not registered.",{"kind":d.identity.kind}))
        elif d.layer!=kind_spec["layer"]: reasons.append(Reason("ARTIFACT_LAYER_MISMATCH","Artifact layer does not match kind policy.",{"expected":kind_spec["layer"],"actual":d.layer}))
        reserved=self.policies.documents["reserved_namespaces"].get("namespaces",{})
        if d.identity.namespace in reserved and d.owner_id not in set(reserved[d.identity.namespace].get("allowed_owner_ids",[])): reasons.append(Reason("RESERVED_NAMESPACE_DENIED","Owner cannot publish into reserved namespace.",{}))
        for existing in self.artifacts.values():
            if existing.canonical_path==d.canonical_path: reasons.append(Reason("CANONICAL_PATH_COLLISION","Canonical path is already registered.",{"path":d.canonical_path}))
            if existing.identity.base_id==d.identity.base_id and existing.identity.digest==d.identity.digest and existing.identity.version!=d.identity.version: reasons.append(Reason("VERSION_WITH_IDENTICAL_CONTENT","New version has identical content digest; use alias or metadata revision.",{}))
        for alias in d.aliases:
            if alias in self.aliases or alias in self.artifacts:
                reasons.append(Reason("ALIAS_ALREADY_REGISTERED","Alias collision.",{"alias":alias}))
            if alias==d.identity.artifact_id:
                reasons.append(Reason("ALIAS_SELF_REFERENCE","Alias cannot equal the artifact identity.",{"alias":alias}))
        if len(set(d.aliases))!=len(d.aliases):
            reasons.append(Reason("ALIAS_DUPLICATE_IN_DESCRIPTOR","Descriptor contains duplicate aliases.",{}))
        if reasons:return reasons
        self.artifacts[d.identity.artifact_id]=d
        for alias in d.aliases: self.aliases[alias]=d.identity.artifact_id
        self.revision+=1; return []

    def register_alias(self,alias:str,target_id:str,permit:RegistryMutationPermit)->list[Reason]:
        tenant=self.artifacts[target_id].identity.tenant_id if target_id in self.artifacts else "system"
        reasons=self.validate_permit(permit,"REGISTER_ALIAS",tenant,target_id)
        if alias in self.aliases or alias in self.artifacts: reasons.append(Reason("ALIAS_COLLISION","Alias collides with an existing identity or alias.",{}))
        if target_id not in self.artifacts: reasons.append(Reason("ALIAS_TARGET_UNRESOLVED","Alias target does not exist.",{}))
        if alias==target_id: reasons.append(Reason("ALIAS_SELF_REFERENCE","Alias cannot target itself.",{}))
        if reasons:return reasons
        self.aliases[alias]=target_id; self.revision+=1; return []

    def resolve_alias(self,ref:str)->tuple[str|None,list[Reason]]:
        seen=[]; cur=ref
        while cur in self.aliases:
            if cur in seen: return None,[Reason("ALIAS_CYCLE","Alias cycle detected.",{"cycle":seen+[cur]})]
            seen.append(cur); cur=self.aliases[cur]
        return (cur if cur in self.artifacts else None),([] if cur in self.artifacts else [Reason("ARTIFACT_NOT_FOUND","Artifact or alias was not found.",{"ref":ref})])

    def validate_graphs(self)->list[Reason]:
        return self.dep_graph.validate(self.artifacts,self.dependencies)+self.lineage_graph.validate(self.artifacts,self.lineage)+self.migration_registry.validate(self.migrations)
