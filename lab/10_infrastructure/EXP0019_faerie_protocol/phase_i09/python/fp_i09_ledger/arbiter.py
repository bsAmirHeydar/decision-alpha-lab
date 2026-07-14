from __future__ import annotations
from fp_i02_kernel.enums import QuotaConsumptionPolicy
from .canonical import canonical_sha256,stable_id
from .contracts import QuotaReservation,ArbitrationDecision
from .enums import *
from .eligibility import evaluate_eligibility
from .errors import FPI09Error

def resolve_pair_session(quota_key,contenders,*,evaluated_utc_ms,seal_state=SessionSealState.OPEN,prior_reservation=None):
    unique={}
    blocked=[]
    for c in contenders:
        if c.quota_key.quota_key_id!=quota_key.quota_key_id: raise FPI09Error("FP_LDG_MIXED_QUOTA_KEYS","all contenders must share one quota key")
        old=unique.get(c.signal.signal_id)
        if old and old.contender_hash!=c.contender_hash: raise FPI09Error("FP_LDG_CONTENDER_COLLISION","same signal has different contender payload")
        unique[c.signal.signal_id]=c
    eligible=[]; ww_suppressed=[]
    for c in unique.values():
        out=evaluate_eligibility(c.eligibility)
        if out is EligibilityOutcome.ELIGIBLE: eligible.append(c)
        elif out is EligibilityOutcome.SUPPRESSED_BY_WW: ww_suppressed.append(c.signal.signal_id)
        else: blocked.append(c.signal.signal_id)
    eligible.sort(key=lambda c:c.rank_key)
    reservation=None; winner=""; quota_suppressed=[]; reasons=[]
    if eligible:
        win=eligible[0]; winner=win.signal.signal_id; quota_suppressed=[c.signal.signal_id for c in eligible[1:]]
        generation=1; prior_id=""; event_reason="FP_LDG_QUOTA_RESERVED_EARLIEST_HUNT"
        if prior_reservation:
            if prior_reservation.quota_key.quota_key_id!=quota_key.quota_key_id: raise FPI09Error("FP_LDG_PRIOR_RESERVATION_KEY_MISMATCH","prior reservation key mismatch")
            generation=prior_reservation.generation + (1 if prior_reservation.winner_signal_id!=winner else 0)
            prior_id=prior_reservation.reservation_id
            event_reason="FP_LDG_RESERVATION_STABLE" if prior_reservation.winner_signal_id==winner else "FP_LDG_RESERVATION_SUPERSEDED_BY_EARLIER_HUNT"
        finality=ReservationFinality.FINAL if seal_state is SessionSealState.SEALED else ReservationFinality.PROVISIONAL
        p={"quota_key_id":quota_key.quota_key_id,"winner_signal_id":winner,"winner_contender_id":win.contender_id,"winner_rank_key":win.rank_key,"generation":generation,"reserved_utc_ms":evaluated_utc_ms,"finality":finality.value,"prior_reservation_id":prior_id,"reason_code":event_reason}
        h=canonical_sha256(p); reservation=QuotaReservation(stable_id("FPRS",p),quota_key,ReservationState.RESERVED,finality,winner,win.contender_id,win.rank_key,generation,evaluated_utc_ms,QuotaConsumptionPolicy.UNSET,prior_id,event_reason,h)
        reasons.append(event_reason)
    else: reasons.append("FP_LDG_NO_ELIGIBLE_CONTENDER")
    contender_ids=tuple(c.contender_id for c in eligible)
    suppressed=tuple(sorted(set(quota_suppressed+ww_suppressed)))
    blocked=tuple(sorted(set(blocked)))
    p={"quota_key_id":quota_key.quota_key_id,"seal_state":seal_state.value,"reservation_id":reservation.reservation_id if reservation else "","winner_signal_id":winner,"contender_ids":contender_ids,"suppressed_signal_ids":suppressed,"blocked_signal_ids":blocked,"evaluated_utc_ms":evaluated_utc_ms,"reason_codes":tuple(sorted(set(reasons)))}
    h=canonical_sha256(p); return ArbitrationDecision(stable_id("FPAD",p),quota_key,seal_state,reservation,winner,contender_ids,suppressed,blocked,evaluated_utc_ms,tuple(sorted(set(reasons))),h)

def assert_consumption_forbidden():
    raise FPI09Error("FP_LDG_CONSUMPTION_POLICY_UNSET","FP-DEC-012 is unresolved; CONSUMED/RELEASED transitions are forbidden")
