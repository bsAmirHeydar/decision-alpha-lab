from __future__ import annotations
import math,re
from dataclasses import dataclass,field,asdict
from typing import Mapping,Any
from .canonical import canonical_sha256
from .enums import *
from .errors import PortfolioError
SHA=re.compile(r'^[0-9a-f]{64}$'); SEMVER=re.compile(r'^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$'); IDENT=re.compile(r'^[A-Za-z0-9][A-Za-z0-9._:@/-]*$')
def _id(v,n):
    if not isinstance(v,str) or not IDENT.fullmatch(v): raise PortfolioError('invalid_identifier',f'{n} invalid',{'value':v})
def _hash(v,n):
    if not isinstance(v,str) or not SHA.fullmatch(v): raise PortfolioError('invalid_hash',f'{n} must be lowercase sha256')
def _ver(v,n='version'):
    if not isinstance(v,str) or not SEMVER.fullmatch(v): raise PortfolioError('invalid_semver',f'{n} invalid')
def _finite(v,n,lo=None,hi=None):
    if not math.isfinite(float(v)): raise PortfolioError('non_finite',f'{n} must be finite')
    if lo is not None and v<lo: raise PortfolioError('below_minimum',f'{n} below minimum')
    if hi is not None and v>hi: raise PortfolioError('above_maximum',f'{n} above maximum')
def _uniq(vals,n,allow_empty=False):
    if (not vals and not allow_empty) or len(vals)!=len(set(vals)): raise PortfolioError('invalid_unique_list',f'{n} must be unique'+('' if allow_empty else ' and non-empty'))

@dataclass(frozen=True,slots=True)
class CalibrationEvidence:
    context_id:str; version:str; evidence_hash:str; status:GateStatus; expected_calibration_error:float; sample_count:int
    def __post_init__(self):
        _id(self.context_id,'context_id');_ver(self.version);_hash(self.evidence_hash,'evidence_hash');_finite(self.expected_calibration_error,'expected_calibration_error',0,1)
        if self.sample_count<1: raise PortfolioError('insufficient_calibration_samples','sample_count must be positive')

@dataclass(frozen=True,slots=True)
class PromotionEvidence:
    context_id:str; policy_hash:str; status:PromotionStatus; signature_hash:str; prospective_complete:bool
    def __post_init__(self):
        _id(self.context_id,'context_id');_hash(self.policy_hash,'policy_hash');_hash(self.signature_hash,'signature_hash')
        if self.status is PromotionStatus.PROMOTE and not self.prospective_complete: raise PortfolioError('promotion_without_prospective','promoted context requires prospective completion')

@dataclass(frozen=True,slots=True)
class OpportunityCandidate:
    candidate_id:str; occurrence_id:str; context_id:str; context_version:str; known_time_ms:int; expires_at_ms:int; symbol:str; currency:str; session_id:str; anatomy_id:str; cluster_id:str; side:Side; utility_mean:float; uncertainty:float; novelty:float; liquidity_score:float; expected_return:float; expected_loss:float; requested_risk:float; capacity_units:float; turnover_cost:float; promotion:PromotionEvidence; calibration:CalibrationEvidence; feature_hash:str; policy_hash:str
    def __post_init__(self):
        for n in ('candidate_id','occurrence_id','context_id','symbol','currency','session_id','anatomy_id','cluster_id'): _id(getattr(self,n),n)
        _ver(self.context_version,'context_version')
        for n in ('feature_hash','policy_hash'): _hash(getattr(self,n),n)
        if self.promotion.context_id!=self.context_id or self.calibration.context_id!=self.context_id: raise PortfolioError('context_evidence_mismatch','candidate evidence context mismatch')
        if self.promotion.status is not PromotionStatus.PROMOTE: raise PortfolioError('context_not_promoted','candidate context is not promoted')
        if self.calibration.status is not GateStatus.PASS: raise PortfolioError('calibration_not_passed','candidate calibration is not accepted')
        if self.known_time_ms<0 or self.expires_at_ms<=self.known_time_ms: raise PortfolioError('invalid_time_window','expiry must be after known time')
        for n in ('utility_mean','uncertainty','novelty','liquidity_score','expected_return','expected_loss','requested_risk','capacity_units','turnover_cost'): _finite(getattr(self,n),n,0)
        for n in ('novelty','liquidity_score'): _finite(getattr(self,n),n,0,1)
        if self.side is Side.FLAT: raise PortfolioError('flat_candidate','portfolio candidate cannot be flat')
    @property
    def candidate_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class OpportunityBatch:
    batch_id:str; version:str; as_of_ms:int; candidates:tuple[OpportunityCandidate,...]; source_manifest_hashes:tuple[str,...]
    def __post_init__(self):
        _id(self.batch_id,'batch_id');_ver(self.version);_uniq(tuple(x.candidate_id for x in self.candidates),'candidate_ids')
        for h in self.source_manifest_hashes:_hash(h,'source_manifest_hash')
        if any(x.known_time_ms>self.as_of_ms for x in self.candidates): raise PortfolioError('future_candidate','candidate known after batch as-of')
    @property
    def batch_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class RankedOpportunity:
    candidate:OpportunityCandidate; score:float; status:OpportunityStatus; reason_codes:tuple[str,...]
    def __post_init__(self): _finite(self.score,'score'); _uniq(self.reason_codes,'reason_codes',allow_empty=True)

@dataclass(frozen=True,slots=True)
class DependenceEdge:
    left_context_id:str; right_context_id:str; correlation:float; source:DependenceSource; confidence:float; evidence_hash:str
    def __post_init__(self):
        _id(self.left_context_id,'left_context_id');_id(self.right_context_id,'right_context_id');_hash(self.evidence_hash,'evidence_hash')
        if self.left_context_id>=self.right_context_id: raise PortfolioError('non_canonical_edge','edge identifiers must be sorted')
        _finite(self.correlation,'correlation',-1,1);_finite(self.confidence,'confidence',0,1)

@dataclass(frozen=True,slots=True)
class DependenceModel:
    model_id:str;version:str;as_of_ms:int;edges:tuple[DependenceEdge,...];fallback_correlation:float;symbol_correlation:float;currency_correlation:float;session_correlation:float;anatomy_correlation:float;cluster_correlation:float
    def __post_init__(self):
        _id(self.model_id,'model_id');_ver(self.version)
        for n in ('fallback_correlation','symbol_correlation','currency_correlation','session_correlation','anatomy_correlation','cluster_correlation'): _finite(getattr(self,n),n,0,1)
        pairs=[(e.left_context_id,e.right_context_id) for e in self.edges];_uniq(tuple(map(str,pairs)),'edge_pairs',allow_empty=True)
    @property
    def model_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class PortfolioLimits:
    limits_id:str;version:str;total_risk:float;per_symbol_risk:float;per_currency_risk:float;per_context_risk:float;per_cluster_risk:float;max_positions:int;max_gross_exposure:float;max_net_exposure:float;max_drawdown_budget:float;min_liquidity_score:float;max_turnover_cost:float;min_context_count:int=2
    def __post_init__(self):
        _id(self.limits_id,'limits_id');_ver(self.version)
        for n in ('total_risk','per_symbol_risk','per_currency_risk','per_context_risk','per_cluster_risk','max_gross_exposure','max_net_exposure','max_drawdown_budget','max_turnover_cost'): _finite(getattr(self,n),n,0)
        _finite(self.min_liquidity_score,'min_liquidity_score',0,1)
        if self.max_positions<1 or self.min_context_count<1: raise PortfolioError('invalid_position_limit','position/context limits must be positive')
        if any(x>self.total_risk for x in (self.per_symbol_risk,self.per_currency_risk,self.per_context_risk,self.per_cluster_risk)): raise PortfolioError('sub_limit_exceeds_total','sub-limit cannot exceed total risk')
    @property
    def limits_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class CapacityQuote:
    quote_id:str;candidate_id:str;known_time_ms:int;max_risk_units:float;expected_fill_ratio:float;spread_bps:float;impact_bps:float;degraded_utility:float;broker_volume_step:float;market_open:bool;source_hash:str
    def __post_init__(self):
        _id(self.quote_id,'quote_id');_id(self.candidate_id,'candidate_id');_hash(self.source_hash,'source_hash')
        for n in ('max_risk_units','spread_bps','impact_bps','degraded_utility','broker_volume_step'): _finite(getattr(self,n),n,0)
        _finite(self.expected_fill_ratio,'expected_fill_ratio',0,1)
        if self.broker_volume_step<=0: raise PortfolioError('invalid_volume_step','volume step must be positive')
    @property
    def quote_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class RiskReservation:
    reservation_id:str;candidate_id:str;context_id:str;symbol:str;currency:str;cluster_id:str;risk_units:float;created_at_ms:int;expires_at_ms:int;status:ReservationStatus;ledger_sequence:int;previous_hash:str;entry_hash:str
    def __post_init__(self):
        for n in ('reservation_id','candidate_id','context_id','symbol','currency','cluster_id'): _id(getattr(self,n),n)
        _finite(self.risk_units,'risk_units',0);_hash(self.previous_hash,'previous_hash');_hash(self.entry_hash,'entry_hash')
        if self.risk_units<=0 or self.expires_at_ms<=self.created_at_ms or self.ledger_sequence<1: raise PortfolioError('invalid_reservation','invalid reservation fields')

@dataclass(frozen=True,slots=True)
class AllocationItem:
    candidate_id:str;context_id:str;symbol:str;side:Side;allocated_risk:float;capacity_risk:float;marginal_risk:float;adjusted_score:float;reservation_id:str;reason_codes:tuple[str,...]
    def __post_init__(self):
        for n in ('candidate_id','context_id','symbol','reservation_id'):_id(getattr(self,n),n)
        for n in ('allocated_risk','capacity_risk','marginal_risk','adjusted_score'):_finite(getattr(self,n),n,0)
        _uniq(self.reason_codes,'reason_codes',allow_empty=True)

@dataclass(frozen=True,slots=True)
class AllocationPlan:
    plan_id:str;version:str;batch_hash:str;dependence_hash:str;limits_hash:str;as_of_ms:int;status:AllocationStatus;selected:tuple[AllocationItem,...];rejected_candidate_ids:tuple[str,...];total_risk:float;gross_exposure:float;net_exposure:float;turnover_cost:float;context_count:int;checks:Mapping[str,bool];reason_codes:tuple[str,...]
    def __post_init__(self):
        _id(self.plan_id,'plan_id');_ver(self.version)
        for n in ('batch_hash','dependence_hash','limits_hash'):_hash(getattr(self,n),n)
        _uniq(tuple(x.candidate_id for x in self.selected),'selected_ids',allow_empty=True);_uniq(self.rejected_candidate_ids,'rejected_ids',allow_empty=True)
        for n in ('total_risk','gross_exposure','turnover_cost'):_finite(getattr(self,n),n,0)
        _finite(self.net_exposure,'net_exposure')
        if set(x.candidate_id for x in self.selected)&set(self.rejected_candidate_ids): raise PortfolioError('selected_rejected_overlap','candidate cannot be selected and rejected')
        if self.status is AllocationStatus.ALLOCATED and (not self.selected or not all(self.checks.values())): raise PortfolioError('false_allocation_pass','allocated plan requires selected items and all checks')
    @property
    def plan_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class InteractionDecision:
    decision_id:str;candidate_ids:tuple[str,...];policy:ConflictPolicy;allowed_candidate_ids:tuple[str,...];blocked_candidate_ids:tuple[str,...];net_side:Side;reason_codes:tuple[str,...]
    def __post_init__(self):
        _id(self.decision_id,'decision_id');_uniq(self.candidate_ids,'candidate_ids');_uniq(self.allowed_candidate_ids,'allowed_ids',allow_empty=True);_uniq(self.blocked_candidate_ids,'blocked_ids',allow_empty=True)
        if set(self.allowed_candidate_ids)&set(self.blocked_candidate_ids): raise PortfolioError('interaction_overlap','allowed and blocked overlap')

@dataclass(frozen=True,slots=True)
class StressScenario:
    scenario_id:str;correlation_multiplier:float;capacity_haircut:float;spread_multiplier:float;drop_context_id:str|None=None;utility_haircut:float=0.0
    def __post_init__(self):
        _id(self.scenario_id,'scenario_id')
        for n in ('correlation_multiplier','spread_multiplier'):_finite(getattr(self,n),n,0)
        for n in ('capacity_haircut','utility_haircut'):_finite(getattr(self,n),n,0,1)
        if self.drop_context_id:_id(self.drop_context_id,'drop_context_id')

@dataclass(frozen=True,slots=True)
class StressResult:
    scenario_id:str;safe:bool;remaining_contexts:int;stressed_risk:float;stressed_drawdown:float;concentration:float;reason_codes:tuple[str,...]
    def __post_init__(self):
        _id(self.scenario_id,'scenario_id')
        for n in ('stressed_risk','stressed_drawdown','concentration'):_finite(getattr(self,n),n,0)

@dataclass(frozen=True,slots=True)
class PortfolioValidationReport:
    report_id:str;version:str;plan_hash:str;status:ValidationStatus;out_of_sample:bool;nested_selection:bool;standalone_attribution:Mapping[str,float];combined_value:float;interaction_value:float;turnover:float;max_drawdown:float;tail_loss:float;concentration:float;capacity_utilization:float;stress_results:tuple[StressResult,...];context_drop_safe:bool;correlation_shock_safe:bool;limitations:tuple[str,...]
    def __post_init__(self):
        _id(self.report_id,'report_id');_ver(self.version);_hash(self.plan_hash,'plan_hash')
        for n in ('combined_value','interaction_value','turnover','max_drawdown','tail_loss','concentration','capacity_utilization'):_finite(getattr(self,n),n)
        if self.status is ValidationStatus.PASS and (not self.out_of_sample or not self.nested_selection or not self.context_drop_safe or not self.correlation_shock_safe): raise PortfolioError('false_validation_pass','portfolio pass requires OOS nested and stress safety')
    @property
    def report_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class PortfolioRuntimeBundle:
    bundle_id:str;version:str;plan_hash:str;limits_hash:str;dependence_hash:str;validation_hash:str;reservation_ledger_hash:str;state:RuntimeState;context_ids:tuple[str,...];order_authority:bool=False;broker_authority:bool=False;network_authority:bool=False;kill_switch_required:bool=True
    def __post_init__(self):
        _id(self.bundle_id,'bundle_id');_ver(self.version)
        for n in ('plan_hash','limits_hash','dependence_hash','validation_hash','reservation_ledger_hash'):_hash(getattr(self,n),n)
        _uniq(self.context_ids,'context_ids')
        if self.order_authority or self.broker_authority or self.network_authority: raise PortfolioError('forbidden_runtime_authority','portfolio bundle cannot own order/broker/network authority')
        if not self.kill_switch_required: raise PortfolioError('missing_kill_switch','kill switch is mandatory')
    @property
    def bundle_hash(self): return canonical_sha256(asdict(self))

@dataclass(frozen=True,slots=True)
class PortfolioEvidenceBundle:
    evidence_id:str;version:str;queue_hash:str;dependence_hash:str;capacity_hashes:tuple[str,...];plan_hash:str;validation_hash:str;runtime_bundle_hash:str;telemetry_hash:str;limitations:tuple[str,...];activation_allowed:bool;next_phase:str
    def __post_init__(self):
        _id(self.evidence_id,'evidence_id');_ver(self.version);_id(self.next_phase,'next_phase')
        for n in ('queue_hash','dependence_hash','plan_hash','validation_hash','runtime_bundle_hash','telemetry_hash'):_hash(getattr(self,n),n)
        for h in self.capacity_hashes:_hash(h,'capacity_hash')
    @property
    def evidence_hash(self): return canonical_sha256(asdict(self))
