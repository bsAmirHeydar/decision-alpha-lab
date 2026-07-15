from __future__ import annotations
from typing import Any
from .canonical import content_hash, stable_id, merkle_root
from .errors import ContractError

def node_from_candidate(c:dict[str,Any])->dict[str,Any]:
    certificate_seed={'candidate_hash':c['candidate_hash'],'failed_constraints':c['failed_constraints'],'deferred_constraints':sorted(e['constraint_name'] for e in c['constraint_evaluations'] if e['status']=='deferred_known_time'),'structurally_feasible':True}
    cert={'certificate_id':stable_id('feascert',certificate_seed),'certificate_hash':content_hash(certificate_seed),**certificate_seed}
    seed={'candidate_hash':c['candidate_hash'],'program_hash':c['program_hash'],'parameter_assignments':c['parameter_assignments'],'action_class':c['action_class'],'certificate_hash':cert['certificate_hash']}
    node={'node_id':stable_id('actionnode',seed),'node_hash':'','candidate_id':c['candidate_id'],'candidate_hash':c['candidate_hash'],'program_id':c['program_id'],'program_hash':c['program_hash'],'program_name':c['program_name'],'action_class':c['action_class'],'parameter_assignments':c['parameter_assignments'],'domain_indices':c['domain_indices'],'instantiated_components':c['instantiated_components'],'feasibility_certificate':cert,'evidence_role':c['evidence_role'],'known_as_of':c['known_as_of'],'selection_authority':False,'execution_authority':False,'limitations':['Structural feasibility is not outcome value.','Node identity conveys no preference, ranking, capital or execution authority.']}
    node['node_hash']=content_hash({k:v for k,v in node.items() if k!='node_hash'})
    return node

def _edge(source:dict[str,Any],target:dict[str,Any],kind:str,mutation:dict[str,Any]|None)->dict[str,Any]:
    seed={'source_node_id':source['node_id'],'target_node_id':target['node_id'],'edge_kind':kind,'mutation':mutation}
    return {'edge_id':stable_id('latticeedge',seed),'edge_hash':content_hash(seed),**seed,'semantic_claim':'adjacency_only_not_preference'}

def build_lattice(feasible:list[dict[str,Any]])->tuple[list[dict[str,Any]],list[dict[str,Any]]]:
    nodes=sorted((node_from_candidate(c) for c in feasible),key=lambda n:n['node_id']);by_id={n['node_id']:n for n in nodes}
    ordinary=[n for n in nodes if n['action_class']=='ordinary'];abstain=[n for n in nodes if n['action_class']=='abstain'];skip=[n for n in nodes if n['action_class']=='skip']
    if len(abstain)!=1 or len(skip)!=1: raise ContractError('exactly one Skip and one Abstain node required')
    edges=[]
    # Atomic structural adjacency. Only adjacent index increments in exactly one governed domain are emitted.
    for i,a in enumerate(ordinary):
        for b in ordinary[i+1:]:
            if a['program_id']!=b['program_id']: continue
            keys=sorted(set(a['domain_indices'])|set(b['domain_indices']))
            diffs=[k for k in keys if a['domain_indices'].get(k)!=b['domain_indices'].get(k)]
            if len(diffs)!=1: continue
            ref=diffs[0];ia=a['domain_indices'][ref];ib=b['domain_indices'][ref]
            if abs(ia-ib)!=1: continue
            source,target=(a,b) if ia<ib else (b,a)
            edges.append(_edge(source,target,'atomic_parameter_step',{'parameter_ref':ref,'from_index':min(ia,ib),'to_index':max(ia,ib),'from_value':source['parameter_assignments'][ref],'to_value':target['parameter_assignments'][ref]}))
    for n in ordinary: edges.append(_edge(n,abstain[0],'fallback_abstain',None))
    edges.append(_edge(abstain[0],skip[0],'fallback_skip',None))
    unique={e['edge_id']:e for e in edges}
    return nodes,sorted(unique.values(),key=lambda e:e['edge_id'])

def lattice_payload(nodes:list[dict[str,Any]],edges:list[dict[str,Any]],source:dict[str,Any])->dict[str,Any]:
    node_root=merkle_root(n['node_hash'] for n in nodes);edge_root=merkle_root(e['edge_hash'] for e in edges)
    seed={'source_result_hash':source['solver_result_hash'],'node_merkle_root':node_root,'edge_merkle_root':edge_root,'node_count':len(nodes),'edge_count':len(edges)}
    out={'lattice_id':stable_id('actionlattice',seed),'lattice_hash':'','source_result_id':source['solver_result_id'],'source_result_hash':source['solver_result_hash'],'node_count':len(nodes),'edge_count':len(edges),'nodes':nodes,'edges':edges,'node_merkle_root':node_root,'edge_merkle_root':edge_root,'is_dag':True,'contains_skip':any(n['action_class']=='skip' for n in nodes),'contains_abstain':any(n['action_class']=='abstain' for n in nodes),'preference_semantics':'none','outcome_semantics':'none','selection_authority':False,'execution_authority':False,'limitations':['Edges encode one-step structural adjacency or fail-closed fallback only.','The lattice is not a score, preference order, policy, allocation or execution plan.']}
    out['lattice_hash']=content_hash({k:v for k,v in out.items() if k!='lattice_hash'})
    return out
