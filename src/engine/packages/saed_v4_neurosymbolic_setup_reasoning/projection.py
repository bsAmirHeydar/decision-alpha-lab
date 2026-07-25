from __future__ import annotations
from .errors import ProjectionError
from .canonical import content_hash

def project(decisions,soft_scores,contract_mapping,hard_blocks,contradiction=False):
    approved=list(contract_mapping['approved_treatments']);baseline=contract_mapping['canonical_baseline'];manual=contract_mapping['manual_fallback']
    if contradiction:return {'directive':'quarantine','treatment_id':baseline,'reason':'contradiction','proof_required':True,'projection_hash':content_hash(['contradiction',baseline])}
    if hard_blocks:return {'directive':'reject','treatment_id':baseline,'reason':'hard_constraint_block','proof_required':True,'projection_hash':content_hash(sorted(hard_blocks))}
    manual_rows=[d for d in decisions if d['manual_doctrine'] and d['effect']=='recommend' and d['treatment_id'] in approved]
    if manual_rows:
        chosen=sorted(manual_rows,key=lambda x:(-x['priority'],x['rule_id']))[0]
        return {'directive':'manual','treatment_id':chosen['treatment_id'],'reason':'manual_doctrine_precedence','proof_required':True,'projection_hash':content_hash(chosen)}
    candidates=[x for x in soft_scores['scores'] if x['effect']=='recommend' and x['treatment_id'] in approved]
    candidates.sort(key=lambda x:(-x['score'],x['treatment_id']))
    if not candidates or candidates[0]['score']<contract_mapping['minimum_symbolic_confidence']:
        return {'directive':'abstain','treatment_id':baseline,'reason':'insufficient_symbolic_confidence','proof_required':True,'projection_hash':content_hash(['abstain',baseline])}
    c=candidates[0];return {'directive':'research_recommendation','treatment_id':c['treatment_id'],'reason':'bounded_symbolic_projection','proof_required':True,'projection_hash':content_hash(c)}
