from __future__ import annotations
from .models import ViewSupportAssessment
from .enums import SupportStatus

def assess_support(spec,features):
    by={f.feature_id:f for f in features};missing=[];stale=[];low=[];oor=[];rp=op=0;rt=ot=0
    for d in spec.features:
        f=by[d.feature_id]
        if d.required:rt+=1
        else:ot+=1
        passed=True
        if f.missing:missing.append(d.feature_id);passed=False
        if f.stale:stale.append(d.feature_id);passed=False
        if f.quality<d.minimum_quality:low.append(d.feature_id);passed=False
        if 'out_of_range' in f.reason_codes:oor.append(d.feature_id);passed=False
        if passed:
            if d.required:rp+=1
            else:op+=1
    total=max(1,rt+ot);score=(rp+op)/total
    if rt and rp<rt:
        status=SupportStatus.UNKNOWN if missing else SupportStatus.UNSUPPORTED
    elif score<spec.minimum_support_score:status=SupportStatus.DEGRADED
    elif missing or stale or low or oor:status=SupportStatus.DEGRADED
    else:status=SupportStatus.SUPPORTED
    reasons=[]
    if missing:reasons.append('missing_features')
    if stale:reasons.append('stale_features')
    if low:reasons.append('low_quality_features')
    if oor:reasons.append('out_of_range_features')
    return ViewSupportAssessment(status,round(score,12),rt,rp,ot,op,tuple(sorted(missing)),tuple(sorted(stale)),tuple(sorted(low)),tuple(sorted(oor)),tuple(sorted(reasons)))
