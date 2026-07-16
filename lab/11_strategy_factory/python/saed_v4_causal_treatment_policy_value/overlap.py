from __future__ import annotations
from .numerics import mean,quantile,effective_sample_size
from .canonical import content_hash

def overlap_audit(crossfit,overlap_floor,min_ess):
    treatments=[]
    for t in crossfit['treatment_ids']:
        ps=[r['propensities'][t] for r in crossfit['predictions']];weights=[1.0/r['propensities'][t] for r in crossfit['predictions'] if r['assigned_treatment']==t]
        treatments.append({'treatment_id':t,'min':min(ps),'p01':quantile(ps,0.01),'p10':quantile(ps,0.10),'median':quantile(ps,0.5),'p90':quantile(ps,0.9),'max':max(ps),'below_floor_share':mean([1.0 if p<overlap_floor else 0.0 for p in ps]),'effective_sample_size':effective_sample_size(weights),'passed':effective_sample_size(weights)>=min_ess})
    out={'phase':'SAED_V4_18','overlap_floor':overlap_floor,'minimum_effective_sample_size':min_ess,'treatments':treatments,'passed':all(x['passed'] for x in treatments),'fallback':'abstain_to_skip_on_unsupported_rows'};out['report_hash']=content_hash(out);return out
