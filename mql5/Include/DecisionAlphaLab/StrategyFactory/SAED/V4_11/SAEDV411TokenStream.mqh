#ifndef __DECISION_ALPHA_LAB_SAED_V4_11_TOKEN_STREAM_MQH__
#define __DECISION_ALPHA_LAB_SAED_V4_11_TOKEN_STREAM_MQH__
#include "SAEDV411Contracts.mqh"
#include "SAEDV411Canonical.mqh"
bool SAEDV411ValidateTokenStream(const SAEDV411TokenStreamContract &stream)
{
   if(stream.record_id=="" || stream.context_id=="" || stream.root_context_id=="") return false;
   if(stream.domain_id=="" || stream.split_name=="") return false;
   if(!SAEDV411KnownTimeValid(stream.event_time,stream.known_time)) return false;
   if(!SAEDV411IsSha256(stream.token_hash)) return false;
   return true;
}
#endif
