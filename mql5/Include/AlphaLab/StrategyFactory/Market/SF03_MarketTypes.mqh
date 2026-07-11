#ifndef __SF03_MARKET_TYPES_MQH__
#define __SF03_MARKET_TYPES_MQH__
#include "SF03_MarketEnums.mqh"
#include "../Contracts/SF01_MarketTimestamp.mqh"
#include "../Contracts/SF01_BarRecord.mqh"

struct SF03_ClockConfig
{
   ENUM_SF03_CLOCK_MODE mode;
   int broker_utc_offset_minutes;
   string broker_timezone_id;
   string source_clock_id;
   bool strict_offset_validation;
};
struct SF03_TickSnapshot
{
   string symbol;
   MqlTick tick;
   long received_at_utc_msc;
   long source_generation;
   ENUM_SF03_DATA_QUALITY quality;
};
struct SF03_SessionDefinition
{
   string session_id;
   bool enabled;
   ENUM_SF03_TIMEZONE_KIND timezone_kind;
   int fixed_offset_minutes;
   int start_minute_of_day;
   int end_minute_of_day;
   int weekday_mask;
};
struct SF03_SessionMatch
{
   bool matched;
   string session_id;
   int local_minute_of_day;
   int local_weekday;
   int utc_offset_minutes;
};
struct SF03_SyncRequirement
{
   string symbol;
   int timeframe_seconds;
   long max_close_skew_milliseconds;
   long max_staleness_milliseconds;
};
struct SF03_SyncResult
{
   ENUM_SF03_SYNC_STATUS status;
   long minimum_close_utc_msc;
   long maximum_close_utc_msc;
   long close_skew_milliseconds;
   int ready_count;
   int required_count;
   string detail;
};
struct SF03_SymbolSpecSnapshot
{
   string symbol;
   int digits;
   double point;
   double tick_size;
   double tick_value;
   double contract_size;
   double volume_min;
   double volume_max;
   double volume_step;
   int stops_level_points;
   int freeze_level_points;
   long filling_mode;
   long order_mode;
   long trade_mode;
   long specification_generation;
   long observed_at_utc_msc;
   ENUM_SF03_DATA_QUALITY quality;
};
struct SF03_MarketTelemetrySnapshot
{
   long tick_updates;
   long tick_hits;
   long tick_misses;
   long bar_refreshes;
   long bar_insertions;
   long bar_replacements;
   long bar_duplicates;
   long detected_gaps;
   long sync_checks;
   long sync_failures;
   long specification_refreshes;
   long source_errors;
   ulong last_refresh_latency_us;
   ulong maximum_refresh_latency_us;
};
#endif
