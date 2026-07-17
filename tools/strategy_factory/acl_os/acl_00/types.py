from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Iterable

class Decision(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    WAIVE = "WAIVE"

class LifecycleState(StrEnum):
    DRAFT_CONTEXT = "DRAFT_CONTEXT"
    SEMANTICALLY_VALIDATED = "SEMANTICALLY_VALIDATED"
    CONTEXT_COMPILED = "CONTEXT_COMPILED"
    REPLAY_VALIDATED = "REPLAY_VALIDATED"
    OCCURRENCE_DATASET_READY = "OCCURRENCE_DATASET_READY"
    SETUP_UNIVERSE_READY = "SETUP_UNIVERSE_READY"
    BATCH_REGISTERED = "BATCH_REGISTERED"
    RESEARCH_RUNNING = "RESEARCH_RUNNING"
    EVIDENCE_COMPLETE = "EVIDENCE_COMPLETE"
    STATISTICALLY_ELIGIBLE = "STATISTICALLY_ELIGIBLE"
    RUNTIME_COMPATIBLE = "RUNTIME_COMPATIBLE"
    PAPER_CHALLENGER = "PAPER_CHALLENGER"
    SHADOW_CHALLENGER = "SHADOW_CHALLENGER"
    MICRO_LIVE_ELIGIBLE = "MICRO_LIVE_ELIGIBLE"
    CHAMPION = "CHAMPION"
    SUSPENDED = "SUSPENDED"
    RETIRED = "RETIRED"

class EvidenceClass(StrEnum):
    OBSERVED = "OBSERVED"
    DERIVED = "DERIVED"
    ESTIMATED = "ESTIMATED"
    SYNTHETIC = "SYNTHETIC"
    PROSPECTIVE = "PROSPECTIVE"
    OPERATIONAL = "OPERATIONAL"
    AUTHORIZATION = "AUTHORIZATION"

class ApprovalDisposition(StrEnum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    ABSTAIN = "ABSTAIN"

class SecurityStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    DEGRADED = "DEGRADED"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class Severity(StrEnum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass(frozen=True, slots=True)
class ArtifactRef:
    artifact_id: str
    version: str
    digest: str
    locator: str | None = None

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> "ArtifactRef":
        _closed(obj, {"artifact_id", "version", "digest", "locator"}, "ArtifactRef")
        return cls(str(obj["artifact_id"]), str(obj["version"]), str(obj["digest"]), obj.get("locator"))

    def to_dict(self) -> dict[str, Any]:
        out={"artifact_id":self.artifact_id,"version":self.version,"digest":self.digest}
        if self.locator is not None: out["locator"]=self.locator
        return out

@dataclass(frozen=True, slots=True)
class Actor:
    actor_id: str
    roles: tuple[str, ...]
    tenant_id: str
    authentication_strength: str = "MFA"
    service_identity: bool = False
    attributes: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> "Actor":
        _closed(obj,{"actor_id","roles","tenant_id","authentication_strength","service_identity","attributes"},"Actor")
        roles=tuple(sorted({str(x) for x in obj.get("roles",[])}))
        return cls(str(obj["actor_id"]),roles,str(obj["tenant_id"]),str(obj.get("authentication_strength","MFA")),bool(obj.get("service_identity",False)),dict(obj.get("attributes",{})))

    def to_dict(self)->dict[str,Any]:
        return {"actor_id":self.actor_id,"roles":list(self.roles),"tenant_id":self.tenant_id,"authentication_strength":self.authentication_strength,"service_identity":self.service_identity,"attributes":dict(sorted(self.attributes.items()))}

@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    evidence_class: EvidenceClass
    subject_ref: ArtifactRef
    artifact_ref: ArtifactRef
    claims: tuple[str, ...]
    observed_at: datetime
    known_at: datetime
    environment: str
    immutable: bool = True
    producer: str = ""

    @classmethod
    def from_dict(cls,obj:dict[str,Any])->"EvidenceRecord":
        _closed(obj,{"evidence_id","evidence_class","subject_ref","artifact_ref","claims","observed_at","known_at","environment","immutable","producer"},"EvidenceRecord")
        return cls(str(obj["evidence_id"]),EvidenceClass(obj["evidence_class"]),ArtifactRef.from_dict(obj["subject_ref"]),ArtifactRef.from_dict(obj["artifact_ref"]),tuple(str(x) for x in obj.get("claims",[])),parse_time(obj["observed_at"]),parse_time(obj["known_at"]),str(obj["environment"]),bool(obj.get("immutable",True)),str(obj.get("producer","")))

    def to_dict(self)->dict[str,Any]:
        return {"evidence_id":self.evidence_id,"evidence_class":self.evidence_class.value,"subject_ref":self.subject_ref.to_dict(),"artifact_ref":self.artifact_ref.to_dict(),"claims":list(self.claims),"observed_at":fmt_time(self.observed_at),"known_at":fmt_time(self.known_at),"environment":self.environment,"immutable":self.immutable,"producer":self.producer}

@dataclass(frozen=True, slots=True)
class ApprovalRecord:
    approval_id: str
    transition_id: str
    approver: Actor
    role: str
    disposition: ApprovalDisposition
    approved_at: datetime
    expires_at: datetime
    request_digest: str
    signature: str
    reason_code: str

    @classmethod
    def from_dict(cls,obj:dict[str,Any])->"ApprovalRecord":
        _closed(obj,{"approval_id","transition_id","approver","role","disposition","approved_at","expires_at","request_digest","signature","reason_code"},"ApprovalRecord")
        return cls(str(obj["approval_id"]),str(obj["transition_id"]),Actor.from_dict(obj["approver"]),str(obj["role"]),ApprovalDisposition(obj["disposition"]),parse_time(obj["approved_at"]),parse_time(obj["expires_at"]),str(obj["request_digest"]),str(obj["signature"]),str(obj["reason_code"]))

    def to_dict(self)->dict[str,Any]:
        return {"approval_id":self.approval_id,"transition_id":self.transition_id,"approver":self.approver.to_dict(),"role":self.role,"disposition":self.disposition.value,"approved_at":fmt_time(self.approved_at),"expires_at":fmt_time(self.expires_at),"request_digest":self.request_digest,"signature":self.signature,"reason_code":self.reason_code}

@dataclass(frozen=True, slots=True)
class SecurityControlResult:
    control_id: str
    status: SecurityStatus
    severity: Severity
    evaluated_at: datetime
    expires_at: datetime
    evaluator: str
    subject_ref: ArtifactRef
    evidence_refs: tuple[ArtifactRef,...] = ()
    reason_code: str = "PASS"

    @classmethod
    def from_dict(cls,obj:dict[str,Any])->"SecurityControlResult":
        _closed(obj,{"control_id","status","severity","evaluated_at","expires_at","evaluator","subject_ref","evidence_refs","reason_code"},"SecurityControlResult")
        return cls(str(obj["control_id"]),SecurityStatus(obj["status"]),Severity(obj["severity"]),parse_time(obj["evaluated_at"]),parse_time(obj["expires_at"]),str(obj["evaluator"]),ArtifactRef.from_dict(obj["subject_ref"]),tuple(ArtifactRef.from_dict(x) for x in obj.get("evidence_refs",[])),str(obj.get("reason_code","PASS")))

    def to_dict(self)->dict[str,Any]:
        return {"control_id":self.control_id,"status":self.status.value,"severity":self.severity.value,"evaluated_at":fmt_time(self.evaluated_at),"expires_at":fmt_time(self.expires_at),"evaluator":self.evaluator,"subject_ref":self.subject_ref.to_dict(),"evidence_refs":[x.to_dict() for x in self.evidence_refs],"reason_code":self.reason_code}

@dataclass(frozen=True, slots=True)
class WaiverRecord:
    waiver_id: str
    transition_id: str
    waived_policy_ids: tuple[str,...]
    subject_ref: ArtifactRef
    issued_by: Actor
    issued_at: datetime
    expires_at: datetime
    compensating_controls: tuple[str,...]
    approvals: tuple[ApprovalRecord,...]
    signature: str

    @classmethod
    def from_dict(cls,obj:dict[str,Any])->"WaiverRecord":
        _closed(obj,{"waiver_id","transition_id","waived_policy_ids","subject_ref","issued_by","issued_at","expires_at","compensating_controls","approvals","signature"},"WaiverRecord")
        return cls(str(obj["waiver_id"]),str(obj["transition_id"]),tuple(str(x) for x in obj.get("waived_policy_ids",[])),ArtifactRef.from_dict(obj["subject_ref"]),Actor.from_dict(obj["issued_by"]),parse_time(obj["issued_at"]),parse_time(obj["expires_at"]),tuple(str(x) for x in obj.get("compensating_controls",[])),tuple(ApprovalRecord.from_dict(x) for x in obj.get("approvals",[])),str(obj["signature"]))

    def to_dict(self)->dict[str,Any]:
        return {"waiver_id":self.waiver_id,"transition_id":self.transition_id,"waived_policy_ids":list(self.waived_policy_ids),"subject_ref":self.subject_ref.to_dict(),"issued_by":self.issued_by.to_dict(),"issued_at":fmt_time(self.issued_at),"expires_at":fmt_time(self.expires_at),"compensating_controls":list(self.compensating_controls),"approvals":[x.to_dict() for x in self.approvals],"signature":self.signature}

@dataclass(frozen=True, slots=True)
class TransitionRequest:
    schema_version: str
    transition_id: str
    subject_ref: ArtifactRef
    tenant_id: str
    from_state: LifecycleState
    to_state: LifecycleState
    requested_by: Actor
    requested_at: datetime
    expected_revision: int
    evidence_ids: tuple[str,...]
    rationale: str
    claim_requested: str
    metadata: dict[str,Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls,obj:dict[str,Any])->"TransitionRequest":
        _closed(obj,{"schema_version","transition_id","subject_ref","tenant_id","from_state","to_state","requested_by","requested_at","expected_revision","evidence_ids","rationale","claim_requested","metadata"},"TransitionRequest")
        return cls(str(obj["schema_version"]),str(obj["transition_id"]),ArtifactRef.from_dict(obj["subject_ref"]),str(obj["tenant_id"]),LifecycleState(obj["from_state"]),LifecycleState(obj["to_state"]),Actor.from_dict(obj["requested_by"]),parse_time(obj["requested_at"]),int(obj["expected_revision"]),tuple(str(x) for x in obj.get("evidence_ids",[])),str(obj["rationale"]),str(obj["claim_requested"]),dict(obj.get("metadata",{})))

    def to_dict(self)->dict[str,Any]:
        return {"schema_version":self.schema_version,"transition_id":self.transition_id,"subject_ref":self.subject_ref.to_dict(),"tenant_id":self.tenant_id,"from_state":self.from_state.value,"to_state":self.to_state.value,"requested_by":self.requested_by.to_dict(),"requested_at":fmt_time(self.requested_at),"expected_revision":self.expected_revision,"evidence_ids":list(self.evidence_ids),"rationale":self.rationale,"claim_requested":self.claim_requested,"metadata":self.metadata}

@dataclass(frozen=True, slots=True)
class Reason:
    code: str
    message: str
    policy_id: str | None = None
    waivable: bool = False
    details: dict[str,Any] = field(default_factory=dict)
    def to_dict(self)->dict[str,Any]:
        out={"code":self.code,"message":self.message,"waivable":self.waivable,"details":self.details}
        if self.policy_id: out["policy_id"]=self.policy_id
        return out

@dataclass(frozen=True, slots=True)
class TransitionDecision:
    schema_version: str
    decision_id: str
    transition_id: str
    subject_ref: ArtifactRef
    from_state: LifecycleState
    to_state: LifecycleState
    decision: Decision
    reasons: tuple[Reason,...]
    applied_waiver_ids: tuple[str,...]
    evidence_ids: tuple[str,...]
    approval_ids: tuple[str,...]
    security_control_ids: tuple[str,...]
    decided_at: datetime
    policy_bundle_digest: str
    allowed_next_actions: tuple[str,...]
    resulting_revision: int
    capital_activation_allowed: bool = False
    live_order_submission_allowed: bool = False

    def to_dict(self)->dict[str,Any]:
        return {"schema_version":self.schema_version,"decision_id":self.decision_id,"transition_id":self.transition_id,"subject_ref":self.subject_ref.to_dict(),"from_state":self.from_state.value,"to_state":self.to_state.value,"decision":self.decision.value,"reasons":[x.to_dict() for x in self.reasons],"applied_waiver_ids":list(self.applied_waiver_ids),"evidence_ids":list(self.evidence_ids),"approval_ids":list(self.approval_ids),"security_control_ids":list(self.security_control_ids),"decided_at":fmt_time(self.decided_at),"policy_bundle_digest":self.policy_bundle_digest,"allowed_next_actions":list(self.allowed_next_actions),"resulting_revision":self.resulting_revision,"capital_activation_allowed":self.capital_activation_allowed,"live_order_submission_allowed":self.live_order_submission_allowed}


def parse_time(value:str|datetime)->datetime:
    if isinstance(value,datetime): dt=value
    else: dt=datetime.fromisoformat(str(value).replace("Z","+00:00"))
    if dt.tzinfo is None: raise ValueError("timestamp must be timezone-aware")
    return dt.astimezone(timezone.utc)

def fmt_time(value:datetime)->str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00","Z")

def _closed(obj:dict[str,Any],allowed:set[str],name:str)->None:
    if not isinstance(obj,dict): raise TypeError(f"{name} must be an object")
    unknown=set(obj)-allowed
    if unknown: raise ValueError(f"{name} unknown fields: {sorted(unknown)}")
