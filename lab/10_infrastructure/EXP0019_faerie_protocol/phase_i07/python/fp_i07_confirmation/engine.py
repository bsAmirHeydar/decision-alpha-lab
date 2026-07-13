from __future__ import annotations
from .canonical import canonical_sha256,stable_id
from .contracts import PendingConfirmation,ConfirmedSignal,ConfirmationResult,ConfirmationEngineSnapshot
from .enums import *
from .lifecycle import transition,admission_event
from .errors import FPI07Error

def admit_candidate(candidate,projection,source_revision_id,admitted_utc_ms):
    material={"candidate":candidate.semantic_hash,"projection":projection.projection_hash,"revision":source_revision_id,"admitted":admitted_utc_ms}
    pending=PendingConfirmation(stable_id("FPPENDING",material,32),candidate,projection,ConfirmationState.PENDING,0,admitted_utc_ms,source_revision_id,canonical_sha256(material))
    return pending,admission_event(pending)

def _signal(pending,bar,obs,config):
    c=pending.candidate
    material={"candidate":c.candidate_id,"relation":c.relation,"direction":c.direction,"side":c.side,"hunter":c.hunter_symbol,"protected":c.protected_symbol,"hunt":c.first_hunt_minute_utc_ms,"bar":bar.host_bar_id,"close":bar.close_utc_ms,"tf":config.host_timeframe,"session":pending.projection.owner_session_id,"config":config.config_hash}
    evidence=canonical_sha256({"observation":obs.evidence_hash,"bar":bar.bar_hash,"candidate":c.semantic_hash})
    return ConfirmedSignal(stable_id("FPSIGNAL",material,40),c.candidate_id,c.relation_instance_id,c.relation,c.direction,c.side,c.hunter_symbol,c.protected_symbol,c.first_hunt_minute_utc_ms,bar.host_bar_id,bar.open_utc_ms,bar.close_utc_ms,config.host_symbol,config.host_timeframe,pending.projection.owner_session_id,obs.source_revision_id,config.config_hash,evidence,canonical_sha256(material))

def finalize(pending,bar,observation,config):
    if pending.state is not ConfirmationState.PENDING: raise FPI07Error("FP_CRC_PENDING_ALREADY_FINAL","pending already terminal")
    if bar.host_bar_id!=pending.projection.target_host_bar_id or observation.host_bar_id!=bar.host_bar_id: raise FPI07Error("FP_CRC_TARGET_BAR_MISMATCH","finalization must use projected bar")
    if not bar.is_closed: raise FPI07Error("FP_CRC_HOST_BAR_NOT_CLOSED","only closed host bar can finalize")
    if observation.source_available_through_utc_ms<bar.close_utc_ms or not bar.coverage_complete or observation.pair_state is ClosePairState.DATA_INCOMPLETE:
        outcome=ConfirmationOutcome.UNAVAILABLE_AT_CLOSE; state=ConfirmationState.INVALID_DATA; reason="FP_CRC_UNAVAILABLE_AT_CLOSE"; sig=None
    elif bar.close_utc_ms>=pending.projection.deadline_utc_ms:
        outcome=ConfirmationOutcome.CONFIRMATION_DEADLINE_MISSED; state=ConfirmationState.EXPIRED_DEADLINE; reason="FP_CRC_CONFIRMATION_DEADLINE_MISSED"; sig=None
    elif observation.pair_state is ClosePairState.BOTH:
        outcome=ConfirmationOutcome.INVALIDATED_DOUBLE_HUNT; state=ConfirmationState.CANCELLED_SECOND_TOUCH; reason="FP_CRC_PROTECTED_TOUCH_BEFORE_CONFIRMATION"; sig=None
    elif observation.pair_state is ClosePairState.PROTECTED_ONLY:
        outcome=ConfirmationOutcome.INVALIDATED_ROLE_CHANGED; state=ConfirmationState.CANCELLED_ROLE_CHANGED; reason="FP_CRC_ROLE_CHANGED_AT_CLOSE"; sig=None
    elif observation.pair_state is ClosePairState.NONE:
        outcome=ConfirmationOutcome.NO_SIGNAL_AT_CLOSE; state=ConfirmationState.NO_SIGNAL_AT_CLOSE; reason="FP_CRC_ASYMMETRY_ABSENT_AT_CLOSE"; sig=None
    elif observation.pair_state is ClosePairState.HUNTER_ONLY:
        outcome=ConfirmationOutcome.CONFIRMED; state=ConfirmationState.CONFIRMED; reason="FP_CRC_SIGNAL_CONFIRMED"; sig=_signal(pending,bar,observation,config)
    else: raise FPI07Error("FP_CRC_PAIR_STATE_UNKNOWN","unknown pair state")
    event=transition(pending.candidate.candidate_id,1,ConfirmationState.PENDING,state,bar.close_utc_ms,observation.observation_id,reason)
    material={"candidate":pending.candidate.candidate_id,"projection":pending.projection.projection_id,"outcome":outcome,"state":state,"bar":bar.host_bar_id,"observation":observation.evidence_hash,"signal":sig.signal_hash if sig else None,"reason":reason,"config":config.config_hash}
    result=ConfirmationResult(stable_id("FPCONFRES",material,36),pending.candidate.candidate_id,pending.projection.projection_id,outcome,state,bar.host_bar_id,bar.close_utc_ms,sig,observation.observation_id,reason,observation.source_revision_id,config.config_hash,canonical_sha256(material))
    return result,event

def expire_without_close(pending,deadline_utc_ms,config):
    if deadline_utc_ms<pending.projection.deadline_utc_ms: raise FPI07Error("FP_CRC_DEADLINE_NOT_REACHED","cannot expire before deadline")
    reason="FP_CRC_CONFIRMATION_DEADLINE_MISSED"; state=ConfirmationState.EXPIRED_DEADLINE
    event=transition(pending.candidate.candidate_id,1,ConfirmationState.PENDING,state,pending.projection.deadline_utc_ms,pending.projection.projection_id,reason)
    material={"candidate":pending.candidate.candidate_id,"projection":pending.projection.projection_id,"outcome":ConfirmationOutcome.CONFIRMATION_DEADLINE_MISSED,"at":pending.projection.deadline_utc_ms,"config":config.config_hash}
    result=ConfirmationResult(stable_id("FPCONFRES",material,36),pending.candidate.candidate_id,pending.projection.projection_id,ConfirmationOutcome.CONFIRMATION_DEADLINE_MISSED,state,pending.projection.target_host_bar_id,pending.projection.deadline_utc_ms,None,pending.projection.projection_id,reason,pending.source_revision_id,config.config_hash,canonical_sha256(material))
    return result,event

def mark_missed_close(pending,detected_utc_ms,config):
    if detected_utc_ms<=pending.projection.target_close_utc_ms: raise FPI07Error("FP_CRC_CLOSE_NOT_MISSED","close not yet missed")
    reason="FP_CRC_MISSED_CLOSE_REPLAY_REQUIRED"; state=ConfirmationState.MISSED_CLOSE_REPLAY_REQUIRED
    event=transition(pending.candidate.candidate_id,1,ConfirmationState.PENDING,state,detected_utc_ms,pending.projection.projection_id,reason)
    material={"candidate":pending.candidate.candidate_id,"projection":pending.projection.projection_id,"detected":detected_utc_ms,"config":config.config_hash}
    result=ConfirmationResult(stable_id("FPCONFRES",material,36),pending.candidate.candidate_id,pending.projection.projection_id,ConfirmationOutcome.MISSED_CLOSE_REPLAY_REQUIRED,state,pending.projection.target_host_bar_id,detected_utc_ms,None,pending.projection.projection_id,reason,pending.source_revision_id,config.config_hash,canonical_sha256(material))
    return result,event

def build_snapshot(config,pending,results,transitions,created_utc_ms,source_revision_id):
    pending=tuple(sorted(pending,key=lambda p:p.pending_id)); results=tuple(sorted(results,key=lambda r:r.result_id)); transitions=tuple(sorted(transitions,key=lambda e:(e.candidate_id,e.sequence,e.event_id)))
    signals=tuple(sorted((r.confirmed_signal for r in results if r.confirmed_signal),key=lambda s:s.signal_id))
    result_candidates={r.candidate_id for r in results}; active=tuple(p for p in pending if p.candidate.candidate_id not in result_candidates)
    if any(r.outcome in (ConfirmationOutcome.UNAVAILABLE_AT_CLOSE,ConfirmationOutcome.MISSED_CLOSE_REPLAY_REQUIRED) for r in results): health=EngineHealth.BLOCKED; reasons=("FP_CRC_ENGINE_BLOCKED_REPLAY_OR_DATA",)
    elif active: health=EngineHealth.READY; reasons=("FP_CRC_ENGINE_READY_PENDING",)
    else: health=EngineHealth.READY; reasons=("FP_CRC_ENGINE_READY",)
    material={"config":config.config_hash,"pending":[p.pending_hash for p in active],"results":[r.result_hash for r in results],"signals":[s.signal_hash for s in signals],"events":[e.event_hash for e in transitions],"health":health,"revision":source_revision_id}
    return ConfirmationEngineSnapshot(stable_id("FPCONFSTATE",material,32),config.config_hash,active,results,signals,transitions,health,reasons,source_revision_id,created_utc_ms,canonical_sha256(material))
