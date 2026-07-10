#ifndef __EXP0018_DAYE_TYPES_MQH__
#define __EXP0018_DAYE_TYPES_MQH__

// EXP0018 Phase 01 — New York Time Kernel v2.
// This module owns time-domain types only. It has no signal, drawing, risk, or order authority.

#define DAYE_TIME_SCHEMA_VERSION 2

enum DAYE_StatusCode
{
   DAYE_STATUS_OK = 0,
   DAYE_STATUS_INVALID_INPUT = 1,
   DAYE_STATUS_INVALID_CONFIG = 2,
   DAYE_STATUS_UNAVAILABLE = 3,
   DAYE_STATUS_AMBIGUOUS_LOCAL_TIME = 4,
   DAYE_STATUS_NONEXISTENT_LOCAL_TIME = 5,
   DAYE_STATUS_IO_ERROR = 6
};

enum DAYE_BrokerOffsetMode
{
   DAYE_BROKER_OFFSET_MANUAL_FIXED = 0,
   DAYE_BROKER_OFFSET_AUTO_CURRENT_LIVE = 1
};

enum DAYE_NyOffsetMode
{
   DAYE_NY_AUTO_US_DST = 0,
   DAYE_NY_MANUAL_UTC_OFFSET = 1
};

enum DAYE_LocalResolutionPolicy
{
   DAYE_LOCAL_REJECT = 0,
   DAYE_LOCAL_EARLIEST = 1,
   DAYE_LOCAL_LATEST = 2
};

enum DAYE_PeriodFamily
{
   DAYE_FAMILY_NONE = 0,
   DAYE_FAMILY_WEEKLY = 1,
   DAYE_FAMILY_DAILY = 2,
   DAYE_FAMILY_SESSION = 3,
   DAYE_FAMILY_SUBCYCLE_90M = 4,
   DAYE_FAMILY_SUBCYCLE_TAIL = 5,
   DAYE_FAMILY_GAP = 6
};

enum DAYE_PeriodId
{
   DAYE_PERIOD_NONE = 0,
   DAYE_PERIOD_W,
   DAYE_PERIOD_D,
   DAYE_PERIOD_GAP,
   DAYE_PERIOD_A,
   DAYE_PERIOD_L,
   DAYE_PERIOD_N,
   DAYE_PERIOD_P,
   DAYE_PERIOD_A1,
   DAYE_PERIOD_A2,
   DAYE_PERIOD_A3,
   DAYE_PERIOD_A4,
   DAYE_PERIOD_L1,
   DAYE_PERIOD_L2,
   DAYE_PERIOD_L3,
   DAYE_PERIOD_L4,
   DAYE_PERIOD_N1,
   DAYE_PERIOD_N2,
   DAYE_PERIOD_N3,
   DAYE_PERIOD_N4,
   DAYE_PERIOD_P1,
   DAYE_PERIOD_P2,
   DAYE_PERIOD_P3,
   DAYE_PERIOD_P4
};

enum DAYE_TimeEventType
{
   DAYE_TIME_EVENT_NONE = 0,
   DAYE_TIME_EVENT_KERNEL_INITIALIZED = 1,
   DAYE_TIME_EVENT_DST_OFFSET_CHANGED = 2,
   DAYE_TIME_EVENT_TRADING_DAY_OPENED = 3,
   DAYE_TIME_EVENT_SESSION_CHANGED = 4,
   DAYE_TIME_EVENT_SUBCYCLE_CHANGED = 5,
   DAYE_TIME_EVENT_GAP_ENTERED = 6,
   DAYE_TIME_EVENT_GAP_EXITED = 7
};

struct DAYE_TimeConfig
{
   int schema_version;
   DAYE_BrokerOffsetMode broker_offset_mode;
   int broker_utc_offset_minutes;
   DAYE_NyOffsetMode ny_offset_mode;
   int manual_new_york_utc_offset_minutes;
   DAYE_LocalResolutionPolicy ambiguous_start_policy;
   DAYE_LocalResolutionPolicy ambiguous_end_policy;
};

struct DAYE_PeriodDefinition
{
   DAYE_PeriodId id;
   DAYE_PeriodFamily family;
   string code;
   int start_second;
   int end_second;
   int nominal_duration_minutes;
   bool wraps_midnight;
   bool implementation_ready;
   string blocker;
};

struct DAYE_PeriodWindow
{
   int schema_version;
   DAYE_StatusCode status;
   string reason_code;
   DAYE_PeriodId period_id;
   DAYE_PeriodFamily family;
   string code;
   string instance_id;
   datetime start_ny;
   datetime end_ny;
   datetime start_utc;
   datetime end_utc;
   int elapsed_minutes_utc;
   bool is_dst_variable_duration;
};

struct DAYE_TimeSnapshot
{
   int schema_version;
   DAYE_StatusCode status;
   string reason_code;
   bool is_valid;
   bool is_replay_safe;

   datetime broker_time;
   datetime utc_time;
   datetime new_york_time;

   int broker_utc_offset_minutes;
   int new_york_utc_offset_minutes;
   bool is_new_york_dst;
   int new_york_fold;

   int second_of_day_ny;
   int minute_of_day_ny;
   string new_york_date_key;
   string trading_day_key;
   bool in_declared_session_gap;

   DAYE_PeriodId session_id;
   DAYE_PeriodId subcycle_id;

   DAYE_PeriodWindow trading_day_window;
   DAYE_PeriodWindow session_window;
   DAYE_PeriodWindow subcycle_window;
};

struct DAYE_TimeEvent
{
   int schema_version;
   DAYE_TimeEventType event_type;
   string event_id;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   string trading_day_key;
   DAYE_PeriodId from_period_id;
   DAYE_PeriodId to_period_id;
   string reason_code;
};

string DAYE_StatusCodeToString(const DAYE_StatusCode value)
{
   switch(value)
   {
      case DAYE_STATUS_OK: return "OK";
      case DAYE_STATUS_INVALID_INPUT: return "INVALID_INPUT";
      case DAYE_STATUS_INVALID_CONFIG: return "INVALID_CONFIG";
      case DAYE_STATUS_UNAVAILABLE: return "UNAVAILABLE";
      case DAYE_STATUS_AMBIGUOUS_LOCAL_TIME: return "AMBIGUOUS_LOCAL_TIME";
      case DAYE_STATUS_NONEXISTENT_LOCAL_TIME: return "NONEXISTENT_LOCAL_TIME";
      case DAYE_STATUS_IO_ERROR: return "IO_ERROR";
      default: return "UNKNOWN";
   }
}

string DAYE_PeriodIdToString(const DAYE_PeriodId id)
{
   switch(id)
   {
      case DAYE_PERIOD_W: return "W";
      case DAYE_PERIOD_D: return "D";
      case DAYE_PERIOD_GAP: return "GAP";
      case DAYE_PERIOD_A: return "A";
      case DAYE_PERIOD_L: return "L";
      case DAYE_PERIOD_N: return "N";
      case DAYE_PERIOD_P: return "P";
      case DAYE_PERIOD_A1: return "a1";
      case DAYE_PERIOD_A2: return "a2";
      case DAYE_PERIOD_A3: return "a3";
      case DAYE_PERIOD_A4: return "a4";
      case DAYE_PERIOD_L1: return "l1";
      case DAYE_PERIOD_L2: return "l2";
      case DAYE_PERIOD_L3: return "l3";
      case DAYE_PERIOD_L4: return "l4";
      case DAYE_PERIOD_N1: return "n1";
      case DAYE_PERIOD_N2: return "n2";
      case DAYE_PERIOD_N3: return "n3";
      case DAYE_PERIOD_N4: return "n4";
      case DAYE_PERIOD_P1: return "p1";
      case DAYE_PERIOD_P2: return "p2";
      case DAYE_PERIOD_P3: return "p3";
      case DAYE_PERIOD_P4: return "p4";
      default: return "NONE";
   }
}

string DAYE_PeriodFamilyToString(const DAYE_PeriodFamily value)
{
   switch(value)
   {
      case DAYE_FAMILY_WEEKLY: return "WEEKLY";
      case DAYE_FAMILY_DAILY: return "DAILY";
      case DAYE_FAMILY_SESSION: return "SESSION";
      case DAYE_FAMILY_SUBCYCLE_90M: return "SUBCYCLE_90M";
      case DAYE_FAMILY_SUBCYCLE_TAIL: return "SUBCYCLE_TAIL";
      case DAYE_FAMILY_GAP: return "GAP";
      default: return "NONE";
   }
}

string DAYE_TimeEventTypeToString(const DAYE_TimeEventType value)
{
   switch(value)
   {
      case DAYE_TIME_EVENT_KERNEL_INITIALIZED: return "KERNEL_INITIALIZED";
      case DAYE_TIME_EVENT_DST_OFFSET_CHANGED: return "DST_OFFSET_CHANGED";
      case DAYE_TIME_EVENT_TRADING_DAY_OPENED: return "TRADING_DAY_OPENED";
      case DAYE_TIME_EVENT_SESSION_CHANGED: return "SESSION_CHANGED";
      case DAYE_TIME_EVENT_SUBCYCLE_CHANGED: return "SUBCYCLE_CHANGED";
      case DAYE_TIME_EVENT_GAP_ENTERED: return "GAP_ENTERED";
      case DAYE_TIME_EVENT_GAP_EXITED: return "GAP_EXITED";
      default: return "NONE";
   }
}

#endif
