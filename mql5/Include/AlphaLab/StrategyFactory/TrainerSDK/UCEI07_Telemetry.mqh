#ifndef ALPHALAB_UCEI07_TELEMETRY_MQH
#define ALPHALAB_UCEI07_TELEMETRY_MQH
#include "UCEI07_Contracts.mqh"
class CUCEI07TelemetryRing{
private:UCEI07_TelemetryEvent m_items[];int m_capacity;int m_count;long m_sequence;
public:
 CUCEI07TelemetryRing(){m_capacity=64;m_count=0;m_sequence=0;ArrayResize(m_items,m_capacity);}
 void Configure(const int capacity){m_capacity=MathMax(1,capacity);m_count=0;m_sequence=0;ArrayResize(m_items,m_capacity);}
 void Emit(const string phase,const string trainer_key,const string fold_id,const string code,const string severity,const long elapsed_ms,const long rows,const long features,const double memory_mb,const string details_json){int idx=(int)(m_sequence%m_capacity);m_sequence++;UCEI07_TelemetryEvent e;e.sequence=m_sequence;e.phase=phase;e.trainer_key=trainer_key;e.fold_id=fold_id;e.event_code=code;e.severity=severity;e.elapsed_ms=elapsed_ms;e.row_count=rows;e.feature_count=features;e.memory_estimate_mb=memory_mb;e.details_json=details_json;m_items[idx]=e;if(m_count<m_capacity)m_count++;}
 int Count()const{return m_count;} long Sequence()const{return m_sequence;}
 bool Latest(UCEI07_TelemetryEvent &out)const{if(m_count<1)return false;int idx=(int)((m_sequence-1)%m_capacity);out=m_items[idx];return true;}
};
#endif
