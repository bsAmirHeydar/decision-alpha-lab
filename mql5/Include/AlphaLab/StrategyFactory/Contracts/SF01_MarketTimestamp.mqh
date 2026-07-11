#ifndef __SF01_MARKET_TIMESTAMP_MQH__
#define __SF01_MARKET_TIMESTAMP_MQH__

#include "SF01_Enums.mqh"
#include "SF01_StringCodec.mqh"


struct SF01_MarketTimestamp
{
   long utc_epoch_milliseconds;
   string source_timezone_id;
   int source_utc_offset_minutes;
   string source_clock_id;
   ENUM_SF01_TIMESTAMP_PRECISION precision;
};

SF01_MarketTimestamp SF01_MakeUtcTimestamp(const datetime utc_seconds,
                                            const string source_timezone_id = "UTC",
                                            const int source_utc_offset_minutes = 0,
                                            const string source_clock_id = "terminal",
                                            const ENUM_SF01_TIMESTAMP_PRECISION precision = SF01_TIME_SECONDS)
{
   SF01_MarketTimestamp value;
   value.utc_epoch_milliseconds = ((long)utc_seconds) * 1000;
   value.source_timezone_id = source_timezone_id;
   value.source_utc_offset_minutes = source_utc_offset_minutes;
   value.source_clock_id = source_clock_id;
   value.precision = precision;
   return value;
}

SF01_MarketTimestamp SF01_MakeUtcMilliseconds(const long utc_epoch_milliseconds,
                                               const string source_timezone_id,
                                               const int source_utc_offset_minutes,
                                               const string source_clock_id,
                                               const ENUM_SF01_TIMESTAMP_PRECISION precision)
{
   SF01_MarketTimestamp value;
   value.utc_epoch_milliseconds = utc_epoch_milliseconds;
   value.source_timezone_id = source_timezone_id;
   value.source_utc_offset_minutes = source_utc_offset_minutes;
   value.source_clock_id = source_clock_id;
   value.precision = precision;
   return value;
}

bool SF01_ValidateTimestamp(const SF01_MarketTimestamp &value, string &error)
{
   if(value.utc_epoch_milliseconds < 0) { error = "negative UTC epoch milliseconds"; return false; }
   if(!SF01_IsSafeIdentifier(value.source_timezone_id, 96)) { error = "invalid source_timezone_id"; return false; }
   if(!SF01_IsSafeIdentifier(value.source_clock_id, 96)) { error = "invalid source_clock_id"; return false; }
   if(value.source_utc_offset_minutes < -14 * 60 || value.source_utc_offset_minutes > 14 * 60)
   { error = "source UTC offset out of range"; return false; }
   error = "";
   return true;
}

int SF01_CompareTimestamp(const SF01_MarketTimestamp &left, const SF01_MarketTimestamp &right)
{
   if(left.utc_epoch_milliseconds < right.utc_epoch_milliseconds) return -1;
   if(left.utc_epoch_milliseconds > right.utc_epoch_milliseconds) return 1;
   return 0;
}

string SF01_TimestampCanonical(const SF01_MarketTimestamp &value)
{
   return IntegerToString(value.utc_epoch_milliseconds) + "|" +
          value.source_timezone_id + "|" +
          IntegerToString(value.source_utc_offset_minutes) + "|" +
          value.source_clock_id + "|" +
          IntegerToString((int)value.precision);
}

#endif
