#ifndef __SF19_TELEMETRY_CONTRACTS_MQH__
#define __SF19_TELEMETRY_CONTRACTS_MQH__
#include <AlphaLab/StrategyFactory/Contracts/SF01_Hash.mqh>
#include <AlphaLab/StrategyFactory/Contracts/SF01_StringCodec.mqh>
#include "SF19_MonitoringEnums.mqh"
struct SF19_TelemetrySchemaEntry
{
 string metric_name,schema_version,unit,stage,description,schema_id;ENUM_SF19_METRIC_KIND metric_kind;double lower_bound,upper_bound;bool has_lower_bound,has_upper_bound;
};
string SF19_TelemetrySchemaCanonical(const SF19_TelemetrySchemaEntry &e)
{
 return e.metric_name+"|"+e.schema_version+"|"+IntegerToString((int)e.metric_kind)+"|"+e.unit+"|"+e.stage+"|"+e.description+"|"+SF01_CanonicalBool(e.has_lower_bound)+"|"+SF01_CanonicalDouble(e.lower_bound)+"|"+SF01_CanonicalBool(e.has_upper_bound)+"|"+SF01_CanonicalDouble(e.upper_bound);
}
string SF19_DeriveSchemaId(const SF19_TelemetrySchemaEntry &e){return SF01_StableId("sf19-schema",SF19_TelemetrySchemaCanonical(e));}
struct SF19_TelemetryEvent
{
 string metric_name,schema_id,run_id,generation_id,strategy_id,model_id,correlation_id,causation_id,payload_hash,event_id;long observed_time_utc_msc,known_time_utc_msc,sequence;double value;
};
string SF19_TelemetryEventCanonical(const SF19_TelemetryEvent &e)
{
 return e.metric_name+"|"+e.schema_id+"|"+e.run_id+"|"+e.generation_id+"|"+e.strategy_id+"|"+e.model_id+"|"+e.correlation_id+"|"+e.causation_id+"|"+IntegerToString(e.observed_time_utc_msc)+"|"+IntegerToString(e.known_time_utc_msc)+"|"+IntegerToString(e.sequence)+"|"+SF01_CanonicalDouble(e.value);
}
string SF19_DeriveTelemetryPayloadHash(const SF19_TelemetryEvent &e){return SF01_StableId("sf19-payload",e.metric_name+"|"+SF01_CanonicalDouble(e.value));}
string SF19_DeriveTelemetryEventId(const SF19_TelemetryEvent &e){return SF01_StableId("sf19-event",e.run_id+"|"+IntegerToString(e.sequence)+"|"+e.metric_name+"|"+IntegerToString(e.known_time_utc_msc)+"|"+e.payload_hash);}
bool SF19_ValidateTelemetryEvent(const SF19_TelemetryEvent &e,string &error)
{
 if(e.metric_name==""||e.schema_id==""||e.run_id==""||e.generation_id==""||e.correlation_id==""){error="required telemetry identity missing";return false;}
 if(e.sequence<1){error="telemetry sequence must be positive";return false;}
 if(e.known_time_utc_msc<e.observed_time_utc_msc){error="known time precedes observed time";return false;}
 if(!MathIsValidNumber(e.value)){error="telemetry value is non-finite";return false;}
 if(e.payload_hash!=SF19_DeriveTelemetryPayloadHash(e)){error="telemetry payload hash mismatch";return false;}
 if(e.event_id!=SF19_DeriveTelemetryEventId(e)){error="telemetry event id mismatch";return false;}error="";return true;
}
struct SF19_HealthSnapshot
{
 string snapshot_id;long known_time_utc_msc;ENUM_SF19_HEALTH_STATE state;int active_alert_count,critical_alert_count,dropped_telemetry_count,duplicate_telemetry_count,schema_rejection_count;string reasons;
};
struct SF19_LifecycleRecommendation
{
 string recommendation_id,scope_id,model_id,generation_id,reason_codes,evidence_ids;ENUM_SF19_LIFECYCLE_ACTION action;long known_time_utc_msc;bool requires_operator_approval,automatic_mutation_allowed;
};
bool SF19_ValidateLifecycleRecommendation(const SF19_LifecycleRecommendation &r,string &error)
{
 if(r.recommendation_id==""||r.scope_id==""||r.generation_id==""){error="recommendation identity missing";return false;}
 if(!r.requires_operator_approval||r.automatic_mutation_allowed){error="Phase 19 cannot mutate runtime automatically";return false;}error="";return true;
}
#endif
