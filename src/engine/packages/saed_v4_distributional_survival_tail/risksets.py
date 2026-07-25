from __future__ import annotations
from .canonical import content_hash

def build(dataset,registry,config):
    rows=[]
    for split in ['train','calibration','selection_validation']:
        subset=[r for r in dataset['rows'] if r['split']==split]
        for h in config.horizons_seconds:
            at=sum(r['event_duration_seconds']>=h for r in subset);events={c:sum(r['event_observed'] and r['event_cause']==c and r['event_duration_seconds']<=h for r in subset) for c in registry.causes};cens=sum((not r['event_observed']) and r['event_duration_seconds']<=h for r in subset)
            rows.append({'split':split,'horizon_seconds':h,'at_risk':at,'observed_events':sum(events.values()),'censored':cens,'cause_events':events,'risk_set_empty':at==0})
    out={'phase':'SAED_V4_16','time_origin':'context_detection_time','horizons_seconds':list(config.horizons_seconds),'row_count':len(rows),'all_risk_sets_nonnegative':all(x['at_risk']>=0 for x in rows),'empty_risk_set_count':sum(x['risk_set_empty'] for x in rows),'rows':rows};out['ledger_hash']=content_hash(out);return out
