#ifndef __FP_I13_RELEASE_GUARD_MQH__
#define __FP_I13_RELEASE_GUARD_MQH__
#include "FP_I13_ReplayTelemetry.mqh"
#include "FP_I13_ReleaseProfiles.mqh"
#include "FP_I13_InstanceIsolation.mqh"
#include "FP_I13_AcceptanceGate.mqh"
#include "FP_I13_Diagnostics.mqh"
class FP_I13_ReleaseGuard { private:bool m_initialized;long m_chart_id;SFP_I13_Config m_cfg;FP_I13_ReplayTelemetry m_telemetry;SFP_I13_Acceptance m_acceptance;datetime m_last_log; public:FP_I13_ReleaseGuard(){m_initialized=false;m_chart_id=0;m_last_log=0;}bool Initialize(long chart_id,const string instance_id,SFP_I13_Config &cfg,string &reason){m_chart_id=chart_id;m_cfg=cfg;if(cfg.open_decision_state!="UNSET"){reason="FP_REL_OPEN_DECISION_STATE_INVALID";return false;}if(!FP_I13_InstanceIsolation::Validate(chart_id,instance_id,reason))return false;m_acceptance=FP_I13_AcceptanceGate::SourceAccepted();m_initialized=true;reason="FP_REL_SOURCE_ACCEPTED";return true;}void ObserveFrame(ulong elapsed_us,int objects,int ops,long events,bool full_scan=false){if(!m_initialized)return;m_telemetry.Observe(m_cfg,elapsed_us,objects,ops,events,full_scan);}void MaybeLog(int interval_seconds){if(!m_initialized||interval_seconds<=0)return;datetime now=TimeCurrent();if(m_last_log>0&&now-m_last_log<interval_seconds)return;m_last_log=now;SFP_I13_Telemetry t=m_telemetry.Snapshot();Print("FP-I13 release telemetry status=",FP_I13_StatusText(t.budget_status)," elapsed_us=",t.elapsed_us," objects=",t.object_count," ops=",t.object_ops," events=",t.event_count," reason=",t.reason_code);}SFP_I13_Telemetry Telemetry()const{return m_telemetry.Snapshot();}SFP_I13_Acceptance Acceptance()const{return m_acceptance;}bool IsInitialized()const{return m_initialized;}void Shutdown(){m_initialized=false;} };
#endif
