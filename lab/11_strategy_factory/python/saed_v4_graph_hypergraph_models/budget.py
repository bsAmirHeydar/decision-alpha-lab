from .errors import BudgetError
def enforce(graph,candidates,envelope):
    checks={'nodes':len(graph['nodes'])<=envelope['node_limit'],'hyperedges':len(graph['hyperedges'])<=envelope['hyperedge_limit'],'pair_edges':len(graph['pair_edges'])<=envelope['pair_edge_limit'],'candidates':len(candidates)<=envelope['candidate_limit'],'gpu_hours':float(envelope['gpu_hours'])==0.0,'distributed_workers':int(envelope['distributed_workers'])==1}
    if not all(checks.values()):raise BudgetError(f'compute envelope exceeded: {checks}')
    return {'passed':True,'checks':checks,'envelope':envelope,'exposure_units':len(graph['nodes'])*len(candidates),'trial_count':len(candidates)}
