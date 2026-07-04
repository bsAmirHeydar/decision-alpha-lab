#ifndef __FP_HOOK_PHASE01_TYPES_MQH__
#define __FP_HOOK_PHASE01_TYPES_MQH__
#property strict

// ============================================================================
// FlagCounting Phoenix - NDS Hook Phase 01 Types
// ----------------------------------------------------------------------------
// Scope:
// - Hook/CycleHook node source adapter foundation
// - display-family control for Rally-only / Hook-only / Rally-and-Hook
// - no execution, no broker request, no risk sizing, no volume sizing
// ============================================================================

#define FP_HOOK_P01_VERSION "HOOK-P01-node-source-adapter"
#define FP_HOOK_P01_SCHEMA_VERSION "hook_phase01_nodes_v1"
#define FP_HOOK_P01_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_HOOK_P01_DEFAULT_PREFIX "DAL_HOOK_P01_"

enum FP_NDSHookDisplayFamily
{
   FP_NDS_HOOK_DISPLAY_RALLY_ONLY       = 0,
   FP_NDS_HOOK_DISPLAY_HOOK_ONLY        = 1,
   FP_NDS_HOOK_DISPLAY_RALLY_AND_HOOK   = 2
};

enum FP_HookPhase01NodeType
{
   FP_HOOK_P01_NODE_PEAK   = 1,
   FP_HOOK_P01_NODE_VALLEY = -1
};

struct FP_HookPhase01Config
{
   bool enabled;
   FP_NDSHookDisplayFamily display_family;

   bool show_peaks;
   bool show_valleys;
   bool draw_nodes;
   bool draw_labels;
   bool export_csv;
   bool print_summary;
   bool print_samples;

   int max_bars_to_scan;
   int max_nodes;
   int max_nodes_to_draw;
   int sample_limit;

   string folder;
   string object_prefix;

   color peak_color;
   color valley_color;
   color label_color;
   int marker_width;
   int label_font_size;
};

struct FP_HookPhase01Node
{
   int node_id;
   int scale_l;
   int bar_index;
   datetime bar_time;
   double price;
   double high;
   double low;
   FP_HookPhase01NodeType node_type;
   bool confirmed;
   string source;
};

struct FP_HookPhase01ScaleSummary
{
   int scale_l;
   int peaks;
   int valleys;
   int total;
};

struct FP_HookPhase01Report
{
   bool attempted;
   bool ok;
   string status;
   string reason;

   int bars_seen;
   int bars_scanned;
   int scales_seen;
   int scales_scanned;
   int total_nodes;
   int peak_nodes;
   int valley_nodes;
   int nodes_drawn;
   int objects_deleted;
   int objects_created;
   int files_written;
   int file_errors;
};

string FP_HookP01BoolName(const bool v)
{
   return (v ? "true" : "false");
}

string FP_HookP01DisplayFamilyName(const FP_NDSHookDisplayFamily family)
{
   if(family == FP_NDS_HOOK_DISPLAY_RALLY_ONLY) return "RALLY_ONLY";
   if(family == FP_NDS_HOOK_DISPLAY_HOOK_ONLY) return "HOOK_ONLY";
   if(family == FP_NDS_HOOK_DISPLAY_RALLY_AND_HOOK) return "RALLY_AND_HOOK";
   return "UNKNOWN_DISPLAY_FAMILY";
}

string FP_HookP01NodeTypeName(const FP_HookPhase01NodeType t)
{
   if(t == FP_HOOK_P01_NODE_PEAK) return "PEAK";
   if(t == FP_HOOK_P01_NODE_VALLEY) return "VALLEY";
   return "UNKNOWN_NODE_TYPE";
}

void FP_ResetHookPhase01Config(FP_HookPhase01Config &cfg)
{
   cfg.enabled = true;
   cfg.display_family = FP_NDS_HOOK_DISPLAY_RALLY_ONLY;

   cfg.show_peaks = true;
   cfg.show_valleys = true;
   cfg.draw_nodes = true;
   cfg.draw_labels = true;
   cfg.export_csv = false;
   cfg.print_summary = false;
   cfg.print_samples = false;

   cfg.max_bars_to_scan = 0;
   cfg.max_nodes = 20000;
   cfg.max_nodes_to_draw = 500;
   cfg.sample_limit = 12;

   cfg.folder = FP_HOOK_P01_DEFAULT_FOLDER;
   cfg.object_prefix = FP_HOOK_P01_DEFAULT_PREFIX;

   cfg.peak_color = clrTomato;
   cfg.valley_color = clrDeepSkyBlue;
   cfg.label_color = clrSilver;
   cfg.marker_width = 1;
   cfg.label_font_size = 7;
}

void FP_ResetHookPhase01Node(FP_HookPhase01Node &n)
{
   n.node_id = -1;
   n.scale_l = 0;
   n.bar_index = -1;
   n.bar_time = 0;
   n.price = 0.0;
   n.high = 0.0;
   n.low = 0.0;
   n.node_type = FP_HOOK_P01_NODE_PEAK;
   n.confirmed = false;
   n.source = "";
}

void FP_ResetHookPhase01ScaleSummary(FP_HookPhase01ScaleSummary &s)
{
   s.scale_l = 0;
   s.peaks = 0;
   s.valleys = 0;
   s.total = 0;
}

void FP_ResetHookPhase01Report(FP_HookPhase01Report &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "HOOK_P01_RESET";
   r.reason = "RESET";

   r.bars_seen = 0;
   r.bars_scanned = 0;
   r.scales_seen = 0;
   r.scales_scanned = 0;
   r.total_nodes = 0;
   r.peak_nodes = 0;
   r.valley_nodes = 0;
   r.nodes_drawn = 0;
   r.objects_deleted = 0;
   r.objects_created = 0;
   r.files_written = 0;
   r.file_errors = 0;
}

#endif // __FP_HOOK_PHASE01_TYPES_MQH__
