#ifndef __EXP0018_DAYE_PERIOD_TYPES_MQH__
#define __EXP0018_DAYE_PERIOD_TYPES_MQH__

#include <DayeTrader/EXP0018/DAYE_DataTypes.mqh>
#include <DayeTrader/EXP0018/DAYE_PeriodRegistry.mqh>

// EXP0018 Phase 03 — Period Aggregation and Completeness v2.
// This module owns period-domain types only. It has no hunt, divergence, drawing, risk, or order authority.

#define DAYE_PERIOD_AGG_SCHEMA_VERSION 2

enum DAYE_PeriodAggregateStatusCode
{
   DAYE_PERIOD_STATUS_OK = 0,
   DAYE_PERIOD_STATUS_INVALID_CONFIG = 1,
   DAYE_PERIOD_STATUS_SOURCE_UNAVAILABLE = 2,
   DAYE_PERIOD_STATUS_UNSUPPORTED_BASE_TIMEFRAME = 3,
   DAYE_PERIOD_STATUS_TIME_WINDOW_FAILED = 4,
   DAYE_PERIOD_STATUS_INVALID_BAR_MEMBERSHIP = 5,
   DAYE_PERIOD_STATUS_DUPLICATE_PERIOD_ID = 6,
   DAYE_PERIOD_STATUS_NON_MONOTONIC_SOURCE = 7,
   DAYE_PERIOD_STATUS_INSUFFICIENT_COMPLETE_PERIODS = 8,
   DAYE_PERIOD_STATUS_PARTIAL_SOURCE_ALIGNMENT = 9,
   DAYE_PERIOD_STATUS_IO_ERROR = 10
};

enum DAYE_PeriodCompleteness
{
   DAYE_PERIOD_COMPLETENESS_UNKNOWN = 0,
   DAYE_PERIOD_COMPLETENESS_EMPTY = 1,
   DAYE_PERIOD_COMPLETENESS_OPEN = 2,
   DAYE_PERIOD_COMPLETENESS_PARTIAL = 3,
   DAYE_PERIOD_COMPLETENESS_COMPLETE = 4,
   DAYE_PERIOD_COMPLETENESS_UNAVAILABLE = 5,
   DAYE_PERIOD_COMPLETENESS_INVALID = 6
};

enum DAYE_PeriodAggregateEventType
{
   DAYE_PERIOD_EVENT_NONE = 0,
   DAYE_PERIOD_EVENT_ENGINE_INITIALIZED = 1,
   DAYE_PERIOD_EVENT_STATUS_CHANGED = 2,
   DAYE_PERIOD_EVENT_STORE_READY = 3,
   DAYE_PERIOD_EVENT_STORE_DEGRADED = 4,
   DAYE_PERIOD_EVENT_DATA_UNAVAILABLE = 5,
   DAYE_PERIOD_EVENT_LATEST_COMPLETE_PERIOD_ADVANCED = 6
};

struct DAYE_PeriodAggregationConfig
{
   int schema_version;
   DAYE_DataSyncConfig data_config;
   bool include_daily_periods;
   bool include_session_periods;
   bool include_subcycle_periods;
   bool include_weekly_periods;
   bool include_open_periods;
   bool publish_partial_periods;
   bool require_both_symbols_complete;
   double minimum_publishable_coverage_percent;
   int minimum_complete_paired_periods;
   int maximum_periods_to_publish;
   int force_full_refresh_seconds;
};

struct DAYE_SymbolPeriodSnapshot
{
   int schema_version;
   DAYE_PeriodAggregateStatusCode status;
   string reason_code;
   DAYE_PeriodCompleteness completeness;
   bool is_publishable;
   bool is_replay_safe;

   string snapshot_id;
   string broker_symbol;
   string canonical_symbol;
   ENUM_TIMEFRAMES base_timeframe;
   int base_bar_seconds;

   DAYE_PeriodId period_id;
   DAYE_PeriodFamily period_family;
   string period_code;
   string period_instance_id;
   string trading_day_key;
   DAYE_PeriodWindow window;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;

   int expected_bar_count;
   int observed_bar_count;
   int missing_bar_count;
   int unexpected_bar_count;
   int invalid_grid_bar_count;
   double coverage_percent;
   bool left_edge_truncated;
   bool right_edge_truncated;
   bool period_is_open;

   datetime first_source_bar_utc;
   datetime last_source_bar_utc;
   datetime last_source_close_utc;
   string first_source_bar_id;
   string last_source_bar_id;

   double open;
   double high;
   double low;
   double close;

   // P08 provenance enrichment. Both first and last occurrences are retained
   // because an equal final extreme can occur more than once inside a period.
   datetime high_first_time_utc;
   datetime high_last_time_utc;
   datetime low_first_time_utc;
   datetime low_last_time_utc;
   string high_first_source_bar_id;
   string high_last_source_bar_id;
   string low_first_source_bar_id;
   string low_last_source_bar_id;

   long tick_volume;
   long real_volume;
   long spread_sum;

   string previous_chronological_period_instance_id;
   string previous_same_code_period_instance_id;
};

struct DAYE_PairedPeriodSnapshot
{
   int schema_version;
   DAYE_PeriodAggregateStatusCode status;
   string reason_code;
   DAYE_PeriodCompleteness completeness;
   bool is_publishable;
   bool is_replay_safe;

   string paired_period_id;
   string period_instance_id;
   DAYE_PeriodId period_id;
   DAYE_PeriodFamily period_family;
   string period_code;
   string trading_day_key;
   DAYE_PeriodWindow window;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;

   int expected_aligned_bar_count;
   int aligned_bar_count;
   int unmatched_a_count;
   int unmatched_b_count;
   double aligned_coverage_percent;

   DAYE_SymbolPeriodSnapshot symbol_a;
   DAYE_SymbolPeriodSnapshot symbol_b;

   string previous_chronological_paired_period_id;
   string previous_same_code_paired_period_id;
};

struct DAYE_PeriodStoreSummary
{
   int schema_version;
   DAYE_PeriodAggregateStatusCode status;
   string reason_code;
   bool is_ready;
   bool is_complete;
   bool is_replay_safe;
   string run_key;

   datetime source_first_event_time_utc;
   datetime source_last_event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;

   int source_bars_a;
   int source_bars_b;
   int source_aligned_pairs;
   int source_unmatched_a;
   int source_unmatched_b;

   int symbol_period_count_a;
   int symbol_period_count_b;
   int paired_period_count;
   int complete_paired_period_count;
   int partial_paired_period_count;
   int open_paired_period_count;
   int unavailable_paired_period_count;
   int daily_period_count;
   int session_period_count;
   int subcycle_period_count;

   string latest_paired_period_id;
   string latest_complete_paired_period_id;
   datetime latest_period_start_utc;
   datetime latest_complete_period_end_utc;
};

struct DAYE_PeriodAggregateEvent
{
   int schema_version;
   DAYE_PeriodAggregateEventType event_type;
   string event_id;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   DAYE_PeriodAggregateStatusCode from_status;
   DAYE_PeriodAggregateStatusCode to_status;
   string period_instance_id;
   string reason_code;
};

string DAYE_PeriodAggregateStatusToString(const DAYE_PeriodAggregateStatusCode value)
{
   switch(value)
   {
      case DAYE_PERIOD_STATUS_OK: return "OK";
      case DAYE_PERIOD_STATUS_INVALID_CONFIG: return "INVALID_CONFIG";
      case DAYE_PERIOD_STATUS_SOURCE_UNAVAILABLE: return "SOURCE_UNAVAILABLE";
      case DAYE_PERIOD_STATUS_UNSUPPORTED_BASE_TIMEFRAME: return "UNSUPPORTED_BASE_TIMEFRAME";
      case DAYE_PERIOD_STATUS_TIME_WINDOW_FAILED: return "TIME_WINDOW_FAILED";
      case DAYE_PERIOD_STATUS_INVALID_BAR_MEMBERSHIP: return "INVALID_BAR_MEMBERSHIP";
      case DAYE_PERIOD_STATUS_DUPLICATE_PERIOD_ID: return "DUPLICATE_PERIOD_ID";
      case DAYE_PERIOD_STATUS_NON_MONOTONIC_SOURCE: return "NON_MONOTONIC_SOURCE";
      case DAYE_PERIOD_STATUS_INSUFFICIENT_COMPLETE_PERIODS: return "INSUFFICIENT_COMPLETE_PERIODS";
      case DAYE_PERIOD_STATUS_PARTIAL_SOURCE_ALIGNMENT: return "PARTIAL_SOURCE_ALIGNMENT";
      case DAYE_PERIOD_STATUS_IO_ERROR: return "IO_ERROR";
      default: return "UNKNOWN";
   }
}

string DAYE_PeriodCompletenessToString(const DAYE_PeriodCompleteness value)
{
   switch(value)
   {
      case DAYE_PERIOD_COMPLETENESS_EMPTY: return "EMPTY";
      case DAYE_PERIOD_COMPLETENESS_OPEN: return "OPEN";
      case DAYE_PERIOD_COMPLETENESS_PARTIAL: return "PARTIAL";
      case DAYE_PERIOD_COMPLETENESS_COMPLETE: return "COMPLETE";
      case DAYE_PERIOD_COMPLETENESS_UNAVAILABLE: return "UNAVAILABLE";
      case DAYE_PERIOD_COMPLETENESS_INVALID: return "INVALID";
      default: return "UNKNOWN";
   }
}

string DAYE_PeriodAggregateEventTypeToString(const DAYE_PeriodAggregateEventType value)
{
   switch(value)
   {
      case DAYE_PERIOD_EVENT_ENGINE_INITIALIZED: return "ENGINE_INITIALIZED";
      case DAYE_PERIOD_EVENT_STATUS_CHANGED: return "STATUS_CHANGED";
      case DAYE_PERIOD_EVENT_STORE_READY: return "STORE_READY";
      case DAYE_PERIOD_EVENT_STORE_DEGRADED: return "STORE_DEGRADED";
      case DAYE_PERIOD_EVENT_DATA_UNAVAILABLE: return "DATA_UNAVAILABLE";
      case DAYE_PERIOD_EVENT_LATEST_COMPLETE_PERIOD_ADVANCED: return "LATEST_COMPLETE_PERIOD_ADVANCED";
      default: return "NONE";
   }
}

#endif
