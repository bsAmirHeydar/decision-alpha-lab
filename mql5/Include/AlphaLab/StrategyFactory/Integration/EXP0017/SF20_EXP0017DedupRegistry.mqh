#ifndef __SF20_EXP0017_DEDUP_REGISTRY_MQH__
#define __SF20_EXP0017_DEDUP_REGISTRY_MQH__
#include "SF20_EXP0017Contracts.mqh"
class CSF20EXP0017DedupRegistry
{
private:string m_ids[];long m_first_seen[],m_last_seen[];bool m_active[];int m_capacity;long m_pulse;
 int Find(const string id)const{for(int i=0;i<ArraySize(m_ids);i++)if(m_ids[i]==id)return i;return -1;}
public:CSF20EXP0017DedupRegistry(){m_capacity=4096;m_pulse=0;}bool Configure(const int capacity,string &error){if(capacity<1||capacity>100000){error="invalid dedup capacity";return false;}m_capacity=capacity;Clear();error="";return true;}
 void Clear(){ArrayResize(m_ids,0);ArrayResize(m_first_seen,0);ArrayResize(m_last_seen,0);ArrayResize(m_active,0);m_pulse=0;}
 void BeginPulse(){m_pulse++;for(int i=0;i<ArraySize(m_active);i++)m_active[i]=false;}
 bool Observe(const string event_id,const long now,bool &is_new,SF20_EXP0017LifecycleRecord &record,string &error)
 {
  int i=Find(event_id);is_new=(i<0);if(i<0){if(ArraySize(m_ids)>=m_capacity){error="dedup capacity exhausted";return false;}i=ArraySize(m_ids);ArrayResize(m_ids,i+1);ArrayResize(m_first_seen,i+1);ArrayResize(m_last_seen,i+1);ArrayResize(m_active,i+1);m_ids[i]=event_id;m_first_seen[i]=now;}
  m_last_seen[i]=now;m_active[i]=true;record.event_id=event_id;record.state=is_new?SF20_LIFECYCLE_FIRST_SEEN:SF20_LIFECYCLE_ACTIVE;record.first_seen_utc_msc=m_first_seen[i];record.last_seen_utc_msc=now;record.pulse_sequence=m_pulse;record.reason="candidate_present";record.record_id=SF01_StableId("sf20life",event_id+"|"+IntegerToString((int)record.state)+"|"+IntegerToString(record.first_seen_utc_msc)+"|"+IntegerToString(now)+"|"+IntegerToString(m_pulse));error="";return true;
 }
 int RetireMissing(const long now,SF20_EXP0017LifecycleRecord &records[])
 {
  ArrayResize(records,0);for(int i=0;i<ArraySize(m_ids);i++){if(m_active[i]||m_last_seen[i]<=0)continue;int n=ArraySize(records);ArrayResize(records,n+1);records[n].event_id=m_ids[i];records[n].state=SF20_LIFECYCLE_RETIRED;records[n].first_seen_utc_msc=m_first_seen[i];records[n].last_seen_utc_msc=now;records[n].pulse_sequence=m_pulse;records[n].reason="candidate_absent_on_completed_pulse";records[n].record_id=SF01_StableId("sf20life",m_ids[i]+"|retired|"+IntegerToString(now)+"|"+IntegerToString(m_pulse));m_last_seen[i]=0;}return ArraySize(records);
 }
 int Count()const{return ArraySize(m_ids);}long PulseSequence()const{return m_pulse;}
};
#endif
