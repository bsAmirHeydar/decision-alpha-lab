#ifndef __SF01_ANATOMY_EVENT_MQH__
#define __SF01_ANATOMY_EVENT_MQH__

#include "SF01_SchemaIdentity.mqh"
#include "SF01_MarketTimestamp.mqh"
#include "SF01_Hash.mqh"


struct SF01_AnatomyEvent
{
   SF01_SchemaIdentity schema;
   string event_id;
   string strategy_id;
   string strategy_version;
   string producer_id;
   string producer_version;
   string symbol;
   string reference_symbol;
   ENUM_SF01_DIRECTION direction;
   SF01_MarketTimestamp event_time;
   SF01_MarketTimestamp known_time;
   SF01_MarketTimestamp confirmation_time;
   double reference_price;
   double invalidation_price;
   int timeframe_seconds;
   string session_id;
   string parent_event_id;
   string market_event_cluster_id;
   string source_hash;
   string anatomy_state;
};

string SF01_AnatomyEventCanonicalIdentity(const SF01_AnatomyEvent &value)
{
   return value.strategy_id + "|" + value.strategy_version + "|" + value.symbol + "|" +
          value.reference_symbol + "|" + SF01_DirectionToString(value.direction) + "|" +
          IntegerToString(value.event_time.utc_epoch_milliseconds) + "|" +
          IntegerToString(value.known_time.utc_epoch_milliseconds) + "|" +
          IntegerToString(value.confirmation_time.utc_epoch_milliseconds) + "|" +
          IntegerToString(value.timeframe_seconds) + "|" + value.parent_event_id + "|" +
          value.market_event_cluster_id + "|" + value.source_hash;
}

string SF01_DeriveAnatomyEventId(const SF01_AnatomyEvent &value)
{
   return SF01_StableId("evt", SF01_AnatomyEventCanonicalIdentity(value));
}

bool SF01_ValidateAnatomyEvent(const SF01_AnatomyEvent &value, string &error)
{
   if(!SF01_ValidateSchemaIdentity(value.schema, error)) return false;
   if(!SF01_IsSafeIdentifier(value.strategy_id)) { error = "invalid strategy_id"; return false; }
   if(!SF01_IsSafeIdentifier(value.strategy_version)) { error = "invalid strategy_version"; return false; }
   if(!SF01_IsSafeIdentifier(value.producer_id)) { error = "invalid producer_id"; return false; }
   if(!SF01_IsSafeIdentifier(value.producer_version)) { error = "invalid producer_version"; return false; }
   if(!SF01_IsSafeIdentifier(value.symbol, 64)) { error = "invalid symbol"; return false; }
   if(value.reference_symbol != "" && !SF01_IsSafeIdentifier(value.reference_symbol, 64))
   { error = "invalid reference_symbol"; return false; }
   if(value.direction == SF01_DIRECTION_NONE) { error = "direction cannot be NONE"; return false; }
   if(!SF01_ValidateTimestamp(value.event_time, error)) return false;
   if(!SF01_ValidateTimestamp(value.known_time, error)) return false;
   if(!SF01_ValidateTimestamp(value.confirmation_time, error)) return false;
   if(SF01_CompareTimestamp(value.event_time, value.known_time) > 0)
   { error = "event_time after known_time"; return false; }
   if(SF01_CompareTimestamp(value.known_time, value.confirmation_time) > 0)
   { error = "known_time after confirmation_time"; return false; }
   if(!MathIsValidNumber(value.reference_price) || !MathIsValidNumber(value.invalidation_price))
   { error = "non-finite price"; return false; }
   if(value.timeframe_seconds <= 0) { error = "timeframe_seconds must be positive"; return false; }
   if(!SF01_IsSafeIdentifier(value.market_event_cluster_id)) { error = "missing or invalid market_event_cluster_id"; return false; }
   if(!SF01_IsSafeIdentifier(value.source_hash)) { error = "invalid source_hash"; return false; }
   const string expected_id = SF01_DeriveAnatomyEventId(value);
   if(value.event_id != "" && value.event_id != expected_id) { error = "event_id does not match canonical identity"; return false; }
   error = "";
   return true;
}

#endif
