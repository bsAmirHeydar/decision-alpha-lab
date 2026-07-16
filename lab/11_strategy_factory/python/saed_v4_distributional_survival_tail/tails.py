from __future__ import annotations
from .canonical import content_hash
from .numerics import quantile,mean,safe_div

def summarize(dataset,config):
    rows=[]
    for split in ['train','calibration','selection_validation']:
        vals=[r['net_r'] for r in dataset['rows'] if r['split']==split and r['outcome_observed']]
        for level in config.tail_levels:
            var=quantile(vals,level);tail=[x for x in vals if x<=var];es=mean(tail) if tail else var
            rows.append({'split':split,'tail_level':level,'effective_samples':len(vals),'tail_samples':len(tail),'value_at_risk':var,'expected_shortfall':es,'tail_probability_empirical':safe_div(len(tail),len(vals)),'sufficient_samples':len(vals)>=config.min_tail_effective_samples})
    out={'phase':'SAED_V4_16','row_count':len(rows),'rows':rows};out['report_hash']=content_hash(out);return out

def calibration(distribution_predictions,dataset,config):
    actual={r['row_id']:r['net_r'] for r in dataset['rows'] if r['split']=='selection_validation' and r['outcome_observed']};rows=[]
    by={}
    for p in distribution_predictions['items']:by.setdefault(p['candidate_id'],[]).append(p)
    for cid,preds in by.items():
        usable=[p for p in preds if p['row_id'] in actual]
        for level in config.tail_levels:
            idx=min(range(len(config.quantiles)),key=lambda i:abs(config.quantiles[i]-level));vars=[p['monotone_quantiles'][idx] for p in usable];exceed=[actual[p['row_id']]<=v for p,v in zip(usable,vars)];tail_actual=[actual[p['row_id']] for p,v in zip(usable,vars) if actual[p['row_id']]<=v]
            rows.append({'candidate_id':cid,'tail_level':level,'evaluation_count':len(usable),'predicted_var_mean':mean(vars),'observed_exceedance_rate':safe_div(sum(exceed),len(exceed)),'exceedance_error':abs(safe_div(sum(exceed),len(exceed))-level),'observed_expected_shortfall':mean(tail_actual),'sufficient_samples':len(usable)>=config.min_tail_effective_samples})
    out={'phase':'SAED_V4_16','row_count':len(rows),'calibration_split':'selection_validation','rows':rows};out['report_hash']=content_hash(out);return out
