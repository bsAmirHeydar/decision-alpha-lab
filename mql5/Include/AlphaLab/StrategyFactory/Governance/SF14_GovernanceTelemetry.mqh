#ifndef __SF14_GOVERNANCE_TELEMETRY_MQH__
#define __SF14_GOVERNANCE_TELEMETRY_MQH__
struct SF14_GovernanceTelemetry{int registered_count;int validated_count;int eligible_count;int rejected_count;int champion_count;int challenger_count;int suspended_count;int rollback_count;int integrity_failure_count;long last_decision_utc_msc;};
void SF14_ResetGovernanceTelemetry(SF14_GovernanceTelemetry &v){v.registered_count=0;v.validated_count=0;v.eligible_count=0;v.rejected_count=0;v.champion_count=0;v.challenger_count=0;v.suspended_count=0;v.rollback_count=0;v.integrity_failure_count=0;v.last_decision_utc_msc=0;}
#endif
