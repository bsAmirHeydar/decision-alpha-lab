from __future__ import annotations
from .types import Finding,Severity

_ALLOWED_LATE={"REJECT","QUARANTINE","APPEND_CORRECTION","ALLOW_WITH_STALE_FLAG"}
_REQUIRED_CLOCKS=("event_time","observation_time","known_time","decision_time","maturity_time","correction_time")

def validate_causal_clock(clock:dict)->dict:
    f=[]; fields=clock.get("clocks",{})
    for name in _REQUIRED_CLOCKS:
        spec=fields.get(name)
        if not isinstance(spec,dict): f.append(Finding("ACL02_CLOCK_MISSING",Severity.BLOCKER,f"causal_clock.clocks.{name}","required causal clock is missing","declare source field, timezone, availability and monotonicity")); continue
        if not spec.get("field") and not spec.get("rule"): f.append(Finding("ACL02_CLOCK_SOURCE_UNDEFINED",Severity.BLOCKER,f"causal_clock.clocks.{name}","clock has no field or derivation rule","declare an observable field or deterministic derivation"))
        if name in {"known_time","decision_time"} and spec.get("can_use_future_revision") is not False: f.append(Finding("ACL02_FUTURE_REVISION_NOT_FORBIDDEN",Severity.BLOCKER,f"causal_clock.clocks.{name}.can_use_future_revision","decision-relevant clock must forbid future revisions","set can_use_future_revision: false"))
    order=clock.get("required_order",[]); expected=["event_time<=observation_time","observation_time<=known_time","known_time<=decision_time","decision_time<=maturity_time","maturity_time<=correction_time"]
    missing=[x for x in expected if x not in order]
    if missing:f.append(Finding("ACL02_CLOCK_ORDER_INCOMPLETE",Severity.BLOCKER,"causal_clock.required_order",f"missing causal order assertions: {missing}","declare every required partial-order invariant"))
    if clock.get("late_data_policy") not in _ALLOWED_LATE:f.append(Finding("ACL02_LATE_DATA_POLICY_INVALID",Severity.BLOCKER,"causal_clock.late_data_policy","unsupported late-data policy","use a registered fail-closed policy"))
    if int(clock.get("clock_skew_tolerance_ms",-1))<0:f.append(Finding("ACL02_CLOCK_SKEW_INVALID",Severity.BLOCKER,"causal_clock.clock_skew_tolerance_ms","clock skew tolerance must be non-negative","declare a measured non-negative tolerance"))
    return {"passed":not any(x.severity==Severity.BLOCKER for x in f),"findings":[x.to_dict() for x in f]}
