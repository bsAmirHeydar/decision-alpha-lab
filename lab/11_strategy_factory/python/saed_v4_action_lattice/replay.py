from __future__ import annotations
from .canonical import content_hash,stable_id

def build_replay_receipt(first:dict,second:dict)->dict:
    identical=first['lattice_hash']==second['lattice_hash'] and first['solver_result_hash']==second['solver_result_hash']
    seed={'first_lattice_hash':first['lattice_hash'],'second_lattice_hash':second['lattice_hash'],'first_result_hash':first['solver_result_hash'],'second_result_hash':second['solver_result_hash'],'identical':identical}
    return {'replay_id':stable_id('latticereplay',seed),'replay_hash':content_hash(seed),**seed,'status':'passed' if identical else 'failed'}
