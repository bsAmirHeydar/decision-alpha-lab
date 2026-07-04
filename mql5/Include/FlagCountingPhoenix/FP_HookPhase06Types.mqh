#ifndef __FP_HOOK_PHASE06_TYPES_MQH__
#define __FP_HOOK_PHASE06_TYPES_MQH__
#property strict

#include "FP_HookPhase05Engine.mqh"

// ============================================================================
// FlagCounting Phoenix - NDS Hook Phase 06 Types
// ----------------------------------------------------------------------------
// Scope:
// - X/Y closure strength scoring
// - Y-sequence step validation independent from Hook Type A/B/C
// - structural quality bucket for audit/training preparation
// - no execution, no broker request, no risk sizing, no volume sizing
// ============================================================================

#define FP_HOOK_P06_VERSION "HOOK-P06-xy-closure-quality-score"
#define FP_HOOK_P06_SCHEMA_VERSION "hook_phase06_xy_quality_v1"
#define FP_HOOK_P06_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_HOOK_P06_DEFAULT_PREFIX "DAL_HOOK_P06_"

enum FP_HookPhase06YClosureState
{
   FP_HOOK_P06_Y_RESET        = 0,
   FP_HOOK_P06_Y_INSUFFICIENT = -1,
   FP_HOOK_P06_Y_NOT_CLOSED   = 1,
   FP_HOOK_P06_Y_PARTIAL      = 2,
   FP_HOOK_P06_Y_CLOSED       = 3
};

enum FP_HookPhase06XYClosureState
{
   FP_HOOK_P06_XY_RESET                 = 0,
   FP_HOOK_P06_XY_DEAD_BY_ORIGIN_RETURN = -2,
   FP_HOOK_P06_XY_INSUFFICIENT          = -1,
   FP_HOOK_P06_XY_OPEN                  = 1,
   FP_HOOK_P06_XY_X_ONLY                = 2,
   FP_HOOK_P06_XY_Y_ONLY                = 3,
   FP_HOOK_P06_XY_CLOSED                = 4
};

enum FP_HookPhase06QualityBucket
{
   FP_HOOK_P06_QUALITY_UNKNOWN = 0,
   FP_HOOK_P06_QUALITY_INVALID = -1,
   FP_HOOK_P06_QUALITY_LOW     = 1,
   FP_HOOK_P06_QUALITY_MEDIUM  = 2,
   FP_HOOK_P06_QUALITY_HIGH    = 3,
   FP_HOOK_P06_QUALITY_ELITE   = 4
};

struct FP_HookPhase06Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;

   bool show_positive;
   bool show_negative;

   bool draw_quality_label;
   bool draw_xy_anchor;
   bool draw_projection_lines;
   bool draw_labels;

   bool export_csv;
   bool print_summary;
   bool print_samples;

   bool include_dead_records;
   bool require_x_closed_for_xy;

   int max_bars_to_scan;
   int max_sequences;
   int max_sequences_to_draw;
   int min_x_nodes_to_keep;
   int max_x_nodes_per_sequence;
   int min_x_nodes_for_quality;
   int min_y_comparisons_for_closed;
   int sample_limit;

   double x_weight;
   double y_weight;
   double type_weight;
   double lifecycle_weight;
   double elite_threshold;
   double high_threshold;
   double medium_threshold;
   double low_threshold;

   string folder;
   string object_prefix;

   color xy_closed_color;
   color x_only_color;
   color y_only_color;
   color open_color;
   color insufficient_color;
   color projection_color;
   color label_color;

   int line_width;
   int marker_width;
   int label_font_size;
};

struct FP_HookPhase06Score
{
   FP_HookPhase06YClosureState y_state;
   FP_HookPhase06XYClosureState xy_state;
   FP_HookPhase06QualityBucket quality_bucket;

   bool x_closed;
   bool y_closed;
   bool y_partial;
   bool dead;
   bool sufficient_x;
   bool sufficient_y;

   int y_comparisons_total;
   int y_comparisons_passed;

   bool y01_y12_passed;
   bool y12_y23_passed;
   bool y23_y34_passed;

   double x_strength;
   double y_strength;
   double type_strength;
   double lifecycle_strength;
   double quality_score;

   datetime anchor_time;
   double anchor_price;
   string anchor_slot;

   string reason;
};

struct FP_HookPhase06Record
{
   FP_HookPhase05Record p05;
   FP_HookPhase06Score score;
   bool valid;
};

struct FP_HookPhase06Report
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
   int phase04_records_seen;
   int phase05_records_seen;
   int records_total;
   int records_positive;
   int records_negative;

   int xy_closed_count;
   int x_only_count;
   int y_only_count;
   int open_count;
   int dead_count;
   int insufficient_count;

   int y_closed_count;
   int y_partial_count;
   int y_not_closed_count;

   int elite_count;
   int high_count;
   int medium_count;
   int low_count;
   int invalid_count;

   int objects_deleted;
   int objects_created;
   int records_drawn;

   int files_written;
   int file_errors;
};

string FP_HookP06BoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_HookP06YStateName(const FP_HookPhase06YClosureState s)
{
   if(s == FP_HOOK_P06_Y_RESET) return "RESET";
   if(s == FP_HOOK_P06_Y_INSUFFICIENT) return "INSUFFICIENT";
   if(s == FP_HOOK_P06_Y_NOT_CLOSED) return "NOT_CLOSED";
   if(s == FP_HOOK_P06_Y_PARTIAL) return "PARTIAL";
   if(s == FP_HOOK_P06_Y_CLOSED) return "CLOSED";
   return "UNKNOWN_Y_CLOSURE_STATE";
}

string FP_HookP06XYStateName(const FP_HookPhase06XYClosureState s)
{
   if(s == FP_HOOK_P06_XY_RESET) return "RESET";
   if(s == FP_HOOK_P06_XY_DEAD_BY_ORIGIN_RETURN) return "DEAD_BY_ORIGIN_RETURN";
   if(s == FP_HOOK_P06_XY_INSUFFICIENT) return "INSUFFICIENT";
   if(s == FP_HOOK_P06_XY_OPEN) return "OPEN";
   if(s == FP_HOOK_P06_XY_X_ONLY) return "X_ONLY";
   if(s == FP_HOOK_P06_XY_Y_ONLY) return "Y_ONLY";
   if(s == FP_HOOK_P06_XY_CLOSED) return "XY_CLOSED";
   return "UNKNOWN_XY_CLOSURE_STATE";
}

string FP_HookP06QualityBucketName(const FP_HookPhase06QualityBucket b)
{
   if(b == FP_HOOK_P06_QUALITY_UNKNOWN) return "UNKNOWN";
   if(b == FP_HOOK_P06_QUALITY_INVALID) return "INVALID";
   if(b == FP_HOOK_P06_QUALITY_LOW) return "LOW";
   if(b == FP_HOOK_P06_QUALITY_MEDIUM) return "MEDIUM";
   if(b == FP_HOOK_P06_QUALITY_HIGH) return "HIGH";
   if(b == FP_HOOK_P06_QUALITY_ELITE) return "ELITE";
   return "UNKNOWN_QUALITY_BUCKET";
}

void FP_ResetHookPhase06Config(FP_HookPhase06Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;

   cfg.show_positive = true;
   cfg.show_negative = true;

   cfg.draw_quality_label = true;
   cfg.draw_xy_anchor = true;
   cfg.draw_projection_lines = true;
   cfg.draw_labels = true;

   cfg.export_csv = false;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.include_dead_records = true;
   cfg.require_x_closed_for_xy = true;

   cfg.max_bars_to_scan = 0;
   cfg.max_sequences = 3000;
   cfg.max_sequences_to_draw = 120;
   cfg.min_x_nodes_to_keep = 1;
   cfg.max_x_nodes_per_sequence = 4;
   cfg.min_x_nodes_for_quality = 3;
   cfg.min_y_comparisons_for_closed = 2;
   cfg.sample_limit = 10;

   cfg.x_weight = 0.30;
   cfg.y_weight = 0.30;
   cfg.type_weight = 0.20;
   cfg.lifecycle_weight = 0.20;
   cfg.elite_threshold = 0.80;
   cfg.high_threshold = 0.65;
   cfg.medium_threshold = 0.45;
   cfg.low_threshold = 0.25;

   cfg.folder = FP_HOOK_P06_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P06_DEFAULT_PREFIX;

   cfg.xy_closed_color = clrLime;
   cfg.x_only_color = clrViolet;
   cfg.y_only_color = clrDeepSkyBlue;
   cfg.open_color = clrOrange;
   cfg.insufficient_color = clrGray;
   cfg.projection_color = clrSlateGray;
   cfg.label_color = clrWhite;

   cfg.line_width = 1;
   cfg.marker_width = 1;
   cfg.label_font_size = 8;
}

void FP_ResetHookPhase06Score(FP_HookPhase06Score &s)
{
   s.y_state = FP_HOOK_P06_Y_RESET;
   s.xy_state = FP_HOOK_P06_XY_RESET;
   s.quality_bucket = FP_HOOK_P06_QUALITY_UNKNOWN;

   s.x_closed = false;
   s.y_closed = false;
   s.y_partial = false;
   s.dead = false;
   s.sufficient_x = false;
   s.sufficient_y = false;

   s.y_comparisons_total = 0;
   s.y_comparisons_passed = 0;

   s.y01_y12_passed = false;
   s.y12_y23_passed = false;
   s.y23_y34_passed = false;

   s.x_strength = 0.0;
   s.y_strength = 0.0;
   s.type_strength = 0.0;
   s.lifecycle_strength = 0.0;
   s.quality_score = 0.0;

   s.anchor_time = 0;
   s.anchor_price = 0.0;
   s.anchor_slot = "";

   s.reason = "RESET";
}

void FP_ResetHookPhase06Record(FP_HookPhase06Record &r)
{
   FP_ResetHookPhase05Record(r.p05);
   FP_ResetHookPhase06Score(r.score);
   r.valid = false;
}

void FP_ResetHookPhase06Report(FP_HookPhase06Report &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "HOOK_P06_RESET";
   r.reason = "RESET";

   r.bars_seen = 0;
   r.bars_scanned = 0;
   r.scales_seen = 0;
   r.nodes_seen = 0;

   r.phase02_sequences_seen = 0;
   r.phase03_records_seen = 0;
   r.phase04_records_seen = 0;
   r.phase05_records_seen = 0;
   r.records_total = 0;
   r.records_positive = 0;
   r.records_negative = 0;

   r.xy_closed_count = 0;
   r.x_only_count = 0;
   r.y_only_count = 0;
   r.open_count = 0;
   r.dead_count = 0;
   r.insufficient_count = 0;

   r.y_closed_count = 0;
   r.y_partial_count = 0;
   r.y_not_closed_count = 0;

   r.elite_count = 0;
   r.high_count = 0;
   r.medium_count = 0;
   r.low_count = 0;
   r.invalid_count = 0;

   r.objects_deleted = 0;
   r.objects_created = 0;
   r.records_drawn = 0;

   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE06_TYPES_MQH__
