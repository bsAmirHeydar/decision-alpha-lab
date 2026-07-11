#ifndef __SF17_TRANSACTION_LEDGER_MQH__
#define __SF17_TRANSACTION_LEDGER_MQH__
#include "SF17_PositionRecord.mqh"
struct SF17_TransactionRecord{string transaction_id;long sequence;ENUM_SF17_TRANSACTION_TYPE transaction_type;string entity_id;long event_time_utc_msc;string previous_chain_hash;string payload_hash;string chain_hash;string message;};
class CSF17TransactionLedger
{
private: SF17_TransactionRecord m_rows[SF17_MAX_TRANSACTIONS];int m_count;string m_tail;
public:
   CSF17TransactionLedger(){Reset();}
   void Reset(){m_count=0;m_tail="GENESIS";}
   int Count()const{return m_count;} string TailHash()const{return m_tail;}
   bool Append(const ENUM_SF17_TRANSACTION_TYPE type,const string entity_id,const long event_time,const string payload_hash,const string message)
   {
      if(m_count>=SF17_MAX_TRANSACTIONS)return false;const long sequence=m_count+1;
      const string canonical=IntegerToString(sequence)+"|"+IntegerToString((int)type)+"|"+entity_id+"|"+IntegerToString(event_time)+"|"+payload_hash+"|"+message;
      SF17_TransactionRecord r;r.transaction_id=SF01_StableId("xtxn",canonical);r.sequence=sequence;r.transaction_type=type;r.entity_id=entity_id;r.event_time_utc_msc=event_time;r.previous_chain_hash=m_tail;r.payload_hash=payload_hash;r.chain_hash=SF01_StableId("xchn",m_tail+"|"+canonical);r.message=message;m_rows[m_count++]=r;m_tail=r.chain_hash;return true;
   }
   bool Get(const int index,SF17_TransactionRecord &out)const{if(index<0||index>=m_count)return false;out=m_rows[index];return true;}
};
#endif
