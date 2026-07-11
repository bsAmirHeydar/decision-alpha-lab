#ifndef __SF05_ENVELOPE_FACTORY_MQH__
#define __SF05_ENVELOPE_FACTORY_MQH__
#include "SF05_ResultEnvelope.mqh"
#include "../Contracts/SF01_ContractCodecs.mqh"

class CSF05EnvelopeFactory
{
private:
   string m_run_id;
   string m_generation_uid;
   long m_sequence;
public:
   CSF05EnvelopeFactory(void){m_run_id="";m_generation_uid="";m_sequence=0;}
   void Configure(const string run_id,const string generation_uid){m_run_id=run_id;m_generation_uid=generation_uid;m_sequence=0;}
   long LastSequence(void)const{return m_sequence;}
   SF05_ResultEnvelope Create(const ENUM_SF05_RECORD_TYPE type,const string aggregate_id,const string producer_id,const string producer_version,const SF01_MarketTimestamp &occurred,const SF01_MarketTimestamp &known,const string payload_schema,const string payload_json)
   {
      SF05_ResultEnvelope v;v.schema="alpha_lab.strategy_factory/result_envelope@1.0.0";v.sequence=++m_sequence;v.record_type=type;v.record_id="";v.run_id=m_run_id;v.generation_uid=m_generation_uid;v.aggregate_id=aggregate_id;v.producer_id=producer_id;v.producer_version=producer_version;v.occurred_at=occurred;v.known_at=known;v.payload_schema=payload_schema;v.payload_hash=SF01_StableId("pay",payload_json);v.payload_json=payload_json;v.record_id=SF05_DeriveResultRecordId(v);return v;
   }
};
#endif
