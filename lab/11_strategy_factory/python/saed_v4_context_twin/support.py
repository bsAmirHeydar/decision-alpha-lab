from __future__ import annotations
from .models import SupportGeometry,SupportEvaluation
from .enums import SupportStatus
from .canonical import parse_time
from .errors import SupportError

def evaluate_support(twin_id:str,geometry:SupportGeometry,latest:dict,known_as_of:str)->SupportEvaluation:
    if not (0<=geometry.minimum_coverage<=1):raise SupportError('invalid minimum coverage')
    if not (0<=geometry.degraded_threshold<=1):raise SupportError('invalid degraded threshold')
    failed=[];unknown=[];reasons=[];earned=0.0;total=sum(max(0,d.weight) for d in geometry.dimensions) or 1.0
    now=parse_time(known_as_of)
    for d in geometry.dimensions:
        obs=latest.get(d.observable_id)
        if obs is None:
            unknown.append(d.dimension_id);reasons.append(f'{d.dimension_id}:missing');continue
        ok=True
        if d.maximum_age_seconds is not None and (now-parse_time(obs.known_time)).total_seconds()>d.maximum_age_seconds:
            ok=False;reasons.append(f'{d.dimension_id}:stale')
        v=obs.value
        if d.allowed_values and v not in d.allowed_values:ok=False;reasons.append(f'{d.dimension_id}:category')
        if d.minimum is not None and (not isinstance(v,(int,float)) or v<d.minimum):ok=False;reasons.append(f'{d.dimension_id}:below')
        if d.maximum is not None and (not isinstance(v,(int,float)) or v>d.maximum):ok=False;reasons.append(f'{d.dimension_id}:above')
        if ok:earned+=max(0,d.weight)
        else:failed.append(d.dimension_id)
    coverage=round(earned/total,12)
    required_unknown={d.dimension_id for d in geometry.dimensions if d.required and d.dimension_id in unknown}
    required_failed={d.dimension_id for d in geometry.dimensions if d.required and d.dimension_id in failed}
    if required_failed:status=SupportStatus.UNSUPPORTED
    elif required_unknown and geometry.unknown_policy=='unsupported':status=SupportStatus.UNSUPPORTED
    elif required_unknown:status=SupportStatus.UNKNOWN
    elif coverage>=geometry.minimum_coverage:status=SupportStatus.SUPPORTED
    elif coverage>=geometry.degraded_threshold:status=SupportStatus.DEGRADED
    else:status=SupportStatus.UNSUPPORTED
    return SupportEvaluation(twin_id,geometry.geometry_id,known_as_of,status,coverage,tuple(sorted(failed)),tuple(sorted(unknown)),tuple(sorted(set(reasons))))
