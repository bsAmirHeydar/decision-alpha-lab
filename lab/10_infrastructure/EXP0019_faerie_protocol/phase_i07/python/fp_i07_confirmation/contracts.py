from __future__ import annotations
from dataclasses import dataclass
import math
from fp_i02_kernel.enums import RelationCode, PriceSide, Direction
from fp_i06_relations.contracts import RawDivergenceCandidate
from fp_i06_relations.enums import CandidateState
from .canonical import canonical_sha256,stable_id,require_identifier,require_sha256,require_semver
from .constants import *
from .enums import *
from .errors import FPI07Error

def _req(v,n):
    if not isinstance(v,str) or not v.strip(): raise FPI07Error("FP_CRC_REQUIRED_FIELD",f"{n} is required",{"field":n})
    return v
def _minute(v,n):
    if not isinstance(v,int) or v<0 or v%M1_MS: raise FPI07Error("FP_CRC_MINUTE_INVALID",f"{n} must be UTC M1 aligned")
    return v
def _finite(v,n):
    if not isinstance(v,(int,float)) or not math.isfinite(float(v)): raise FPI07Error("FP_CRC_NONFINITE_VALUE",f"{n} must be finite")
    return float(v)

@dataclass(frozen=True,slots=True)
class ConfirmationConfig:
    context_id:str; pair_id:str; host_symbol:str; host_timeframe:HostTimeframe; host_timeframe_seconds:int
    projection_version:str=PROJECTION_VERSION; confirmation_engine_version:str=CONFIRMATION_ENGINE_VERSION
    lifecycle_engine_version:str=LIFECYCLE_ENGINE_VERSION; policy:str=DEFAULT_POLICY
    def __post_init__(self):
        require_identifier(self.context_id,"context_id");require_identifier(self.pair_id,"pair_id");require_identifier(self.host_symbol,"host_symbol")
        require_semver(self.projection_version,"projection_version");require_semver(self.confirmation_engine_version,"confirmation_engine_version");require_semver(self.lifecycle_engine_version,"lifecycle_engine_version")
        if self.host_timeframe_seconds<=0 or self.host_timeframe_seconds%60: raise FPI07Error("FP_CRC_TIMEFRAME_SECONDS_INVALID","host timeframe seconds must be positive whole minutes")
        if not self.policy: raise FPI07Error("FP_CRC_POLICY_REQUIRED","confirmation policy required")
    @property
    def config_hash(self): return canonical_sha256(self)

@dataclass(frozen=True,slots=True)
class HostBar:
    host_bar_id:str; canonical_symbol:str; timeframe:HostTimeframe; open_utc_ms:int; close_utc_ms:int
    open_price:float; high_price:float; low_price:float; close_price:float; is_closed:bool; availability_utc_ms:int
    coverage_complete:bool; constituent_m1_hash:str; source_revision_id:str; bar_hash:str
    def __post_init__(self):
        _req(self.host_bar_id,"host_bar_id");require_identifier(self.canonical_symbol,"canonical_symbol");_minute(self.open_utc_ms,"open_utc_ms");_minute(self.close_utc_ms,"close_utc_ms")
        if self.close_utc_ms<=self.open_utc_ms: raise FPI07Error("FP_CRC_HOST_BAR_INTERVAL_INVALID","host bar close must follow open")
        for n in ("open_price","high_price","low_price","close_price"):_finite(getattr(self,n),n)
        if self.high_price<max(self.open_price,self.close_price,self.low_price) or self.low_price>min(self.open_price,self.close_price,self.high_price): raise FPI07Error("FP_CRC_HOST_BAR_OHLC_INVALID","invalid host bar OHLC")
        if self.availability_utc_ms<self.close_utc_ms: raise FPI07Error("FP_CRC_BAR_AVAILABLE_BEFORE_CLOSE","bar cannot be available before close")
        require_sha256(self.constituent_m1_hash,"constituent_m1_hash");_req(self.source_revision_id,"source_revision_id");require_sha256(self.bar_hash,"bar_hash")

@dataclass(frozen=True,slots=True)
class ConfirmationProjection:
    projection_id:str; candidate_id:str; owner_session_id:str; host_symbol:str; host_timeframe:HostTimeframe
    candidate_utc_ms:int; deadline_utc_ms:int; target_host_bar_id:str; target_open_utc_ms:int; target_close_utc_ms:int
    source_candidate_hash:str; config_hash:str; projection_hash:str
    def __post_init__(self):
        _req(self.projection_id,"projection_id");_req(self.candidate_id,"candidate_id");_req(self.owner_session_id,"owner_session_id");require_identifier(self.host_symbol,"host_symbol")
        _minute(self.candidate_utc_ms,"candidate_utc_ms");_minute(self.deadline_utc_ms,"deadline_utc_ms");_req(self.target_host_bar_id,"target_host_bar_id");_minute(self.target_open_utc_ms,"target_open_utc_ms");_minute(self.target_close_utc_ms,"target_close_utc_ms")
        if self.target_close_utc_ms<=self.candidate_utc_ms: raise FPI07Error("FP_CRC_TARGET_CLOSE_NOT_AFTER_CANDIDATE","target close must be after candidate")
        require_sha256(self.source_candidate_hash,"source_candidate_hash");require_sha256(self.config_hash,"config_hash");require_sha256(self.projection_hash,"projection_hash")

@dataclass(frozen=True,slots=True)
class PendingConfirmation:
    pending_id:str; candidate:RawDivergenceCandidate; projection:ConfirmationProjection; state:ConfirmationState
    state_sequence:int; admitted_utc_ms:int; source_revision_id:str; pending_hash:str
    def __post_init__(self):
        _req(self.pending_id,"pending_id");
        if self.candidate.state is not CandidateState.RAW_ACTIVE: raise FPI07Error("FP_CRC_CANDIDATE_NOT_ACTIVE","only RAW_ACTIVE candidate can be pending")
        if self.projection.candidate_id!=self.candidate.candidate_id: raise FPI07Error("FP_CRC_PROJECTION_CANDIDATE_MISMATCH","projection candidate mismatch")
        if self.state is not ConfirmationState.PENDING: raise FPI07Error("FP_CRC_PENDING_STATE_INVALID","pending contract must be PENDING")
        if self.state_sequence<0: raise FPI07Error("FP_CRC_STATE_SEQUENCE_INVALID","state sequence invalid")
        _minute(self.admitted_utc_ms,"admitted_utc_ms");_req(self.source_revision_id,"source_revision_id");require_sha256(self.pending_hash,"pending_hash")

@dataclass(frozen=True,slots=True)
class CloseObservation:
    observation_id:str; candidate_id:str; host_bar_id:str; pair_state:ClosePairState; observed_utc_ms:int
    source_available_through_utc_ms:int; hunter_touch_preserved:bool; protected_touch_seen:bool; source_revision_id:str
    evidence_hash:str; reason_code:str
    def __post_init__(self):
        _req(self.observation_id,"observation_id");_req(self.candidate_id,"candidate_id");_req(self.host_bar_id,"host_bar_id");_minute(self.observed_utc_ms,"observed_utc_ms");_minute(self.source_available_through_utc_ms,"source_available_through_utc_ms")
        _req(self.source_revision_id,"source_revision_id");require_sha256(self.evidence_hash,"evidence_hash");_req(self.reason_code,"reason_code")
        if self.pair_state is ClosePairState.HUNTER_ONLY and (not self.hunter_touch_preserved or self.protected_touch_seen): raise FPI07Error("FP_CRC_PAIR_STATE_FACT_MISMATCH","HUNTER_ONLY facts mismatch")
        if self.pair_state is ClosePairState.BOTH and not self.protected_touch_seen: raise FPI07Error("FP_CRC_PAIR_STATE_FACT_MISMATCH","BOTH requires protected touch")

@dataclass(frozen=True,slots=True)
class ConfirmedSignal:
    signal_id:str; candidate_id:str; relation_instance_id:str; relation:RelationCode; direction:Direction; side:PriceSide
    hunter_symbol:str; protected_symbol:str; first_hunt_minute_utc_ms:int; confirmation_bar_id:str
    confirmation_open_utc_ms:int; confirmation_close_utc_ms:int; host_symbol:str; host_timeframe:HostTimeframe
    owner_session_id:str; source_revision_id:str; config_hash:str; evidence_hash:str; signal_hash:str
    def __post_init__(self):
        _req(self.signal_id,"signal_id");_req(self.candidate_id,"candidate_id");_req(self.relation_instance_id,"relation_instance_id");require_identifier(self.hunter_symbol,"hunter_symbol");require_identifier(self.protected_symbol,"protected_symbol")
        if self.hunter_symbol==self.protected_symbol: raise FPI07Error("FP_CRC_ROLE_COLLISION","roles collide")
        _minute(self.first_hunt_minute_utc_ms,"first_hunt_minute_utc_ms");_req(self.confirmation_bar_id,"confirmation_bar_id");_minute(self.confirmation_open_utc_ms,"confirmation_open_utc_ms");_minute(self.confirmation_close_utc_ms,"confirmation_close_utc_ms")
        if self.confirmation_close_utc_ms<=self.first_hunt_minute_utc_ms: raise FPI07Error("FP_CRC_CONFIRMATION_ORDER_INVALID","confirmation must follow hunt")
        require_identifier(self.host_symbol,"host_symbol");_req(self.owner_session_id,"owner_session_id");_req(self.source_revision_id,"source_revision_id");require_sha256(self.config_hash,"config_hash");require_sha256(self.evidence_hash,"evidence_hash");require_sha256(self.signal_hash,"signal_hash")

@dataclass(frozen=True,slots=True)
class ConfirmationTransitionRecord:
    event_id:str; candidate_id:str; sequence:int; transition:ConfirmationTransition; prior_state:ConfirmationState|None
    next_state:ConfirmationState; event_utc_ms:int; evidence_id:str; reason_code:str; event_hash:str
    def __post_init__(self):
        _req(self.event_id,"event_id");_req(self.candidate_id,"candidate_id");_req(self.evidence_id,"evidence_id");_req(self.reason_code,"reason_code");require_sha256(self.event_hash,"event_hash");_minute(self.event_utc_ms,"event_utc_ms")
        if self.sequence<0: raise FPI07Error("FP_CRC_EVENT_SEQUENCE_INVALID","event sequence invalid")

@dataclass(frozen=True,slots=True)
class ConfirmationResult:
    result_id:str; candidate_id:str; projection_id:str; outcome:ConfirmationOutcome; final_state:ConfirmationState
    host_bar_id:str; finalized_utc_ms:int; confirmed_signal:ConfirmedSignal|None; observation_id:str
    reason_code:str; source_revision_id:str; config_hash:str; result_hash:str
    def __post_init__(self):
        _req(self.result_id,"result_id");_req(self.candidate_id,"candidate_id");_req(self.projection_id,"projection_id");_req(self.host_bar_id,"host_bar_id");_minute(self.finalized_utc_ms,"finalized_utc_ms")
        _req(self.observation_id,"observation_id");_req(self.reason_code,"reason_code");_req(self.source_revision_id,"source_revision_id");require_sha256(self.config_hash,"config_hash");require_sha256(self.result_hash,"result_hash")
        if self.outcome is ConfirmationOutcome.CONFIRMED and self.confirmed_signal is None: raise FPI07Error("FP_CRC_CONFIRMED_SIGNAL_REQUIRED","confirmed outcome requires signal")
        if self.outcome is not ConfirmationOutcome.CONFIRMED and self.confirmed_signal is not None: raise FPI07Error("FP_CRC_NONCONFIRMED_SIGNAL_FORBIDDEN","nonconfirmed outcome cannot carry signal")

@dataclass(frozen=True,slots=True)
class RevisionImpact:
    impact_id:str; revision_id:str; affected_start_utc_ms:int; affected_end_utc_ms:int; candidate_id:str
    disposition:RevisionDisposition; reason_code:str; impact_hash:str
    def __post_init__(self):
        _req(self.impact_id,"impact_id");_req(self.revision_id,"revision_id");_minute(self.affected_start_utc_ms,"affected_start_utc_ms");_minute(self.affected_end_utc_ms,"affected_end_utc_ms");_req(self.candidate_id,"candidate_id");_req(self.reason_code,"reason_code");require_sha256(self.impact_hash,"impact_hash")
        if self.affected_end_utc_ms<=self.affected_start_utc_ms: raise FPI07Error("FP_CRC_REVISION_RANGE_INVALID","revision range invalid")

@dataclass(frozen=True,slots=True)
class ConfirmationCheckpoint:
    checkpoint_id:str; checkpoint_version:str; config_hash:str; pending:tuple[PendingConfirmation,...]
    results:tuple[ConfirmationResult,...]; last_processed_close_utc_ms:int; source_revision_id:str; payload_hash:str
    def __post_init__(self):
        _req(self.checkpoint_id,"checkpoint_id");require_semver(self.checkpoint_version,"checkpoint_version");require_sha256(self.config_hash,"config_hash");_minute(self.last_processed_close_utc_ms,"last_processed_close_utc_ms");_req(self.source_revision_id,"source_revision_id");require_sha256(self.payload_hash,"payload_hash")
        if len({p.candidate.candidate_id for p in self.pending})!=len(self.pending): raise FPI07Error("FP_CRC_DUPLICATE_PENDING","duplicate pending candidate")
        if len({r.candidate_id for r in self.results})!=len(self.results): raise FPI07Error("FP_CRC_DUPLICATE_RESULT","duplicate candidate result")

@dataclass(frozen=True,slots=True)
class ConfirmationEngineSnapshot:
    snapshot_id:str; config_hash:str; pending:tuple[PendingConfirmation,...]; results:tuple[ConfirmationResult,...]
    signals:tuple[ConfirmedSignal,...]; transitions:tuple[ConfirmationTransitionRecord,...]; health:EngineHealth
    reason_codes:tuple[str,...]; source_revision_id:str; created_utc_ms:int; snapshot_hash:str
    def __post_init__(self):
        _req(self.snapshot_id,"snapshot_id");require_sha256(self.config_hash,"config_hash");_req(self.source_revision_id,"source_revision_id");_minute(self.created_utc_ms,"created_utc_ms");require_sha256(self.snapshot_hash,"snapshot_hash")
        if len({r.candidate_id for r in self.results})!=len(self.results): raise FPI07Error("FP_CRC_DUPLICATE_RESULT","duplicate result")
        if len({s.signal_id for s in self.signals})!=len(self.signals): raise FPI07Error("FP_CRC_DUPLICATE_SIGNAL","duplicate signal")
