#ifndef __EXP0019_FP_I03_TYPES_MQH__
#define __EXP0019_FP_I03_TYPES_MQH__

#include "FP_I03_Enums.mqh"

#define FP_I03_SCHEMA_VERSION "1.0.0"
#define FP_I03_TIMEZONE "America/New_York"
#define FP_I03_TIME_RULE_VERSION "FP-NY-US-DST-2007PLUS@1.0.0"
#define FP_I03_CALENDAR_VERSION "FP-CALENDAR-ALN-WEEK@1.0.0"
#define FP_I03_SESSION_REGISTRY_VERSION "FP-SESSION-REGISTRY@1.0.0"
#define FP_I03_MIN_YEAR 2007
#define FP_I03_MAX_YEAR 2099

struct FP_I03_TimeKernelConfig
  {
   string context_id;
   string timezone_name;
   string time_rule_version;
   string calendar_version;
   string session_registry_version;
   int minimum_supported_year;
   int maximum_supported_year;
   FP_I03_LocalResolutionPolicy ambiguous_start_policy;
   FP_I03_LocalResolutionPolicy ambiguous_end_policy;
   string config_hash;
  };

struct FP_I03_NyTimestamp
  {
   datetime utc_time;
   datetime ny_time;
   string local_iso;
   string local_date;
   int second_of_day;
   int utc_offset_minutes;
   FP_I03_DstRegime dst_regime;
   int fold;
   string timestamp_id;
  };

struct FP_I03_LocalResolution
  {
   string local_iso;
   FP_I03_LocalTimeStatus status;
   datetime candidate_utc_earliest;
   datetime candidate_utc_latest;
   int candidate_count;
   datetime selected_utc;
   FP_I03_LocalResolutionPolicy policy;
   string reason_code;
   string resolution_id;
  };

struct FP_I03_SessionDefinition
  {
   FP_I03_CalendarSegment code;
   int start_second;
   int end_second;
   bool wraps_midnight;
   int ordinal;
   string definition_id;
  };

struct FP_I03_TradingDayWindow
  {
   string trading_day_id;
   string trading_date;
   datetime start_ny;
   datetime end_ny;
   datetime start_utc;
   datetime end_utc;
   int elapsed_seconds;
   string window_id;
  };

struct FP_I03_SessionWindow
  {
   string session_id;
   FP_I03_CalendarSegment session_code;
   string trading_day_id;
   string trading_date;
   datetime start_ny;
   datetime end_ny;
   datetime start_utc;
   datetime end_utc;
   int elapsed_seconds;
   bool contains_reference_time;
   string window_id;
  };

struct FP_I03_WeekWindow
  {
   string week_id;
   string start_date;
   string end_date;
   datetime start_ny;
   datetime end_ny;
   datetime start_utc;
   datetime end_utc;
   int elapsed_seconds;
   FP_I03_WeekState state;
   bool contains_reference_time;
   string window_id;
  };

struct FP_I03_CalendarSnapshot
  {
   string snapshot_id;
   datetime reference_utc;
   FP_I03_NyTimestamp ny_timestamp;
   FP_I03_TradingDayWindow trading_day;
   FP_I03_CalendarSegment segment;
   FP_I03_SessionWindow session;
   bool has_session;
   FP_I03_WeekWindow week;
   datetime daily_gap_start_utc;
   datetime daily_gap_end_utc;
   FP_I03_CalendarHealth health;
   string reason_code;
   string config_hash;
   string boundary_evidence_hash;
  };

struct FP_I03_SelfTestResult
  {
   int check_count;
   int pass_count;
   int fail_count;
   string latest_failed_check;
   string evidence_key;
  };

#endif
