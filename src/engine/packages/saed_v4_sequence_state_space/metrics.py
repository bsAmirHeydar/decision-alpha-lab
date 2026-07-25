from __future__ import annotations
from .trainer import predict_next
from .numerics import cosine,max_abs_diff
from .canonical import content_hash,stable_id

def mse(a,b): return sum((float(x)-float(y))**2 for x,y in zip(a,b))/max(1,len(a))
def evaluate_candidate(model,weights,sequences):
    rows=[]
    for seq in sequences:
        preds=predict_next(model,weights,seq);targets=[p.vector for p in seq.points[1:]]
        for i,(p,t) in enumerate(zip(preds,targets)):
            rows.append({'sequence_id':seq.sequence_id,'split':seq.split,'step':i,'mse':mse(p,t),'cosine':cosine(p,t)})
    summary={}
    for split in ('train','validation','test'):
        x=[r for r in rows if r['split']==split]
        summary[split]={'count':len(x),'mean_mse':sum(r['mse'] for r in x)/len(x) if x else None,'mean_cosine':sum(r['cosine'] for r in x)/len(x) if x else None}
    material={'candidate_id':model.candidate_id,'architecture':model.architecture,'summary':summary,'row_hash':content_hash(rows)}
    return {**material,'metric_id':stable_id('seqmetrics',material),'metric_hash':content_hash(material),'rows':rows}

def truncation_sensitivity(model,weights,sequences):
    rows=[]
    for seq in sequences:
        if len(seq.points)<3:continue
        full=predict_next(model,weights,seq)[-1];short_seq=type(seq)(seq.sequence_id+':truncated',seq.root_context_id,seq.domain_id,seq.split,seq.points[-2:],seq.source_hash);short=predict_next(model,weights,short_seq)[-1];rows.append({'sequence_id':seq.sequence_id,'split':seq.split,'max_abs_diff':max_abs_diff(full,short)})
    return {'candidate_id':model.candidate_id,'rows':rows,'mean_max_abs_diff':sum(r['max_abs_diff'] for r in rows)/len(rows) if rows else 0.0,'report_hash':content_hash(rows)}
