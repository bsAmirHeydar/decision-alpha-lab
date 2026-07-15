from __future__ import annotations
from .numerics import max_abs_diff
from .canonical import content_hash,stable_id
from .errors import ParityError

def _dts(points):
    from datetime import datetime
    out=[];prev=None
    for p in points:
        now=datetime.fromisoformat(p.event_time.replace('Z','+00:00')).timestamp();out.append(1.0 if prev is None else max(0.001,now-prev));prev=now
    return out

def batch_streaming_parity(model,sequence,tolerance=1e-10):
    xs=[p.vector for p in sequence.points];dts=_dts(sequence.points)
    batch,final=model.batch(xs,dts)
    state=model.initial_state();stream=[]
    for x,dt in zip(xs,dts):
        y,state=model.step(x,state,dt);stream.append(y)
    diffs=[max_abs_diff(a,b) for a,b in zip(batch,stream)];mx=max(diffs,default=0.0)
    passed=mx<=tolerance and max_abs_diff(final.hidden,state.hidden)<=tolerance
    material={'candidate_id':model.candidate_id,'sequence_id':sequence.sequence_id,'tolerance':tolerance,'max_abs_diff':mx,'step_count':len(xs),'passed':passed}
    if not passed:raise ParityError(f'batch/streaming parity failed: {mx}')
    return {**material,'certificate_id':stable_id('streamparity',material),'certificate_hash':content_hash(material)}

def chunked_parity(model,sequence,chunk_size,tolerance=1e-10):
    xs=[p.vector for p in sequence.points];dts=_dts(sequence.points);full,_=model.batch(xs,dts);state=model.initial_state();chunked=[]
    for i in range(0,len(xs),chunk_size):
        ys,state=model.batch(xs[i:i+chunk_size],dts[i:i+chunk_size],state);chunked.extend(ys)
    mx=max((max_abs_diff(a,b) for a,b in zip(full,chunked)),default=0.0);passed=mx<=tolerance
    material={'candidate_id':model.candidate_id,'sequence_id':sequence.sequence_id,'chunk_size':chunk_size,'tolerance':tolerance,'max_abs_diff':mx,'passed':passed}
    if not passed:raise ParityError('chunked parity failed')
    return {**material,'certificate_id':stable_id('chunkparity',material),'certificate_hash':content_hash(material)}
