from __future__ import annotations
from .canonical import content_hash,stable_id

def build_telemetry(result:dict,lattice:dict)->dict:
    counts={k:sum(1 for n in lattice['nodes'] if n['action_class']==k) for k in ('ordinary','abstain','skip')}
    seed={'solver_result_hash':result['solver_result_hash'],'lattice_hash':lattice['lattice_hash'],'candidate_count':result['candidate_count'],'feasible_count':result['feasible_count'],'pruned_count':result['pruned_count'],'node_count':lattice['node_count'],'edge_count':lattice['edge_count'],'action_class_counts':counts,'deferred_constraint_count':sum(1 for n in lattice['nodes'] for e in n['feasibility_certificate'].get('deferred_constraints',[]))}
    return {'telemetry_id':stable_id('latticetelemetry',seed),'telemetry_hash':content_hash(seed),**seed,'production_metric':False}
