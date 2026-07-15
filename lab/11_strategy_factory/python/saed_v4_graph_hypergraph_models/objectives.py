from __future__ import annotations
from collections import defaultdict
from .numerics import ridge_fit,ridge_predict,cosine,mean,dot
from .canonical import content_hash

def reconstruction(graph,encoded):
    by={n['node_id']:n for n in graph['nodes']};train=[n for n in graph['nodes'] if n['split']=='train'];ev=[n for n in graph['nodes'] if n['split']=='eval'] or train[-1:]
    xs=[encoded['embeddings'][n['node_id']] for n in train];ys=[n['feature'][:6] for n in train];w=ridge_fit(xs,ys,1e-2)
    errors=[]
    for n in ev:
        p=ridge_predict(w,encoded['embeddings'][n['node_id']]);errors.append(sum((p[i]-n['feature'][i])**2 for i in range(6))/6)
    mse=sum(errors)/len(errors);return {'mse':mse,'score':1/(1+mse),'readout_hash':content_hash(w),'train_count':len(train),'eval_count':len(ev)}
def relation_prediction(graph,encoded):
    cent=defaultdict(list)
    for e in graph['pair_edges']:
        z=tuple((a+b)/2 for a,b in zip(encoded['embeddings'][e['source']],encoded['embeddings'][e['target']]))
        for r in e['relation_kinds']:cent[r].append(z)
    cent={r:mean(v) for r,v in cent.items()};correct=total=0
    for e in graph['pair_edges']:
        z=tuple((a+b)/2 for a,b in zip(encoded['embeddings'][e['source']],encoded['embeddings'][e['target']]))
        pred=max(cent,key=lambda r:cosine(z,cent[r]))
        correct+=pred in e['relation_kinds'];total+=1
    return {'accuracy':correct/max(1,total),'score':correct/max(1,total),'relation_count':len(cent),'pair_count':total,'centroid_hash':content_hash(cent)}
def hyperedge_membership(graph,encoded):
    positives=[];negatives=[];ids=sorted(encoded['embeddings'])
    for e in graph['hyperedges']:
        h=mean([encoded['embeddings'][n] for n in e['member_node_ids']])
        positives += [cosine(h,encoded['embeddings'][n]) for n in e['member_node_ids']]
        non=[n for n in ids if n not in e['member_node_ids']]
        if non:negatives.append(cosine(h,encoded['embeddings'][non[int(content_hash(e['edge_id'])[:8],16)%len(non)]]))
    score=sum(1 for p in positives for n in negatives if p>n)/max(1,len(positives)*len(negatives))
    return {'pairwise_auc':score,'score':score,'positive_count':len(positives),'negative_count':len(negatives)}
def temporal_consistency(graph,encoded):
    vals=[]
    for e in graph['pair_edges']:
        vals.append((cosine(encoded['embeddings'][e['source']],encoded['embeddings'][e['target']])+1)/2)
    s=sum(vals)/max(1,len(vals));return {'mean_neighbor_cosine_unit':s,'score':s,'pair_count':len(vals)}
def sequence_alignment(graph,encoded):
    vals=[]
    for n in graph['nodes']:
        z=encoded['embeddings'][n['node_id']];s=n['sequence_state'];s=tuple(s[i%len(s)] for i in range(len(z)));vals.append((cosine(z,s)+1)/2)
    v=sum(vals)/max(1,len(vals));return {'mean_alignment_unit':v,'score':v,'node_count':len(vals)}
def evaluate(graph,encoded,objective_specs):
    funcs={'masked_node_reconstruction':reconstruction,'relation_type_prediction':relation_prediction,'hyperedge_membership':hyperedge_membership,'temporal_consistency':temporal_consistency,'sequence_state_alignment':sequence_alignment}
    reports={};weighted=total=0.0
    for o in objective_specs:
        r=funcs[o.name](graph,encoded);reports[o.name]=r;weighted+=o.weight*r['score'];total+=o.weight
    return {'candidate_id':encoded['candidate_id'],'architecture':encoded['architecture'],'objectives':reports,'composite_score':weighted/total,'outcome_supervision':False,'evaluation_hash':content_hash(reports)}
