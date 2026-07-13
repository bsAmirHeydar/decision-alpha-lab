from __future__ import annotations
from dataclasses import replace
from fp_i02_kernel.enums import PriceSide,ReferenceState
from .canonical import canonical_sha256,stable_id
from .contracts import ReferenceLevel,ReferenceSet,ReferenceTransitionRecord
from .enums import WindowBuildState,ReferenceTransition,TouchActor
from .errors import FPI05Error

def derive_reference_set(pair_window,created_utc_ms:int):
    refs=[]
    for agg in (pair_window.left,pair_window.right):
        if agg.state is not WindowBuildState.COMPLETE: raise FPI05Error('FP_RRC_REFERENCE_SOURCE_NOT_COMPLETE','references require completed symbol window',{'symbol':agg.canonical_symbol,'state':str(agg.state)})
        for side,price,extreme in ((PriceSide.HIGH,agg.high,agg.high_utc_ms),(PriceSide.LOW,agg.low,agg.low_utc_ms)):
            material={'pair_id':pair_window.descriptor.pair_id,'symbol':agg.canonical_symbol,'side':side,'price':price,'extreme':extreme,'source_pair_window_id':pair_window.pair_window_id,'source_descriptor_id':pair_window.descriptor.descriptor_id,'kind':pair_window.descriptor.kind,'trading_date':pair_window.descriptor.trading_date,'week_id':pair_window.descriptor.week_id,'revision':pair_window.source_revision_id}
            sem=canonical_sha256(material); rid=stable_id('FPREF',material,32)
            refs.append(ReferenceLevel(rid,pair_window.descriptor.pair_id,agg.canonical_symbol,side,price,extreme,pair_window.pair_window_id,pair_window.descriptor.descriptor_id,pair_window.descriptor.kind,pair_window.descriptor.trading_date,pair_window.descriptor.week_id,pair_window.source_revision_id,ReferenceState.FRESH,0,created_utc_ms,created_utc_ms,'FP_RRC_REFERENCE_CREATED',sem))
    refs=tuple(sorted(refs,key=lambda r:(r.canonical_symbol,r.side.value)))
    material={'pair_window_id':pair_window.pair_window_id,'refs':[r.semantic_hash for r in refs],'revision':pair_window.source_revision_id}
    return ReferenceSet(stable_id('FPREFSET',material,32),pair_window.pair_window_id,refs,pair_window.source_revision_id,canonical_sha256(material))

def transition_reference(reference:ReferenceLevel,transition:ReferenceTransition,event_utc_ms:int,evidence_id:str,actor:TouchActor|None=None):
    if event_utc_ms < reference.last_transition_utc_ms or event_utc_ms % 60_000:
        raise FPI05Error('FP_RRC_REFERENCE_EVENT_TIME_INVALID','reference event must be monotonic UTC M1')
    prior=reference.state
    if transition is ReferenceTransition.HUNTER_TOUCH_OBSERVED:
        if actor is not TouchActor.HUNTER or prior not in (ReferenceState.FRESH,ReferenceState.HUNTER_SEEN): raise FPI05Error('FP_RRC_REFERENCE_TRANSITION_ILLEGAL','invalid hunter transition')
        nxt=ReferenceState.HUNTER_SEEN;reason='FP_RRC_HUNTER_TOUCH_NONCONSUMING'
    elif transition is ReferenceTransition.PROTECTED_TOUCH_CONSUMED:
        if actor is not TouchActor.PROTECTED or prior not in (ReferenceState.FRESH,ReferenceState.HUNTER_SEEN): raise FPI05Error('FP_RRC_REFERENCE_TRANSITION_ILLEGAL','invalid protected transition')
        nxt=ReferenceState.CONSUMED_BY_PROTECTED_TOUCH;reason='FP_RRC_REFERENCE_CONSUMED_BY_PROTECTED'
    elif transition is ReferenceTransition.EXPIRED:
        if prior not in (ReferenceState.FRESH,ReferenceState.HUNTER_SEEN): raise FPI05Error('FP_RRC_REFERENCE_TRANSITION_ILLEGAL','invalid expiry transition')
        nxt=ReferenceState.EXPIRED;reason='FP_RRC_REFERENCE_EXPIRED'
    elif transition is ReferenceTransition.SUPERSEDED:
        if prior in (ReferenceState.EXPIRED,ReferenceState.SUPERSEDED): raise FPI05Error('FP_RRC_REFERENCE_TRANSITION_ILLEGAL','invalid supersede transition')
        nxt=ReferenceState.SUPERSEDED;reason='FP_RRC_REFERENCE_SUPERSEDED'
    else: raise FPI05Error('FP_RRC_REFERENCE_TRANSITION_ILLEGAL','unsupported transition')
    seq=reference.state_sequence+1
    material={'reference_id':reference.reference_id,'sequence':seq,'transition':transition,'prior':prior,'next':nxt,'actor':actor,'event_utc_ms':event_utc_ms,'evidence_id':evidence_id}
    event_hash=canonical_sha256(material); event=ReferenceTransitionRecord(stable_id('FPREFEVT',material,32),reference.reference_id,seq,transition,prior,nxt,actor,event_utc_ms,evidence_id,reason,event_hash)
    updated=replace(reference,state=nxt,state_sequence=seq,last_transition_utc_ms=event_utc_ms,reason_code=reason)
    return updated,event
