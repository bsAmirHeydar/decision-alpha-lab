
#ifndef __EXP0018_DAYE_DATA_TYPES_MQH__
#define __EXP0018_DAYE_DATA_TYPES_MQH__

#include <DayeTrader/EXP0018/DAYE_Types.mqh>

// EXP0018 Phase 02 — Multi-Symbol Data Synchronization v2.
// This module owns data-domain types only. It has no hunt, signal, drawing, risk, or order authority.

#define DAYE_DATA_SCHEMA_VERSION 2

enum DAYE_DataStatusCode
{
   DAYE_DATA_STATUS_OK = 0,
   DAYE_DATA_STATUS_INVALID_CONFIG = 1,
   DAYE_DATA_STATUS_SYMBOL_UNAVAILABLE = 2,
   DAYE_DATA_STATUS_SYMBOL_NOT_SELECTED = 3,
   DAYE_DATA_STATUS_HISTORY_NOT_SYNCHRONIZED = 4,
   DAYE_DATA_STATUS_INSUFFICIENT_BARS = 5,
   DAYE_DATA_STATUS_COPY_RATES_FAILED = 6,
   DAYE_DATA_STATUS_INVALID_BAR = 7,
   DAYE_DATA_STATUS_DUPLICATE_TIMESTAMP = 8,
   DAYE_DATA_STATUS_NON_MONOTONIC_TIME = 9,
   DAYE_DATA_STATUS_NO_COMMON_TIMESTAMPS = 10,
   DAYE_DATA_STATUS_PARTIAL_ALIGNMENT = 11,
   DAYE_DATA_STATUS_STALE_DATA = 12,
   DAYE_DATA_STATUS_TIME_CONVERSION_FAILED = 13,
   DAYE_DATA_STATUS_IO_ERROR = 14
};

enum DAYE_BarCompleteness
{
   DAYE_BAR_COMPLETENESS_UNKNOWN = 0,
   DAYE_BAR_COMPLETENESS_OPEN = 1,
   DAYE_BAR_COMPLETENESS_CLOSED = 2
};

enum DAYE_DataEventType
{
   DAYE_DATA_EVENT_NONE = 0,
   DAYE_DATA_EVENT_ENGINE_INITIALIZED = 1,
   DAYE_DATA_EVENT_STATUS_CHANGED = 2,
   DAYE_DATA_EVENT_ALIGNMENT_READY = 3,
   DAYE_DATA_EVENT_ALIGNMENT_DEGRADED = 4,
   DAYE_DATA_EVENT_DATA_UNAVAILABLE = 5,
   DAYE_DATA_EVENT_LATEST_COMMON_BAR_ADVANCED = 6
};

struct DAYE_DataSyncConfig
{
   int schema_version;
   string broker_symbol_a;
   string broker_symbol_b;
   string canonical_symbol_a;
   string canonical_symbol_b;
   ENUM_TIMEFRAMES base_timeframe;
   int requested_bars_per_symbol;
   int minimum_common_bars;
   int maximum_pairs_to_publish;
   bool use_closed_bars_only;
   bool require_series_synchronized;
   bool fail_on_any_invalid_bar;
   bool require_complete_alignment;
   bool enforce_freshness;
   int maximum_latest_bar_age_seconds;
   int force_full_refresh_seconds;
};

struct DAYE_SymbolDescriptor
{
   int schema_version;
   DAYE_DataStatusCode status;
   string reason_code;
   string broker_symbol;
   string canonical_symbol;
   bool selected;
   bool visible;
   int digits;
   double point;
};

struct DAYE_SymbolBar
{
   int schema_version;
   DAYE_DataStatusCode status;
   string reason_code;
   bool is_valid;

   string broker_symbol;
   string canonical_symbol;
   ENUM_TIMEFRAMES timeframe;

   datetime broker_open_time;
   datetime event_time_utc;
   datetime event_time_ny;
   datetime close_time_utc;

   double open;
   double high;
   double low;
   double close;
   long tick_volume;
   int spread;
   long real_volume;

   DAYE_BarCompleteness completeness;
   bool is_replay_safe;
};

struct DAYE_SymbolDataHealth
{
   int schema_version;
   DAYE_DataStatusCode status;
   string reason_code;
   string broker_symbol;
   string canonical_symbol;
   bool symbol_selected;
   bool series_synchronized;
   int bars_available;
   int requested_bars;
   int copied_bars;
   int accepted_bars;
   int invalid_bar_count;
   int duplicate_timestamp_count;
   int non_monotonic_count;
   datetime first_event_time_utc;
   datetime last_event_time_utc;
   int latest_closed_bar_age_seconds;
};

struct DAYE_SynchronizedBarPair
{
   int schema_version;
   DAYE_DataStatusCode status;
   string reason_code;
   string pair_id;
   ENUM_TIMEFRAMES timeframe;
   datetime event_time_utc;
   datetime event_time_ny;
   datetime availability_time_utc;
   datetime processing_time_utc;
   DAYE_SymbolBar symbol_a;
   DAYE_SymbolBar symbol_b;
};

struct DAYE_DataSyncSummary
{
   int schema_version;
   DAYE_DataStatusCode status;
   string reason_code;
   bool is_ready;
   bool is_complete;
   bool is_replay_safe;
   string run_key;
   string broker_symbol_a;
   string broker_symbol_b;
   string canonical_symbol_a;
   string canonical_symbol_b;
   ENUM_TIMEFRAMES timeframe;
   int requested_bars_per_symbol;
   int copied_a;
   int copied_b;
   int aligned_count;
   int unmatched_a;
   int unmatched_b;
   int invalid_a;
   int invalid_b;
   int duplicate_a;
   int duplicate_b;
   datetime first_common_event_time_utc;
   datetime last_common_event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
};

struct DAYE_DataSyncEvent
{
   int schema_version;
   DAYE_DataEventType event_type;
   string event_id;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   DAYE_DataStatusCode from_status;
   DAYE_DataStatusCode to_status;
   datetime latest_common_event_time_utc;
   string reason_code;
};

string DAYE_DataStatusCodeToString(const DAYE_DataStatusCode value)
{
   switch(value)
   {
      case DAYE_DATA_STATUS_OK: return "OK";
      case DAYE_DATA_STATUS_INVALID_CONFIG: return "INVALID_CONFIG";
      case DAYE_DATA_STATUS_SYMBOL_UNAVAILABLE: return "SYMBOL_UNAVAILABLE";
      case DAYE_DATA_STATUS_SYMBOL_NOT_SELECTED: return "SYMBOL_NOT_SELECTED";
      case DAYE_DATA_STATUS_HISTORY_NOT_SYNCHRONIZED: return "HISTORY_NOT_SYNCHRONIZED";
      case DAYE_DATA_STATUS_INSUFFICIENT_BARS: return "INSUFFICIENT_BARS";
      case DAYE_DATA_STATUS_COPY_RATES_FAILED: return "COPY_RATES_FAILED";
      case DAYE_DATA_STATUS_INVALID_BAR: return "INVALID_BAR";
      case DAYE_DATA_STATUS_DUPLICATE_TIMESTAMP: return "DUPLICATE_TIMESTAMP";
      case DAYE_DATA_STATUS_NON_MONOTONIC_TIME: return "NON_MONOTONIC_TIME";
      case DAYE_DATA_STATUS_NO_COMMON_TIMESTAMPS: return "NO_COMMON_TIMESTAMPS";
      case DAYE_DATA_STATUS_PARTIAL_ALIGNMENT: return "PARTIAL_ALIGNMENT";
      case DAYE_DATA_STATUS_STALE_DATA: return "STALE_DATA";
      case DAYE_DATA_STATUS_TIME_CONVERSION_FAILED: return "TIME_CONVERSION_FAILED";
      case DAYE_DATA_STATUS_IO_ERROR: return "IO_ERROR";
      default: return "UNKNOWN";
   }
}

string DAYE_BarCompletenessToString(const DAYE_BarCompleteness value)
{
   switch(value)
   {
      case DAYE_BAR_COMPLETENESS_OPEN: return "OPEN";
      case DAYE_BAR_COMPLETENESS_CLOSED: return "CLOSED";
      default: return "UNKNOWN";
   }
}

string DAYE_DataEventTypeToString(const DAYE_DataEventType value)
{
   switch(value)
   {
      case DAYE_DATA_EVENT_ENGINE_INITIALIZED: return "ENGINE_INITIALIZED";
      case DAYE_DATA_EVENT_STATUS_CHANGED: return "STATUS_CHANGED";
      case DAYE_DATA_EVENT_ALIGNMENT_READY: return "ALIGNMENT_READY";
      case DAYE_DATA_EVENT_ALIGNMENT_DEGRADED: return "ALIGNMENT_DEGRADED";
      case DAYE_DATA_EVENT_DATA_UNAVAILABLE: return "DATA_UNAVAILABLE";
      case DAYE_DATA_EVENT_LATEST_COMMON_BAR_ADVANCED: return "LATEST_COMMON_BAR_ADVANCED";
      default: return "NONE";
   }
}

#endif
