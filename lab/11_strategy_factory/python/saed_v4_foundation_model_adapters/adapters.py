from __future__ import annotations
import math
from .canonical import content_hash,stable_id,hash_signed,hash_unit
from .numerics import mean,tanh_vec,softmax,quantile

def matrix(seed,rows,cols,scale=.1): return tuple(tuple(scale*hash_signed(f'{seed}|{i}|{j}') for j in range(cols)) for i in range(rows))
def project(v,w): return tuple(sum(float(v[j])*float(w[i][j]) for j in range(len(v))) for i in range(len(w)))
def patches(tokens,n): return [tokens[i:i+n] for i in range(0,len(tokens),n) if tokens[i:i+n]]
def pooled_features(seq): return mean([tuple(t['feature']) for t in seq['tokens']])
def trend_features(seq):
    xs=[t['feature'] for t in seq['tokens']]
    if len(xs)<2:return tuple(0.0 for _ in xs[0])
    return tuple(xs[-1][i]-xs[0][i] for i in range(len(xs[0])))
def route_weights(token,candidate): return softmax([hash_unit(f"{candidate.seed}|{candidate.candidate_id}|{token['token_id']}|expert|{e}") for e in range(candidate.expert_count)])

def _representation(seq,config,candidate):
    tokens=seq['tokens'];base=pooled_features(seq);trend=trend_features(seq);mode=candidate.adapter_mode
    if mode=='causal_linear': source=tuple(base[i]+.25*trend[i] for i in range(len(base)))
    elif mode=='frozen_embedding':
        ps=[mean([tuple(t['feature']) for t in p]) for p in patches(tokens,config.patch_length)];source=mean([tanh_vec(p) for p in ps])
    elif mode=='zero_shot_distribution':
        bins=[]
        for t in tokens:
            bins.append(tuple(round(max(-4,min(4,x))*4)/4 for x in t['feature']))
        source=mean([tanh_vec(x) for x in bins])
    elif mode=='masked_representation':
        rows=[]
        for idx,t in enumerate(tokens):
            mask_idx=(idx+candidate.seed)%len(t['feature']);rows.append(tuple(0.0 if j==mask_idx else x for j,x in enumerate(t['feature'])))
        source=mean(rows)
    elif mode=='probabilistic_multiscale':
        scales=[1,max(1,config.patch_length//2),config.patch_length];views=[]
        for s in scales:views.extend(mean([tuple(t['feature']) for t in p]) for p in patches(tokens,s))
        source=mean(views)
    elif mode=='sparse_expert_features':
        expert_states=[]
        for e in range(candidate.expert_count):
            weighted=[];weights=[]
            for t in tokens:
                r=route_weights(t,candidate)[e];weighted.append(tuple(r*x for x in t['feature']));weights.append(r)
            den=sum(weights) or 1.0;expert_states.append(tuple(sum(v[i] for v in weighted)/den for i in range(len(base))))
        source=mean(expert_states)
    else: raise ValueError(mode)
    w=matrix(f'{candidate.candidate_id}|repr',config.embedding_dim,len(source),.12);return tanh_vec(project(source,w))

def run_adapter(seq,config,candidate):
    rep=_representation(seq,config,candidate);scalar_history=[sum(t['feature'])/len(t['feature']) for t in seq['tokens']];last=scalar_history[-1];trend=(scalar_history[-1]-scalar_history[0])/max(1,len(scalar_history)-1)
    center=last+trend*config.horizon*(.4+.2*hash_unit(candidate.candidate_id));spread=max(.05,(max(scalar_history)-min(scalar_history))*.15+.02*candidate.expert_count)
    qvals=[{'q':q,'value':center+(q-.5)*2.8*spread} for q in config.quantiles]
    router=[]
    if candidate.adapter_mode=='sparse_expert_features':
        avg=[0.0]*candidate.expert_count
        for t in seq['tokens']:
            rw=route_weights(t,candidate)
            for i,x in enumerate(rw):avg[i]+=x/len(seq['tokens'])
        router=avg
    doc={'phase':'SAED_V4_14','candidate_id':candidate.candidate_id,'intake_id':candidate.intake_id,'family':candidate.family,'adapter_mode':candidate.adapter_mode,'source_token_sequence_hash':seq['token_sequence_hash'],'known_as_of':seq['known_as_of'],'embedding':list(rep),'quantile_forecast':qvals,'uncertainty_scale':spread,'router_weights':router,'external_model_invoked':False,'external_weights_loaded':False,'future_suffix_accessed':False,'online_learning':False,'runtime_authority':False,'production_eligible':False}
    doc['feature_hash']=content_hash(doc);doc['feature_id']=stable_id('fmfeature',doc);return doc
