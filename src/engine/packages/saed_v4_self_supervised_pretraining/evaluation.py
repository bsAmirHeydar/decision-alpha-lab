from __future__ import annotations
import math
from collections import defaultdict
from .encoder import cosine
from .canonical import content_hash, stable_id
from .errors import EvaluationError

def _mean(xs): return 0.0 if not xs else sum(xs)/len(xs)
def _variance(xs):
    if not xs:return 0.0
    m=_mean(xs);return _mean([(x-m)**2 for x in xs])

def collapse_metrics(encoder,streams:list)->dict:
    selected=[s for s in streams if s.split in {'train','validation','test'}]
    embs=[encoder.encode(s.tokens) for s in selected]
    if not embs: raise EvaluationError('no evaluation streams')
    dim_var=[_variance([e[i] for e in embs]) for i in range(len(embs[0]))]
    pair_cos=[]
    for i in range(len(embs)):
        for j in range(i+1,len(embs)): pair_cos.append(cosine(embs[i],embs[j]))
    rounded={tuple(round(x,6) for x in e) for e in embs}
    return {"record_count":len(embs),"mean_dimension_variance":_mean(dim_var),"minimum_dimension_variance":min(dim_var),"mean_pairwise_cosine":_mean(pair_cos),"unique_embedding_fraction":len(rounded)/len(embs),"collapsed":_mean(dim_var)<1e-10 or len(rounded)<2}

def temporal_retrieval(encoder,streams:list,k:int=2)->dict:
    ordered=sorted([s for s in streams if s.split in {'train','validation','test'}],key=lambda s:(s.known_time,s.record_id))
    hits=0;eligible=0
    for i,s in enumerate(ordered):
        future=[x for x in ordered[i+1:] if x.root_context_id==s.root_context_id]
        if not future: continue
        target=future[0];eligible+=1
        candidates=[x for x in ordered if x.record_id!=s.record_id]
        ranked=sorted(candidates,key=lambda x:(-cosine(encoder.encode(s.tokens),encoder.encode(x.tokens)),x.record_id))[:k]
        if target.record_id in {x.record_id for x in ranked}: hits+=1
    return {"k":k,"eligible":eligible,"hits":hits,"recall_at_k":0.0 if eligible==0 else hits/eligible}

def nearest_centroid_probe(encoder,streams:list,label_kind:str='domain_id')->dict:
    train=[s for s in streams if s.split=='train'];evals=[s for s in streams if s.split in {'validation','test'}]
    groups=defaultdict(list)
    for s in train: groups[getattr(s,label_kind)].append(encoder.encode(s.tokens))
    centroids={label:[_mean([e[i] for e in rows]) for i in range(len(rows[0]))] for label,rows in groups.items()}
    correct=0;preds=[]
    for s in evals:
        scores={label:cosine(encoder.encode(s.tokens),c) for label,c in centroids.items()}
        pred=max(scores,key=lambda x:(scores[x],x)) if scores else None
        actual=getattr(s,label_kind);correct+=int(pred==actual);preds.append({"record_id":s.record_id,"actual":actual,"predicted":pred,"scores":scores})
    return {"label_kind":label_kind,"train_count":len(train),"evaluation_count":len(evals),"accuracy":0.0 if not evals else correct/len(evals),"predictions":preds,"outcome_label":False}

def random_label_probe(encoder,streams:list)->dict:
    selected=[s for s in streams if s.split in {'validation','test'}]
    labels={s.record_id:int(content_hash(s.record_id)[0],16)%2 for s in selected}
    # Deliberately simple, non-fitted membership-safe probe.
    preds={s.record_id:int(sum(encoder.encode(s.tokens))>=0) for s in selected}
    acc=0.0 if not selected else sum(labels[x.record_id]==preds[x.record_id] for x in selected)/len(selected)
    return {"evaluation_count":len(selected),"accuracy":acc,"chance_reference":0.5,"random_labels":True,"admission_effect":"diagnostic_only"}

def leakage_probe(checkpoint:dict,forbidden_tokens:set[str])->dict:
    hits=[]
    for token in checkpoint['vocabulary']:
        low=token.lower()
        if any(x in low for x in forbidden_tokens): hits.append(token)
    return {"passed":not hits,"hits":sorted(hits),"checked_tokens":len(checkpoint['vocabulary'])}

def evaluate_representation(encoder,streams,checkpoint,control_name='trained_reference')->dict:
    collapse=collapse_metrics(encoder,streams)
    retrieval=temporal_retrieval(encoder,streams)
    domain_probe=nearest_centroid_probe(encoder,streams,'domain_id')
    random_probe=random_label_probe(encoder,streams)
    leakage=leakage_probe(checkpoint,{"outcome","net_r","gross_r","mfe","mae","protected_final","prospective","shadow","live_fill","policy_value"})
    accepted=(not collapse['collapsed']) and leakage['passed'] and collapse['unique_embedding_fraction']>=0.5
    payload={"phase":"SAED_V4_11","checkpoint_hash":checkpoint['checkpoint_hash'],"control_name":control_name,"collapse":collapse,"temporal_retrieval":retrieval,"linear_probe":domain_probe,"random_label_probe":random_probe,"leakage_probe":leakage,"accepted_for_reference_registry":accepted,"claims":{"real_alpha":False,"outcome_prediction":False,"production_authorization":False},"limitations":["Synthetic corpus metrics are conformance evidence, not economic evidence.","Probe labels are non-outcome structural labels."]}
    payload['dossier_id']=stable_id('representationdossier',payload);payload['dossier_hash']=content_hash(payload);return payload
