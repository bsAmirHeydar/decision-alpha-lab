#ifndef __SF05_RESULT_ENVELOPE_MQH__
#define __SF05_RESULT_ENVELOPE_MQH__
#include "SF05_RuntimeGeneration.mqh"

struct SF05_ResultEnvelope
{
   string schema;
   long sequence;
   ENUM_SF05_RECORD_TYPE record_type;
   string record_id;
   string run_id;
   string generation_uid;
   string aggregate_id;
   string producer_id;
   string producer_version;
   SF01_MarketTimestamp occurred_at;
   SF01_MarketTimestamp known_at;
   string payload_schema;
   string payload_hash;
   string payload_json;
};

string SF05_ResultEnvelopeCanonical(const SF05_ResultEnvelope &v)
{
   return v.schema+"|"+IntegerToString(v.sequence)+"|"+IntegerToString((int)v.record_type)+"|"+
          v.run_id+"|"+v.generation_uid+"|"+v.aggregate_id+"|"+v.producer_id+"|"+
          v.producer_version+"|"+IntegerToString(v.occurred_at.utc_epoch_milliseconds)+"|"+
          IntegerToString(v.known_at.utc_epoch_milliseconds)+"|"+v.payload_schema+"|"+
          v.payload_hash;
}

string SF05_DeriveResultRecordId(const SF05_ResultEnvelope &v)
{
   return SF01_StableId("rec",SF05_ResultEnvelopeCanonical(v));
}

bool SF05_ValidateResultEnvelope(const SF05_ResultEnvelope &v,string &e)
{
   if(v.schema!="alpha_lab.strategy_factory/result_envelope@1.0.0"){e="unsupported envelope schema";return false;}
   if(v.sequence<=0){e="sequence must be positive";return false;}
   if(v.record_type==SF05_RECORD_UNKNOWN){e="unknown record type";return false;}
   if(!SF01_IsSafeIdentifier(v.run_id,128)||!SF01_IsSafeIdentifier(v.generation_uid,128)){e="invalid run or generation";return false;}
   if(!SF01_IsSafeIdentifier(v.aggregate_id,128)){e="invalid aggregate_id";return false;}
   if(!SF01_IsSafeIdentifier(v.producer_id,128)||!SF01_IsSafeIdentifier(v.producer_version,64)){e="invalid producer";return false;}
   if(!SF01_ValidateTimestamp(v.occurred_at,e)||!SF01_ValidateTimestamp(v.known_at,e))return false;
   if(v.known_at.utc_epoch_milliseconds<v.occurred_at.utc_epoch_milliseconds){e="known_at before occurred_at";return false;}
   if(StringLen(v.payload_schema)<=0||StringLen(v.payload_schema)>160){e="invalid payload schema";return false;}
   if(!SF01_IsSafeIdentifier(v.payload_hash,128)){e="invalid payload hash";return false;}
   if(StringLen(v.payload_json)<=0){e="payload required";return false;}
   string expected=SF05_DeriveResultRecordId(v);
   if(v.record_id!=""&&v.record_id!=expected){e="record_id mismatch";return false;}
   e="";return true;
}

string SF05_ResultEnvelopeToJson(const SF05_ResultEnvelope &v)
{
   string id=v.record_id==""?SF05_DeriveResultRecordId(v):v.record_id;
   return "{\"schema\":\""+SF01_JsonEscape(v.schema)+"\",\"sequence\":"+IntegerToString(v.sequence)+
          ",\"record_type\":\""+SF05_RecordTypeToString(v.record_type)+"\",\"record_id\":\""+id+
          "\",\"run_id\":\""+SF01_JsonEscape(v.run_id)+"\",\"generation_uid\":\""+
          SF01_JsonEscape(v.generation_uid)+"\",\"aggregate_id\":\""+
          SF01_JsonEscape(v.aggregate_id)+"\",\"producer_id\":\""+
          SF01_JsonEscape(v.producer_id)+"\",\"producer_version\":\""+
          SF01_JsonEscape(v.producer_version)+"\",\"occurred_at\":"+
          SF01_TimestampToJson(v.occurred_at)+",\"known_at\":"+
          SF01_TimestampToJson(v.known_at)+",\"payload_schema\":\""+
          SF01_JsonEscape(v.payload_schema)+"\",\"payload_hash\":\""+
          SF01_JsonEscape(v.payload_hash)+"\",\"payload\":"+v.payload_json+"}";
}
#endif
