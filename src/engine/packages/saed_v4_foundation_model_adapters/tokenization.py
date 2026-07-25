from __future__ import annotations
from .canonical import content_hash,stable_id
from .numerics import mean,std

def champion_embedding(embeddings,champion_id):
    rows=[x for x in embeddings['candidates'] if x['candidate_id']==champion_id]
    if len(rows)!=1: raise ValueError('champion embedding cardinality mismatch')
    return rows[0]

def compile_token_sequence(compiled_graph,embeddings,champion_id,config,known_as_of=None):
    c=champion_embedding(embeddings,champion_id); by_node={n['node_id']:n for n in compiled_graph['nodes']}; ordered=[]
    for node_id,vec in sorted(c['embeddings'].items(), key=lambda kv:(by_node[kv[0]]['known_time'],kv[0])):
        kt=by_node[node_id]['known_time']
        if known_as_of is not None and kt>known_as_of: continue
        raw=[float(x) for x in vec]
        expanded=(raw*((config.feature_dim+len(raw)-1)//len(raw)))[:config.feature_dim]
        ordered.append({'token_id':stable_id('fmtoken',{'node_id':node_id,'known_time':kt}),'source_node_id':node_id,'known_time':kt,'raw_feature':expanded,'missing_mask':[False]*config.feature_dim,'age_seconds':[0]*config.feature_dim})
    ordered=ordered[-config.sequence_length:]
    normalized=[]
    history=[[] for _ in range(config.feature_dim)]
    for row in ordered:
        z=[]
        for j,x in enumerate(row['raw_feature']):
            prev=history[j];m=sum(prev)/len(prev) if prev else 0.0;s=std(prev) if len(prev)>1 else 1.0
            z.append((x-m)/(s if s>1e-8 else 1.0));history[j].append(x)
        normalized.append({**row,'feature':z})
    doc={'phase':'SAED_V4_14','source_candidate_id':champion_id,'source_embedding_hash':c['embedding_hash'],'compiled_graph_hash':compiled_graph['compiled_graph_hash'],'known_as_of':known_as_of or max(x['known_time'] for x in ordered),'sequence_length':len(normalized),'feature_dim':config.feature_dim,'normalization':'causal_expanding_zscore','tokens':normalized,'future_suffix_accessed':False}
    doc['token_sequence_hash']=content_hash(doc);doc['token_sequence_id']=stable_id('fmtokenseq',doc);return doc
