#ifndef __EXP0018_DAYE_RENDER_TYPES_MQH__
#define __EXP0018_DAYE_RENDER_TYPES_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleEngine.mqh>

// EXP0018 Phase 08 — Divergence Drawing and Historical Visual Projection v2.
// This layer projects immutable accepted P07 uses onto hunter-symbol charts.
// It has drawing authority only. It has no detection, lifecycle, direction,
// risk, order, model, licensing, or execution authority.

#define DAYE_RENDER_SCHEMA_VERSION 2
#define DAYE_RENDER_OBJECT_PREFIX "EXP0018_P08_"

enum DAYE_RenderTargetPolicy
{
   DAYE_RENDER_TARGET_CURRENT_CHART_IF_HUNTER = 0,
   DAYE_RENDER_TARGET_FIRST_OPEN_HUNTER_CHART = 1,
   DAYE_RENDER_TARGET_ALL_OPEN_HUNTER_CHARTS = 2
};

enum DAYE_ExtremeAnchorPolicy
{
   DAYE_EXTREME_ANCHOR_FIRST_OCCURRENCE = 0,
   DAYE_EXTREME_ANCHOR_LAST_OCCURRENCE = 1
};

enum DAYE_RenderProjectionStatus
{
   DAYE_RENDER_STATUS_UNKNOWN = 0,
   DAYE_RENDER_STATUS_CREATED = 1,
   DAYE_RENDER_STATUS_VERIFIED = 2,
   DAYE_RENDER_STATUS_REPAIRED = 3,
   DAYE_RENDER_STATUS_WAITING_FOR_HUNTER_CHART = 4,
   DAYE_RENDER_STATUS_SOURCE_PERIOD_NOT_FOUND = 5,
   DAYE_RENDER_STATUS_SOURCE_EXTREME_UNAVAILABLE = 6,
   DAYE_RENDER_STATUS_INVALID_GEOMETRY = 7,
   DAYE_RENDER_STATUS_OBJECT_CREATE_FAILED = 8,
   DAYE_RENDER_STATUS_OBJECT_UPDATE_FAILED = 9,
   DAYE_RENDER_STATUS_SKIPPED_NOT_ACCEPTED = 10,
   DAYE_RENDER_STATUS_SKIPPED_TARGET_POLICY = 11,
   DAYE_RENDER_STATUS_STORE_CAPACITY_EXCEEDED = 12
};

enum DAYE_RenderEngineStatus
{
   DAYE_RENDER_ENGINE_UNKNOWN = 0,
   DAYE_RENDER_ENGINE_READY = 1,
   DAYE_RENDER_ENGINE_SOURCE_NOT_READY = 2,
   DAYE_RENDER_ENGINE_NO_ACCEPTED_USES = 3,
   DAYE_RENDER_ENGINE_WAITING_FOR_CHART = 4,
   DAYE_RENDER_ENGINE_DEGRADED = 5,
   DAYE_RENDER_ENGINE_INVALID_CONFIG = 6,
   DAYE_RENDER_ENGINE_IO_ERROR = 7
};

enum DAYE_RenderEventType
{
   DAYE_RENDER_EVENT_NONE = 0,
   DAYE_RENDER_EVENT_ENGINE_INITIALIZED = 1,
   DAYE_RENDER_EVENT_STATUS_CHANGED = 2,
   DAYE_RENDER_EVENT_LINE_CREATED = 3,
   DAYE_RENDER_EVENT_LINE_VERIFIED = 4,
   DAYE_RENDER_EVENT_LINE_REPAIRED = 5,
   DAYE_RENDER_EVENT_WAITING_FOR_HUNTER_CHART = 6,
   DAYE_RENDER_EVENT_SOURCE_PERIOD_MISSING = 7,
   DAYE_RENDER_EVENT_SOURCE_EXTREME_MISSING = 8,
   DAYE_RENDER_EVENT_OBJECT_API_FAILED = 9,
   DAYE_RENDER_EVENT_MANUAL_DELETE_REPAIRED = 10
};

struct DAYE_RenderConfig
{
   int schema_version;
   DAYE_LifecycleConfig lifecycle_config;

   DAYE_RenderTargetPolicy target_policy;
   DAYE_ExtremeAnchorPolicy extreme_anchor_policy;
   bool require_target_chart_host_timeframe;
   bool open_missing_hunter_chart;
   ENUM_TIMEFRAMES opened_chart_timeframe;

   color line_color;
   ENUM_LINE_STYLE line_style;
   int line_width;
   bool line_ray_left;
   bool line_ray_right;
   bool line_back;
   bool line_selectable;
   bool line_hidden;

   bool show_major_labels;
   bool use_midpoint_text_object;
   string label_font;
   int label_font_size;
   color label_color;
   double label_vertical_offset_points;

   bool verify_existing_owned_objects;
   bool repair_existing_owned_objects;
   bool recreate_manually_deleted_owned_objects;
   bool preserve_orphaned_owned_objects;
   bool delete_owned_objects_on_deinit;

   int maximum_projection_records;
   int maximum_target_charts_per_use;
};

struct DAYE_RenderGeometry
{
   bool is_valid;
   string reason_code;
   DAYE_HuntSide side;
   datetime reference_time_utc;
   datetime confirmation_time_utc;
   datetime reference_time_broker;
   datetime confirmation_time_broker;
   double reference_price;
   double confirmation_price;
   datetime label_time_broker;
   double label_price;
   string reference_source_bar_id;
   DAYE_ExtremeAnchorPolicy extreme_anchor_policy;
};

struct DAYE_RenderProjection
{
   int schema_version;
   DAYE_RenderProjectionStatus status;
   string reason_code;
   bool is_drawn;
   bool is_major;
   bool is_historical_immutable;
   bool is_replay_safe;

   string projection_id;
   string use_id;
   string reference_id;
   string relationship_id;
   string source_alias;
   string chart_label;
   DAYE_HuntSide side;

   string hunter_broker_symbol;
   string hunter_canonical_symbol;
   string protected_canonical_symbol;
   long target_chart_id;
   ENUM_TIMEFRAMES target_chart_timeframe;

   string line_object_name;
   string text_object_name;
   DAYE_RenderGeometry geometry;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   int create_count;
   int verify_count;
   int repair_count;
};

struct DAYE_RenderStoreSummary
{
   int schema_version;
   DAYE_RenderEngineStatus status;
   string reason_code;
   bool is_ready;
   bool is_replay_safe;

   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;

   int source_use_count;
   int accepted_source_use_count;
   int source_period_count;
   int open_hunter_chart_count;
   int projection_count;
   int created_count;
   int verified_count;
   int repaired_count;
   int waiting_chart_count;
   int source_period_missing_count;
   int source_extreme_missing_count;
   int failed_object_count;
   int major_label_count;
   int minor_unlabeled_count;

   string latest_use_id;
   string latest_projection_id;
   string latest_object_name;
};

struct DAYE_RenderEvent
{
   int schema_version;
   DAYE_RenderEventType event_type;
   string event_id;
   string projection_id;
   string use_id;
   string object_name;
   long target_chart_id;
   DAYE_RenderProjectionStatus from_status;
   DAYE_RenderProjectionStatus to_status;
   datetime event_time_utc;
   datetime availability_time_utc;
   datetime processing_time_utc;
   string reason_code;
};

string DAYE_RenderProjectionStatusToString(const DAYE_RenderProjectionStatus value)
{
   switch(value)
   {
      case DAYE_RENDER_STATUS_CREATED: return "CREATED";
      case DAYE_RENDER_STATUS_VERIFIED: return "VERIFIED";
      case DAYE_RENDER_STATUS_REPAIRED: return "REPAIRED";
      case DAYE_RENDER_STATUS_WAITING_FOR_HUNTER_CHART: return "WAITING_FOR_HUNTER_CHART";
      case DAYE_RENDER_STATUS_SOURCE_PERIOD_NOT_FOUND: return "SOURCE_PERIOD_NOT_FOUND";
      case DAYE_RENDER_STATUS_SOURCE_EXTREME_UNAVAILABLE: return "SOURCE_EXTREME_UNAVAILABLE";
      case DAYE_RENDER_STATUS_INVALID_GEOMETRY: return "INVALID_GEOMETRY";
      case DAYE_RENDER_STATUS_OBJECT_CREATE_FAILED: return "OBJECT_CREATE_FAILED";
      case DAYE_RENDER_STATUS_OBJECT_UPDATE_FAILED: return "OBJECT_UPDATE_FAILED";
      case DAYE_RENDER_STATUS_SKIPPED_NOT_ACCEPTED: return "SKIPPED_NOT_ACCEPTED";
      case DAYE_RENDER_STATUS_SKIPPED_TARGET_POLICY: return "SKIPPED_TARGET_POLICY";
      case DAYE_RENDER_STATUS_STORE_CAPACITY_EXCEEDED: return "STORE_CAPACITY_EXCEEDED";
      default: return "UNKNOWN";
   }
}

string DAYE_RenderEngineStatusToString(const DAYE_RenderEngineStatus value)
{
   switch(value)
   {
      case DAYE_RENDER_ENGINE_READY: return "READY";
      case DAYE_RENDER_ENGINE_SOURCE_NOT_READY: return "SOURCE_NOT_READY";
      case DAYE_RENDER_ENGINE_NO_ACCEPTED_USES: return "NO_ACCEPTED_USES";
      case DAYE_RENDER_ENGINE_WAITING_FOR_CHART: return "WAITING_FOR_CHART";
      case DAYE_RENDER_ENGINE_DEGRADED: return "DEGRADED";
      case DAYE_RENDER_ENGINE_INVALID_CONFIG: return "INVALID_CONFIG";
      case DAYE_RENDER_ENGINE_IO_ERROR: return "IO_ERROR";
      default: return "UNKNOWN";
   }
}

string DAYE_RenderEventTypeToString(const DAYE_RenderEventType value)
{
   switch(value)
   {
      case DAYE_RENDER_EVENT_ENGINE_INITIALIZED: return "ENGINE_INITIALIZED";
      case DAYE_RENDER_EVENT_STATUS_CHANGED: return "STATUS_CHANGED";
      case DAYE_RENDER_EVENT_LINE_CREATED: return "LINE_CREATED";
      case DAYE_RENDER_EVENT_LINE_VERIFIED: return "LINE_VERIFIED";
      case DAYE_RENDER_EVENT_LINE_REPAIRED: return "LINE_REPAIRED";
      case DAYE_RENDER_EVENT_WAITING_FOR_HUNTER_CHART: return "WAITING_FOR_HUNTER_CHART";
      case DAYE_RENDER_EVENT_SOURCE_PERIOD_MISSING: return "SOURCE_PERIOD_MISSING";
      case DAYE_RENDER_EVENT_SOURCE_EXTREME_MISSING: return "SOURCE_EXTREME_MISSING";
      case DAYE_RENDER_EVENT_OBJECT_API_FAILED: return "OBJECT_API_FAILED";
      case DAYE_RENDER_EVENT_MANUAL_DELETE_REPAIRED: return "MANUAL_DELETE_REPAIRED";
      default: return "NONE";
   }
}

#endif
