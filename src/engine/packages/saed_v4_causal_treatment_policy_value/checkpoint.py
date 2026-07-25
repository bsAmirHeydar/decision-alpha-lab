from __future__ import annotations
from .canonical import content_hash,stable_id

def build_checkpoints(tournament,policy_values,claim_report):
    checkpoints=[]
    for p in policy_values['policies']:
        payload={'phase':'SAED_V4_18','policy_id':p['policy_id'],'dr_value':p['dr_value'],'lower_bound':p['multiplicity_adjusted_lower'],'claim_tier':claim_report['claim_tier'],'research_only':True,'promotion_authority':False}
        payload['checkpoint_id']=stable_id('v418_checkpoint',payload);payload['checkpoint_hash']=content_hash(payload);checkpoints.append(payload)
    champion=next(x for x in checkpoints if x['policy_id']==tournament['reference_champion_id'])
    registry={'phase':'SAED_V4_18','registry_id':stable_id('v418_registry',checkpoints),'immutable':True,'reference_champion_id':champion['checkpoint_id'],'policy_champion_id':champion['policy_id'],'checkpoints':checkpoints,'production_registry':False};registry['registry_hash']=content_hash(registry);return {'checkpoints':checkpoints,'registry':registry}
