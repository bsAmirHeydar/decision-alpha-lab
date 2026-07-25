from .contracts import *
def derive_health(admission=None,plan=None,run=None,checkpoint=None):
    reasons=[]
    if admission and admission.status==AdmissionStatus.BLOCKED: reasons+=list(admission.reason_codes)
    if plan and plan.state==PlanState.BLOCKED: reasons+=list(plan.reason_codes)
    if run and run.health==HealthState.BLOCKED: reasons+=list(run.reason_codes)
    if checkpoint and checkpoint.disposition!=CheckpointDisposition.ACCEPTED: reasons+=list(checkpoint.reason_codes)
    if reasons: return HealthState.BLOCKED,tuple(sorted(set(reasons)))
    if run and run.health==HealthState.DEGRADED: return HealthState.DEGRADED,run.reason_codes
    return HealthState.READY,("FP_PAPER_HEALTH_READY",)
