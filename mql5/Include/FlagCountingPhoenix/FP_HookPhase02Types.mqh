#ifndef __FP_HOOK_PHASE02_TYPES_MQH__
#define __FP_HOOK_PHASE02_TYPES_MQH__
#property strict

#include "FP_HookPhase01Rules.mqh"
#include "FP_Types.mqh"

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
   FP_HOOK_P02_NODE_LABEL_NUMBERS_WITH_O = 2,
   FP_HOOK_P02_NODE_LABEL_NUMBERS_FROM_ONE_HIDE_ORIGIN = 3
};

enum FP_HookPhase02CycleArcEndMode
{
   FP_HOOK_P02_CYCLE_ARC_END_LAST_VISIBLE_X = 0,
   FP_HOOK_P02_CYCLE_ARC_END_DIRECTIONAL_EXTREME = 1
};

struct FP_HookPhase02Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;
   FP_HookPhase02OriginPolicy origin_policy;
   FP_HookPhase02SequenceDrawMode sequence_draw_mode;
   FP_HookPhase02NodeLabelMode node_label_mode;
   FP_HookPhase02CycleArcEndMode cycle_arc_end_mode;

   bool show_positive;
   bool show_negative;

   bool draw_sequences;
   bool draw_origin;
   bool draw_x_nodes;
   bool draw_node_markers;
   bool draw_x_lines;
   bool draw_death_boundary;
   bool draw_cycle_arc;
   bool cycle_arc_use_sequence_color;
   bool group_cycle_arc_by_origin;
   bool draw_sequence_count_label;
   bool draw_labels;
   bool use_sequence_palette_colors;
   bool color_origin_with_sequence;
   bool color_node_labels_with_sequence;
   bool color_node_numbers_by_index;
   bool minimal_numbers_only;
   bool use_minimal_node_markers;
   bool stack_node_labels_on_collisions;
   bool show_hook_sequence_ids_in_labels;
   bool responsive_label_offsets;
   bool require_confirmed_resolve_node;
   bool death_on_boundary_touch;
   bool require_near_death_for_semantic_arc;
   bool seed_used_nodes_cannot_restart;
   bool show_only_valid_hooks;

   bool export_csv;
   bool print_summary;
   bool print_samples;

   int max_bars_to_scan;
   int max_sequences;
   int max_sequences_to_draw;
   int min_x_count_to_draw;
   int arc_min_x_count_to_draw;
   int sequence_draw_scale_l;
   int sequence_draw_direction;
   int sequence_draw_sequence_id;
   int min_x_nodes_to_keep;
   int max_x_nodes_per_sequence;
   int sample_limit;
   int cycle_arc_segments;
   int cycle_arc_max_height_points;
   int node_number_offset_points;
   int node_label_stack_step_points;
   int responsive_label_lookback_bars;
   int responsive_label_min_offset_points;
   int responsive_label_max_offset_points;
   int responsive_label_min_step_points;
   int responsive_label_max_step_points;
   int label_time_cluster_seconds;
   int label_time_cluster_bars;
   int label_price_cluster_points;
   int minimal_node_marker_arrow_code;

   double cycle_arc_height_ratio;
   double near_death_retrace_threshold;
   double responsive_label_offset_range_ratio;
   double responsive_label_step_range_ratio;
   bool cycle_arc_align_to_bar_index;

   string folder;
   string object_prefix;

   color positive_color;
   color negative_color;
   color origin_color;
   color death_color;
   color cycle_arc_color;
   color sequence_count_label_color;
   color label_color;
   color node1_label_color;
   color node2_label_color;
   color node3_label_color;
   color node4_label_color;

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

   int cycle_crown_node_id;
   datetime cycle_crown_time;
   double cycle_crown_price;
   bool cycle_crown_valid;

   int resolve_node_id;
   datetime resolve_time;
   double resolve_price;
   bool resolve_confirmed;

   double retracement_ratio;
   bool near_death_confirmed;
   bool hook_failed;
   int failure_node_id;
   datetime failure_time;
   double failure_price;
   bool render_eligible;
   string visibility_reason;

   bool valid_after_hook;
   bool valid_after_opposing_f3;
   bool valid_hook_family;
   string hook_validity_family;
   int previous_hook_sequence_id;
   int previous_hook_terminal_node_id;
   int opposing_f3_event_id;

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
   int seed_reuse_rejects;
   int valid_after_hook;
   int valid_after_opposing_f3;
   int valid_hook_family_total;
   int invalid_family_filtered;

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
   if(m == FP_HOOK_P02_NODE_LABEL_NUMBERS_FROM_ONE_HIDE_ORIGIN) return "NUMBERS_FROM_ONE_HIDE_ORIGIN";
   return "UNKNOWN_NODE_LABEL_MODE";
}

string FP_HookP02CycleArcEndModeName(const FP_HookPhase02CycleArcEndMode m)
{
   if(m == FP_HOOK_P02_CYCLE_ARC_END_LAST_VISIBLE_X) return "LAST_VISIBLE_X";
   if(m == FP_HOOK_P02_CYCLE_ARC_END_DIRECTIONAL_EXTREME) return "DIRECTIONAL_EXTREME";
   return "UNKNOWN_CYCLE_ARC_END_MODE";
}

void FP_ResetHookPhase02Config(FP_HookPhase02Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;
   cfg.origin_policy = FP_HOOK_P02_ORIGIN_FIXED_EVERY_NODE;
   cfg.sequence_draw_mode = FP_HOOK_P02_DRAW_LATEST_PER_SCALE_DIRECTION;
   cfg.node_label_mode = FP_HOOK_P02_NODE_LABEL_NUMBERS_FROM_ONE_HIDE_ORIGIN;
   cfg.cycle_arc_end_mode = FP_HOOK_P02_CYCLE_ARC_END_DIRECTIONAL_EXTREME;

   cfg.show_positive = true;
   cfg.show_negative = true;

   cfg.draw_sequences = true;
   cfg.draw_origin = true;
   cfg.draw_x_nodes = true;
   cfg.draw_node_markers = false;
   cfg.draw_x_lines = false;
   cfg.draw_death_boundary = false;
   cfg.draw_cycle_arc = true;
   cfg.cycle_arc_use_sequence_color = false;
   cfg.group_cycle_arc_by_origin = true;
   cfg.draw_sequence_count_label = false;
   cfg.draw_labels = true;
   cfg.use_sequence_palette_colors = true;
   cfg.color_origin_with_sequence = false;
   cfg.color_node_labels_with_sequence = true;
   cfg.color_node_numbers_by_index = false;
   cfg.minimal_numbers_only = true;
   cfg.use_minimal_node_markers = false;
   cfg.stack_node_labels_on_collisions = true;
   cfg.show_hook_sequence_ids_in_labels = true;
   cfg.responsive_label_offsets = true;
   cfg.require_confirmed_resolve_node = true;
   cfg.death_on_boundary_touch = true;
   cfg.require_near_death_for_semantic_arc = true;
   cfg.seed_used_nodes_cannot_restart = true;
   cfg.show_only_valid_hooks = false;

   cfg.export_csv = false;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.max_bars_to_scan = 0;
   cfg.max_sequences = 3000;
   cfg.max_sequences_to_draw = 6;
   cfg.min_x_count_to_draw = 1;
   cfg.arc_min_x_count_to_draw = 1;
   cfg.sequence_draw_scale_l = 0;
   cfg.sequence_draw_direction = 0;
   cfg.sequence_draw_sequence_id = -1;
   cfg.min_x_nodes_to_keep = 1;
   cfg.max_x_nodes_per_sequence = 4;
   cfg.sample_limit = 10;
   cfg.cycle_arc_segments = 16;
   cfg.cycle_arc_max_height_points = 0;
   cfg.node_number_offset_points = 30;
   cfg.node_label_stack_step_points = 18;
   cfg.responsive_label_lookback_bars = 12;
   cfg.responsive_label_min_offset_points = 16;
   cfg.responsive_label_max_offset_points = 120;
   cfg.responsive_label_min_step_points = 10;
   cfg.responsive_label_max_step_points = 80;
   cfg.label_time_cluster_seconds = 0;
   cfg.label_time_cluster_bars = 2;
   cfg.label_price_cluster_points = 28;
   cfg.minimal_node_marker_arrow_code = 159;

   cfg.cycle_arc_height_ratio = 0.35;
   cfg.near_death_retrace_threshold = 0.50;
   cfg.responsive_label_offset_range_ratio = 0.35;
   cfg.responsive_label_step_range_ratio = 0.22;
   cfg.cycle_arc_align_to_bar_index = true;

   cfg.folder = FP_HOOK_P02_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P02_DEFAULT_PREFIX;

   cfg.positive_color = clrDeepSkyBlue;
   cfg.negative_color = clrTomato;
   cfg.origin_color = clrGold;
   cfg.death_color = clrDimGray;
   cfg.cycle_arc_color = C'40,40,40';
   cfg.sequence_count_label_color = clrGold;
   cfg.label_color = clrSilver;
   cfg.node1_label_color = clrAqua;
   cfg.node2_label_color = clrGold;
   cfg.node3_label_color = clrOrchid;
   cfg.node4_label_color = clrTomato;

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

   s.cycle_crown_node_id = -1;
   s.cycle_crown_time = 0;
   s.cycle_crown_price = 0.0;
   s.cycle_crown_valid = false;

   s.resolve_node_id = -1;
   s.resolve_time = 0;
   s.resolve_price = 0.0;
   s.resolve_confirmed = false;

   s.retracement_ratio = 0.0;
   s.near_death_confirmed = false;
   s.hook_failed = false;
   s.failure_node_id = -1;
   s.failure_time = 0;
   s.failure_price = 0.0;
   s.render_eligible = false;
   s.visibility_reason = "";

   s.valid_after_hook = false;
   s.valid_after_opposing_f3 = false;
   s.valid_hook_family = false;
   s.hook_validity_family = "UNQUALIFIED";
   s.previous_hook_sequence_id = -1;
   s.previous_hook_terminal_node_id = -1;
   s.opposing_f3_event_id = -1;

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
   r.seed_reuse_rejects = 0;
   r.valid_after_hook = 0;
   r.valid_after_opposing_f3 = 0;
   r.valid_hook_family_total = 0;
   r.invalid_family_filtered = 0;

   r.objects_deleted = 0;
   r.objects_created = 0;
   r.sequences_drawn = 0;

   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE02_TYPES_MQH__
