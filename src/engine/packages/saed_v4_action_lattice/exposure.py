from __future__ import annotations
from .canonical import content_hash,stable_id

def build_exposure_ledger(result:dict)->dict:
    rows=[]
    for c in result['feasible_candidates']:
        rows.append({'candidate_id':c['candidate_id'],'candidate_hash':c['candidate_hash'],'status':'feasible','failed_constraints':[]})
    for p in result['pruning_ledger']['records']:
        rows.append({'candidate_id':p['candidate_id'],'candidate_hash':p['candidate_hash'],'status':'pruned','failed_constraints':p['failed_constraints']})
    rows=sorted(rows,key=lambda r:r['candidate_id']);seed={'solver_result_hash':result['solver_result_hash'],'exposure_count':len(rows),'rows':rows}
    return {'ledger_id':stable_id('latticeexposure',seed),'ledger_hash':content_hash(seed),**seed,'complete_accounting':len(rows)==result['candidate_count']}
