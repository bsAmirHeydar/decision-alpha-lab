from __future__ import annotations
from .canonical import content_hash
from .numerics import mean

def quantile_crossing(distribution_predictions):
    rows=[]
    for p in distribution_predictions['items']:
        rows.append({'candidate_id':p['candidate_id'],'row_id':p['row_id'],'crossing_before_projection':p['quantile_crossing_before_projection'],'crossing_after_projection':p['quantile_crossing_after_projection'],'monotone_after_projection':not p['quantile_crossing_after_projection']})
    out={'phase':'SAED_V4_16','row_count':len(rows),'crossing_before_count':sum(x['crossing_before_projection'] for x in rows),'crossing_after_count':sum(x['crossing_after_projection'] for x in rows),'all_monotone_after_projection':all(x['monotone_after_projection'] for x in rows),'rows':rows};out['report_hash']=content_hash(out);return out

def competing_risk_simplex(survival_predictions):
    rows=[]
    for p in survival_predictions['items']:
        max_total=max(sum(p['cause_cumulative_incidence'][c][k] for c in p['cause_cumulative_incidence']) for k in range(len(p['horizons_seconds'])))
        rows.append({'candidate_id':p['candidate_id'],'row_id':p['row_id'],'maximum_cumulative_incidence_sum':max_total,'minimum_survival_probability':min(p['survival_probability']),'simplex_valid':max_total<=1+1e-12 and min(p['survival_probability'])>=-1e-12})
    out={'phase':'SAED_V4_16','row_count':len(rows),'all_simplex_valid':all(x['simplex_valid'] for x in rows),'rows':rows};out['report_hash']=content_hash(out);return out
