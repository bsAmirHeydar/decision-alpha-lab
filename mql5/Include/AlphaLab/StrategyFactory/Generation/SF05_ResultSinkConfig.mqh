#ifndef __SF05_RESULT_SINK_CONFIG_MQH__
#define __SF05_RESULT_SINK_CONFIG_MQH__
#include "../Contracts/SF01_StringCodec.mqh"
#include "../Contracts/SF01_Hash.mqh"
#include "SF05_GenerationEnums.mqh"

struct SF05_ResultSinkConfig
{
   string schema;
   string sink_id;
   string sink_version;
   ENUM_SF05_SINK_MODE mode;
   ENUM_SF05_FILE_SCOPE file_scope;
   string root_path;
   bool append_only;
   bool fail_closed_on_write_error;
   bool mirror_to_print;
   bool include_payload_hash;
   int flush_every_records;
   long flush_every_milliseconds;
   int max_record_bytes;
};

SF05_ResultSinkConfig SF05_DefaultResultSinkConfig(void)
{
   SF05_ResultSinkConfig v;
   v.schema="alpha_lab.strategy_factory/result_sink_config@1.0.0";
   v.sink_id="sf05.jsonl";
   v.sink_version="1.0.0";
   v.mode=SF05_SINK_JSONL;
   v.file_scope=SF05_FILE_TERMINAL_LOCAL;
   v.root_path="StrategyFactory";
   v.append_only=true;
   v.fail_closed_on_write_error=true;
   v.mirror_to_print=false;
   v.include_payload_hash=true;
   v.flush_every_records=32;
   v.flush_every_milliseconds=1000;
   v.max_record_bytes=1048576;
   return v;
}

string SF05_ResultSinkConfigCanonical(const SF05_ResultSinkConfig &v)
{
   return v.schema+"|"+v.sink_id+"|"+v.sink_version+"|"+
          IntegerToString((int)v.mode)+"|"+IntegerToString((int)v.file_scope)+"|"+
          v.root_path+"|"+SF01_CanonicalBool(v.append_only)+"|"+
          SF01_CanonicalBool(v.fail_closed_on_write_error)+"|"+
          SF01_CanonicalBool(v.mirror_to_print)+"|"+
          SF01_CanonicalBool(v.include_payload_hash)+"|"+
          IntegerToString(v.flush_every_records)+"|"+
          LongToString(v.flush_every_milliseconds)+"|"+
          IntegerToString(v.max_record_bytes);
}

string SF05_ResultSinkConfigHash(const SF05_ResultSinkConfig &v)
{
   return SF01_StableId("snk",SF05_ResultSinkConfigCanonical(v));
}

bool SF05_ValidateResultSinkConfig(const SF05_ResultSinkConfig &v,string &e)
{
   if(v.schema!="alpha_lab.strategy_factory/result_sink_config@1.0.0"){e="unsupported sink schema";return false;}
   if(!SF01_IsSafeIdentifier(v.sink_id,128)){e="invalid sink_id";return false;}
   if(StringLen(v.sink_version)<5){e="invalid sink_version";return false;}
   if(v.mode<SF05_SINK_MEMORY||v.mode>SF05_SINK_COMPOSITE){e="invalid sink mode";return false;}
   if(StringLen(v.root_path)<=0||StringLen(v.root_path)>240){e="invalid root_path";return false;}
   if(StringFind(v.root_path,"..")>=0){e="root_path traversal forbidden";return false;}
   if(!v.append_only){e="phase 05 requires append_only";return false;}
   if(v.flush_every_records<1||v.flush_every_records>100000){e="flush_every_records out of range";return false;}
   if(v.flush_every_milliseconds<10||v.flush_every_milliseconds>3600000){e="flush interval out of range";return false;}
   if(v.max_record_bytes<256||v.max_record_bytes>16777216){e="max_record_bytes out of range";return false;}
   e="";return true;
}
#endif
