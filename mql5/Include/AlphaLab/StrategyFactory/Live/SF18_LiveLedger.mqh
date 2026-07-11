#ifndef __SF18_LIVE_LEDGER_MQH__
#define __SF18_LIVE_LEDGER_MQH__
#include "SF18_CircuitBreaker.mqh"
struct SF18_LiveTransaction{string transaction_id;int sequence;ENUM_SF18_TRANSACTION_TYPE transaction_type;string entity_id;long event_time_utc_msc;string previous_chain_hash,payload_hash,chain_hash,message;};
class CSF18LiveLedger
{
private:SF18_LiveTransaction m_rows[SF18_MAX_LEDGER_RECORDS];int m_count;string m_tail;
public:
 CSF18LiveLedger(){Reset();}void Reset(void){m_count=0;m_tail="GENESIS";}
 bool Append(const ENUM_SF18_TRANSACTION_TYPE type,const string entity_id,const long now,const string payload_hash,const string message)
 {
  if(m_count>=SF18_MAX_LEDGER_RECORDS)return false;const int seq=m_count+1;const string canonical=IntegerToString(seq)+"|"+IntegerToString((int)type)+"|"+entity_id+"|"+IntegerToString(now)+"|"+m_tail+"|"+payload_hash+"|"+message;
  SF18_LiveTransaction r;r.transaction_id=SF01_StableId("ltx",canonical);r.sequence=seq;r.transaction_type=type;r.entity_id=entity_id;r.event_time_utc_msc=now;r.previous_chain_hash=m_tail;r.payload_hash=payload_hash;r.chain_hash=SF01_StableId("lchn",m_tail+"|"+canonical);r.message=message;m_rows[m_count++]=r;m_tail=r.chain_hash;return true;
 }
 int Count(void)const{return m_count;}string TailHash(void)const{return m_tail;}bool Get(const int index,SF18_LiveTransaction &out)const{if(index<0||index>=m_count)return false;out=m_rows[index];return true;}
};
#endif
