#ifndef __SF19_LIFECYCLE_GOVERNOR_MQH__
#define __SF19_LIFECYCLE_GOVERNOR_MQH__
#include "SF19_TelemetryContracts.mqh"
class CSF19LifecycleGovernor
{
 public:
 void BuildHealth(const long now,const int active,const int critical,const int dropped,const int duplicates,const int schema_rejections,const string extra_reasons,SF19_HealthSnapshot &h)const
 {h.known_time_utc_msc=now;h.active_alert_count=active;h.critical_alert_count=critical;h.dropped_telemetry_count=dropped;h.duplicate_telemetry_count=duplicates;h.schema_rejection_count=schema_rejections;h.reasons=extra_reasons;h.state=SF19_HEALTH_HEALTHY;if(active>0||dropped>0||schema_rejections>0)h.state=SF19_HEALTH_DEGRADED;if(critical>0||schema_rejections>0)h.state=SF19_HEALTH_CRITICAL;if(StringFind(extra_reasons,"RECONCILIATION_MISMATCH")>=0||StringFind(extra_reasons,"MISSING_LIVE_TRANSACTION")>=0||StringFind(extra_reasons,"MODEL_INTEGRITY_FAILURE")>=0)h.state=SF19_HEALTH_SUSPEND_RECOMMENDED;h.snapshot_id=SF01_StableId("sf19-health",IntegerToString(now)+"|"+IntegerToString((int)h.state)+"|"+IntegerToString(active)+"|"+IntegerToString(critical)+"|"+IntegerToString(dropped)+"|"+IntegerToString(duplicates)+"|"+IntegerToString(schema_rejections)+"|"+extra_reasons);}
 void Recommend(const SF19_HealthSnapshot &h,const string scope_id,const string model_id,const string generation_id,const string evidence_ids,SF19_LifecycleRecommendation &r)const
 {r.scope_id=scope_id;r.model_id=model_id;r.generation_id=generation_id;r.known_time_utc_msc=h.known_time_utc_msc;r.reason_codes=h.reasons;r.evidence_ids=evidence_ids;r.requires_operator_approval=true;r.automatic_mutation_allowed=false;r.action=SF19_ACTION_CONTINUE;if(h.state==SF19_HEALTH_DEGRADED)r.action=SF19_ACTION_OBSERVE;else if(h.state==SF19_HEALTH_CRITICAL)r.action=SF19_ACTION_INVESTIGATE;else if(h.state==SF19_HEALTH_SUSPEND_RECOMMENDED)r.action=SF19_ACTION_SUSPEND;if(StringFind(h.reasons,"MODEL_INTEGRITY_FAILURE")>=0)r.action=SF19_ACTION_ROLLBACK;r.recommendation_id=SF01_StableId("sf19-recommendation",h.snapshot_id+"|"+IntegerToString((int)r.action)+"|"+scope_id+"|"+model_id+"|"+generation_id+"|"+evidence_ids);}
};
#endif
