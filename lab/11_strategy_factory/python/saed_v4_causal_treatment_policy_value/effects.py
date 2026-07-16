from __future__ import annotations
import math
from .numerics import mean,std,quantile,normal_lcb,ridge_fit,predict
from .canonical import content_hash

def dr_potential_score(row,treatment):
    mu=row['mu_hat'][treatment];p=max(1e-9,row['propensities'][treatment]);return mu+(1.0 if row['assigned_treatment']==treatment else 0.0)/p*(row['observed_outcome']-mu)

def estimate_ate(crossfit,baseline_treatment):
    rows=crossfit['predictions'];treatments=crossfit['treatment_ids'];scores={t:[dr_potential_score(r,t) for r in rows] for t in treatments};base=scores[baseline_treatment];effects=[]
    for t in treatments:
        dif=[a-b for a,b in zip(scores[t],base)];se=std(dif)/math.sqrt(len(dif)) if dif else 0.0
        effects.append({'treatment_id':t,'estimate':mean(dif),'standard_error':se,'lower_95':normal_lcb(mean(dif),se),'upper_95':mean(dif)+1.96*se,'row_count':len(dif),'estimand':'ATE_vs_baseline'})
    out={'phase':'SAED_V4_18','baseline_treatment_id':baseline_treatment,'estimator':'cross_fitted_aipw_dr','effects':effects,'synthetic_only':True};out['report_hash']=content_hash(out);return out

def fit_cate_models(crossfit,baseline_treatment,ridge=0.02):
    rows=crossfit['predictions'];models={};summary=[]
    for t in crossfit['treatment_ids']:
        if t==baseline_treatment:continue
        pseudo=[dr_potential_score(r,t)-dr_potential_score(r,baseline_treatment) for r in rows];beta=ridge_fit([r['features'] for r in rows],pseudo,ridge);pred=[predict(beta,r['features']) for r in rows]
        models[t]=beta;summary.append({'treatment_id':t,'mean_predicted_effect':mean(pred),'p10':quantile(pred,0.1),'p50':quantile(pred,0.5),'p90':quantile(pred,0.9),'positive_share':mean([1.0 if v>0 else 0.0 for v in pred]),'coefficient_count':len(beta)})
    out={'phase':'SAED_V4_18','baseline_treatment_id':baseline_treatment,'algorithm':'cross_fitted_dr_pseudo_outcome_linear_cate','models':models,'summary':summary,'synthetic_only':True};out['report_hash']=content_hash(out);return out

def predict_cate(cate_report,row,treatment):
    if treatment==cate_report['baseline_treatment_id']:return 0.0
    return predict(cate_report['models'][treatment],row['features'])

def subgroup_effects(crossfit,cate_report):
    reports=[]
    for feature_idx,feature in enumerate(['context_strength','liquidity_state','volatility_state','execution_friction','structure_state','tail_risk']):
        vals=sorted(r['features'][feature_idx] for r in crossfit['predictions']);cut=vals[len(vals)//2]
        for label,predicate in [('low',lambda x:x<=cut),('high',lambda x:x>cut)]:
            rows=[r for r in crossfit['predictions'] if predicate(r['features'][feature_idx])]
            effects={t:mean([predict_cate(cate_report,r,t) for r in rows]) for t in cate_report['models']}
            reports.append({'feature':feature,'subgroup':label,'threshold':cut,'row_count':len(rows),'mean_predicted_effects':effects})
    out={'phase':'SAED_V4_18','subgroup_count':len(reports),'subgroups':reports};out['report_hash']=content_hash(out);return out
