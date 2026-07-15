from __future__ import annotations
from .models import ModelState
from .canonical import content_hash,stable_id
from .errors import IntegrityError

def create_snapshot(candidate_id,state,sequence_id,point_id):
    material={'candidate_id':candidate_id,'sequence_id':sequence_id,'point_id':point_id,'hidden':list(state.hidden),'history':[list(x) for x in state.history],'step_count':state.step_count}
    return {**material,'snapshot_id':stable_id('statesnapshot',material),'snapshot_hash':content_hash(material)}
def restore_snapshot(snapshot):
    material={k:snapshot[k] for k in ('candidate_id','sequence_id','point_id','hidden','history','step_count')}
    if snapshot.get('snapshot_hash')!=content_hash(material):raise IntegrityError('state snapshot hash mismatch')
    return ModelState(tuple(map(float,snapshot['hidden'])),tuple(tuple(map(float,x)) for x in snapshot['history']),int(snapshot['step_count']))
def restart_parity(model,sequence,cut,tolerance=1e-10):
    from .numerics import max_abs_diff
    from .streaming import _dts
    xs=[p.vector for p in sequence.points];dts=_dts(sequence.points);state=model.initial_state();outs=[]
    if not xs or cut < 0 or cut >= len(xs):raise IntegrityError('invalid restart cut')
    snap=None
    for i,(x,dt) in enumerate(zip(xs,dts)):
        y,state=model.step(x,state,dt);outs.append(y)
        if i==cut:
            snap=create_snapshot(model.candidate_id,state,sequence.sequence_id,sequence.points[i].record_id);state=restore_snapshot(snap)
    full,_=model.batch(xs,dts);mx=max((max_abs_diff(a,b) for a,b in zip(full,outs)),default=0.0)
    if snap is None:raise IntegrityError('snapshot was not created')
    return {'candidate_id':model.candidate_id,'sequence_id':sequence.sequence_id,'cut':cut,'max_abs_diff':mx,'tolerance':tolerance,'passed':mx<=tolerance,'snapshot_hash':snap['snapshot_hash']}
