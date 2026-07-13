from __future__ import annotations
from fp_i02_kernel.enums import PriceSide,Direction
from dataclasses import replace
from .canonical import canonical_sha256,stable_id
from .contracts import FirstSweepClassification,RawDivergenceCandidate,CandidateTransitionRecord
from .enums import ContactState,SweepOutcome,CandidateState,CandidateTransition
from .errors import FPI06Error

def classify_first_sweep(plan,observations):
    for obs in observations:
        if obs.contact_state is ContactState.DATA_BLOCKED:
            material={'plan':plan.side_plan_id,'outcome':SweepOutcome.DATA_BLOCKED,'minute':obs.minute_utc_ms,'observation':obs.evidence_hash}
            return FirstSweepClassification(stable_id('FPSWEEP',material,32),plan.side_plan_id,plan.relation_instance_id,SweepOutcome.DATA_BLOCKED,None,'','','',(),obs.minute_utc_ms,'FP_HRC_CLASSIFICATION_DATA_BLOCKED',canonical_sha256(material))
        if obs.contact_state is ContactState.BOTH_SAME_M1:
            ids=tuple(sorted((obs.left_hunt_fact_id,obs.right_hunt_fact_id)))
            material={'plan':plan.side_plan_id,'outcome':SweepOutcome.SYMMETRIC_SAME_M1,'minute':obs.minute_utc_ms,'facts':ids}
            return FirstSweepClassification(stable_id('FPSWEEP',material,32),plan.side_plan_id,plan.relation_instance_id,SweepOutcome.SYMMETRIC_SAME_M1,obs.minute_utc_ms,'','','',ids,None,'FP_HRC_CLASSIFICATION_SYMMETRIC_SAME_M1',canonical_sha256(material))
        if obs.contact_state in (ContactState.LEFT_ONLY,ContactState.RIGHT_ONLY):
            left=obs.contact_state is ContactState.LEFT_ONLY
            outcome=SweepOutcome.LEFT_FIRST if left else SweepOutcome.RIGHT_FIRST
            hunter=plan.left_symbol if left else plan.right_symbol;protected=plan.right_symbol if left else plan.left_symbol;fact=obs.left_hunt_fact_id if left else obs.right_hunt_fact_id
            material={'plan':plan.side_plan_id,'outcome':outcome,'minute':obs.minute_utc_ms,'hunter':hunter,'protected':protected,'fact':fact}
            return FirstSweepClassification(stable_id('FPSWEEP',material,32),plan.side_plan_id,plan.relation_instance_id,outcome,obs.minute_utc_ms,hunter,protected,fact,(),None,'FP_HRC_CLASSIFICATION_ASYMMETRIC_FIRST_SWEEP',canonical_sha256(material))
    material={'plan':plan.side_plan_id,'outcome':SweepOutcome.NO_CONTACT,'observation_count':len(observations)}
    return FirstSweepClassification(stable_id('FPSWEEP',material,32),plan.side_plan_id,plan.relation_instance_id,SweepOutcome.NO_CONTACT,None,'','','',(),None,'FP_HRC_CLASSIFICATION_NO_CONTACT',canonical_sha256(material))

def create_candidate(plan,classification,source_revision_id):
    if classification.outcome not in (SweepOutcome.LEFT_FIRST,SweepOutcome.RIGHT_FIRST):return None,()
    direction=Direction.BULLISH if plan.side is PriceSide.LOW else Direction.BEARISH
    material={'side_plan':plan.semantic_hash,'relation_instance':plan.relation_instance_id,'relation':plan.relation,'direction':direction,'side':plan.side,'hunter':classification.hunter_symbol,'protected':classification.protected_symbol,'first_hunt':classification.first_hunt_minute_utc_ms,'hunt_fact':classification.hunter_hunt_fact_id,'check_end':plan.check_end_utc_ms,'revision':source_revision_id}
    sem=canonical_sha256(material);cid=stable_id('FPCAND',material,32)
    candidate=RawDivergenceCandidate(cid,plan.side_plan_id,plan.relation_instance_id,plan.relation,direction,plan.side,classification.hunter_symbol,classification.protected_symbol,classification.first_hunt_minute_utc_ms,classification.hunter_hunt_fact_id,CandidateState.RAW_ACTIVE,0,None,'',plan.check_end_utc_ms,source_revision_id,'FP_HRC_RAW_CANDIDATE_CREATED',sem)
    event_material={'candidate':cid,'sequence':0,'transition':CandidateTransition.CREATED,'next':CandidateState.RAW_ACTIVE,'time':classification.first_hunt_minute_utc_ms,'evidence':classification.classification_id}
    event=CandidateTransitionRecord(stable_id('FPCANDEVT',event_material,32),cid,0,CandidateTransition.CREATED,None,CandidateState.RAW_ACTIVE,classification.first_hunt_minute_utc_ms,classification.classification_id,'FP_HRC_RAW_CANDIDATE_CREATED',canonical_sha256(event_material))
    return candidate,(event,)

def reduce_candidate(candidate,observation,hunt_facts):
    if candidate.state is not CandidateState.RAW_ACTIVE:return candidate,None
    if observation.minute_utc_ms<=candidate.first_hunt_minute_utc_ms:return candidate,None
    if observation.contact_state is ContactState.DATA_BLOCKED:
        transition=CandidateTransition.DATA_INVALIDATED;nxt=CandidateState.INVALID_DATA;reason='FP_HRC_CANDIDATE_DATA_INVALIDATED';evidence=observation.observation_id;second=None;fact=''
    else:
        protected_fact=next((f for f in hunt_facts if f.canonical_symbol==candidate.protected_symbol),None)
        if protected_fact is None:return candidate,None
        transition=CandidateTransition.SECOND_TOUCH_CANCELLED;nxt=CandidateState.CANCELLED_SECOND_TOUCH;reason='FP_HRC_CANDIDATE_CANCELLED_SECOND_TOUCH';evidence=protected_fact.hunt_fact_id;second=observation.minute_utc_ms;fact=protected_fact.hunt_fact_id
    seq=candidate.state_sequence+1
    material={'candidate':candidate.candidate_id,'sequence':seq,'transition':transition,'prior':candidate.state,'next':nxt,'time':observation.minute_utc_ms,'evidence':evidence}
    event=CandidateTransitionRecord(stable_id('FPCANDEVT',material,32),candidate.candidate_id,seq,transition,candidate.state,nxt,observation.minute_utc_ms,evidence,reason,canonical_sha256(material))
    return replace(candidate,state=nxt,state_sequence=seq,second_touch_minute_utc_ms=second,second_touch_fact_id=fact,reason_code=reason),event

def close_candidate_at_window(candidate):
    if candidate.state is not CandidateState.RAW_ACTIVE:return candidate,None
    seq=candidate.state_sequence+1;material={'candidate':candidate.candidate_id,'sequence':seq,'transition':CandidateTransition.WINDOW_ENDED,'prior':candidate.state,'next':CandidateState.CHECK_WINDOW_ENDED,'time':candidate.check_end_utc_ms}
    event=CandidateTransitionRecord(stable_id('FPCANDEVT',material,32),candidate.candidate_id,seq,CandidateTransition.WINDOW_ENDED,candidate.state,CandidateState.CHECK_WINDOW_ENDED,candidate.check_end_utc_ms,candidate.side_plan_id,'FP_HRC_CHECK_WINDOW_ENDED',canonical_sha256(material))
    return replace(candidate,state=CandidateState.CHECK_WINDOW_ENDED,state_sequence=seq,reason_code='FP_HRC_CHECK_WINDOW_ENDED'),event
