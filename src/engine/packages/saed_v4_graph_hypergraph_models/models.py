from __future__ import annotations
import math
from collections import defaultdict
from .canonical import hash_signed,content_hash
from .features import relation_embedding
from .graph_compiler import adjacency,incidence
from .numerics import mean,tanh_vec,dot,softmax
from .errors import ContractError

def _matrix(seed,rows,cols,scale=0.12): return tuple(tuple(scale*hash_signed(f'{seed}|{i}|{j}') for j in range(cols)) for i in range(rows))
def _project(v,w): return tuple(sum(float(v[j])*float(w[i][j]) for j in range(len(v))) for i in range(len(w)))
def _base(graph,spec,cand):
    w=_matrix(f'{cand.candidate_id}|input',cand.hidden_dim,spec.input_dim)
    return {n['node_id']:tanh_vec(_project(n['feature'],w)) for n in graph['nodes']}
def _out(states,cand):
    w=_matrix(f'{cand.candidate_id}|output',cand.output_dim,cand.hidden_dim)
    return {k:tanh_vec(_project(v,w)) for k,v in states.items()}

def encode(graph:dict,spec,cand)->dict:
    states=_base(graph,spec,cand);adj=adjacency(graph);node_by={n['node_id']:n for n in graph['nodes']}
    if cand.architecture=='relation_mean_baseline':
        for _ in range(cand.layers):states={n:mean([states[n]]+[states[t] for t,_ in adj.get(n,())]) for n in states}
    elif cand.architecture=='relational_gcn':
        for layer in range(cand.layers):
            nxt={}
            for n in states:
                msgs=[states[n]]
                for t,rels in adj.get(n,()):
                    rv=mean([relation_embedding(r,cand.hidden_dim) for r in rels]);msgs.append(tuple(states[t][i]+0.15*rv[i] for i in range(cand.hidden_dim)))
                nxt[n]=tanh_vec(mean(msgs))
            states=nxt
    elif cand.architecture=='graph_attention':
        for layer in range(cand.layers):
            nxt={}
            for n in states:
                neigh=adj.get(n,());candidates=[n]+[t for t,_ in neigh]
                scores=[dot(states[n],states[t])/math.sqrt(cand.hidden_dim) for t in candidates];weights=softmax(scores)
                nxt[n]=tanh_vec(tuple(sum(weights[j]*states[t][i] for j,t in enumerate(candidates)) for i in range(cand.hidden_dim)))
            states=nxt
    elif cand.architecture=='hypergraph_diffusion':
        for layer in range(cand.layers):
            hedge_state={e['edge_id']:mean([states[n] for n in e['member_node_ids']]) for e in graph['hyperedges']};inc=incidence(graph)
            states={n:tanh_vec(mean([states[n]]+[hedge_state[e] for e in inc.get(n,())])) for n in states}
    elif cand.architecture=='temporal_graph_memory':
        for layer in range(cand.layers):
            nxt={}
            for n in states:
                msgs=[states[n]];tn=node_by[n]['known_time']
                for t,rels in adj.get(n,()):
                    # deterministic bounded pseudo-decay from timestamp lexical hashes; no future access
                    delta=abs(int(content_hash(tn+'|'+node_by[t]['known_time'])[:6],16)%3600);decay=math.exp(-delta/3600.0)
                    msgs.append(tuple(decay*x for x in states[t]))
                nxt[n]=tanh_vec(mean(msgs))
            states=nxt
    elif cand.architecture=='heterogeneous_graph_fusion':
        inc=incidence(graph)
        for layer in range(cand.layers):
            hedge_state={e['edge_id']:mean([states[n] for n in e['member_node_ids']]) for e in graph['hyperedges']}
            nxt={}
            for n in states:
                rel_msgs=[]
                for t,rels in adj.get(n,()):
                    rv=mean([relation_embedding(r,cand.hidden_dim) for r in rels]);rel_msgs.append(tuple(states[t][i]+0.10*rv[i] for i in range(cand.hidden_dim)))
                hmsgs=[hedge_state[e] for e in inc.get(n,())]
                seq=node_by[n]['sequence_state'];seq=tuple(seq[i%len(seq)] for i in range(cand.hidden_dim))
                nxt[n]=tanh_vec(mean([states[n],seq]+rel_msgs+hmsgs))
            states=nxt
    else: raise ContractError(f'unsupported architecture {cand.architecture}')
    embeddings=_out(states,cand)
    return {'candidate_id':cand.candidate_id,'architecture':cand.architecture,'embeddings':embeddings,'embedding_hash':content_hash(embeddings),'node_count':len(embeddings),'runtime_authority':False}
