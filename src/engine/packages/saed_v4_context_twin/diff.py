from __future__ import annotations
from .models import TwinDiff

def diff_snapshots(left,right):
    if left.twin_id!=right.twin_id:raise ValueError('different twins')
    changed=[]
    for f in ['known_as_of','lifecycle_state','twin_state','support_evaluation_id','sequence']:
        if getattr(left,f)!=getattr(right,f):changed.append(f)
    lo=set(left.observation_ids);ro=set(right.observation_ids)
    lc=set(left.contradiction_ids);rc=set(right.contradiction_ids)
    return TwinDiff(left.twin_id,left.snapshot_hash,right.snapshot_hash,tuple(sorted(changed)),tuple(sorted(ro-lo)),tuple(sorted(lo-ro)),tuple(sorted(rc-lc)),tuple(sorted(lc-rc)),left.lifecycle_state!=right.lifecycle_state)
