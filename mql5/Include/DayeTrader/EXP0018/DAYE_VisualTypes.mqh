#ifndef __EXP0018_DAYE_VISUAL_TYPES_MQH__
#define __EXP0018_DAYE_VISUAL_TYPES_MQH__

#include <DayeTrader/EXP0018/DAYE_RenderEngine.mqh>

// EXP0018 Phase 10 — Unified Core Visual Anatomy v2.
// Object projection only. No strategy mutation, risk, order, model, network,
// licensing, or execution authority.

#define DAYE_VISUAL_SCHEMA_VERSION 3
#define DAYE_VISUAL_OBJECT_PREFIX "EXP0018_P10_"

enum DAYE_VisualTargetPolicy
{
   DAYE_VISUAL_TARGET_CURRENT_CHART_IF_SYMBOL = 0,
   DAYE_VISUAL_TARGET_FIRST_OPEN_SYMBOL_CHART = 1,
   DAYE_VISUAL_TARGET_ALL_OPEN_SYMBOL_CHARTS = 2
};

enum DAYE_TwoAnchorPolicy
{
   DAYE_TWO_TUESDAY_1800_LITERAL = 0,
   DAYE_TWO_MONDAY_1800_TUESDAY_TRADING_DAY = 1
};

enum DAYE_ProvisionalWeekPolicy
{
   DAYE_WEEK_SUNDAY_1800_TO_FRIDAY_1700 = 0,
   DAYE_WEEK_MONDAY_1800_TO_FRIDAY_1700 = 1
};

enum DAYE_VisualStatus
{
   DAYE_VISUAL_STATUS_UNKNOWN = 0,
   DAYE_VISUAL_STATUS_READY = 1,
   DAYE_VISUAL_STATUS_SOURCE_NOT_READY = 2,
   DAYE_VISUAL_STATUS_WAITING_FOR_CHART = 3,
   DAYE_VISUAL_STATUS_DEGRADED = 4,
   DAYE_VISUAL_STATUS_INVALID_CONFIG = 5
};

struct DAYE_VisualConfig
{
   int schema_version;
   DAYE_VisualTargetPolicy target_policy;
   int lookback_weeks;
   int maximum_target_charts_per_symbol;
   bool open_missing_symbol_chart;
   ENUM_TIMEFRAMES opened_chart_timeframe;

   bool render_daily_frame;
   bool render_daily_boundaries;
   bool render_daily_label;
   bool render_session_boxes;
   bool render_session_boundaries;
   bool render_session_labels;
   bool render_subcycle_boxes;
   bool render_subcycle_boundaries;
   bool render_subcycle_labels;
   bool render_micro_22_5_boundaries;
   bool render_micro_22_5_labels;
   bool render_gap_band;
   bool render_gap_boundaries;
   bool render_tdo;
   bool render_two;
   bool render_extended_session_true_opens;
   bool render_provisional_week_boundaries;
   bool render_legend;

   bool render_complete_periods;
   bool render_open_periods;
   bool render_partial_periods;
   DAYE_TwoAnchorPolicy two_anchor_policy;
   DAYE_ProvisionalWeekPolicy provisional_week_policy;

   color daily_color;
   color session_a_color;
   color session_l_color;
   color session_n_color;
   color session_p_color;
   color subcycle_color;
   color micro_color;
   color gap_color;
   color tdo_color;
   color two_color;
   color true_open_color;
   color week_color;
   color label_color;

   int daily_fill_alpha;
   int session_fill_alpha;
   int subcycle_fill_alpha;
   int gap_fill_alpha;
   ENUM_LINE_STYLE major_boundary_style;
   ENUM_LINE_STYLE subcycle_boundary_style;
   ENUM_LINE_STYLE micro_boundary_style;
   int major_boundary_width;
   int subcycle_boundary_width;
   int micro_boundary_width;
   int anchor_width;
   bool draw_boxes_in_background;
   bool objects_selectable;
   bool objects_hidden;
   string label_font;
   int major_label_font_size;
   int minor_label_font_size;
   double label_vertical_offset_points;

   bool verify_existing_owned_objects;
   bool repair_existing_owned_objects;
   bool recreate_manually_deleted_owned_objects;
   bool delete_owned_objects_on_deinit;
   int object_verification_interval_seconds;

   // Hotfix002 resilience policy. The temporal anatomy is allowed to render from
   // the attached chart even when the paired divergence source cannot initialize.
   bool allow_single_symbol_time_fallback;
   bool fail_init_when_pair_pipeline_unavailable;
   int local_visual_minimum_bars;
   bool print_detailed_source_diagnostics;
};

struct DAYE_VisualSummary
{
   int schema_version;
   DAYE_VisualStatus status;
   string reason_code;
   bool is_ready;
   bool is_replay_safe;
   datetime processing_time_utc;
   int source_period_count;
   int target_chart_count;
   int daily_frame_count;
   int session_box_count;
   int subcycle_box_count;
   int boundary_count;
   int micro_boundary_count;
   int label_count;
   int gap_count;
   int tdo_count;
   int two_count;
   int true_open_count;
   int week_boundary_count;
   int created_count;
   int updated_count;
   int failed_count;
   int skipped_count;

   bool pair_pipeline_initialized;
   bool local_fallback_used;
   int local_period_count;
   string pair_pipeline_reason;
   string local_fallback_reason;
};

string DAYE_VisualStatusToString(const DAYE_VisualStatus value)
{
   switch(value)
   {
      case DAYE_VISUAL_STATUS_READY: return "READY";
      case DAYE_VISUAL_STATUS_SOURCE_NOT_READY: return "SOURCE_NOT_READY";
      case DAYE_VISUAL_STATUS_WAITING_FOR_CHART: return "WAITING_FOR_CHART";
      case DAYE_VISUAL_STATUS_DEGRADED: return "DEGRADED";
      case DAYE_VISUAL_STATUS_INVALID_CONFIG: return "INVALID_CONFIG";
      default: return "UNKNOWN";
   }
}

#endif
