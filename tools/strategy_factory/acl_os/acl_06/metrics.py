from __future__ import annotations
from typing import Any
from .canonical import with_digest

def evaluate_segment(candidate:dict[str,Any],rows:list[dict[str,Any]],segment:str,lane:str,evaluator)->dict[str,Any]:
    observations=[]
    for r in rows:
        if r['segment']!=segment or not r['label_mature']: continue
        d=evaluator(candidate,r,lane); direction=d['direction']; correct=None; signed=None
        if direction is not None:
            correct=(r['primary_label']=='UP') if direction==1 else (r['primary_label']=='NOT_UP')
            signed=float(r['forward_delta'])*direction
        observations.append({'event_time':r['event_time'],'symbol':r['symbol'],'decision':d['decision'],'direction':direction,'primary_label':r['primary_label'],'correct':correct,'signed_forward_delta':signed,'diagnostic_mae':r['diagnostic_mae'] if lane=='DIAGNOSTIC' else None})
    signals=[o for o in observations if o['direction'] is not None]; correct=sum(1 for o in signals if o['correct']); support=len(observations)
    body={'schema_version':'1.0.0','setup_id':candidate['setup_id'],'candidate_id':candidate['candidate_id'],'candidate_digest':candidate['candidate_digest'],'lane':lane,'segment':segment,'support':support,'signals':len(signals),'abstentions':sum(1 for o in observations if o['decision']=='ABSTAIN'),'cancellations':sum(1 for o in observations if o['decision']=='CANCEL'),'no_signal':sum(1 for o in observations if o['decision']=='NO_SIGNAL'),'correct':correct,'incorrect':len(signals)-correct,'coverage':(len(signals)/support if support else None),'accuracy':(correct/len(signals) if signals else None),'mean_signed_forward_delta':(sum(o['signed_forward_delta'] for o in signals)/len(signals) if signals else None),'observations':observations,'descriptive_only':True,'alpha_claim_allowed':False,'selectable_for_promotion':lane!='DIAGNOSTIC'}
    return with_digest(body,'segment_result_digest')
def aggregate_candidate(candidate:dict[str,Any],segments:list[dict[str,Any]],lane:str)->dict[str,Any]:
    support=sum(x['support'] for x in segments); signals=sum(x['signals'] for x in segments); correct=sum(x['correct'] for x in segments)
    signed=[o['signed_forward_delta'] for x in segments for o in x['observations'] if o['signed_forward_delta'] is not None]
    body={'schema_version':'1.0.0','setup_id':candidate['setup_id'],'candidate_id':candidate['candidate_id'],'candidate_digest':candidate['candidate_digest'],'behavior_digest':candidate['behavior_digest'],'origin':candidate['origin'],'lane':lane,'segment_result_digests':[x['segment_result_digest'] for x in sorted(segments,key=lambda z:z['segment'])],'support':support,'signals':signals,'correct':correct,'incorrect':signals-correct,'coverage':(signals/support if support else None),'accuracy':(correct/signals if signals else None),'mean_signed_forward_delta':(sum(signed)/len(signed) if signed else None),'descriptive_only':True,'validation_status':'NOT_VALIDATED','alpha_claim_allowed':False,'promotion_allowed':False,'diagnostic_selectable':False if lane=='DIAGNOSTIC' else None}
    return with_digest(body,'candidate_result_digest')
