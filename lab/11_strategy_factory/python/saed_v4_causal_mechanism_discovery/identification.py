from __future__ import annotations
from .canonical import content_hash

def _parents(graph,node):return sorted(e['source'] for e in graph['edges'] if e['target']==node)
def _children(graph,node):return sorted(e['target'] for e in graph['edges'] if e['source']==node)
def backdoor_audit(graph,treatment,outcome,registry):
    treatment_parents=_parents(graph,treatment);observed={v['variable_id'] for v in registry.variables if v['observed']};negative={v['variable_id'] for v in registry.variables if v['negative_control']}
    adjustment=sorted((set(treatment_parents)&observed)-negative)
    out={'phase':'SAED_V4_17','treatment_proxy_id':treatment,'outcome_proxy_id':outcome,'treatment_parents':treatment_parents,'candidate_adjustment_set':adjustment,'backdoor_candidate_exists':bool(adjustment),'identification_claim_allowed':False,'reason':'graph is synthetic reference evidence and unmeasured confounding remains a sensitivity dimension'};out['audit_hash']=content_hash(out);return out
def frontdoor_audit(graph,treatment,outcome):
    mediators=[n for n in _children(graph,treatment) if outcome in _children(graph,n)]
    out={'phase':'SAED_V4_17','treatment_proxy_id':treatment,'outcome_proxy_id':outcome,'candidate_mediators':sorted(mediators),'frontdoor_candidate_exists':bool(mediators),'frontdoor_identification_claim_allowed':False,'reason':'front-door graphical compatibility is not identification proof'};out['audit_hash']=content_hash(out);return out
def temporal_audit(graph,constraints):
    rows=[]
    for e in graph['edges']:
        a,b=e['source'],e['target'];rows.append({'source':a,'target':b,'source_tier':constraints.temporal_tiers[a],'target_tier':constraints.temporal_tiers[b],'future_to_past':constraints.temporal_tiers[a]>constraints.temporal_tiers[b],'passed':constraints.temporal_tiers[a]<=constraints.temporal_tiers[b]})
    out={'phase':'SAED_V4_17','edge_count':len(rows),'all_passed':all(r['passed'] for r in rows),'rows':rows};out['audit_hash']=content_hash(out);return out
def acyclicity_audit(graph):
    out={'phase':'SAED_V4_17','candidate_id':graph['candidate_id'],'node_count':len(graph['nodes']),'edge_count':len(graph['edges']),'topological_order':graph['topological_order'],'acyclic':bool(graph['topological_order']),'passed':bool(graph['topological_order'])};out['audit_hash']=content_hash(out);return out
