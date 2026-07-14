#ifndef __FP_I10_ENGINE_MQH__
#define __FP_I10_ENGINE_MQH__
#include "FP_I10_InputValidation.mqh"
#include "FP_I10_InstanceIdentity.mqh"
#include "FP_I10_EngineComposition.mqh"
#include "FP_I10_Health.mqh"
#include "FP_I10_OutputBuffers.mqh"
class FP_I10_Engine {
private:
 SFP_I10_Config m_config; SFP_I10_EngineSnapshot m_snapshot; bool m_initialized; long m_calculate_calls; long m_timer_calls;
public:
 FP_I10_Engine(){m_initialized=false;m_calculate_calls=0;m_timer_calls=0;}
 bool Initialize(SFP_I10_Config &config,const long chart_id,string &reason){
  m_snapshot.health.lifecycle=FP_I10_INITIALIZING; if(!FP_I10_ValidateConfig(config,reason)) return false; if(!FP_I10_ValidateComposition(reason)) return false; m_config=config; m_snapshot.instance=FP_I10_BuildInstance(config,chart_id); m_snapshot.sequence=0; m_snapshot.last_processed_m1=0; m_snapshot.source_revision_id="REV-INIT"; m_snapshot.health.lifecycle=FP_I10_READY; m_snapshot.health.data_readiness=FP_I10_DATA_PARTIAL; m_snapshot.health.history_ready=false; m_snapshot.health.checkpoint=FP_I10_CKPT_ABSENT; m_snapshot.health.incremental_lag_minutes=0; m_snapshot.health.last_processing_us=0; m_snapshot.health.overall=FP_I10_HEALTH_DEGRADED; FP_I10_ClearOutput(m_snapshot.output); m_snapshot.snapshot_hash=FP_I10_StableId("FPSNAP",m_snapshot.instance.instance_id+"|INIT"); m_initialized=true; reason="FP_IND_ENGINE_READY"; return true;
 }
 bool OnCalculate(const datetime newest_closed_m1,const int rates_total,const int prev_calculated){
  if(!m_initialized || newest_closed_m1<=0) return false;
  m_calculate_calls++;
  if(newest_closed_m1>m_snapshot.last_processed_m1){ m_snapshot.last_processed_m1=newest_closed_m1; m_snapshot.sequence++; }
  const long required_m1_bars=(long)m_config.history_days*1440;
  const int primary_m1_bars=Bars(m_config.primary_symbol,PERIOD_M1);
  const int secondary_m1_bars=Bars(m_config.secondary_symbol,PERIOD_M1);
  m_snapshot.health.history_ready=(primary_m1_bars>=required_m1_bars && secondary_m1_bars>=required_m1_bars);
  m_snapshot.health.data_readiness=m_snapshot.health.history_ready?FP_I10_DATA_READY:FP_I10_DATA_PARTIAL;
  m_snapshot.health.overall=FP_I10_AggregateHealth(m_snapshot.health.lifecycle,m_snapshot.health.data_readiness,m_snapshot.health.history_ready,m_snapshot.health.incremental_lag_minutes);
  m_snapshot.output.health_code=(double)m_snapshot.health.overall;
  m_snapshot.output.lifecycle_code=(double)m_snapshot.health.lifecycle;
  m_snapshot.output.data_readiness_code=(double)m_snapshot.health.data_readiness;
  m_snapshot.output.heartbeat_utc_minute=(double)(TimeGMT()/60);
  m_snapshot.snapshot_hash=FP_I10_StableId("FPSNAP",m_snapshot.instance.instance_id+"|"+IntegerToString(m_snapshot.sequence)+"|"+TimeToString(m_snapshot.last_processed_m1,TIME_DATE|TIME_MINUTES));
  m_snapshot.output.snapshot_hash=m_snapshot.snapshot_hash;
  return true;
 }
 void OnTimer(){ if(!m_initialized)return; m_timer_calls++; m_snapshot.output.heartbeat_utc_minute=(double)(TimeGMT()/60); }
 void OnChartEvent(const int id,const long lparam,const double dparam,const string sparam){ if(!m_initialized)return; }
 void Shutdown(){ if(!m_initialized)return; m_snapshot.health.lifecycle=FP_I10_STOPPING; m_snapshot.health.lifecycle=FP_I10_STOPPED; m_initialized=false; }
 bool IsInitialized()const{return m_initialized;} SFP_I10_EngineSnapshot Snapshot()const{return m_snapshot;} string InstanceId()const{return m_snapshot.instance.instance_id;}
};
#endif
