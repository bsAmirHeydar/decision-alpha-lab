from __future__ import annotations
from copy import deepcopy
from .numerics import mean
from .policy_value import evaluate_policy_values
from .canonical import content_hash

def propensity_clip_sensitivity(crossfit,policy_catalog,baseline_policy_id,grid):
    runs=[]
    for clip in grid:
        x=deepcopy(crossfit)
        for r in x['predictions']:
            p={t:max(clip,v) for t,v in r['propensities'].items()};s=sum(p.values());r['propensities']={t:v/s for t,v in p.items()}
        report=evaluate_policy_values(x,policy_catalog,baseline_policy_id);runs.append({'clip':clip,'values':{p['policy_id']:p['dr_value'] for p in report['policies']}})
    out={'phase':'SAED_V4_18','grid':list(grid),'runs':runs,'sign_stability':{pid:len({v>=0 for v in [r['values'][pid] for r in runs]})==1 for pid in runs[0]['values']}};out['report_hash']=content_hash(out);return out

def hidden_confounder_sensitivity(policy_value_report,bias_grid):
    runs=[]
    for b in bias_grid:runs.append({'absolute_bias':b,'adjusted_lower_bounds':{p['policy_id']:p['multiplicity_adjusted_lower']-b for p in policy_value_report['policies']}})
    out={'phase':'SAED_V4_18','bias_grid':list(bias_grid),'runs':runs,'identification_claim':False};out['report_hash']=content_hash(out);return out

def cost_stress(crossfit,policy_catalog,baseline_policy_id,multipliers):
    costs={crossfit['treatment_ids'][0]:0.0,crossfit['treatment_ids'][1]:0.018,crossfit['treatment_ids'][2]:0.014,crossfit['treatment_ids'][3]:0.022};runs=[]
    for m in multipliers:
        x=deepcopy(crossfit)
        for r in x['predictions']:
            r['observed_outcome']-=costs[r['assigned_treatment']]*(m-1.0)
            r['mu_hat']={t:v-costs[t]*(m-1.0) for t,v in r['mu_hat'].items()}
        report=evaluate_policy_values(x,policy_catalog,baseline_policy_id);runs.append({'cost_multiplier':m,'values':{p['policy_id']:p['dr_value'] for p in report['policies']}})
    out={'phase':'SAED_V4_18','multipliers':list(multipliers),'runs':runs};out['report_hash']=content_hash(out);return out

def environment_transport(policy_value_rows,policy_catalog):
    reports=[]
    for env in sorted(set(r['environment_id'] for r in policy_value_rows['predictions'])):
        x=dict(policy_value_rows);x['predictions']=[r for r in policy_value_rows['predictions'] if r['environment_id']==env]
        report=evaluate_policy_values(x,policy_catalog,policy_catalog['policies'][0]['policy_id'])
        reports.append({'environment_id':env,'row_count':len(x['predictions']),'values':{p['policy_id']:p['dr_value'] for p in report['policies']}})
    out={'phase':'SAED_V4_18','environment_count':len(reports),'environments':reports,'transport_claim':False};out['report_hash']=content_hash(out);return out
