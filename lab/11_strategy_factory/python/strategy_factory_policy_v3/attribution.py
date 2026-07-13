from __future__ import annotations
from .contracts import AttributionOpportunity,IncrementalValueReport
from .canonical import canonical_sha256,stable_id
from .errors import PolicyError

def incremental_value(opportunities):
    ops=tuple(opportunities)
    if not ops: raise PolicyError('empty_attribution','attribution requires opportunities')
    manual=sum(o.manual_value for o in ops); hybrid=sum(o.hybrid_value for o in ops); total=hybrid-manual
    selection=treatment=risk=timing=0.0
    for o in ops:
        d=o.hybrid_value-o.manual_value
        if o.manual_selected!=o.hybrid_selected: selection+=d
        elif o.treatment_changed:treatment+=d
        elif o.risk_changed:risk+=d
        timing+=o.timing_delta
    residual=total-selection-treatment-risk-timing
    components={'selection':selection,'treatment':treatment,'risk':risk,'timing':timing,'residual':residual}
    wins=sum(o.hybrid_value>o.manual_value for o in ops)/len(ops)
    payload={'opportunities':[o.opportunity_id for o in ops],'manual_total':manual,'hybrid_total':hybrid,'components':components}
    return IncrementalValueReport(stable_id('incremental_value',payload),len(ops),manual,hybrid,total,components,wins,canonical_sha256(payload))
