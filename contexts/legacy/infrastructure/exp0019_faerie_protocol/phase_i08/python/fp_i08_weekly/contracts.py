from __future__ import annotations
from dataclasses import dataclass
import math
from fp_i02_kernel.enums import RelationCode,PriceSide,Direction,WindowKind
from fp_i06_relations.contracts import RelationSidePlan,RelationScanResult
from fp_i07_confirmation.contracts import ConfirmedSignal,ConfirmationResult
from .canonical import canonical_sha256,stable_id,require_identifier,require_sha256,require_semver
from .constants import *
from .enums import *
from .errors import FPI08Error

def _req(v,n):
    if not isinstance(v,str) or not v.strip(): raise FPI08Error("FP_WRC_REQUIRED_FIELD",f"{n} required")
    return v
def _minute(v,n):
    if not isinstance(v,int) or v<0 or v%M1_MS: raise FPI08Error("FP_WRC_MINUTE_INVALID",f"{n} must be UTC M1 aligned")
    return v
def _finite(v,n):
    if not isinstance(v,(int,float)) or not math.isfinite(float(v)): raise FPI08Error("FP_WRC_NONFINITE_VALUE",f"{n} finite required")
    return float(v)

@dataclass(frozen=True,slots=True)
class WWConfig:
    context_id:str; pair_id:str; reference_store_hash:str; confirmation_config_hash:str
    neutralization_policy:str=DEFAULT_NEUTRALIZATION_POLICY
    tradeability_policy:str=DEFAULT_TRADEABILITY_POLICY
    no_active_policy:str=DEFAULT_NO_ACTIVE_POLICY
    resolution_policy:str=DEFAULT_RESOLUTION_POLICY
    compiler_version:str=WW_COMPILER_VERSION; engine_version:str=WW_ENGINE_VERSION
    stack_version:str=WW_STACK_VERSION; gate_version:str=WW_GATE_VERSION
    def __post_init__(self):
        require_identifier(self.context_id,"context_id");require_identifier(self.pair_id,"pair_id")
        require_sha256(self.reference_store_hash,"reference_store_hash");require_sha256(self.confirmation_config_hash,"confirmation_config_hash")
        for n in ("compiler_version","engine_version","stack_version","gate_version"):require_semver(getattr(self,n),n)
        expected={"neutralization_policy":DEFAULT_NEUTRALIZATION_POLICY,"tradeability_policy":DEFAULT_TRADEABILITY_POLICY,"no_active_policy":DEFAULT_NO_ACTIVE_POLICY,"resolution_policy":DEFAULT_RESOLUTION_POLICY}
        for n,v in expected.items():
            if getattr(self,n)!=v: raise FPI08Error("FP_WRC_POLICY_NONCANONICAL",f"{n} must be {v}")
    @property
    def config_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class WWRelationInstance:
    relation_instance_id:str; pair_id:str; previous_week_id:str; current_week_id:str
    reference_pair_window_id:str; check_pair_window_id:str; check_start_utc_ms:int; check_end_utc_ms:int
    source_store_hash:str; source_revision_id:str; data_state:WWDataState; reason_codes:tuple[str,...]; semantic_hash:str
    def __post_init__(self):
        _req(self.relation_instance_id,"relation_instance_id");require_identifier(self.pair_id,"pair_id");_req(self.previous_week_id,"previous_week_id");_req(self.current_week_id,"current_week_id")
        if self.previous_week_id==self.current_week_id: raise FPI08Error("FP_WRC_WEEK_COLLISION","reference and check weeks must differ")
        _req(self.reference_pair_window_id,"reference_pair_window_id");_req(self.check_pair_window_id,"check_pair_window_id")
        _minute(self.check_start_utc_ms,"check_start_utc_ms");_minute(self.check_end_utc_ms,"check_end_utc_ms")
        if self.check_end_utc_ms<=self.check_start_utc_ms: raise FPI08Error("FP_WRC_CHECK_INTERVAL_INVALID","check week interval invalid")
        require_sha256(self.source_store_hash,"source_store_hash");_req(self.source_revision_id,"source_revision_id");require_sha256(self.semantic_hash,"semantic_hash")

@dataclass(frozen=True,slots=True)
class WWSidePlan:
    side_plan_id:str; relation_instance_id:str; pair_id:str; side:PriceSide
    left_reference_id:str; left_symbol:str; left_reference_price:float
    right_reference_id:str; right_symbol:str; right_reference_price:float
    check_start_utc_ms:int; check_end_utc_ms:int; source_reference_hashes:tuple[str,...]
    data_state:WWDataState; reason_codes:tuple[str,...]; semantic_hash:str
    def __post_init__(self):
        _req(self.side_plan_id,"side_plan_id");_req(self.relation_instance_id,"relation_instance_id");require_identifier(self.pair_id,"pair_id")
        _req(self.left_reference_id,"left_reference_id");require_identifier(self.left_symbol,"left_symbol");_finite(self.left_reference_price,"left_reference_price")
        _req(self.right_reference_id,"right_reference_id");require_identifier(self.right_symbol,"right_symbol");_finite(self.right_reference_price,"right_reference_price")
        if self.left_symbol==self.right_symbol: raise FPI08Error("FP_WRC_PAIR_SYMBOLS_EQUAL","WW symbols must differ")
        _minute(self.check_start_utc_ms,"check_start_utc_ms");_minute(self.check_end_utc_ms,"check_end_utc_ms")
        if tuple(sorted(set(self.source_reference_hashes)))!=self.source_reference_hashes or len(self.source_reference_hashes)!=2: raise FPI08Error("FP_WRC_REFERENCE_HASHES_INVALID","two canonical reference hashes required")
        require_sha256(self.semantic_hash,"semantic_hash")
    def to_i06_plan(self):
        from fp_i06_relations.enums import SidePlanState
        state=SidePlanState.ELIGIBLE if self.data_state is WWDataState.COMPLETE else SidePlanState.DATA_BLOCKED
        return RelationSidePlan(self.side_plan_id,self.relation_instance_id,RelationCode.WW,self.side,self.left_reference_id,self.left_symbol,self.left_reference_price,self.right_reference_id,self.right_symbol,self.right_reference_price,self.check_start_utc_ms,self.check_end_utc_ms,state,self.reason_codes,self.source_reference_hashes,self.semantic_hash)

@dataclass(frozen=True,slots=True)
class WWCompilationReport:
    report_id:str; instance:WWRelationInstance|None; side_plans:tuple[WWSidePlan,...]; blocked_items:tuple[str,...]
    source_store_hash:str; evidence_hash:str
    def __post_init__(self):
        _req(self.report_id,"report_id");require_sha256(self.source_store_hash,"source_store_hash");require_sha256(self.evidence_hash,"evidence_hash")
        if len({p.side_plan_id for p in self.side_plans})!=len(self.side_plans): raise FPI08Error("FP_WRC_DUPLICATE_SIDE_PLAN","duplicate WW side plan")

@dataclass(frozen=True,slots=True)
class WWScanRecord:
    scan_record_id:str; side_plan_id:str; relation_scan:RelationScanResult; source_revision_id:str; evidence_hash:str
    def __post_init__(self):
        _req(self.scan_record_id,"scan_record_id");_req(self.side_plan_id,"side_plan_id");_req(self.source_revision_id,"source_revision_id");require_sha256(self.evidence_hash,"evidence_hash")
        if self.relation_scan.side_plan_id!=self.side_plan_id: raise FPI08Error("FP_WRC_SCAN_PLAN_MISMATCH","scan plan mismatch")
        if self.relation_scan.candidate and self.relation_scan.candidate.relation is not RelationCode.WW: raise FPI08Error("FP_WRC_NON_WW_CANDIDATE","WW scan produced non-WW candidate")

@dataclass(frozen=True,slots=True)
class WWContext:
    ww_context_id:str; source_signal:ConfirmedSignal; confirmation_result_id:str; side_plan_id:str
    direction:Direction; side:PriceSide; hunter_symbol:str; protected_symbol:str
    hunter_reference_id:str; hunter_reference_price:float; protected_reference_id:str; protected_reference_price:float
    previous_week_id:str; current_week_id:str; check_week_end_utc_ms:int
    state:WWLifecycleState; confirmed_utc_ms:int; neutralized_utc_ms:int; neutralizing_hunt_id:str
    expired_utc_ms:int; reason_code:str; source_revision_id:str; config_hash:str; context_hash:str
    def __post_init__(self):
        _req(self.ww_context_id,"ww_context_id");_req(self.confirmation_result_id,"confirmation_result_id");_req(self.side_plan_id,"side_plan_id")
        if self.source_signal.relation is not RelationCode.WW: raise FPI08Error("FP_WRC_NON_WW_SIGNAL","context requires WW signal")
        if self.direction is not self.source_signal.direction or self.side is not self.source_signal.side: raise FPI08Error("FP_WRC_SIGNAL_CONTEXT_MISMATCH","direction/side mismatch")
        require_identifier(self.hunter_symbol,"hunter_symbol");require_identifier(self.protected_symbol,"protected_symbol")
        if self.hunter_symbol==self.protected_symbol: raise FPI08Error("FP_WRC_ROLE_COLLISION","WW roles collide")
        _req(self.hunter_reference_id,"hunter_reference_id");_finite(self.hunter_reference_price,"hunter_reference_price");_req(self.protected_reference_id,"protected_reference_id");_finite(self.protected_reference_price,"protected_reference_price")
        _req(self.previous_week_id,"previous_week_id");_req(self.current_week_id,"current_week_id");_minute(self.check_week_end_utc_ms,"check_week_end_utc_ms");_minute(self.confirmed_utc_ms,"confirmed_utc_ms")
        if self.confirmed_utc_ms>=self.check_week_end_utc_ms: raise FPI08Error("FP_WRC_CONFIRMATION_AFTER_WEEK","WW confirmation must occur inside check week")
        if self.state is WWLifecycleState.NEUTRALIZED and (self.neutralized_utc_ms<=self.confirmed_utc_ms or not self.neutralizing_hunt_id): raise FPI08Error("FP_WRC_NEUTRALIZATION_INVALID","neutralization requires later second-symbol hunt")
        if self.state is WWLifecycleState.EXPIRED and self.expired_utc_ms<self.check_week_end_utc_ms: raise FPI08Error("FP_WRC_EXPIRY_EARLY","WW cannot expire before check week end")
        _req(self.reason_code,"reason_code");_req(self.source_revision_id,"source_revision_id");require_sha256(self.config_hash,"config_hash");require_sha256(self.context_hash,"context_hash")
    @property
    def active(self): return self.state is WWLifecycleState.CONFIRMED

@dataclass(frozen=True,slots=True)
class WWTransitionRecord:
    event_id:str; ww_context_id:str; sequence:int; transition:WWTransition; prior_state:WWLifecycleState|None; next_state:WWLifecycleState
    event_utc_ms:int; evidence_id:str; reason_code:str; event_hash:str
    def __post_init__(self):
        _req(self.event_id,"event_id");_req(self.ww_context_id,"ww_context_id");_req(self.evidence_id,"evidence_id");_req(self.reason_code,"reason_code");require_sha256(self.event_hash,"event_hash");_minute(self.event_utc_ms,"event_utc_ms")
        if self.sequence<0: raise FPI08Error("FP_WRC_SEQUENCE_INVALID","transition sequence invalid")

@dataclass(frozen=True,slots=True)
class WWNeutralizationObservation:
    observation_id:str; ww_context_id:str; symbol:str; side:PriceSide; minute_utc_ms:int; observed_extreme:float
    reference_id:str; reference_price:float; data_complete:bool; source_revision_id:str; evidence_hash:str
    def __post_init__(self):
        _req(self.observation_id,"observation_id");_req(self.ww_context_id,"ww_context_id");require_identifier(self.symbol,"symbol");_minute(self.minute_utc_ms,"minute_utc_ms");_finite(self.observed_extreme,"observed_extreme");_req(self.reference_id,"reference_id");_finite(self.reference_price,"reference_price");_req(self.source_revision_id,"source_revision_id");require_sha256(self.evidence_hash,"evidence_hash")

@dataclass(frozen=True,slots=True)
class WWNeutralizationResult:
    result_id:str; ww_context_id:str; outcome:NeutralizationOutcome; context:WWContext; observation_id:str; reason_code:str; result_hash:str
    def __post_init__(self):
        _req(self.result_id,"result_id");_req(self.ww_context_id,"ww_context_id");_req(self.observation_id,"observation_id");_req(self.reason_code,"reason_code");require_sha256(self.result_hash,"result_hash")
        if self.context.ww_context_id!=self.ww_context_id: raise FPI08Error("FP_WRC_CONTEXT_RESULT_MISMATCH","neutralization context mismatch")

@dataclass(frozen=True,slots=True)
class WWStackEntry:
    ww_context_id:str; signal_id:str; direction:Direction; confirmed_utc_ms:int; state:WWLifecycleState; disposition:WWStackDisposition; recency_rank:int; winner_ww_context_id:str; reason_code:str; entry_hash:str
    def __post_init__(self):
        _req(self.ww_context_id,"ww_context_id");_req(self.signal_id,"signal_id");_minute(self.confirmed_utc_ms,"confirmed_utc_ms");_req(self.reason_code,"reason_code");require_sha256(self.entry_hash,"entry_hash")
        if self.recency_rank<0: raise FPI08Error("FP_WRC_RECENCY_RANK_INVALID","recency rank invalid")

@dataclass(frozen=True,slots=True)
class WWActiveStack:
    stack_id:str; pair_id:str; entries:tuple[WWStackEntry,...]; active_ww_context_id:str; active_signal_id:str; active_direction:Direction|None
    data_state:WWDataState; evaluated_utc_ms:int; resolution_policy:str; reason_code:str; config_hash:str; stack_hash:str
    def __post_init__(self):
        _req(self.stack_id,"stack_id");require_identifier(self.pair_id,"pair_id");_minute(self.evaluated_utc_ms,"evaluated_utc_ms");_req(self.resolution_policy,"resolution_policy");_req(self.reason_code,"reason_code");require_sha256(self.config_hash,"config_hash");require_sha256(self.stack_hash,"stack_hash")
        winners=[e for e in self.entries if e.disposition is WWStackDisposition.ACTIVE_WINNER]
        if self.active_ww_context_id and len(winners)!=1: raise FPI08Error("FP_WRC_STACK_WINNER_INVALID","active stack requires exactly one winner")
        if not self.active_ww_context_id and winners: raise FPI08Error("FP_WRC_STACK_WINNER_ORPHAN","winner exists without active id")

@dataclass(frozen=True,slots=True)
class DirectionGateDecision:
    decision_id:str; subject_signal_id:str; subject_relation:RelationCode; subject_direction:Direction
    eligibility:GateEligibility; active_ww_context_id:str; active_ww_direction:Direction|None; evaluated_utc_ms:int
    reason_code:str; stack_hash:str; decision_hash:str
    def __post_init__(self):
        _req(self.decision_id,"decision_id");_req(self.subject_signal_id,"subject_signal_id");_minute(self.evaluated_utc_ms,"evaluated_utc_ms");_req(self.reason_code,"reason_code");require_sha256(self.stack_hash,"stack_hash");require_sha256(self.decision_hash,"decision_hash")

@dataclass(frozen=True,slots=True)
class WWEngineSnapshot:
    snapshot_id:str; config_hash:str; contexts:tuple[WWContext,...]; transitions:tuple[WWTransitionRecord,...]; active_stack:WWActiveStack
    gate_decisions:tuple[DirectionGateDecision,...]; health:EngineHealth; reason_codes:tuple[str,...]; source_revision_id:str; created_utc_ms:int; snapshot_hash:str
    def __post_init__(self):
        _req(self.snapshot_id,"snapshot_id");require_sha256(self.config_hash,"config_hash");_req(self.source_revision_id,"source_revision_id");_minute(self.created_utc_ms,"created_utc_ms");require_sha256(self.snapshot_hash,"snapshot_hash")
        if len({c.ww_context_id for c in self.contexts})!=len(self.contexts): raise FPI08Error("FP_WRC_DUPLICATE_CONTEXT","duplicate WW context")
