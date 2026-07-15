from __future__ import annotations
from .canonical import content_hash,stable_id

def summarize(cube)->dict:
    closed=[r for r in cube.rows if r.status=='closed'];net=[r.net_r for r in closed]
    statuses={};reasons={}
    for r in cube.rows:statuses[r.status]=statuses.get(r.status,0)+1;reasons[r.exit_reason]=reasons.get(r.exit_reason,0)+1
    payload={'cube_id':cube.cube_id,'cube_hash':cube.cube_hash,'row_count':cube.row_count,'closed_count':len(closed),'status_counts':dict(sorted(statuses.items())),'exit_reason_counts':dict(sorted(reasons.items())),'net_r_min':min(net) if net else 0.0,'net_r_max':max(net) if net else 0.0,'net_r_mean':sum(net)/len(net) if net else 0.0,'descriptive_only':True,'ranking_authority':False}
    payload['summary_id']=stable_id('cubesummary',payload);payload['summary_hash']=content_hash(payload);return payload
