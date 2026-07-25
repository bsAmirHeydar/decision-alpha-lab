from dataclasses import asdict
from .golden import *
from .ranking import PairwiseLinearRanker,ranking_metrics,build_pairs
from .treatment import DirectOutcomeSelector
from .survival import DiscreteHazardModel,survival_metrics
from .distributional import EmpiricalQuantileModel,fit_conformal_interval,apply_conformal,distributional_metrics,distributional_summary
from .multitask import SharedLinearHeads,RegimeGate
from .policy import audit_policy_support,ConservativePolicyImprovement,compare_logged_policy
from .registry import AdvancedTaskRegistry
from .canonical import canonical_sha256
from .enums import RegimeFallback

def run_conformance():
 results={}
 rr=ranking_rows();r1=PairwiseLinearRanker().fit(rr,('x','g','xg'));r2=PairwiseLinearRanker().fit(rr,('x','g','xg'));scores=r1.predict(rr);rm=ranking_metrics(rr,scores,3);results['ranking']={'deterministic':r1.state_hash==r2.state_hash,'pairs':len(build_pairs(rr)),'ndcg':rm.mean_ndcg_at_k,'pairwise':rm.pairwise_accuracy}
 tr,actions=treatment_rows();selector=DirectOutcomeSelector(5).fit(tr,actions);pred=[selector.predict_one(r,mask(r.row_id,actions)) for r in tr[:6]];results['treatment']={'supported':len(selector.models)==3,'actions':[p.chosen_action_key for p in pred],'deterministic_hash':canonical_sha256(pred)}
 obs=survival_observations();sm=DiscreteHazardModel((60000,120000,180000,240000,360000)).fit(obs);curve=sm.curve();cif=sm.competing_curve();curves={o.row_id:sm.curve(o.row_id) for o in obs};risk={o.row_id:1/o.duration_ms for o in obs};sr=survival_metrics(obs,risk,curves,sm.horizons);results['survival']={'monotone':all(a>=b for a,b in zip(curve.survival,curve.survival[1:])),'cif_causes':cif.cause_ids,'c_index':sr.concordance_index}
 vals=quantile_values();qm=EmpiricalQuantileModel((.05,.25,.5,.75,.95)).fit(vals);preds=[qm.predict(f'q{i}') for i in range(10)];state=fit_conformal_interval(vals[:30],[qm.values[2]]*30,.1);intervals=[apply_conformal(f'q{i}',qm.values[2],state) for i in range(10)];dm=distributional_metrics(vals[:10],preds,intervals);ds=distributional_summary('global',vals,.05,1.,-1.);results['distributional']={'monotone':all(p.monotone for p in preds),'coverage':dm.interval_coverage,'cvar_le_var':ds.conditional_value_at_risk<=ds.value_at_risk}
 pr,pa=policy_rows();audit=audit_policy_support(pr,pa,5,.01);cpi=ConservativePolicyImprovement(pa,5,1.0,0).fit(pr);decisions={r.row_id:cpi.decide(r,'wide_stop').selected_action_key for r in pr[:12]};baseline={r.row_id:'wide_stop' for r in pr[:12]};q={(r.row_id,a):cpi.stats[a][0] for r in pr[:12] for a in pa};cmp=compare_logged_policy(pr[:12],decisions,baseline,q,audit.audit_id);results['policy']={'support':audit.decision.value,'no_unseen':set(decisions.values())<=set(pa),'comparison':cmp.decision.value}
 reg=AdvancedTaskRegistry().freeze().snapshot();results['registry']={'count':len(reg.descriptors),'frozen':reg.frozen,'hash':reg.evidence_hash};results['passed']=all((results['ranking']['deterministic'],results['ranking']['ndcg']>.9,results['treatment']['supported'],results['survival']['monotone'],results['distributional']['monotone'],results['distributional']['cvar_le_var'],results['policy']['no_unseen'],reg.frozen));return results
