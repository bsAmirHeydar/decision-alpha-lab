from .contracts import *
from .canonical import sha256,stable_id

def apply_projection_budget(facts:tuple[ProjectionFact,...],max_objects:int)->DegradationDecision:
    if max_objects<1: raise ValueError('max_objects must be positive')
    ordered=tuple(sorted(facts,key=lambda x:(int(x.priority),x.is_historical,x.semantic_id,x.object_id)))
    projected=ordered[:max_objects];deferred=ordered[max_objects:]
    health=HealthState.READY if not deferred else HealthState.DEGRADED
    reasons=() if not deferred else ('FP_REL_NONCRITICAL_PROJECTION_DEFERRED',)
    body={'semantic_count':len(facts),'projected':tuple(x.object_id for x in projected),'deferred':tuple(x.object_id for x in deferred),'health':health.value}
    return DegradationDecision(stable_id('FPDEGRADE',body),health,len(facts),body['projected'],body['deferred'],reasons,sha256(body))
