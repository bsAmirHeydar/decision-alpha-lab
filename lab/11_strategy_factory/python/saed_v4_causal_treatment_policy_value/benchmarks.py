from __future__ import annotations
import math
from .numerics import mean,std,normal_lcb
from .canonical import content_hash

def estimator_scorecard(crossfit,ate_report,baseline_treatment):
    rows=crossfit['predictions'];treatments=crossfit['treatment_ids'];methods=[]
    dim=[]
    base_obs=[r['observed_outcome'] for r in rows if r['assigned_treatment']==baseline_treatment]
    for t in treatments:
        obs=[r['observed_outcome'] for r in rows if r['assigned_treatment']==t];dim.append({'treatment_id':t,'estimate':mean(obs)-mean(base_obs)})
    methods.append({'estimator_id':'est_dim','algorithm':'difference_in_means','effects':dim,'cross_fitted':False,'orthogonal':False})
    for key,eid,alg in [('mu_s_hat','est_s_learner','s_learner_ridge'),('mu_hat','est_t_learner','t_learner_ridge')]:
        effects=[]
        for t in treatments:
            d=[r[key][t]-r[key][baseline_treatment] for r in rows];se=std(d)/math.sqrt(len(d));effects.append({'treatment_id':t,'estimate':mean(d),'standard_error':se,'lower_95':normal_lcb(mean(d),se)})
        methods.append({'estimator_id':eid,'algorithm':alg,'effects':effects,'cross_fitted':True,'orthogonal':False})
    methods.append({'estimator_id':'est_aipw_dr','algorithm':'aipw_dr','effects':ate_report['effects'],'cross_fitted':True,'orthogonal':True})
    r_effects=[]
    for t in treatments:
        if t==baseline_treatment:r_effects.append({'treatment_id':t,'estimate':0.0,'standard_error':0.0,'lower_95':0.0});continue
        pseudo=[]
        for r in rows:
            pa=r['propensities'][t];pb=r['propensities'][baseline_treatment]
            score=(1.0 if r['assigned_treatment']==t else 0.0-pa)*(r['observed_outcome']-r['mu_hat'][r['assigned_treatment']])-(1.0 if r['assigned_treatment']==baseline_treatment else 0.0-pb)*(r['observed_outcome']-r['mu_hat'][r['assigned_treatment']])
            pseudo.append(score)
        se=std(pseudo)/math.sqrt(len(pseudo));r_effects.append({'treatment_id':t,'estimate':mean(pseudo),'standard_error':se,'lower_95':normal_lcb(mean(pseudo),se)})
    methods.append({'estimator_id':'est_r_learner','algorithm':'r_learner_linear_reference_score','effects':r_effects,'cross_fitted':True,'orthogonal':True})
    out={'phase':'SAED_V4_18','baseline_treatment_id':baseline_treatment,'methods':methods,'baseline_preserved':True,'selection_basis':'aipw_dr_only_for_reference_tournament'};out['report_hash']=content_hash(out);return out
