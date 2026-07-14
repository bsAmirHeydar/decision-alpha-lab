#ifndef __FP_I13_REPLAY_TELEMETRY_MQH__
#define __FP_I13_REPLAY_TELEMETRY_MQH__
#include "FP_I13_PerformanceBudget.mqh"
class FP_I13_ReplayTelemetry { private:SFP_I13_Telemetry m_t; public:FP_I13_ReplayTelemetry(){Reset();}void Reset(){m_t.frame_sequence=0;m_t.elapsed_us=0;m_t.object_count=0;m_t.object_ops=0;m_t.event_count=0;m_t.full_scan_count=0;m_t.incremental_count=0;m_t.events_per_second=0;m_t.budget_status=FP_I13_BUDGET_PASS;m_t.reason_code="FP_REL_REPLAY_STARTED";}void Observe(const SFP_I13_Config &c,ulong elapsed_us,int objects,int ops,long events,bool full_scan){m_t.frame_sequence++;m_t.elapsed_us=elapsed_us;m_t.object_count=objects;m_t.object_ops=ops;m_t.event_count=events;if(full_scan)m_t.full_scan_count++;else m_t.incremental_count++;m_t.events_per_second=(elapsed_us>0?(double)events*1000000.0/(double)elapsed_us:0.0);m_t.budget_status=FP_I13_PerformanceBudget::Evaluate(c,elapsed_us,objects,ops,m_t.reason_code);}SFP_I13_Telemetry Snapshot()const{return m_t;} };
#endif
