from __future__ import annotations
from .canonical import content_hash,stable_id
from .numerics import l1_distribution,mean

def synthetic_veto(candidate,baseline,upstream_docs,actions,ledger=None):
    divergences=[]
    for s in baseline['states']:divergences.append(l1_distribution(candidate['states'].get(s,{}),baseline['states'][s],actions))
    uncertainty=upstream_docs['GOLDEN_UNCERTAINTY_MAP'];exploit=upstream_docs['GOLDEN_EXPLOITABILITY_REPORT'];fidelity=upstream_docs['GOLDEN_FIDELITY_REPORT']
    score=mean(divergences)*(1+float(exploit.get('exploitation_score',0.0)))+max(0.0,1-float(fidelity.get('fidelity_score',1.0)))
    threshold=0.85;passed=score<=threshold and int(uncertainty.get('trusted_horizon',0))>0 and bool(fidelity.get('passed')) and bool(exploit.get('passed'))
    out={'challenge_id':stable_id('synthetic_veto',{'candidate':candidate['policy_id'],'upstream':upstream_docs['GOLDEN_GENERATIVE_STRESS_CERTIFICATE']['certificate_hash']}),'candidate_policy_id':candidate['policy_id'],'mean_l1_from_baseline':mean(divergences),'synthetic_veto_score':score,'threshold':threshold,'passed':passed,'positive_evidence_contribution':0.0,'synthetic_positive_evidence':False,'upstream_certificate_hash':upstream_docs['GOLDEN_GENERATIVE_STRESS_CERTIFICATE']['certificate_hash']}
    out['challenge_hash']=content_hash(out)
    if ledger:ledger.consume('synthetic_challenges',1,candidate['policy_id'])
    return out

def matrix(candidates,ope_reports,support_reports,stress_reports,baseline_id,margin):
    rows=[]
    base=ope_reports[baseline_id];base_lower=float(base['aggregate_lower_bound'])
    for c in candidates:
        pid=c['policy_id'];ope=ope_reports[pid];support=support_reports[pid];stress=stress_reports[pid]
        lower_margin=float(ope['aggregate_lower_bound'])-base_lower
        research_pass=bool(support['passed'] and stress['passed'] and ope['effective_sample_size']>0 and lower_margin>=margin and c.get('projection',{}).get('passed',True))
        rows.append({'policy_id':pid,'family':c['family'],'support_passed':support['passed'],'synthetic_veto_passed':stress['passed'],'ope_lower_bound':ope['aggregate_lower_bound'],'ope_upper_bound':ope['aggregate_upper_bound'],'lower_bound_margin_vs_baseline':lower_margin,'estimator_spread':ope['estimator_spread'],'research_challenger_passed':research_pass,'promotion_eligible':False,'runtime_executable':False})
    accepted=[r for r in rows if r['research_challenger_passed'] and r['policy_id']!=baseline_id]
    selected=sorted(accepted,key=lambda r:(-r['lower_bound_margin_vs_baseline'],r['estimator_spread'],r['policy_id']))[0]['policy_id'] if accepted else baseline_id
    out={'matrix_id':stable_id('policy_challenge_matrix',{'rows':rows,'baseline':baseline_id}),'baseline_policy_id':baseline_id,'selected_research_policy_id':selected,'selection_is_research_only':True,'promotion_authority':False,'runtime_authority':False,'rows':rows,'abstain_if_no_challenger':True}
    out['matrix_hash']=content_hash(out);return out
