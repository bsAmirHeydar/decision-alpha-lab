from .contracts import *
from .canonical import *
from .admission import admit_winner
from .geometry import build_geometry
from .sizing import size_fixed_risk

def build_plan(proof,winner,readiness,quote,spec,risk,created_utc_ms,parent_plan_id="",revision=1):
    adm=admit_winner(proof,winner,readiness)
    geo=build_geometry(winner,quote,spec,risk)
    size=size_fixed_risk(geo,spec,risk)
    reasons=tuple(sorted(set(adm.reason_codes+geo.reason_codes+size.reason_codes)))
    state=PlanState.READY if adm.status==AdmissionStatus.ADMITTED and geo.status==GeometryStatus.READY and size.status==GeometryStatus.READY else PlanState.BLOCKED
    payload={"parent":parent_plan_id,"revision":revision,"signal":winner.signal_id,"signal_hash":winner.signal_hash,"quota":winner.quota_key_id,"i09":winner.i09_reservation_id,"symbol":winner.protected_symbol,"direction":winner.direction,"geometry":geo.geometry_hash,"sizing":size.sizing_hash,"risk":risk.config_hash,"acceptance":proof.acceptance_id,"revision_id":winner.source_revision_id,"created":created_utc_ms,"state":state,"reasons":reasons}
    pid=stable_id("FPPLAN",payload)
    return ExecutionPlan(pid,parent_plan_id,revision,state,winner.signal_id,winner.signal_hash,winner.quota_key_id,winner.i09_reservation_id,winner.protected_symbol,winner.direction,geo,size,risk.config_hash,proof.acceptance_id,winner.source_revision_id,created_utc_ms,reasons,sha256(payload))
