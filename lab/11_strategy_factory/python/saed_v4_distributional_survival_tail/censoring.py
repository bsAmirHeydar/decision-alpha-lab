from __future__ import annotations
from .canonical import content_hash,stable_id
from .numerics import clamp,safe_div

def audit(dataset,registry,policy):
    rows=dataset['rows'];viol=[]
    for r in rows:
        if r['event_cause'] not in set(registry.causes)|{registry.censor_label}:viol.append({'row_id':r['row_id'],'violation':'unknown_cause'})
        if not r['event_observed'] and r['event_cause']!=registry.censor_label:viol.append({'row_id':r['row_id'],'violation':'censored_cause_mismatch'})
        if r['event_observed'] and r['event_cause']==registry.censor_label:viol.append({'row_id':r['row_id'],'violation':'observed_marked_censored'})
        if r['interval_lower_seconds']>r['event_duration_seconds'] or r['event_duration_seconds']>r['interval_upper_seconds']:viol.append({'row_id':r['row_id'],'violation':'interval_not_covering_event'})
        if r['feature_known_time']>r['context_time'] or r['outcome_known_time']<r['context_time']:viol.append({'row_id':r['row_id'],'violation':'known_time_order'})
    out={'phase':'SAED_V4_16','row_count':len(rows),'observed_count':sum(r['event_observed'] for r in rows),'right_censored_count':sum(not r['event_observed'] for r in rows),'interval_censored_count':sum(r['interval_lower_seconds']!=r['interval_upper_seconds'] for r in rows),'censored_as_outcome_count':sum((not r['event_observed']) and r['outcome_observed'] for r in rows),'violation_count':len(viol),'violations':viol,'passed':not viol and not any((not r['event_observed']) and r['outcome_observed'] for r in rows),'censoring_policy_version':policy.exact_version}
    out['audit_hash']=content_hash(out);return out

def censor_survival(rows,horizons):
    # Kaplan-Meier estimate of G(t)=P(not censored by t), with event=administrative/observational censoring.
    result=[];surv=1.0
    for h in horizons:
        at=sum(r['event_duration_seconds']>=h for r in rows);d=sum((not r['event_observed']) and r['event_duration_seconds']<=h and r['event_duration_seconds']>=(0 if not result else result[-1]['horizon_seconds']) for r in rows)
        if at:surv*=max(0.0,1-d/at)
        result.append({'horizon_seconds':h,'at_risk':at,'censor_events':d,'censor_survival':surv})
    return result

def ipcw(dataset,model_config,policy):
    train=[r for r in dataset['rows'] if r['split']=='train'];g=censor_survival(train,model_config.horizons_seconds);items=[]
    for r in dataset['rows']:
        nearest=min(g,key=lambda x:abs(x['horizon_seconds']-r['event_duration_seconds']))
        raw=1/max(policy.ipcw_floor,nearest['censor_survival']);weight=clamp(raw,1/policy.ipcw_ceiling,policy.ipcw_ceiling)
        items.append({'row_id':r['row_id'],'split':r['split'],'duration_seconds':r['event_duration_seconds'],'censor_survival':nearest['censor_survival'],'raw_weight':raw,'ipcw_weight':weight,'clipped':weight!=raw})
    out={'phase':'SAED_V4_16','method':'kaplan_meier_inverse_probability_of_censoring','floor':policy.ipcw_floor,'ceiling':policy.ipcw_ceiling,'item_count':len(items),'clipped_count':sum(x['clipped'] for x in items),'items':items};out['ledger_hash']=content_hash(out);return out
