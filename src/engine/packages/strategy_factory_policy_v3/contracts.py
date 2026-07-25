from __future__ import annotations
import math,re
from dataclasses import dataclass,field,asdict
from typing import Any,Mapping
from .canonical import canonical_sha256,stable_id
from .enums import *
from .errors import PolicyError
_SHA=re.compile(r'^[0-9a-f]{64}$'); _SEMVER=re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$'); _ID=re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:@/-]*$')
def _id(v,n):
    if not isinstance(v,str) or not _ID.match(v): raise PolicyError('invalid_identifier',f'{n} is invalid',{'value':v})
def _hash(v,n):
    if not isinstance(v,str) or not _SHA.match(v): raise PolicyError('invalid_sha256',f'{n} must be lowercase SHA-256')
def _semver(v,n):
    if not isinstance(v,str) or not _SEMVER.match(v): raise PolicyError('invalid_semver',f'{n} must be semantic version')
def _finite(v,n):
    if not math.isfinite(float(v)): raise PolicyError('non_finite_value',f'{n} must be finite')
def _prob(v,n):
    _finite(v,n)
    if not 0<=float(v)<=1: raise PolicyError('invalid_probability',f'{n} must be in [0,1]')

def _distribution(d,n):
    if not d: raise PolicyError('empty_distribution',f'{n} cannot be empty')
    for k,v in d.items(): _id(k,f'{n}.key'); _prob(v,f'{n}.{k}')
    if abs(sum(float(v) for v in d.values())-1.0)>1e-8: raise PolicyError('distribution_not_normalized',f'{n} must sum to one')

@dataclass(frozen=True,slots=True)
class PromotionAdmission:
    admission_id:str; version:str; decision_hash:str; evidence_bundle_hash:str; signature_valid:bool; outcome:str; model_id:str; model_version:str
    context_types:tuple[str,...]; treatments:tuple[str,...]; risk_tiers:tuple[str,...]; actions:tuple[str,...]; valid_from_ms:int; valid_until_ms:int
    capability_flags:tuple[str,...]=(); residual_risks:tuple[str,...]=()
    def __post_init__(self):
        _id(self.admission_id,'admission_id'); _semver(self.version,'version'); _hash(self.decision_hash,'decision_hash'); _hash(self.evidence_bundle_hash,'evidence_bundle_hash'); _id(self.model_id,'model_id'); _semver(self.model_version,'model_version')
        if self.outcome not in ('reject','challenge','promote'): raise PolicyError('invalid_promotion_outcome','outcome invalid')
        if self.valid_until_ms<self.valid_from_ms: raise PolicyError('invalid_admission_horizon','valid_until precedes valid_from')
        for seq,n in ((self.context_types,'context_types'),(self.treatments,'treatments'),(self.risk_tiers,'risk_tiers'),(self.actions,'actions')):
            if not seq: raise PolicyError('empty_support',f'{n} cannot be empty')
            for x in seq:_id(x,n)
    @property
    def admission_hash(self): return canonical_sha256(asdict(self))
    def assert_ai_usable(self,at_ms:int):
        if not self.signature_valid: raise PolicyError('signature_failure','promotion signature is invalid')
        if self.outcome!='promote': raise PolicyError('model_not_promoted','AI nodes require promote outcome',{'outcome':self.outcome})
        if not self.valid_from_ms<=at_ms<=self.valid_until_ms: raise PolicyError('promotion_expired','promotion admission is outside validity horizon')

@dataclass(frozen=True,slots=True)
class Predicate:
    field:str; operator:str; value:Any
    def __post_init__(self):
        _id(self.field,'field')
        if self.operator not in ('eq','ne','gt','ge','lt','le','in','not_in','exists','between'): raise PolicyError('unsupported_operator','predicate operator unsupported')

@dataclass(frozen=True,slots=True)
class ExceptionRule:
    rule_id:str; when:tuple[Predicate,...]; action:Action|None=None; treatment:str|None=None; risk_tier:str|None=None; veto:bool=False; note:str=''
    def __post_init__(self):
        _id(self.rule_id,'rule_id')
        if not self.when: raise PolicyError('empty_exception_rule','exception rule requires predicates')
        if self.treatment is not None:_id(self.treatment,'treatment')
        if self.risk_tier is not None:_id(self.risk_tier,'risk_tier')

@dataclass(frozen=True,slots=True)
class ManualPolicyDefinition:
    setup_id:str; version:str; context_type:str; eligibility:tuple[Predicate,...]; action:Action; treatment:str; risk_tier:str
    vetoes:tuple[Predicate,...]=(); exceptions:tuple[ExceptionRule,...]=(); operator_notes:str=''; valid_from_ms:int=0; valid_until_ms:int=2**63-1
    def __post_init__(self):
        _id(self.setup_id,'setup_id'); _semver(self.version,'version'); _id(self.context_type,'context_type'); _id(self.treatment,'treatment'); _id(self.risk_tier,'risk_tier')
        if not self.eligibility: raise PolicyError('empty_manual_eligibility','manual policy requires eligibility predicates')
        if self.valid_until_ms<self.valid_from_ms: raise PolicyError('invalid_manual_horizon','manual validity horizon inverted')
    @property
    def policy_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class ContextOccurrence:
    occurrence_id:str; context_type:str; known_time_ms:int; feature_time_ms:int; features:Mapping[str,Any]; views_present:tuple[str,...]
    available_treatments:tuple[str,...]; available_risk_tiers:tuple[str,...]; candidate_actions:tuple[str,...]; metadata:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        _id(self.occurrence_id,'occurrence_id'); _id(self.context_type,'context_type')
        if self.feature_time_ms>self.known_time_ms: raise PolicyError('future_feature_time','feature time exceeds known time')
        if not self.features: raise PolicyError('empty_features','features cannot be empty')
        for seq,n in ((self.views_present,'views_present'),(self.available_treatments,'available_treatments'),(self.available_risk_tiers,'available_risk_tiers'),(self.candidate_actions,'candidate_actions')):
            for x in seq:_id(x,n)
    @property
    def occurrence_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class ManualDecision:
    eligible:bool; action:Action; treatment:str|None; risk_tier:str|None; vetoed:bool; matched_exceptions:tuple[str,...]; reasons:tuple[str,...]; policy_hash:str
    def __post_init__(self): _hash(self.policy_hash,'policy_hash')
    @property
    def decision_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class ModelOutput:
    model_id:str; model_version:str; occurrence_id:str; as_of_ms:int; valid_until_ms:int; action_probabilities:Mapping[str,float]; utility:float; rank_score:float
    treatment_distribution:Mapping[str,float]; risk_distribution:Mapping[str,float]; survival_probability:float; tail_loss_probability:float; uncertainty:float; novelty:float
    calibration_state:CalibrationState; required_views:tuple[str,...]; feature_hash:str; output_schema_version:str='1.0.0'; diagnostics:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        _id(self.model_id,'model_id'); _semver(self.model_version,'model_version'); _id(self.occurrence_id,'occurrence_id'); _semver(self.output_schema_version,'output_schema_version'); _hash(self.feature_hash,'feature_hash')
        if self.valid_until_ms<self.as_of_ms: raise PolicyError('invalid_model_horizon','model horizon inverted')
        _distribution(self.action_probabilities,'action_probabilities'); _distribution(self.treatment_distribution,'treatment_distribution'); _distribution(self.risk_distribution,'risk_distribution')
        for n in ('utility','rank_score'): _finite(getattr(self,n),n)
        for n in ('survival_probability','tail_loss_probability','uncertainty','novelty'): _prob(getattr(self,n),n)
    @property
    def output_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class FallbackRule:
    reason:FallbackReason; action:FallbackAction; note:str=''
@dataclass(frozen=True,slots=True)
class FallbackPolicy:
    policy_id:str; version:str; rules:tuple[FallbackRule,...]; default_action:FallbackAction=FallbackAction.ABSTAIN
    def __post_init__(self):
        _id(self.policy_id,'policy_id'); _semver(self.version,'version')
        reasons=[r.reason for r in self.rules]
        if len(set(reasons))!=len(reasons): raise PolicyError('duplicate_fallback_reason','fallback reasons must be unique')
    @property
    def policy_hash(self): return canonical_sha256(asdict(self))
    def action_for(self,reason:FallbackReason)->FallbackAction:
        return next((r.action for r in self.rules if r.reason is reason),self.default_action)

@dataclass(frozen=True,slots=True)
class AuthorityRule:
    conflict:str; winner:Authority; losers:tuple[Authority,...]; disposition:ConflictDisposition; hard_veto:bool=False
    def __post_init__(self): _id(self.conflict,'conflict')
@dataclass(frozen=True,slots=True)
class AuthorityMatrix:
    matrix_id:str; version:str; rules:tuple[AuthorityRule,...]; precedence:tuple[Authority,...]
    def __post_init__(self):
        _id(self.matrix_id,'matrix_id'); _semver(self.version,'version')
        if len(set(self.precedence))!=len(self.precedence): raise PolicyError('duplicate_authority','authority precedence contains duplicates')
        if set(self.precedence)!=set(Authority): raise PolicyError('incomplete_authority_matrix','every authority must be ordered')
    @property
    def matrix_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class OperatorOverride:
    override_id:str; occurrence_id:str; kind:OverrideKind; operator_id:str; reason:str; issued_at_ms:int; expires_at_ms:int; signature_hash:str
    def __post_init__(self):
        for n in ('override_id','occurrence_id','operator_id'):_id(getattr(self,n),n)
        _hash(self.signature_hash,'signature_hash')
        if not self.reason.strip(): raise PolicyError('missing_override_reason','override reason required')
        if self.expires_at_ms<self.issued_at_ms: raise PolicyError('invalid_override_horizon','override horizon inverted')

@dataclass(frozen=True,slots=True)
class PolicyNodeSpec:
    node_id:str; kind:NodeKind; dependencies:tuple[str,...]; authority:Authority; config:Mapping[str,Any]=field(default_factory=dict)
    def __post_init__(self):
        _id(self.node_id,'node_id')
        for d in self.dependencies:_id(d,'dependency')
        if self.node_id in self.dependencies: raise PolicyError('self_dependency','node cannot depend on itself')
    @property
    def node_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class PolicyGraphSpec:
    graph_id:str; version:str; mode:PolicyMode; nodes:tuple[PolicyNodeSpec,...]; output_node_id:str; manual_policy_hash:str; fallback_policy_hash:str; authority_matrix_hash:str
    supported_context_types:tuple[str,...]; supported_treatments:tuple[str,...]; supported_risk_tiers:tuple[str,...]; supported_actions:tuple[str,...]; admission_hash:str|None=None
    def __post_init__(self):
        _id(self.graph_id,'graph_id'); _semver(self.version,'version'); _id(self.output_node_id,'output_node_id')
        for n in ('manual_policy_hash','fallback_policy_hash','authority_matrix_hash'):_hash(getattr(self,n),n)
        if self.admission_hash is not None:_hash(self.admission_hash,'admission_hash')
        if not self.nodes: raise PolicyError('empty_policy_graph','policy graph cannot be empty')
    @property
    def graph_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class PolicyDecision:
    decision_id:str; occurrence_id:str; status:DecisionStatus; action:Action; treatment:str|None; risk_tier:str|None; score:float|None; reasons:tuple[str,...]
    trace:tuple[Mapping[str,Any],...]; fallback_used:FallbackAction|None; decisive_authority:Authority; graph_hash:str; manual_decision_hash:str; model_output_hash:str|None; known_time_ms:int
    def __post_init__(self):
        _id(self.decision_id,'decision_id'); _id(self.occurrence_id,'occurrence_id'); _hash(self.graph_hash,'graph_hash'); _hash(self.manual_decision_hash,'manual_decision_hash')
        if self.model_output_hash is not None:_hash(self.model_output_hash,'model_output_hash')
        if self.score is not None:_finite(self.score,'score')
    @property
    def decision_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class AttributionOpportunity:
    opportunity_id:str; manual_selected:bool; hybrid_selected:bool; manual_value:float; hybrid_value:float; treatment_changed:bool=False; risk_changed:bool=False; timing_delta:float=0.0
    def __post_init__(self):
        _id(self.opportunity_id,'opportunity_id')
        for n in ('manual_value','hybrid_value','timing_delta'):_finite(getattr(self,n),n)
@dataclass(frozen=True,slots=True)
class IncrementalValueReport:
    report_id:str; opportunity_count:int; manual_total:float; hybrid_total:float; incremental_total:float; components:Mapping[str,float]; paired_win_rate:float; evidence_hash:str
    def __post_init__(self):
        _id(self.report_id,'report_id'); _hash(self.evidence_hash,'evidence_hash'); _prob(self.paired_win_rate,'paired_win_rate')
        if self.opportunity_count<1: raise PolicyError('empty_attribution','attribution requires opportunities')
