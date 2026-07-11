#ifndef __SF02_EVENT_ENVELOPE_MQH__
#define __SF02_EVENT_ENVELOPE_MQH__

#include "SF02_RuntimeEnums.mqh"
#include "../Contracts/SF01_MarketTimestamp.mqh"
#include "../Contracts/SF01_StringCodec.mqh"

struct SF02_EventEnvelope
{
   long sequence;
   ENUM_SF02_EVENT_TYPE event_type;
   string aggregate_id;
   string source_id;
   SF01_MarketTimestamp occurred_at;
   SF01_MarketTimestamp known_at;
   string payload_hash;
   int priority;
};

bool SF02_ValidateEventEnvelope(const SF02_EventEnvelope &value, string &error)
{
   if(value.event_type == SF02_EVENT_NONE) { error = "event_type cannot be NONE"; return false; }
   if(!SF01_IsSafeIdentifier(value.aggregate_id)) { error = "invalid aggregate_id"; return false; }
   if(!SF01_IsSafeIdentifier(value.source_id)) { error = "invalid source_id"; return false; }
   if(!SF01_ValidateTimestamp(value.occurred_at, error)) return false;
   if(!SF01_ValidateTimestamp(value.known_at, error)) return false;
   if(SF01_CompareTimestamp(value.occurred_at, value.known_at) > 0)
   { error = "event occurred_at after known_at"; return false; }
   if(!SF01_IsSafeIdentifier(value.payload_hash)) { error = "invalid payload_hash"; return false; }
   if(value.priority < 0 || value.priority > 100) { error = "priority out of range"; return false; }
   error = "";
   return true;
}

#endif
