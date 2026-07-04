#ifndef __FP_HOOK_PHASE02_TYPES_MQH__
#define __FP_HOOK_PHASE02_TYPES_MQH__
#property strict

#include "FP_HookPhase01Rules.mqh"

// ============================================================================
// FlagCounting Phoenix - NDS Hook Phase 02 Types
// ----------------------------------------------------------------------------
// Scope:
// - CycleHook object skeleton
// - positive/negative strict X-sequence builder
// - origin + X nodes + death boundary visualization foundation
// - no closure, no Y-axis, no Hook Type A/B/C yet
// - no execution, no broker request, no risk sizing, no volume sizing
// ============================================================================

#define FP_HOOK_P02_VERSION "HOOK-P02-cyclehook-sequence-builder"
#define FP_HOOK_P02_SCHEMA_VERSION "hook_phase02_sequences_v1"
#define FP_HOOK_P02_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_HOOK_P02_DEFAULT_PREFIX "DAL_HOOK_P02_"

enum FP_HookPhase02Direction
{
   FP_HOOK_P02_DIRECTION_POSITIVE = 1,
   FP_HOOK_P02_DIRECTION_NEGATIVE = -1
};

enum FP_HookPhase02SequenceState
{
   FP_HOOK_P02_STATE_RESET       = 0,
   FP_HOOK_P02_STATE_CANDIDATE   = 1,
   FP_HOOK_P02_STATE_READY       = 2,
   FP_HOOK_P02_STATE_MATURE      = 3,
   FP_HOOK_P02_STATE_CAPPED      = 4,
   FP_HOOK_P02_STATE_REJECTED    = -1
};

enum FP_HookPhase02OriginPolicy
{
   FP_HOOK_P02_ORIGIN_FIXED_EVERY_NODE      = 0,
   FP_HOOK_P02_ORIGIN_PROMOTE_WITH_INTERNAL_X = 1
};

enum FP_HookPhase02SequenceDrawMode
{
   FP_HOOK_P02_DRAW_RECENT_N = 0,
   FP_HOOK_P02_DRAW_LATEST_PER_SCALE_DIRECTION = 1,
   FP_HOOK_P02_DRAW_BY_SCALE_RECENT_N = 2,
   FP_HOOK_P02_DRAW_BY_SEQUENCE_ID = 3
};

enum FP_HookPhase02NodeLabelMode
{
   FP_HOOK_P02_NODE_LABEL_FULL = 0,
   FP_HOOK_P02_NODE_LABEL_NUMBERS_FROM_ZERO = 1,
   FP_HOOK_P02_NODE_LABEL_NUMBERS_WITH_O = 2
};

struct FP_HookPhase02Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;
   FP_HookPhase02OriginPolicy origin_policy;
   FP_HookPhase02SequenceDrawMode sequence_draw_mode;
   FP_HookPhase02NodeLabelMode node_label_mode;

   bool show_positive;
   bool show_negative;

   bool draw_sequences;
   bool draw_origin;
   bool draw_x_nodes;
   bool draw_x_lines;
   bool draw_death_boundary;
   bool draw_cycle_arc;
   bool draw_sequence_count_label;
   bool draw_labels;
   bool use_sequence_palette_colors;
   bool color_origin_with_sequence;
   bool color_node_labels_with_sequence;
   bool minimal_numbers_only;

   bool export_csv;
   bool print_summary;
   bool print_samples;

   int max_bars_to_scan;
   int max_sequences;
   int max_sequences_to_draw;
   int sequence_draw_scale_l;
   int sequence_draw_direction;
   int sequence_draw_sequence_id;
   int min_x_nodes_to_keep;
   int max_x_nodes_per_sequence;
   int sample_limit;
   int cycle_arc_segments;

   double cycle_arc_height_ratio;

   string folder;
   string object_prefix;

   color positive_color;
   color negative_color;
   color origin_color;
   color death_color;
   color cycle_arc_color;
   color sequence_count_label_color;
   color label_color;

   int line_width;
   int marker_width;
   int label_font_size;
};

struct FP_HookPhase02Sequence
{
   int sequence_id;
   int scale_l;
   FP_HookPhase02Direction direction;
   FP_HookPhase02SequenceState state;

   int origin_node_id;
   int origin_bar_index;
   datetime origin_time;
   double origin_price;

   int x_count;

   int x1_node_id;
   int x1_bar_index;
   datetime x1_time;
   double x1_price;

   int x2_node_id;
   int x2_bar_index;
   datetime x2_time;
   double x2_price;

   int x3_node_id;
   int x3_bar_index;
   datetime x3_time;
   double x3_price;

   int x4_node_id;
   int x4_bar_index;
   datetime x4_time;
   double x4_price;

   double last_x_price;
   datetime last_x_time;
   int last_x_bar_index;

   double death_boundary_price;
   bool capped;
   bool valid;
   string source;
   string reject_reason;
};

struct FP_HookPhase02Report
{
   bool attempted;
   bool ok;
   string status;
   string reason;

   int bars_seen;
   int bars_scanned;
   int scales_seen;
   int nodes_seen;

   int sequences_total;
   int sequences_positive;
   int sequences_negative;
   int sequences_ready;
   int sequences_mature;
   int sequences_capped;
   int rejected_candidates;
   int origin_promotions;
   int promoted_chains;

   int objects_deleted;
   int objects_created;
   int sequences_drawn;

   int files_written;
   int file_errors;
};

string FP_HookP02BoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_HookP02DirectionName(const FP_HookPhase02Direction d)
{
   if(d == FP_HOOK_P02_DIRECTION_POSITIVE) return "POSITIVE";
   if(d == FP_HOOK_P02_DIRECTION_NEGATIVE) return "NEGATIVE";
   return "UNKNOWN_DIRECTION";
}

string FP_HookP02OriginPolicyName(const FP_HookPhase02OriginPolicy p)
{
   if(p == FP_HOOK_P02_ORIGIN_FIXED_EVERY_NODE) return "FIXED_EVERY_NODE";
   if(p == FP_HOOK_P02_ORIGIN_PROMOTE_WITH_INTERNAL_X) return "PROMOTE_WITH_INTERNAL_X";
   return "UNKNOWN_ORIGIN_POLICY";
}

string FP_HookP02StateName(const FP_HookPhase02SequenceState s)
{
   if(s == FP_HOOK_P02_STATE_RESET) return "RESET";
   if(s == FP_HOOK_P02_STATE_CANDIDATE) return "CANDIDATE";
   if(s == FP_HOOK_P02_STATE_READY) return "READY";
   if(s == FP_HOOK_P02_STATE_MATURE) return "MATURE";
   if(s == FP_HOOK_P02_STATE_CAPPED) return "CAPPED";
   if(s == FP_HOOK_P02_STATE_REJECTED) return "REJECTED";
   return "UNKNOWN_STATE";
}

string FP_HookP02SequenceDrawModeName(const FP_HookPhase02SequenceDrawMode m)
{
   if(m == FP_HOOK_P02_DRAW_RECENT_N) return "RECENT_N";
   if(m == FP_HOOK_P02_DRAW_LATEST_PER_SCALE_DIRECTION) return "LATEST_PER_SCALE_DIRECTION";
   if(m == FP_HOOK_P02_DRAW_BY_SCALE_RECENT_N) return "BY_SCALE_RECENT_N";
   if(m == FP_HOOK_P02_DRAW_BY_SEQUENCE_ID) return "BY_SEQUENCE_ID";
   return "UNKNOWN_SEQUENCE_DRAW_MODE";
}

string FP_HookP02NodeLabelModeName(const FP_HookPhase02NodeLabelMode m)
{
   if(m == FP_HOOK_P02_NODE_LABEL_FULL) return "FULL";
   if(m == FP_HOOK_P02_NODE_LABEL_NUMBERS_FROM_ZERO) return "NUMBERS_FROM_ZERO";
   if(m == FP_HOOK_P02_NODE_LABEL_NUMBERS_WITH_O) return "NUMBERS_WITH_O";
   return "UNKNOWN_NODE_LABEL_MODE";
}

void FP_ResetHookPhase02Config(FP_HookPhase02Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;
   cfg.origin_policy = FP_HOOK_P02_ORIGIN_FIXED_EVERY_NODE;
   cfg.sequence_draw_mode = FP_HOOK_P02_DRAW_LATEST_PER_SCALE_DIRECTION;
   cfg.node_label_mode = FP_HOOK_P02_NODE_LABEL_FULL;

   cfg.show_positive = true;
   cfg.show_negative = true;

   cfg.draw_sequences = true;
   cfg.draw_origin = true;
   cfg.draw_x_nodes = true;
   cfg.draw_x_lines = true;
   cfg.draw_death_boundary = true;
   cfg.draw_cycle_arc = false;
   cfg.draw_sequence_count_label = false;
   cfg.draw_labels = true;
   cfg.use_sequence_palette_colors = false;
   cfg.color_origin_with_sequence = false;
   cfg.color_node_labels_with_sequence = false;
   cfg.minimal_numbers_only = false;

   cfg.export_csv = false;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.max_bars_to_scan = 0;
   cfg.max_sequences = 3000;
   cfg.max_sequences_to_draw = 6;
   cfg.sequence_draw_scale_l = 0;
   cfg.sequence_draw_direction = 0;
   cfg.sequence_draw_sequence_id = -1;
   cfg.min_x_nodes_to_keep = 1;
   cfg.max_x_nodes_per_sequence = 4;
   cfg.sample_limit = 10;
   cfg.cycle_arc_segments = 16;

   cfg.cycle_arc_height_ratio = 0.35;

   cfg.folder = FP_HOOK_P02_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P02_DEFAULT_PREFIX;

   cfg.positive_color = clrDeepSkyBlue;
   cfg.negative_color = clrTomato;
   cfg.origin_color = clrGold;
   cfg.death_color = clrDimGray;
   cfg.cycle_arc_color = clrSlateGray;
   cfg.sequence_count_label_color = clrGold;
   cfg.label_color = clrSilver;

   cfg.line_width = 1;
   cfg.marker_width = 1;
   cfg.label_font_size = 7;
}

void FP_ResetHookPhase02Sequence(FP_HookPhase02Sequence &s)
{
   s.sequence_id = -1;
   s.scale_l = 0;
   s.direction = FP_HOOK_P02_DIRECTION_POSITIVE;
   s.state = FP_HOOK_P02_STATE_RESET;

   s.origin_node_id = -1;
   s.origin_bar_index = -1;
   s.origin_time = 0;
   s.origin_price = 0.0;

   s.x_count = 0;

   s.x1_node_id = -1;
   s.x1_bar_index = -1;
   s.x1_time = 0;
   s.x1_price = 0.0;

   s.x2_node_id = -1;
   s.x2_bar_index = -1;
   s.x2_time = 0;
   s.x2_price = 0.0;

   s.x3_node_id = -1;
   s.x3_bar_index = -1;
   s.x3_time = 0;
   s.x3_price = 0.0;

   s.x4_node_id = -1;
   s.x4_bar_index = -1;
   s.x4_time = 0;
   s.x4_price = 0.0;

   s.last_x_price = 0.0;
   s.last_x_time = 0;
   s.last_x_bar_index = -1;

   s.death_boundary_price = 0.0;
   s.capped = false;
   s.valid = false;
   s.source = "";
   s.reject_reason = "";
}

void FP_ResetHookPhase02Report(FP_HookPhase02Report &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "HOOK_P02_RESET";
   r.reason = "RESET";

   r.bars_seen = 0;
   r.bars_scanned = 0;
   r.scales_seen = 0;
   r.nodes_seen = 0;

   r.sequences_total = 0;
   r.sequences_positive = 0;
   r.sequences_negative = 0;
   r.sequences_ready = 0;
   r.sequences_mature = 0;
   r.sequences_capped = 0;
   r.rejected_candidates = 0;
   r.origin_promotions = 0;
   r.promoted_chains = 0;

   r.objects_deleted = 0;
   r.objects_created = 0;
   r.sequences_drawn = 0;

   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE02_TYPES_MQH__
