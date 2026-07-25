from __future__ import annotations
from .canonical import content_hash
from .numerics import mean,safe_div

def time_calibration(survival_predictions,dataset):
    actual={r['row_id']:r for r in dataset['rows'] if r['split']=='selection_validation'};by={}
    for p in survival_predictions['items']:by.setdefault(p['candidate_id'],[]).append(p)
    rows=[]
    for cid,preds in by.items():
        horizons=preds[0]['horizons_seconds']
        for k,h in enumerate(horizons):
            pred=mean([1-p['survival_probability'][k] for p in preds]);obs=mean([actual[p['row_id']]['event_duration_seconds']<=h for p in preds]);rows.append({'candidate_id':cid,'horizon_seconds':h,'predicted_event_probability':pred,'observed_event_rate':obs,'absolute_calibration_error':abs(pred-obs),'evaluation_count':len(preds)})
    out={'phase':'SAED_V4_16','row_count':len(rows),'rows':rows};out['report_hash']=content_hash(out);return out

def distribution_calibration(distribution_predictions,dataset):
    actual={r['row_id']:r['net_r'] for r in dataset['rows'] if r['split']=='selection_validation' and r['outcome_observed']};rows=[];by={}
    for p in distribution_predictions['items']:by.setdefault(p['candidate_id'],[]).append(p)
    for cid,preds in by.items():
        for idx,q in enumerate(preds[0]['quantile_levels']):
            usable=[p for p in preds if p['row_id'] in actual];obs=mean([actual[p['row_id']]<=p['monotone_quantiles'][idx] for p in usable]);rows.append({'candidate_id':cid,'quantile_level':q,'observed_below_rate':obs,'absolute_calibration_error':abs(obs-q),'evaluation_count':len(usable)})
    out={'phase':'SAED_V4_16','row_count':len(rows),'rows':rows};out['report_hash']=content_hash(out);return out
