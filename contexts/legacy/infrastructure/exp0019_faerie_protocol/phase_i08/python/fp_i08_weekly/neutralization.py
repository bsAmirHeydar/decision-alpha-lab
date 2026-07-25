from __future__ import annotations
from dataclasses import replace
from fp_i02_kernel.enums import PriceSide
from .canonical import canonical_sha256,stable_id
from .contracts import WWNeutralizationResult,WWTransitionRecord
from .enums import WWLifecycleState,NeutralizationOutcome,WWTransition

def _contact(side,extreme,price): return extreme>=price if side is PriceSide.HIGH else extreme<=price

def apply_neutralization(context,observation,sequence=1):
    outcome=NeutralizationOutcome.UNAFFECTED;reason="FP_WRC_NEUTRALIZATION_UNAFFECTED";updated=context;event=None
    if context.state is not WWLifecycleState.CONFIRMED: reason="FP_WRC_CONTEXT_NOT_ACTIVE"
    elif not observation.data_complete: outcome=NeutralizationOutcome.DATA_BLOCKED;reason="FP_WRC_NEUTRALIZATION_DATA_BLOCKED"
    elif observation.minute_utc_ms<=context.confirmed_utc_ms: outcome=NeutralizationOutcome.TOO_EARLY;reason="FP_WRC_NEUTRALIZATION_BEFORE_CONFIRMATION"
    elif observation.symbol!=context.protected_symbol: outcome=NeutralizationOutcome.WRONG_SYMBOL;reason="FP_WRC_NEUTRALIZATION_WRONG_SYMBOL"
    elif observation.side is not context.side or observation.reference_id!=context.protected_reference_id: outcome=NeutralizationOutcome.WRONG_SIDE;reason="FP_WRC_NEUTRALIZATION_WRONG_REFERENCE"
    elif not _contact(context.side,observation.observed_extreme,context.protected_reference_price): outcome=NeutralizationOutcome.NO_CONTACT;reason="FP_WRC_NEUTRALIZATION_NO_CONTACT"
    else:
        outcome=NeutralizationOutcome.NEUTRALIZED;reason="FP_RC_WW_NEUTRALIZED"
        updated=replace(context,state=WWLifecycleState.NEUTRALIZED,neutralized_utc_ms=observation.minute_utc_ms,neutralizing_hunt_id=observation.observation_id,reason_code=reason,source_revision_id=observation.source_revision_id,context_hash=canonical_sha256({"prior":context.context_hash,"neutralized":observation.evidence_hash,"reason":reason}))
        em={"context":context.ww_context_id,"sequence":sequence,"transition":WWTransition.SECOND_SYMBOL_NEUTRALIZED,"time":observation.minute_utc_ms,"evidence":observation.observation_id}
        event=WWTransitionRecord(stable_id("FPWWEVT",em,32),context.ww_context_id,sequence,WWTransition.SECOND_SYMBOL_NEUTRALIZED,WWLifecycleState.CONFIRMED,WWLifecycleState.NEUTRALIZED,observation.minute_utc_ms,observation.observation_id,reason,canonical_sha256(em))
    mat={"context":context.ww_context_id,"outcome":outcome,"observation":observation.evidence_hash,"updated":updated.context_hash,"reason":reason}
    return WWNeutralizationResult(stable_id("FPWWNEUT",mat,32),context.ww_context_id,outcome,updated,observation.observation_id,reason,canonical_sha256(mat)),event

def expire_context(context,now_utc_ms,sequence=1):
    if context.state is not WWLifecycleState.CONFIRMED or now_utc_ms<context.check_week_end_utc_ms:return context,None
    reason="FP_WRC_WW_CHECK_WEEK_EXPIRED"
    updated=replace(context,state=WWLifecycleState.EXPIRED,expired_utc_ms=now_utc_ms,reason_code=reason,context_hash=canonical_sha256({"prior":context.context_hash,"expired":now_utc_ms}))
    em={"context":context.ww_context_id,"sequence":sequence,"transition":WWTransition.WEEK_EXPIRED,"time":now_utc_ms}
    evt=WWTransitionRecord(stable_id("FPWWEVT",em,32),context.ww_context_id,sequence,WWTransition.WEEK_EXPIRED,WWLifecycleState.CONFIRMED,WWLifecycleState.EXPIRED,now_utc_ms,context.source_signal.signal_id,reason,canonical_sha256(em))
    return updated,evt
