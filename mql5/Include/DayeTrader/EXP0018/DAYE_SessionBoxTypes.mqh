#ifndef __EXP0018_DAYE_SESSION_BOX_TYPES_MQH__
#define __EXP0018_DAYE_SESSION_BOX_TYPES_MQH__

#include <DayeTrader/EXP0018/DAYE_PeriodEngine.mqh>

// EXP0018 Phase 09 — Session Box Rendering v2.
// This layer projects A/L/N/P period ranges from P03 onto symbol-local charts.
// It has rectangle-object authority only. It has no hunt, signal, lifecycle,
// direction, risk, order, network, model, or execution authority.

#define DAYE_SESSION_BOX_SCHEMA_VERSION 2
#define DAYE_SESSION_BOX_OBJECT_PREFIX "EXP0018_P09_BOX_"

enum DAYE_SessionBoxTargetPolicy
{
   DAYE_SESSION_BOX_TARGET_CURRENT_CHART_IF_SYMBOL = 0,
   DAYE_SESSION_BOX_TARGET_FIRST_OPEN_SYMBOL_CHART = 1,
   DAYE_SESSION_BOX_TARGET_ALL_OPEN_SYMBOL_CHARTS = 2
};

enum DAYE_SessionBoxProjectionStatus
{
   DAYE_SESSION_BOX_STATUS_UNKNOWN = 0,
   DAYE_SESSION_BOX_STATUS_CREATED = 1,
   DAYE_SESSION_BOX_STATUS_UPDATED_OPEN = 2,
   DAYE_SESSION_BOX_STATUS_VERIFIED_CLOSED = 3,
   DAYE_SESSION_BOX_STATUS_REPAIRED = 4,
   DAYE_SESSION_BOX_STATUS_WAITING_FOR_SYMBOL_CHART = 5,
   DAYE_SESSION_BOX_STATUS_SKIPPED_DISABLED_SESSION = 6,
   DAYE_SESSION_BOX_STATUS_SKIPPED_OUTSIDE_LOOKBACK = 7,
   DAYE_SESSION_BOX_STATUS_SKIPPED_INELIGIBLE_COMPLETENESS = 8,
   DAYE_SESSION_BOX_STATUS_INVALID_GEOMETRY = 9,
   DAYE_SESSION_BOX_STATUS_OBJECT_CREATE_FAILED = 10,
   DAYE_SESSION_BOX_STATUS_OBJECT_UPDATE_FAILED = 11,
   DAYE_SESSION_BOX_STATUS_STORE_CAPACITY_EXCEEDED = 12,
   DAYE_SESSION_BOX_STATUS_ORPHAN_DELETED = 13
};

enum DAYE_SessionBoxEngineStatus
{
   DAYE_SESSION_BOX_ENGINE_UNKNOWN = 0,
   DAYE_SESSION_BOX_ENGINE_READY = 1,
   DAYE_SESSION_BOX_ENGINE_SOURCE_NOT_READY = 2,
   DAYE_SESSION_BOX_ENGINE_NO_ELIGIBLE_SESSIONS = 3,
   DAYE_SESSION_BOX_ENGINE_WAITING_FOR_CHART = 4,
   DAYE_SESSION_BOX_ENGINE_DEGRADED = 5,
   DAYE_SESSION_BOX_ENGINE_INVALID_CONFIG = 6,
   DAYE_SESSION_BOX_ENGINE_IO_ERROR = 7
};

enum DAYE_SessionBoxEventType
{
   DAYE_SESSION_BOX_EVENT_NONE = 0,
   DAYE_SESSION_BOX_EVENT_ENGINE_INITIALIZED = 1,
   DAYE_SESSION_BOX_EVENT_STATUS_CHANGED = 2,
   DAYE_SESSION_BOX_EVENT_BOX_CREATED = 3,
   DAYE_SESSION_BOX_EVENT_OPEN_BOX_UPDATED = 4,
   DAYE_SESSION_BOX_EVENT_CLOSED_BOX_VERIFIED = 5,
   DAYE_SESSION_BOX_EVENT_BOX_REPAIRED = 6,
   DAYE_SESSION_BOX_EVENT_WAITING_FOR_CHART = 7,
   DAYE_SESSION_BOX_EVENT_SOURCE_NOT_READY = 8,
   DAYE_SESSION_BOX_EVENT_OBJECT_API_FAILED = 9,
   DAYE_SESSION_BOX_EVENT_ORPHAN_DELETED = 10
};

struct DAYE_SessionBoxConfig
{
   int schema_version;
   DAYE_PeriodAggregationConfig period_config;
   DAYE_SessionBoxTargetPolicy target_policy;

   int lookback_weeks;
   bool render_session_a;
   bool render_session_l;
   bool render_session_n;
   bool render_session_p;
   bool render_complete_sessions;
   bool render_open_sessions;
   bool render_partial_sessions;
   bool require_symbol_period_publishable;
   bool open_missing_symbol_chart;
   ENUM_TIMEFRAMES opened_chart_timeframe;
   int maximum_target_charts_per_symbol;

   color color_a;
   color color_l;
   color color_n;
   color color_p;
   int fill_alpha;
   ENUM_LINE_STYLE border_style;
   int border_width;
   bool draw_in_background;
   bool selectable;
   bool hidden;

   bool verify_existing_owned_objects;
   bool repair_existing_owned_objects;
   bool recreate_manually_deleted_owned_objects;
   bool delete_owned_objects_outside_lookback;
   bool delete_owned_objects_on_deinit;
   int object_verification_interval_seconds;
   int maximum_projection_records;
};

struct DAYE_SessionBoxGeometry
{
   bool is_valid;
   string reason_code;
   datetime start_time_utc;
   datetime end_time_utc;
   datetime start_time_broker;
   datetime end_time_broker;
   double high_price;
   double low_price;
};

struct DAYE_SessionBoxProjection
{
   int schema_version;
   DAYE_SessionBoxProjectionStatus status;
   string reason_code;
   bool is_drawn;
   bool is_open_session;
   bool is_replay_safe;

   string projection_id;
   string symbol_snapshot_id;
   string period_instance_id;
   string trading_day_key;
   string session_code;
   string broker_symbol;
   string canonical_symbol;
   long target_chart_id;
   ENUM_TIMEFRAMES target_chart_timeframe;
   string object_name;
   DAYE_PeriodCompleteness source_completeness;
   DAYE_SessionBoxGeometry geometry;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   int create_count;
   int update_count;
   int verify_count;
   int repair_count;
};

struct DAYE_SessionBoxStoreSummary
{
   int schema_version;
   DAYE_SessionBoxEngineStatus status;
   string reason_code;
   bool is_ready;
   bool is_replay_safe;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;

   int source_period_count;
   int source_session_count;
   int eligible_symbol_session_count;
   int projection_count;
   int created_count;
   int updated_open_count;
   int verified_closed_count;
   int repaired_count;
   int waiting_chart_count;
   int skipped_ineligible_count;
   int invalid_geometry_count;
   int failed_object_count;
   int deleted_orphan_count;
   int open_box_count;
   int closed_box_count;

   string latest_period_instance_id;
   string latest_projection_id;
   string latest_object_name;
};

struct DAYE_SessionBoxEvent
{
   int schema_version;
   DAYE_SessionBoxEventType event_type;
   string event_id;
   string projection_id;
   string object_name;
   string period_instance_id;
   string broker_symbol;
   string session_code;
   long target_chart_id;
   DAYE_SessionBoxProjectionStatus from_status;
   DAYE_SessionBoxProjectionStatus to_status;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   string reason_code;
};

string DAYE_SessionBoxProjectionStatusToString(const DAYE_SessionBoxProjectionStatus value)
{
   switch(value)
   {
      case DAYE_SESSION_BOX_STATUS_CREATED: return "CREATED";
      case DAYE_SESSION_BOX_STATUS_UPDATED_OPEN: return "UPDATED_OPEN";
      case DAYE_SESSION_BOX_STATUS_VERIFIED_CLOSED: return "VERIFIED_CLOSED";
      case DAYE_SESSION_BOX_STATUS_REPAIRED: return "REPAIRED";
      case DAYE_SESSION_BOX_STATUS_WAITING_FOR_SYMBOL_CHART: return "WAITING_FOR_SYMBOL_CHART";
      case DAYE_SESSION_BOX_STATUS_SKIPPED_DISABLED_SESSION: return "SKIPPED_DISABLED_SESSION";
      case DAYE_SESSION_BOX_STATUS_SKIPPED_OUTSIDE_LOOKBACK: return "SKIPPED_OUTSIDE_LOOKBACK";
      case DAYE_SESSION_BOX_STATUS_SKIPPED_INELIGIBLE_COMPLETENESS: return "SKIPPED_INELIGIBLE_COMPLETENESS";
      case DAYE_SESSION_BOX_STATUS_INVALID_GEOMETRY: return "INVALID_GEOMETRY";
      case DAYE_SESSION_BOX_STATUS_OBJECT_CREATE_FAILED: return "OBJECT_CREATE_FAILED";
      case DAYE_SESSION_BOX_STATUS_OBJECT_UPDATE_FAILED: return "OBJECT_UPDATE_FAILED";
      case DAYE_SESSION_BOX_STATUS_STORE_CAPACITY_EXCEEDED: return "STORE_CAPACITY_EXCEEDED";
      case DAYE_SESSION_BOX_STATUS_ORPHAN_DELETED: return "ORPHAN_DELETED";
      default: return "UNKNOWN";
   }
}

string DAYE_SessionBoxEngineStatusToString(const DAYE_SessionBoxEngineStatus value)
{
   switch(value)
   {
      case DAYE_SESSION_BOX_ENGINE_READY: return "READY";
      case DAYE_SESSION_BOX_ENGINE_SOURCE_NOT_READY: return "SOURCE_NOT_READY";
      case DAYE_SESSION_BOX_ENGINE_NO_ELIGIBLE_SESSIONS: return "NO_ELIGIBLE_SESSIONS";
      case DAYE_SESSION_BOX_ENGINE_WAITING_FOR_CHART: return "WAITING_FOR_CHART";
      case DAYE_SESSION_BOX_ENGINE_DEGRADED: return "DEGRADED";
      case DAYE_SESSION_BOX_ENGINE_INVALID_CONFIG: return "INVALID_CONFIG";
      case DAYE_SESSION_BOX_ENGINE_IO_ERROR: return "IO_ERROR";
      default: return "UNKNOWN";
   }
}

string DAYE_SessionBoxEventTypeToString(const DAYE_SessionBoxEventType value)
{
   switch(value)
   {
      case DAYE_SESSION_BOX_EVENT_ENGINE_INITIALIZED: return "ENGINE_INITIALIZED";
      case DAYE_SESSION_BOX_EVENT_STATUS_CHANGED: return "STATUS_CHANGED";
      case DAYE_SESSION_BOX_EVENT_BOX_CREATED: return "BOX_CREATED";
      case DAYE_SESSION_BOX_EVENT_OPEN_BOX_UPDATED: return "OPEN_BOX_UPDATED";
      case DAYE_SESSION_BOX_EVENT_CLOSED_BOX_VERIFIED: return "CLOSED_BOX_VERIFIED";
      case DAYE_SESSION_BOX_EVENT_BOX_REPAIRED: return "BOX_REPAIRED";
      case DAYE_SESSION_BOX_EVENT_WAITING_FOR_CHART: return "WAITING_FOR_CHART";
      case DAYE_SESSION_BOX_EVENT_SOURCE_NOT_READY: return "SOURCE_NOT_READY";
      case DAYE_SESSION_BOX_EVENT_OBJECT_API_FAILED: return "OBJECT_API_FAILED";
      case DAYE_SESSION_BOX_EVENT_ORPHAN_DELETED: return "ORPHAN_DELETED";
      default: return "NONE";
   }
}

#endif
