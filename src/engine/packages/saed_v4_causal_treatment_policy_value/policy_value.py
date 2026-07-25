from __future__ import annotations
import math
from .numerics import mean,std,effective_sample_size,normal_lcb,cvar_lower
from .canonical import content_hash

def _value_scores(rows,assignments,outcome_field='observed_outcome'):
    amap={x['row_id']:x['selected_treatment'] for x in assignments};dm=[];ipw=[];dr=[];weights=[];matched=0
    for r in rows:
        t=amap[r['row_id']];mu=r['mu_hat'][t];p=max(1e-9,r['propensities'][t]);match=r['assigned_treatment']==t
        d=mu;i=(r[outcome_field]/p if match else 0.0);q=mu+((r[outcome_field]-mu)/p if match else 0.0)
        dm.append(d);ipw.append(i);dr.append(q)
        if match:matched+=1;weights.append(1.0/p)
    return dm,ipw,dr,weights,matched

def evaluate_policy_values(crossfit,policy_catalog,baseline_policy_id,alpha=0.1):
    rows=crossfit['predictions'];results=[]
    for p in policy_catalog['policies']:
        dm,ipw,dr,weights,matched=_value_scores(rows,p['assignments']);se=std(dr)/math.sqrt(len(dr)) if dr else 0.0
        results.append({'policy_id':p['policy_id'],'direct_method_value':mean(dm),'ipw_value':mean(ipw),'dr_value':mean(dr),'standard_error':se,'lower_95':normal_lcb(mean(dr),se),'multiplicity_adjusted_lower':normal_lcb(mean(dr),se,2.58),'lower_tail_cvar_10':cvar_lower(dr,alpha),'matched_rows':matched,'support_rate':matched/len(rows) if rows else 0.0,'effective_sample_size':effective_sample_size(weights),'row_count':len(rows)})
    base=next(x for x in results if x['policy_id']==baseline_policy_id)
    for x in results:x['incremental_dr_vs_baseline']=x['dr_value']-base['dr_value'];x['incremental_lcb_vs_baseline']=x['multiplicity_adjusted_lower']-base['multiplicity_adjusted_lower']
    out={'phase':'SAED_V4_18','estimator':'chronological_cluster_aware_cross_fitted_aipw_dr','baseline_policy_id':baseline_policy_id,'policies':results,'synthetic_only':True,'policy_authority':False};out['report_hash']=content_hash(out);return out

def negative_control_policy_value(crossfit,policy_catalog):
    rows=[]
    for r in crossfit['predictions']:
        q=dict(r);q['observed_outcome']=r['negative_control_outcome'];q['mu_hat']={t:0.0 for t in crossfit['treatment_ids']};rows.append(q)
    fake=dict(crossfit);fake['predictions']=rows
    report=evaluate_policy_values(fake,policy_catalog,policy_catalog['policies'][0]['policy_id'])
    values=[abs(x['dr_value']) for x in report['policies']]
    out={'phase':'SAED_V4_18','test':'negative_control_outcome_policy_value','policy_values':report['policies'],'maximum_absolute_value':max(values),'threshold':0.18,'passed':max(values)<0.18};out['report_hash']=content_hash(out);return out
