#ifndef __FP_HOOK_PHASE03_TYPES_MQH__
#define __FP_HOOK_PHASE03_TYPES_MQH__
#property strict

#include "FP_HookPhase02Engine.mqh"

// ============================================================================
// FlagCounting Phoenix - NDS Hook Phase 03 Types
// ----------------------------------------------------------------------------
// Scope:
// - Y-axis opposite Extreme extraction for CycleHook X sequences
// - Y01/Y12/Y23/Y34 audit rows
// - X/Y visual diagnostics
// - no closure, no ND confirmation, no Hook Type A/B/C yet
// - no execution, no broker request, no risk sizing, no volume sizing
// ============================================================================

#define FP_HOOK_P03_VERSION "HOOK-P03-y-axis-opposite-extremes"
#define FP_HOOK_P03_SCHEMA_VERSION "hook_phase03_y_axis_v1"
#define FP_HOOK_P03_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_HOOK_P03_DEFAULT_PREFIX "DAL_HOOK_P03_"

enum FP_HookPhase03YState
{
   FP_HOOK_P03_Y_RESET     = 0,
   FP_HOOK_P03_Y_MISSING   = 1,
   FP_HOOK_P03_Y_READY     = 2,
   FP_HOOK_P03_Y_PARTIAL   = 3,
   FP_HOOK_P03_Y_COMPLETE  = 4
};

struct FP_HookPhase03Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;

   bool show_positive;
   bool show_negative;

   bool draw_y_extremes;
   bool draw_y_lines;
   bool draw_x_reference;
   bool draw_labels;

   bool export_csv;
   bool print_summary;
   bool print_samples;

   int max_bars_to_scan;
   int max_sequences;
   int max_sequences_to_draw;
   int min_x_nodes_to_keep;
   int max_x_nodes_per_sequence;
   int sample_limit;

   string folder;
   string object_prefix;

   color positive_y_color;
   color negative_y_color;
   color x_reference_color;
   color label_color;

   int line_width;
   int marker_width;
   int label_font_size;
};

struct FP_HookPhase03YAxis
{
   bool has_y01;
   int y01_bar_index;
   datetime y01_time;
   double y01_price;

   bool has_y12;
   int y12_bar_index;
   datetime y12_time;
   double y12_price;

   bool has_y23;
   int y23_bar_index;
   datetime y23_time;
   double y23_price;

   bool has_y34;
   int y34_bar_index;
   datetime y34_time;
   double y34_price;

   int y_count;
   FP_HookPhase03YState y_state;
   string y_state_reason;
};

struct FP_HookPhase03Record
{
   FP_HookPhase02Sequence sequence;
   FP_HookPhase03YAxis y_axis;
   bool valid;
};

struct FP_HookPhase03Report
{
   bool attempted;
   bool ok;
   string status;
   string reason;

   int bars_seen;
   int bars_scanned;
   int scales_seen;
   int nodes_seen;

   int phase02_sequences_seen;
   int records_total;
   int records_positive;
   int records_negative;

   int y01_count;
   int y12_count;
   int y23_count;
   int y34_count;
   int y_complete_count;
   int y_partial_count;
   int y_missing_count;

   int objects_deleted;
   int objects_created;
   int records_drawn;

   int files_written;
   int file_errors;
};

string FP_HookP03BoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_HookP03YStateName(const FP_HookPhase03YState s)
{
   if(s == FP_HOOK_P03_Y_RESET) return "RESET";
   if(s == FP_HOOK_P03_Y_MISSING) return "MISSING";
   if(s == FP_HOOK_P03_Y_READY) return "READY";
   if(s == FP_HOOK_P03_Y_PARTIAL) return "PARTIAL";
   if(s == FP_HOOK_P03_Y_COMPLETE) return "COMPLETE";
   return "UNKNOWN_Y_STATE";
}

void FP_ResetHookPhase03Config(FP_HookPhase03Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;

   cfg.show_positive = true;
   cfg.show_negative = true;

   cfg.draw_y_extremes = true;
   cfg.draw_y_lines = true;
   cfg.draw_x_reference = false;
   cfg.draw_labels = true;

   cfg.export_csv = false;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.max_bars_to_scan = 0;
   cfg.max_sequences = 3000;
   cfg.max_sequences_to_draw = 120;
   cfg.min_x_nodes_to_keep = 1;
   cfg.max_x_nodes_per_sequence = 4;
   cfg.sample_limit = 10;

   cfg.folder = FP_HOOK_P03_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P03_DEFAULT_PREFIX;

   cfg.positive_y_color = clrDodgerBlue;
   cfg.negative_y_color = clrOrangeRed;
   cfg.x_reference_color = clrDarkGray;
   cfg.label_color = clrSilver;

   cfg.line_width = 1;
   cfg.marker_width = 1;
   cfg.label_font_size = 7;
}

void FP_ResetHookPhase03YAxis(FP_HookPhase03YAxis &y)
{
   y.has_y01 = false;
   y.y01_bar_index = -1;
   y.y01_time = 0;
   y.y01_price = 0.0;

   y.has_y12 = false;
   y.y12_bar_index = -1;
   y.y12_time = 0;
   y.y12_price = 0.0;

   y.has_y23 = false;
   y.y23_bar_index = -1;
   y.y23_time = 0;
   y.y23_price = 0.0;

   y.has_y34 = false;
   y.y34_bar_index = -1;
   y.y34_time = 0;
   y.y34_price = 0.0;

   y.y_count = 0;
   y.y_state = FP_HOOK_P03_Y_RESET;
   y.y_state_reason = "RESET";
}

void FP_ResetHookPhase03Record(FP_HookPhase03Record &r)
{
   FP_ResetHookPhase02Sequence(r.sequence);
   FP_ResetHookPhase03YAxis(r.y_axis);
   r.valid = false;
}

void FP_ResetHookPhase03Report(FP_HookPhase03Report &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "HOOK_P03_RESET";
   r.reason = "RESET";

   r.bars_seen = 0;
   r.bars_scanned = 0;
   r.scales_seen = 0;
   r.nodes_seen = 0;

   r.phase02_sequences_seen = 0;
   r.records_total = 0;
   r.records_positive = 0;
   r.records_negative = 0;

   r.y01_count = 0;
   r.y12_count = 0;
   r.y23_count = 0;
   r.y34_count = 0;
   r.y_complete_count = 0;
   r.y_partial_count = 0;
   r.y_missing_count = 0;

   r.objects_deleted = 0;
   r.objects_created = 0;
   r.records_drawn = 0;

   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE03_TYPES_MQH__
