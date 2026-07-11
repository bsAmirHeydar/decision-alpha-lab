#ifndef __SF19_MONITORING_COORDINATOR_MQH__
#define __SF19_MONITORING_COORDINATOR_MQH__
#include "SF19_TelemetryRing.mqh"
#include "SF19_LatencyHistogram.mqh"
#include "SF19_DriftMonitor.mqh"
#include "SF19_ExecutionDrift.mqh"
#include "SF19_AlertEngine.mqh"
#include "SF19_LifecycleGovernor.mqh"
class CSF19MonitoringCoordinator
{
 private:
 string m_run_id,m_generation_id,m_strategy_id,m_model_id;CSF19TelemetryRing m_ring;CSF19AlertEngine m_alerts;CSF19LifecycleGovernor m_governor;int m_schema_rejections,m_alert_events;string m_extra_reasons;
 public:
 CSF19MonitoringCoordinator(){m_run_id="";m_generation_id="";m_strategy_id="";m_model_id="";m_schema_rejections=0;m_alert_events=0;m_extra_reasons="";}
 bool Configure(const string run_id,const string generation_id,const string strategy_id,const string model_id,const int ring_capacity,string &error){if(run_id==""||generation_id==""||strategy_id==""){error="monitoring lineage missing";return false;}m_run_id=run_id;m_generation_id=generation_id;m_strategy_id=strategy_id;m_model_id=model_id;m_schema_rejections=0;m_alert_events=0;m_extra_reasons="";return m_ring.Configure(ring_capacity,error);}
 bool AddAlertPolicy(const SF19_AlertPolicy &p,string &error){return m_alerts.AddPolicy(p,error);}
 bool Ingest(const SF19_TelemetrySchemaEntry &schema,SF19_TelemetryEvent &event,string &error)
 {
  if(event.run_id!=m_run_id||event.generation_id!=m_generation_id||event.schema_id!=schema.schema_id||event.metric_name!=schema.metric_name){m_schema_rejections++;error="telemetry lineage or schema mismatch";return false;}
  if(schema.has_lower_bound&&event.value<schema.lower_bound){m_schema_rejections++;error="telemetry below lower bound";return false;}if(schema.has_upper_bound&&event.value>schema.upper_bound){m_schema_rejections++;error="telemetry above upper bound";return false;}
  if(!SF19_ValidateTelemetryEvent(event,error)){m_schema_rejections++;return false;}if(!m_ring.Append(event,error))return false;SF19_AlertEvent a;bool emitted=false;if(!m_alerts.Observe(event.metric_name,event.value,event.known_time_utc_msc,event.correlation_id,a,emitted,error))return false;if(emitted)m_alert_events++;return true;
 }
 void AddReason(const string reason){if(reason=="")return;if(StringFind(m_extra_reasons,reason)<0)m_extra_reasons+=(m_extra_reasons==""?"":"|")+reason;}
 void Snapshot(const long now,SF19_HealthSnapshot &health,SF19_LifecycleRecommendation &recommendation)const{m_governor.BuildHealth(now,m_alerts.ActiveCount(),m_alerts.CriticalCount(),m_ring.DroppedCount(),m_ring.DuplicateCount(),m_schema_rejections,m_extra_reasons,health);m_governor.Recommend(health,m_strategy_id,m_model_id,m_generation_id,"alerts="+IntegerToString(m_alert_events),recommendation);}
 int TelemetryCount()const{return m_ring.Count();}int DroppedCount()const{return m_ring.DroppedCount();}int SchemaRejectionCount()const{return m_schema_rejections;}
};
#endif
