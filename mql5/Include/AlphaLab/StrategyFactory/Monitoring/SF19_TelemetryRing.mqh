#ifndef __SF19_TELEMETRY_RING_MQH__
#define __SF19_TELEMETRY_RING_MQH__
#include "SF19_TelemetryContracts.mqh"
class CSF19TelemetryRing
{
 private: SF19_TelemetryEvent m_items[SF19_MAX_TELEMETRY_RECORDS];int m_capacity,m_count,m_head,m_dropped,m_duplicates,m_sequence_rejections;long m_last_sequence;string m_run_id;
 public:
 CSF19TelemetryRing(){m_capacity=0;m_count=0;m_head=0;m_dropped=0;m_duplicates=0;m_sequence_rejections=0;m_last_sequence=0;m_run_id="";}
 bool Configure(const int capacity,string &error){if(capacity<1||capacity>SF19_MAX_TELEMETRY_RECORDS){error="invalid telemetry ring capacity";return false;}m_capacity=capacity;m_count=0;m_head=0;m_dropped=0;m_duplicates=0;m_sequence_rejections=0;m_last_sequence=0;m_run_id="";error="";return true;}
 bool Contains(const string event_id)const{for(int i=0;i<m_count;i++){int idx=(m_head+i)%m_capacity;if(m_items[idx].event_id==event_id)return true;}return false;}
 bool Append(const SF19_TelemetryEvent &e,string &error)
 {
  if(m_capacity<1){error="ring not configured";return false;}if(Contains(e.event_id)){m_duplicates++;error="duplicate telemetry event";return false;}
  if(m_run_id==e.run_id&&e.sequence<=m_last_sequence){m_sequence_rejections++;error="non-monotonic sequence";return false;}
  if(m_count==m_capacity){m_head=(m_head+1)%m_capacity;m_count--;m_dropped++;}
  int idx=(m_head+m_count)%m_capacity;m_items[idx]=e;m_count++;m_run_id=e.run_id;m_last_sequence=e.sequence;error="";return true;
 }
 int Count()const{return m_count;}int DroppedCount()const{return m_dropped;}int DuplicateCount()const{return m_duplicates;}int SequenceRejectionCount()const{return m_sequence_rejections;}
 bool At(const int logical_index,SF19_TelemetryEvent &out)const{if(logical_index<0||logical_index>=m_count)return false;out=m_items[(m_head+logical_index)%m_capacity];return true;}
};
#endif
