from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from .canonical import digest_object
from .errors import ContractError
from .identity import validate_component, validate_digest, validate_artifact_id
from .semver import Version

class ArtifactMutability(StrEnum):
    AUTHORED="AUTHORED"
    GENERATED="GENERATED"
    IMMUTABLE="IMMUTABLE"
    APPEND_ONLY="APPEND_ONLY"
    EPHEMERAL="EPHEMERAL"

class RegistryStatus(StrEnum):
    ACTIVE="ACTIVE"
    DEPRECATED="DEPRECATED"
    QUARANTINED="QUARANTINED"
    TOMBSTONED="TOMBSTONED"

class ResolutionStatus(StrEnum):
    RESOLVED="RESOLVED"
    NOT_FOUND="NOT_FOUND"
    AMBIGUOUS="AMBIGUOUS"
    INTEGRITY_FAILURE="INTEGRITY_FAILURE"
    POLICY_DENIED="POLICY_DENIED"
    INCOMPATIBLE="INCOMPATIBLE"

@dataclass(frozen=True, slots=True)
class Reason:
    code:str
    message:str
    details:dict[str,Any]=field(default_factory=dict)
    def to_dict(self): return {"code":self.code,"message":self.message,"details":self.details}

@dataclass(frozen=True, slots=True)
class ArtifactIdentity:
    artifact_id:str
    tenant_id:str
    namespace:str
    kind:str
    name:str
    version:str
    digest:str

    def __post_init__(self):
        for label,value in (("tenant_id",self.tenant_id),("namespace",self.namespace),("kind",self.kind),("name",self.name)):
            validate_component(value,label)
        Version.parse(self.version); validate_digest(self.digest); validate_artifact_id(self)

    @property
    def base_id(self)->str:
        return f"al://{self.tenant_id}/{self.namespace}/{self.kind}/{self.name}"

    def to_dict(self):
        return {"artifact_id":self.artifact_id,"tenant_id":self.tenant_id,"namespace":self.namespace,"kind":self.kind,"name":self.name,"version":self.version,"digest":self.digest}

    @classmethod
    def from_dict(cls,obj:dict[str,Any])->"ArtifactIdentity":
        _closed(obj,{"artifact_id","tenant_id","namespace","kind","name","version","digest"},"ArtifactIdentity")
        return cls(**obj)

@dataclass(frozen=True, slots=True)
class ArtifactDescriptor:
    identity:ArtifactIdentity
    zone:str
    canonical_path:str
    layer:str
    owner_id:str
    schema_id:str
    security_classification:str
    mutability:ArtifactMutability
    status:RegistryStatus=RegistryStatus.ACTIVE
    aliases:tuple[str,...]=()
    metadata:dict[str,Any]=field(default_factory=dict)
    authority_decision_ref:str|None=None

    def to_dict(self):
        out={"identity":self.identity.to_dict(),"zone":self.zone,"canonical_path":self.canonical_path,"layer":self.layer,"owner_id":self.owner_id,"schema_id":self.schema_id,"security_classification":self.security_classification,"mutability":self.mutability.value,"status":self.status.value,"aliases":list(self.aliases),"metadata":self.metadata}
        if self.authority_decision_ref: out["authority_decision_ref"]=self.authority_decision_ref
        return out

    @classmethod
    def from_dict(cls,obj:dict[str,Any])->"ArtifactDescriptor":
        _closed(obj,{"identity","zone","canonical_path","layer","owner_id","schema_id","security_classification","mutability","status","aliases","metadata","authority_decision_ref"},"ArtifactDescriptor")
        return cls(ArtifactIdentity.from_dict(obj["identity"]),obj["zone"],obj["canonical_path"],obj["layer"],obj["owner_id"],obj["schema_id"],obj["security_classification"],ArtifactMutability(obj["mutability"]),RegistryStatus(obj.get("status","ACTIVE")),tuple(obj.get("aliases",[])),dict(obj.get("metadata",{})),obj.get("authority_decision_ref"))

@dataclass(frozen=True, slots=True)
class RegistryMutationPermit:
    decision_id:str
    decision:str
    tenant_id:str
    subject_artifact_id:str
    action:str
    policy_digest:str
    issued_at:datetime
    expires_at:datetime
    live_order_submission_allowed:bool=False
    capital_activation_allowed:bool=False

    @classmethod
    def from_dict(cls,obj:dict[str,Any])->"RegistryMutationPermit":
        _closed(obj,{"decision_id","decision","tenant_id","subject_artifact_id","action","policy_digest","issued_at","expires_at","live_order_submission_allowed","capital_activation_allowed"},"RegistryMutationPermit")
        return cls(obj["decision_id"],obj["decision"],obj["tenant_id"],obj["subject_artifact_id"],obj["action"],obj["policy_digest"],_dt(obj["issued_at"]),_dt(obj["expires_at"]),bool(obj.get("live_order_submission_allowed",False)),bool(obj.get("capital_activation_allowed",False)))

    def to_dict(self):
        return {"decision_id":self.decision_id,"decision":self.decision,"tenant_id":self.tenant_id,"subject_artifact_id":self.subject_artifact_id,"action":self.action,"policy_digest":self.policy_digest,"issued_at":self.issued_at.isoformat().replace("+00:00","Z"),"expires_at":self.expires_at.isoformat().replace("+00:00","Z"),"live_order_submission_allowed":self.live_order_submission_allowed,"capital_activation_allowed":self.capital_activation_allowed}

@dataclass(frozen=True, slots=True)
class LocatorResult:
    status:ResolutionStatus
    requested_ref:str
    descriptor:ArtifactDescriptor|None
    reasons:tuple[Reason,...]
    resolved_at:datetime
    registry_digest:str
    verified_digest:bool=False
    live_order_submission_allowed:bool=False
    capital_activation_allowed:bool=False

    def to_dict(self):
        return {"status":self.status.value,"requested_ref":self.requested_ref,"descriptor":self.descriptor.to_dict() if self.descriptor else None,"reasons":[x.to_dict() for x in self.reasons],"resolved_at":self.resolved_at.isoformat().replace("+00:00","Z"),"registry_digest":self.registry_digest,"verified_digest":self.verified_digest,"live_order_submission_allowed":False,"capital_activation_allowed":False}


def _dt(value:str)->datetime:
    out=datetime.fromisoformat(value.replace("Z","+00:00"))
    if out.tzinfo is None: raise ContractError("datetime must be timezone-aware")
    return out.astimezone(timezone.utc)


def _closed(obj:dict[str,Any], allowed:set[str], label:str):
    unknown=set(obj)-allowed
    if unknown: raise ContractError(f"{label} contains unknown fields: {sorted(unknown)}")
