from __future__ import annotations
from .canonical import content_hash,stable_id
from .numerics import correlation,partial_correlation,topological_sort
from .errors import GraphError

def _series(dataset,var,split=None):return [r['values'][var] for r in dataset['rows'] if split is None or r['split']==split]
def _nodes(registry):return [v['variable_id'] for v in registry.variables if v['role']!='environment']
def _edge_key(e):return (e['source'],e['target'])
def validate_graph(nodes,edges,constraints):
    pairs=[_edge_key(e) if isinstance(e,dict) else tuple(e) for e in edges]
    if len(pairs)!=len(set(pairs)):raise GraphError('duplicate edge')
    if any(a==b or a not in nodes or b not in nodes for a,b in pairs):raise GraphError('invalid edge endpoint')
    if any((a,b) in constraints.forbidden_edges for a,b in pairs):raise GraphError('forbidden edge')
    if constraints.no_future_to_past and any(constraints.temporal_tiers[a]>constraints.temporal_tiers[b] for a,b in pairs):raise GraphError('future-to-past edge')
    parent_count={n:0 for n in nodes}
    for a,b in pairs:parent_count[b]+=1
    if max(parent_count.values(),default=0)>constraints.max_parents:raise GraphError('parent budget exceeded')
    topo=topological_sort(nodes,pairs)
    if constraints.acyclic_required and not topo:raise GraphError('cycle detected')
    return {'valid':True,'topological_order':topo,'maximum_parent_count':max(parent_count.values(),default=0)}

def association_baseline(dataset,registry,constraints,config):
    nodes=_nodes(registry);rows=[];edges=[]
    for i,a in enumerate(nodes):
        for b in nodes[i+1:]:
            c=correlation(_series(dataset,a,'train'),_series(dataset,b,'train'));rows.append({'variable_a':a,'variable_b':b,'correlation':c,'absolute_correlation':abs(c)})
            if abs(c)>=config.association_threshold:
                ta,tb=constraints.temporal_tiers[a],constraints.temporal_tiers[b]
                source,target=(a,b) if ta<=tb else (b,a)
                if (source,target) not in constraints.forbidden_edges:edges.append({'source':source,'target':target,'score':abs(c),'evidence_class':'association_only'})
    edges=sorted({(e['source'],e['target']):(e) for e in edges}.values(),key=lambda e:(e['source'],e['target']))
    graph={'candidate_id':'v417_correlation_baseline','algorithm':'correlation_baseline','nodes':nodes,'edges':edges,'claim_tier':'associational','production_eligible':False};audit=validate_graph(nodes,edges,constraints);graph.update(audit);graph['graph_hash']=content_hash(graph)
    report={'phase':'SAED_V4_17','pair_count':len(rows),'rows':rows,'graph':graph};report['report_hash']=content_hash(report);return report

def temporal_candidate(dataset,registry,constraints,config,candidate_id='v417_temporal_pc'):
    nodes=_nodes(registry);edges=[];tests=[]
    for target in nodes:
        tier_t=constraints.temporal_tiers[target]
        predecessors=[n for n in nodes if n!=target and constraints.temporal_tiers[n]<=tier_t and (n,target) not in constraints.forbidden_edges]
        scored=[]
        for source in predecessors:
            controls=[n for n in predecessors if n!=source and constraints.temporal_tiers[n]<=constraints.temporal_tiers[source]][:2]
            x=_series(dataset,source,'train');y=_series(dataset,target,'train');z=[[r['values'][n] for n in controls] for r in dataset['rows'] if r['split']=='train']
            raw=correlation(x,y);pc=partial_correlation(x,y,z) if controls else raw
            tests.append({'source':source,'target':target,'conditioning_set':controls,'raw_correlation':raw,'partial_correlation':pc,'independent':abs(pc)<config.conditional_independence_threshold})
            if abs(pc)>=config.conditional_independence_threshold:scored.append((abs(pc),source,pc))
        for score,source,pc in sorted(scored,reverse=True)[:constraints.max_parents]:edges.append({'source':source,'target':target,'score':score,'signed_score':pc,'evidence_class':'conditional_association'})
    # enforce required edges only for synthetic benchmark controls, never as evidence of real causality
    present={(e['source'],e['target']) for e in edges}
    for a,b in constraints.required_edges:
        if (a,b) not in present:edges.append({'source':a,'target':b,'score':1.0,'signed_score':1.0,'evidence_class':'declared_synthetic_prior'})
    # deterministic de-dup and cycle-safe forward tier edges
    edges=sorted({(e['source'],e['target']):e for e in edges}.values(),key=lambda e:(constraints.temporal_tiers[e['target']],e['target'],-e['score'],e['source']))
    accepted=[]
    for e in edges:
        trial=accepted+[e]
        try:validate_graph(nodes,trial,constraints);accepted=trial
        except GraphError:pass
    graph={'candidate_id':candidate_id,'algorithm':'temporal_pc_reference','nodes':nodes,'edges':accepted,'claim_tier':'mechanism_compatible_synthetic','production_eligible':False};graph.update(validate_graph(nodes,accepted,constraints));graph['graph_hash']=content_hash(graph)
    report={'phase':'SAED_V4_17','test_count':len(tests),'tests':tests,'graph':graph};report['report_hash']=content_hash(report);return report

def graph_metrics(graph,truth):
    pred={(e['source'],e['target']) for e in graph['edges']};actual={(e['source'],e['target']) for e in truth['edges']};tp=len(pred&actual);fp=len(pred-actual);fn=len(actual-pred)
    precision=tp/(tp+fp) if tp+fp else 0.0;recall=tp/(tp+fn) if tp+fn else 0.0;f1=2*precision*recall/(precision+recall) if precision+recall else 0.0
    return {'true_positive_edges':tp,'false_positive_edges':fp,'false_negative_edges':fn,'precision':precision,'recall':recall,'f1':f1,'structural_hamming_distance':fp+fn}
