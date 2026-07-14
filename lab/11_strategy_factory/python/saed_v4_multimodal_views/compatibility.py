from .models import CrossViewCompatibility
from .enums import CompatibilityStatus,ViewStatus
from .errors import CompatibilityError

def assess_compatibility(views,required_view_names):
    if not views:raise CompatibilityError('empty view package')
    twins={v.twin_id for v in views};known={v.known_as_of for v in views};event={v.event_as_of for v in views};roles={v.evidence_role for v in views}
    reasons=[]
    if len(twins)!=1:reasons.append('twin_mismatch')
    if len(known)!=1:reasons.append('known_boundary_mismatch')
    if len(event)!=1:reasons.append('event_boundary_mismatch')
    if len(roles)!=1:reasons.append('evidence_role_mismatch')
    names={v.view_name for v in views};missing=tuple(sorted(set(required_view_names)-names));degraded=tuple(sorted(v.view_name for v in views if v.status!=ViewStatus.COMPLETE))
    if missing:reasons.append('missing_required_views')
    if reasons:status=CompatibilityStatus.INCOMPATIBLE
    elif degraded:status=CompatibilityStatus.DEGRADED
    else:status=CompatibilityStatus.COMPATIBLE
    return CrossViewCompatibility(status,next(iter(twins)) if len(twins)==1 else '',next(iter(known)) if len(known)==1 else '',next(iter(event)) if len(event)==1 else '',next(iter(roles)) if len(roles)==1 else views[0].evidence_role,tuple(sorted(v.view_id for v in views)),missing,degraded,tuple(sorted(reasons)))
