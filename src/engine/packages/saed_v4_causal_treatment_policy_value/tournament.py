from __future__ import annotations
from .canonical import content_hash,stable_id

def run_tournament(policy_values,overlap_report,negative_control,sensitivity,manual_policy_id,baseline_policy_id):
    overlap_ok=overlap_report['passed'];negative_ok=negative_control['passed'];rows=[]
    for p in policy_values['policies']:
        stable=sensitivity['sign_stability'].get(p['policy_id'],False)
        admissible=overlap_ok and negative_ok and stable and p['effective_sample_size']>=10
        score=p['multiplicity_adjusted_lower']+0.15*p['lower_tail_cvar_10']-0.02*(p['policy_id'] not in {baseline_policy_id,manual_policy_id})
        rows.append({'policy_id':p['policy_id'],'score':score,'admissible':admissible,'lower_bound':p['multiplicity_adjusted_lower'],'tail_value':p['lower_tail_cvar_10'],'support_rate':p['support_rate'],'baseline':p['policy_id']==baseline_policy_id,'manual_baseline':p['policy_id']==manual_policy_id})
    admissible=[x for x in rows if x['admissible']];champion=max(admissible,key=lambda x:(x['score'],x['policy_id'])) if admissible else next(x for x in rows if x['policy_id']==baseline_policy_id)
    out={'phase':'SAED_V4_18','tournament_id':stable_id('v418_tournament',rows),'candidates':rows,'reference_champion_id':champion['policy_id'],'baseline_policy_id':baseline_policy_id,'manual_policy_id':manual_policy_id,'baseline_preserved':True,'manual_fallback_preserved':True,'production_promotion_allowed':False};out['tournament_hash']=content_hash(out);return out
