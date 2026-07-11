#ifndef __SF01_BAR_RECORD_MQH__
#define __SF01_BAR_RECORD_MQH__

#include "SF01_SchemaIdentity.mqh"
#include "SF01_MarketTimestamp.mqh"
#include "SF01_Hash.mqh"


struct SF01_BarRecord
{
   SF01_SchemaIdentity schema;
   string symbol;
   int timeframe_seconds;
   SF01_MarketTimestamp open_time;
   SF01_MarketTimestamp close_time;
   double open_price;
   double high_price;
   double low_price;
   double close_price;
   long tick_volume;
   long real_volume;
   double bid_close;
   double ask_close;
   double spread_points;
   string source_id;
   string source_bar_id;
};

string SF01_BarCanonicalIdentity(const SF01_BarRecord &value)
{
   return value.symbol + "|" + IntegerToString(value.timeframe_seconds) + "|" +
          IntegerToString(value.open_time.utc_epoch_milliseconds) + "|" + value.source_id + "|" + value.source_bar_id;
}

string SF01_BarId(const SF01_BarRecord &value)
{
   return SF01_StableId("bar", SF01_BarCanonicalIdentity(value));
}

bool SF01_ValidateBarRecord(const SF01_BarRecord &value, string &error)
{
   if(!SF01_ValidateSchemaIdentity(value.schema, error)) return false;
   if(!SF01_IsSafeIdentifier(value.symbol, 64)) { error = "invalid symbol"; return false; }
   if(value.timeframe_seconds <= 0) { error = "timeframe_seconds must be positive"; return false; }
   if(!SF01_ValidateTimestamp(value.open_time, error)) return false;
   if(!SF01_ValidateTimestamp(value.close_time, error)) return false;
   if(SF01_CompareTimestamp(value.open_time, value.close_time) >= 0) { error = "bar close must be after open"; return false; }
   if(!MathIsValidNumber(value.open_price) || !MathIsValidNumber(value.high_price) ||
      !MathIsValidNumber(value.low_price) || !MathIsValidNumber(value.close_price))
   { error = "non-finite OHLC"; return false; }
   if(value.high_price < value.low_price) { error = "high below low"; return false; }
   if(value.open_price > value.high_price || value.open_price < value.low_price) { error = "open outside range"; return false; }
   if(value.close_price > value.high_price || value.close_price < value.low_price) { error = "close outside range"; return false; }
   if(value.tick_volume < 0 || value.real_volume < 0) { error = "negative volume"; return false; }
   if(value.ask_close > 0.0 && value.bid_close > 0.0 && value.ask_close < value.bid_close)
   { error = "ask below bid"; return false; }
   if(value.spread_points < 0.0) { error = "negative spread"; return false; }
   if(!SF01_IsSafeIdentifier(value.source_id, 96)) { error = "invalid source_id"; return false; }
   error = "";
   return true;
}

#endif
