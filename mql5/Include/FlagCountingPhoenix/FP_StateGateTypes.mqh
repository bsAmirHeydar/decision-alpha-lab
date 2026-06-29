#ifndef __FP_STATE_GATE_TYPES_MQH__
#define __FP_STATE_GATE_TYPES_MQH__
#property strict

#include "FP_Types.mqh"

// ============================================================================
// FlagCounting Phoenix - Level 19 State Gate Types
// ----------------------------------------------------------------------------
// The State Gate is a read-only anatomy projection layer above the locked Node,
// Hook/ND, Flag Body, Internal Count, F1/F2/F3 lifecycle, ownership,
// canonicalization, renderer, validation, release, and license logic.
//
// Phase 2 adds the real closed-bar tracker for three configured timeframes. It
// still does not project or reinterpret F-counting or Hook/ND anatomy; Rally and
// Hook rows remain explicit placeholders until Phase 3/4.
// ============================================================================

#define FP_STATE_GATE_VERSION "19.10-phase2"
#define FP_STATE_GATE_TF_SLOTS 3
#define FP_STATE_GATE_MAX_RALLY_ROWS 24
#define FP_STATE_GATE_MAX_HOOK_ROWS 48
#define FP_STATE_GATE_DEFAULT_PREFIX "FP_L19_STATE_GATE_"
#define FP_STATE_GATE_DEFAULT_EXPORT_FOLDER "FlagCountingPhoenix"

#define FP_STATE_GATE_STATUS_DISABLED "STATE_GATE_DISABLED"
#define FP_STATE_GATE_STATUS_TRACKING "TRACKING_CLOSED_BAR"
#define FP_STATE_GATE_STATUS_UNCHANGED "CLOSED_BAR_UNCHANGED"
#define FP_STATE_GATE_STATUS_DIRTY "CLOSED_BAR_CHANGED"
#define FP_STATE_GATE_STATUS_FIRST "FIRST_CLOSED_BAR_SNAPSHOT"
#define FP_STATE_GATE_STATUS_TF_UNUSABLE "TF_UNUSABLE"
#define FP_STATE_GATE_STATUS_TF_UNAVAILABLE "TF_DATA_UNAVAILABLE"

#define FP_STATE_GATE_REASON_PHASE2 "phase2_closed_bar_tracker"
#define FP_STATE_GATE_REASON_PROJECTION_PENDING "rally_hook_projection_pending"

enum FP_StateGateViewType
{
   FP_STATE_GATE_VIEW_NONE  = 0,
   FP_STATE_GATE_VIEW_RALLY = 1,
   FP_STATE_GATE_VIEW_HOOK  = 2
};

enum FP_StateGateRowStatus
{
   FP_STATE_GATE_ROW_EMPTY       = 0,
   FP_STATE_GATE_ROW_PLACEHOLDER = 1,
   FP_STATE_GATE_ROW_PROJECTED   = 2,
   FP_STATE_GATE_ROW_UNKNOWN     = 3
};

struct FP_StateGateConfig
{
   bool enabled;
   ENUM_TIMEFRAMES tf1;
   ENUM_TIMEFRAMES tf2;
   ENUM_TIMEFRAMES tf3;

   bool panel_enabled;
   bool panel_start_minimized;
   int  panel_corner;
   int  panel_x;
   int  panel_y;
   int  panel_width;
   int  panel_font_size;
   int  max_rally_rows_per_tf;
   int  max_hook_rows_per_tf;
   bool show_ids;
   bool show_scale_l;
   bool export_csv;
   bool export_overwrite_latest;
   string export_folder;
   bool print_audit;
   string object_prefix;
};

struct FP_StateGateTimeframeState
{
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime last_closed_bar_time;
   datetime previous_closed_bar_time;
   double last_closed_bar_close;
   bool closed_bar_available;
   bool dirty;
   bool initialized;
   int bars_available;
   int update_count;
   int rally_row_count;
   int hook_row_count;
   string latest_established_f_summary;
   string probable_next_f_summary;
   string hook_summary;
   string tracker_status;
   string status;
   string reason;
};

struct FP_StateGateRallyRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   int source_event_id;
   int sequence_id;
   int parent_event_id;
   int scale_L;
   int direction;
   int f_level;
   string latest_established_f;
   string probable_next_f;
   string body_state;
   string flag_stage;
   string post_flag_stage;
   string source_id;
   string label;
};

struct FP_StateGateHookRow
{
   int slot_index;
   ENUM_TIMEFRAMES timeframe;
   string timeframe_label;
   datetime last_closed_bar_time;
   double last_closed_bar_close;
   int status;
   int source_hook_id;
   int sequence_id;
   int scale_L;
   int direction;
   string polarity;
   int current_node_number;
   int latest_high_node_id;
   double latest_high_node_price;
   int latest_low_node_id;
   double latest_low_node_price;
   string position_label;
   string source_id;
   string label;
};

struct FP_StateGateSnapshot
{
   bool initialized;
   string symbol;
   ENUM_TIMEFRAMES chart_timeframe;
   datetime generated_at;
   int timeframe_count;
   int dirty_timeframes;
   int available_timeframes;
   int unchanged_timeframes;
   int unavailable_timeframes;
   int update_serial;
   bool any_dirty;
   FP_StateGateTimeframeState tf_states[FP_STATE_GATE_TF_SLOTS];
   FP_StateGateRallyRow rally_rows[FP_STATE_GATE_MAX_RALLY_ROWS];
   FP_StateGateHookRow hook_rows[FP_STATE_GATE_MAX_HOOK_ROWS];
   int rally_row_count;
   int hook_row_count;
   string status;
   string reason;
};

struct FP_StateGateRuntime
{
   bool initialized;
   bool minimized;
   bool panel_has_drawn;
   bool export_has_written;
   bool last_run_had_dirty;
   datetime last_processed_closed_bar_time[FP_STATE_GATE_TF_SLOTS];
   datetime previous_closed_bar_time[FP_STATE_GATE_TF_SLOTS];
   bool slot_initialized[FP_STATE_GATE_TF_SLOTS];
   int slot_update_count[FP_STATE_GATE_TF_SLOTS];
   int update_serial;
   datetime last_engine_run_time;
   FP_StateGateSnapshot snapshot;
};

struct FP_StateGateReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   string version;
   string symbol;
   int timeframe_count;
   int slots_checked;
   int available_timeframes;
   int dirty_timeframes;
   int unchanged_timeframes;
   int unavailable_timeframes;
   int rally_rows;
   int hook_rows;
   int objects_requested;
   int objects_created;
   int object_errors;
   int objects_deleted;
   int files_written;
   int file_errors;
   bool panel_redrawn;
   bool export_attempted;
   bool skipped_no_dirty;
};

void FP_ResetStateGateTimeframeState(FP_StateGateTimeframeState &s)
{
   s.timeframe = PERIOD_CURRENT;
   s.timeframe_label = "TF?";
   s.last_closed_bar_time = 0;
   s.previous_closed_bar_time = 0;
   s.last_closed_bar_close = 0.0;
   s.closed_bar_available = false;
   s.dirty = false;
   s.initialized = false;
   s.bars_available = 0;
   s.update_count = 0;
   s.rally_row_count = 0;
   s.hook_row_count = 0;
   s.latest_established_f_summary = "RALLY_VIEW_PENDING";
   s.probable_next_f_summary = "RALLY_VIEW_PENDING";
   s.hook_summary = "HOOK_VIEW_PENDING";
   s.tracker_status = "reset";
   s.status = "empty";
   s.reason = "reset";
}

void FP_ResetStateGateRallyRow(FP_StateGateRallyRow &r)
{
   r.slot_index = -1;
   r.timeframe = PERIOD_CURRENT;
   r.timeframe_label = "TF?";
   r.last_closed_bar_time = 0;
   r.last_closed_bar_close = 0.0;
   r.status = FP_STATE_GATE_ROW_EMPTY;
   r.source_event_id = -1;
   r.sequence_id = -1;
   r.parent_event_id = -1;
   r.scale_L = 0;
   r.direction = FP_DIR_NONE;
   r.f_level = FP_LEVEL_NONE;
   r.latest_established_f = "F?_PENDING";
   r.probable_next_f = "F?_PENDING";
   r.body_state = "PHASE2_PLACEHOLDER";
   r.flag_stage = "PHASE2_PLACEHOLDER";
   r.post_flag_stage = "PHASE2_PLACEHOLDER";
   r.source_id = "";
   r.label = "Rally View placeholder: projection starts in Level 19 Phase 3";
}

void FP_ResetStateGateHookRow(FP_StateGateHookRow &r)
{
   r.slot_index = -1;
   r.timeframe = PERIOD_CURRENT;
   r.timeframe_label = "TF?";
   r.last_closed_bar_time = 0;
   r.last_closed_bar_close = 0.0;
   r.status = FP_STATE_GATE_ROW_EMPTY;
   r.source_hook_id = -1;
   r.sequence_id = -1;
   r.scale_L = 0;
   r.direction = FP_DIR_NONE;
   r.polarity = "HOOK?_PENDING";
   r.current_node_number = -1;
   r.latest_high_node_id = -1;
   r.latest_high_node_price = 0.0;
   r.latest_low_node_id = -1;
   r.latest_low_node_price = 0.0;
   r.position_label = "PHASE2_PLACEHOLDER";
   r.source_id = "";
   r.label = "Hook View placeholder: projection starts in Level 19 Phase 4";
}

void FP_ResetStateGateSnapshot(FP_StateGateSnapshot &s)
{
   s.initialized = false;
   s.symbol = "";
   s.chart_timeframe = PERIOD_CURRENT;
   s.generated_at = 0;
   s.timeframe_count = FP_STATE_GATE_TF_SLOTS;
   s.dirty_timeframes = 0;
   s.available_timeframes = 0;
   s.unchanged_timeframes = 0;
   s.unavailable_timeframes = 0;
   s.update_serial = 0;
   s.any_dirty = false;
   for(int i=0; i<FP_STATE_GATE_TF_SLOTS; i++)
      FP_ResetStateGateTimeframeState(s.tf_states[i]);
   for(int r=0; r<FP_STATE_GATE_MAX_RALLY_ROWS; r++)
      FP_ResetStateGateRallyRow(s.rally_rows[r]);
   for(int h=0; h<FP_STATE_GATE_MAX_HOOK_ROWS; h++)
      FP_ResetStateGateHookRow(s.hook_rows[h]);
   s.rally_row_count = 0;
   s.hook_row_count = 0;
   s.status = "reset";
   s.reason = "reset";
}

void FP_ResetStateGateRuntime(FP_StateGateRuntime &rt)
{
   rt.initialized = false;
   rt.minimized = false;
   rt.panel_has_drawn = false;
   rt.export_has_written = false;
   rt.last_run_had_dirty = false;
   for(int i=0; i<FP_STATE_GATE_TF_SLOTS; i++)
   {
      rt.last_processed_closed_bar_time[i] = 0;
      rt.previous_closed_bar_time[i] = 0;
      rt.slot_initialized[i] = false;
      rt.slot_update_count[i] = 0;
   }
   rt.update_serial = 0;
   rt.last_engine_run_time = 0;
   FP_ResetStateGateSnapshot(rt.snapshot);
}

void FP_ResetStateGateReport(FP_StateGateReport &r)
{
   r.attempted = false;
   r.ok = true;
   r.status = "not_run";
   r.reason = "not_attempted";
   r.version = FP_STATE_GATE_VERSION;
   r.symbol = "";
   r.timeframe_count = 0;
   r.slots_checked = 0;
   r.available_timeframes = 0;
   r.dirty_timeframes = 0;
   r.unchanged_timeframes = 0;
   r.unavailable_timeframes = 0;
   r.rally_rows = 0;
   r.hook_rows = 0;
   r.objects_requested = 0;
   r.objects_created = 0;
   r.object_errors = 0;
   r.objects_deleted = 0;
   r.files_written = 0;
   r.file_errors = 0;
   r.panel_redrawn = false;
   r.export_attempted = false;
   r.skipped_no_dirty = false;
}

void FP_DefaultStateGateConfig(FP_StateGateConfig &cfg)
{
   cfg.enabled = true;
   cfg.tf1 = PERIOD_M1;
   cfg.tf2 = PERIOD_M10;
   cfg.tf3 = PERIOD_H1;
   cfg.panel_enabled = true;
   cfg.panel_start_minimized = false;
   cfg.panel_corner = CORNER_RIGHT_UPPER;
   cfg.panel_x = 16;
   cfg.panel_y = 24;
   cfg.panel_width = 520;
   cfg.panel_font_size = 8;
   cfg.max_rally_rows_per_tf = 6;
   cfg.max_hook_rows_per_tf = 10;
   cfg.show_ids = true;
   cfg.show_scale_l = true;
   cfg.export_csv = true;
   cfg.export_overwrite_latest = true;
   cfg.export_folder = FP_STATE_GATE_DEFAULT_EXPORT_FOLDER;
   cfg.print_audit = true;
   cfg.object_prefix = FP_STATE_GATE_DEFAULT_PREFIX;
}

#endif // __FP_STATE_GATE_TYPES_MQH__
