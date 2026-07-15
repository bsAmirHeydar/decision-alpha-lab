from __future__ import annotations
from .streaming import _dts
from .numerics import mean_vec,l2
from .canonical import content_hash,stable_id

def state_probe(model,sequences):
    rows=[]
    for seq in sequences:
        hs,_=model.batch([p.vector for p in seq.points],_dts(seq.points));
        for i,h in enumerate(hs):rows.append({'sequence_id':seq.sequence_id,'split':seq.split,'step':i,'state_norm':l2(h),'state_mean':sum(h)/len(h),'domain_id':seq.domain_id})
    norms=[r['state_norm'] for r in rows];collapse=(max(norms)-min(norms)<1e-8) if norms else True
    material={'candidate_id':model.candidate_id,'row_count':len(rows),'state_norm_min':min(norms) if norms else 0.0,'state_norm_max':max(norms) if norms else 0.0,'collapsed':collapse,'rows':rows}
    return {**material,'probe_id':stable_id('stateprobe',material),'probe_hash':content_hash(material)}

def stability_probe(model,sequence,epsilon=1e-7):
    xs=[tuple(v+(epsilon if j==0 else 0.0) for j,v in enumerate(p.vector)) for p in sequence.points];base,_=model.batch([p.vector for p in sequence.points],_dts(sequence.points));pert,_=model.batch(xs,_dts(sequence.points));d=max((max(abs(a-b) for a,b in zip(x,y)) for x,y in zip(base,pert)),default=0.0)
    material={'candidate_id':model.candidate_id,'sequence_id':sequence.sequence_id,'epsilon':epsilon,'max_state_delta':d,'finite_and_bounded':d<1.0}
    return {**material,'probe_id':stable_id('stabilityprobe',material),'probe_hash':content_hash(material)}
