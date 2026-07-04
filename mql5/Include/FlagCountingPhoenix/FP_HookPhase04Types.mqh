#ifndef __FP_HOOK_PHASE04_TYPES_MQH__
#define __FP_HOOK_PHASE04_TYPES_MQH__
#property strict

#include "FP_HookPhase03Engine.mqh"

// ============================================================================
// FlagCounting Phoenix - NDS Hook Phase 04 Types
// ----------------------------------------------------------------------------
// Scope:
// - ND / return-toward-origin candidate detection
// - origin return penetration / death lifecycle marker
// - 50% X-closure skeleton using Y-axis opposite Extreme
// - lifecycle visualization and CSV audit
// - no Hook Type A/B/C yet
// - no execution, no broker request, no risk sizing, no volume sizing
// ============================================================================

#define FP_HOOK_P04_VERSION "HOOK-P04-nd-death-x-closure-skeleton"
#define FP_HOOK_P04_SCHEMA_VERSION "hook_phase04_lifecycle_v1"
#define FP_HOOK_P04_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_HOOK_P04_DEFAULT_PREFIX "DAL_HOOK_P04_"

enum FP_HookPhase04LifecycleState
{
   FP_HOOK_P04_LIFE_RESET                  = 0,
   FP_HOOK_P04_LIFE_ALIVE                  = 1,
   FP_HOOK_P04_LIFE_ND_CANDIDATE           = 2,
   FP_HOOK_P04_LIFE_X_CLOSURE_CANDIDATE    = 3,
   FP_HOOK_P04_LIFE_X_CLOSED               = 4,
   FP_HOOK_P04_LIFE_DEAD_BY_ORIGIN_RETURN  = -1,
   FP_HOOK_P04_LIFE_INSUFFICIENT_DATA      = -2
};

struct FP_HookPhase04Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;

   bool show_positive;
   bool show_negative;

   bool draw_nd;
   bool draw_death;
   bool draw_x_closure;
   bool draw_thresholds;
   bool draw_labels;

   bool export_csv;
   bool print_summary;
   bool print_samples;

   int max_bars_to_scan;
   int max_sequences;
   int max_sequences_to_draw;
   int min_x_nodes_to_keep;
   int max_x_nodes_per_sequence;
   int min_x_nodes_for_closure;
   int sample_limit;

   double nd_return_ratio;
   double closure_retrace_ratio;

   string folder;
   string object_prefix;

   color nd_color;
   color death_color;
   color closure_color;
   color threshold_color;
   color label_color;

   int line_width;
   int marker_width;
   int label_font_size;
};

struct FP_HookPhase04Lifecycle
{
   FP_HookPhase04LifecycleState state;
   string state_reason;

   bool nd_detected;
   datetime nd_time;
   int nd_bar_index;
   double nd_price;
   double nd_threshold_price;
   double nd_return_ratio;

   bool origin_return_penetrated;
   datetime death_time;
   int death_bar_index;
   double death_price;
   double death_boundary_price;

   bool x_closure_candidate;
   bool x_closed;
   datetime x_closure_time;
   int x_closure_bar_index;
   double x_closure_price;
   double x_closure_threshold_price;
   double x_closure_reference_y_price;
   datetime x_closure_reference_y_time;
   string x_closure_reference_y_slot;
   double closure_retrace_ratio;

   bool has_required_y;
   bool has_required_x;
};

struct FP_HookPhase04Record
{
   FP_HookPhase03Record p03;
   FP_HookPhase04Lifecycle lifecycle;
   bool valid;
};

struct FP_HookPhase04Report
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
   int phase03_records_seen;
   int records_total;
   int records_positive;
   int records_negative;

   int nd_count;
   int death_count;
   int x_closure_candidate_count;
   int x_closed_count;
   int alive_count;
   int insufficient_count;

   int objects_deleted;
   int objects_created;
   int records_drawn;

   int files_written;
   int file_errors;
};

string FP_HookP04BoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_HookP04LifecycleStateName(const FP_HookPhase04LifecycleState s)
{
   if(s == FP_HOOK_P04_LIFE_RESET) return "RESET";
   if(s == FP_HOOK_P04_LIFE_ALIVE) return "ALIVE";
   if(s == FP_HOOK_P04_LIFE_ND_CANDIDATE) return "ND_CANDIDATE";
   if(s == FP_HOOK_P04_LIFE_X_CLOSURE_CANDIDATE) return "X_CLOSURE_CANDIDATE";
   if(s == FP_HOOK_P04_LIFE_X_CLOSED) return "X_CLOSED";
   if(s == FP_HOOK_P04_LIFE_DEAD_BY_ORIGIN_RETURN) return "DEAD_BY_ORIGIN_RETURN";
   if(s == FP_HOOK_P04_LIFE_INSUFFICIENT_DATA) return "INSUFFICIENT_DATA";
   return "UNKNOWN_LIFECYCLE_STATE";
}

void FP_ResetHookPhase04Config(FP_HookPhase04Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;

   cfg.show_positive = true;
   cfg.show_negative = true;

   cfg.draw_nd = true;
   cfg.draw_death = true;
   cfg.draw_x_closure = true;
   cfg.draw_thresholds = true;
   cfg.draw_labels = true;

   cfg.export_csv = false;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.max_bars_to_scan = 0;
   cfg.max_sequences = 3000;
   cfg.max_sequences_to_draw = 120;
   cfg.min_x_nodes_to_keep = 1;
   cfg.max_x_nodes_per_sequence = 4;
   cfg.min_x_nodes_for_closure = 3;
   cfg.sample_limit = 10;

   cfg.nd_return_ratio = 0.50;
   cfg.closure_retrace_ratio = 0.50;

   cfg.folder = FP_HOOK_P04_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P04_DEFAULT_PREFIX;

   cfg.nd_color = clrMediumSpringGreen;
   cfg.death_color = clrRed;
   cfg.closure_color = clrViolet;
   cfg.threshold_color = clrSlateGray;
   cfg.label_color = clrSilver;

   cfg.line_width = 1;
   cfg.marker_width = 1;
   cfg.label_font_size = 7;
}

void FP_ResetHookPhase04Lifecycle(FP_HookPhase04Lifecycle &l)
{
   l.state = FP_HOOK_P04_LIFE_RESET;
   l.state_reason = "RESET";

   l.nd_detected = false;
   l.nd_time = 0;
   l.nd_bar_index = -1;
   l.nd_price = 0.0;
   l.nd_threshold_price = 0.0;
   l.nd_return_ratio = 0.0;

   l.origin_return_penetrated = false;
   l.death_time = 0;
   l.death_bar_index = -1;
   l.death_price = 0.0;
   l.death_boundary_price = 0.0;

   l.x_closure_candidate = false;
   l.x_closed = false;
   l.x_closure_time = 0;
   l.x_closure_bar_index = -1;
   l.x_closure_price = 0.0;
   l.x_closure_threshold_price = 0.0;
   l.x_closure_reference_y_price = 0.0;
   l.x_closure_reference_y_time = 0;
   l.x_closure_reference_y_slot = "";
   l.closure_retrace_ratio = 0.0;

   l.has_required_y = false;
   l.has_required_x = false;
}

void FP_ResetHookPhase04Record(FP_HookPhase04Record &r)
{
   FP_ResetHookPhase03Record(r.p03);
   FP_ResetHookPhase04Lifecycle(r.lifecycle);
   r.valid = false;
}

void FP_ResetHookPhase04Report(FP_HookPhase04Report &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "HOOK_P04_RESET";
   r.reason = "RESET";

   r.bars_seen = 0;
   r.bars_scanned = 0;
   r.scales_seen = 0;
   r.nodes_seen = 0;

   r.phase02_sequences_seen = 0;
   r.phase03_records_seen = 0;
   r.records_total = 0;
   r.records_positive = 0;
   r.records_negative = 0;

   r.nd_count = 0;
   r.death_count = 0;
   r.x_closure_candidate_count = 0;
   r.x_closed_count = 0;
   r.alive_count = 0;
   r.insufficient_count = 0;

   r.objects_deleted = 0;
   r.objects_created = 0;
   r.records_drawn = 0;

   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE04_TYPES_MQH__
