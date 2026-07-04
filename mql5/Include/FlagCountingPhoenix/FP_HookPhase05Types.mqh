#ifndef __FP_HOOK_PHASE05_TYPES_MQH__
#define __FP_HOOK_PHASE05_TYPES_MQH__
#property strict

#include "FP_HookPhase04Engine.mqh"

// ============================================================================
// FlagCounting Phoenix - NDS Hook Phase 05 Types
// ----------------------------------------------------------------------------
// Scope:
// - Hook Type A/B/C classifier
// - positive and negative type logic
// - type labels and CSV audit
// - no symmetry scoring yet
// - no quality score yet
// - no training labels yet
// - no execution, no broker request, no risk sizing, no volume sizing
// ============================================================================

#define FP_HOOK_P05_VERSION "HOOK-P05-type-abc-classifier"
#define FP_HOOK_P05_SCHEMA_VERSION "hook_phase05_type_abc_v1"
#define FP_HOOK_P05_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_HOOK_P05_DEFAULT_PREFIX "DAL_HOOK_P05_"

enum FP_HookPhase05HookType
{
   FP_HOOK_P05_TYPE_UNKNOWN      = 0,
   FP_HOOK_P05_TYPE_INSUFFICIENT = -1,
   FP_HOOK_P05_TYPE_A            = 3,
   FP_HOOK_P05_TYPE_B            = 2,
   FP_HOOK_P05_TYPE_C            = 1
};

enum FP_HookPhase05TypeState
{
   FP_HOOK_P05_STATE_RESET        = 0,
   FP_HOOK_P05_STATE_CLASSIFIED   = 1,
   FP_HOOK_P05_STATE_INSUFFICIENT = -1
};

struct FP_HookPhase05Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;

   bool show_positive;
   bool show_negative;

   bool draw_type_label;
   bool draw_type_anchor;
   bool draw_type_comparison_lines;
   bool draw_labels;

   bool export_csv;
   bool print_summary;
   bool print_samples;

   bool allow_y34_as_third_evidence;

   int max_bars_to_scan;
   int max_sequences;
   int max_sequences_to_draw;
   int min_x_nodes_to_keep;
   int max_x_nodes_per_sequence;
   int min_x_nodes_for_type;
   int sample_limit;

   string folder;
   string object_prefix;

   color type_a_color;
   color type_b_color;
   color type_c_color;
   color insufficient_color;
   color comparison_color;
   color label_color;

   int line_width;
   int marker_width;
   int label_font_size;
};

struct FP_HookPhase05Classification
{
   FP_HookPhase05HookType hook_type;
   FP_HookPhase05TypeState state;

   bool has_y01;
   bool has_y12;
   bool has_y23;
   bool has_y34;
   bool used_y34_as_third;

   double y01_price;
   double y12_price;
   double y23_price;
   double y34_price;
   double third_y_price;

   datetime y01_time;
   datetime y12_time;
   datetime y23_time;
   datetime y34_time;
   datetime third_y_time;

   string third_y_slot;

   bool condition_first;
   bool condition_second;

   int evidence_count;
   double confidence_score;
   double type_rank_score;

   string reason;
};

struct FP_HookPhase05Record
{
   FP_HookPhase04Record p04;
   FP_HookPhase05Classification classification;
   bool valid;
};

struct FP_HookPhase05Report
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
   int records_total;
   int records_positive;
   int records_negative;

   int type_a_count;
   int type_b_count;
   int type_c_count;
   int insufficient_count;
   int y34_fallback_count;

   int objects_deleted;
   int objects_created;
   int records_drawn;

   int files_written;
   int file_errors;
};

string FP_HookP05BoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_HookP05TypeName(const FP_HookPhase05HookType t)
{
   if(t == FP_HOOK_P05_TYPE_A) return "TYPE_A";
   if(t == FP_HOOK_P05_TYPE_B) return "TYPE_B";
   if(t == FP_HOOK_P05_TYPE_C) return "TYPE_C";
   if(t == FP_HOOK_P05_TYPE_INSUFFICIENT) return "INSUFFICIENT";
   return "UNKNOWN";
}

string FP_HookP05ShortTypeName(const FP_HookPhase05HookType t)
{
   if(t == FP_HOOK_P05_TYPE_A) return "A";
   if(t == FP_HOOK_P05_TYPE_B) return "B";
   if(t == FP_HOOK_P05_TYPE_C) return "C";
   if(t == FP_HOOK_P05_TYPE_INSUFFICIENT) return "INS";
   return "UNK";
}

string FP_HookP05StateName(const FP_HookPhase05TypeState s)
{
   if(s == FP_HOOK_P05_STATE_CLASSIFIED) return "CLASSIFIED";
   if(s == FP_HOOK_P05_STATE_INSUFFICIENT) return "INSUFFICIENT";
   if(s == FP_HOOK_P05_STATE_RESET) return "RESET";
   return "UNKNOWN_STATE";
}

void FP_ResetHookPhase05Config(FP_HookPhase05Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;

   cfg.show_positive = true;
   cfg.show_negative = true;

   cfg.draw_type_label = true;
   cfg.draw_type_anchor = true;
   cfg.draw_type_comparison_lines = true;
   cfg.draw_labels = true;

   cfg.export_csv = false;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.allow_y34_as_third_evidence = false;

   cfg.max_bars_to_scan = 0;
   cfg.max_sequences = 3000;
   cfg.max_sequences_to_draw = 120;
   cfg.min_x_nodes_to_keep = 1;
   cfg.max_x_nodes_per_sequence = 4;
   cfg.min_x_nodes_for_type = 2;
   cfg.sample_limit = 10;

   cfg.folder = FP_HOOK_P05_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P05_DEFAULT_PREFIX;

   cfg.type_a_color = clrLime;
   cfg.type_b_color = clrDeepSkyBlue;
   cfg.type_c_color = clrOrange;
   cfg.insufficient_color = clrGray;
   cfg.comparison_color = clrSlateGray;
   cfg.label_color = clrWhite;

   cfg.line_width = 1;
   cfg.marker_width = 1;
   cfg.label_font_size = 8;
}

void FP_ResetHookPhase05Classification(FP_HookPhase05Classification &c)
{
   c.hook_type = FP_HOOK_P05_TYPE_UNKNOWN;
   c.state = FP_HOOK_P05_STATE_RESET;

   c.has_y01 = false;
   c.has_y12 = false;
   c.has_y23 = false;
   c.has_y34 = false;
   c.used_y34_as_third = false;

   c.y01_price = 0.0;
   c.y12_price = 0.0;
   c.y23_price = 0.0;
   c.y34_price = 0.0;
   c.third_y_price = 0.0;

   c.y01_time = 0;
   c.y12_time = 0;
   c.y23_time = 0;
   c.y34_time = 0;
   c.third_y_time = 0;

   c.third_y_slot = "";

   c.condition_first = false;
   c.condition_second = false;

   c.evidence_count = 0;
   c.confidence_score = 0.0;
   c.type_rank_score = 0.0;

   c.reason = "RESET";
}

void FP_ResetHookPhase05Record(FP_HookPhase05Record &r)
{
   FP_ResetHookPhase04Record(r.p04);
   FP_ResetHookPhase05Classification(r.classification);
   r.valid = false;
}

void FP_ResetHookPhase05Report(FP_HookPhase05Report &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "HOOK_P05_RESET";
   r.reason = "RESET";

   r.bars_seen = 0;
   r.bars_scanned = 0;
   r.scales_seen = 0;
   r.nodes_seen = 0;

   r.phase02_sequences_seen = 0;
   r.phase03_records_seen = 0;
   r.phase04_records_seen = 0;
   r.records_total = 0;
   r.records_positive = 0;
   r.records_negative = 0;

   r.type_a_count = 0;
   r.type_b_count = 0;
   r.type_c_count = 0;
   r.insufficient_count = 0;
   r.y34_fallback_count = 0;

   r.objects_deleted = 0;
   r.objects_created = 0;
   r.records_drawn = 0;

   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE05_TYPES_MQH__
