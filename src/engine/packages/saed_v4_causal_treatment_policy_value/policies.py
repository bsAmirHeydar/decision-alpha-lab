from __future__ import annotations
from .effects import predict_cate
from .canonical import content_hash

def manual_rule(row,treatment_ids):
    x=row['feature_map']
    if x['context_strength']>0.22 and x['volatility_state']<0.45:return treatment_ids[1]
    if x['liquidity_state']>0.28 and x['tail_risk']<0.72:return treatment_ids[2]
    if x['structure_state']>0.34 and x['execution_friction']<0.76:return treatment_ids[3]
    return treatment_ids[0]

def choose(policy,row,treatment_ids,cate_report,overlap_floor):
    if policy['policy_type']=='skip_all':return treatment_ids[0],'baseline'
    if policy['policy_type']=='fixed_treatment':return policy['treatment_id'],'fixed'
    if policy['policy_type']=='manual_rule':return manual_rule(row,treatment_ids),'manual'
    effects={t:predict_cate(cate_report,row,t) for t in treatment_ids}
    ranked=sorted(effects,key=lambda t:(effects[t],t),reverse=True);best=ranked[0]
    if min(row['propensities'].values())<overlap_floor and policy['abstain_on_support_failure']:return treatment_ids[0],'support_abstain'
    threshold=policy['minimum_uplift']+(0.06 if policy['policy_type']=='conservative_lcb' else 0.0)
    if effects[best]<threshold:return treatment_ids[0],'uplift_abstain'
    return best,'uplift'

def compile_assignments(crossfit,policies,cate_report,overlap_floor):
    out=[]
    for p in policies:
        rows=[]
        for r in crossfit['predictions']:
            t,reason=choose(p,r,crossfit['treatment_ids'],cate_report,overlap_floor);rows.append({'row_id':r['row_id'],'selected_treatment':t,'reason':reason})
        counts={t:sum(x['selected_treatment']==t for x in rows) for t in crossfit['treatment_ids']};out.append({'policy_id':p['policy_id'],'policy_type':p['policy_type'],'assignments':rows,'assignment_counts':counts,'evaluation_only':p['evaluation_only']})
    result={'phase':'SAED_V4_18','policy_count':len(out),'policies':out,'runtime_selectable':False};result['catalog_hash']=content_hash(result);return result
