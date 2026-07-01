#ifndef __FP_STATE_GATE_TYPES_MQH__
#define __FP_STATE_GATE_TYPES_MQH__
#property strict

#define FP_LEVEL19_STATE_GATE_VERSION "19.10-closed-bar-ledger"
#define FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER "FlagCountingPhoenix"
#define FP_LEVEL19_STATE_GATE_DEFAULT_PANEL_PREFIX "DAL_L19_STATE_GATE_PANEL_"

// ============================================================================
// FlagCounting Phoenix - Level 19 Clean Isolated State Gate Types
// ----------------------------------------------------------------------------
// Contract:
// - read-only
// - no renderer mutation
// - no F/Hook/Node/RTV/Zone object cleanup
// - panel disabled by default from EA inputs
// - CSV diagnostics only unless panel is explicitly enabled
// ============================================================================

struct FP_Level19StateGateConfig
{
   bool enabled;
   bool export_csv;
   bool export_closed_bar_ledger_csv;
   bool panel_enabled;
   bool panel_clean_on_init;
   bool panel_clean_on_deinit;
   bool print_summary;

   string folder;
   string object_prefix;

   ENUM_BASE_CORNER panel_corner;
   int panel_x;
   int panel_y;
   int panel_width;
   int panel_font_size;
};

struct FP_Level19StateGateSnapshot
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   int bars;
   int scale_count;

   bool timebase_ok;
   string timebase_status;
   string timebase_reason;
   datetime first_bar_time;
   datetime last_bar_time;

   int raw_nodes_total;
   int nodes_total;
   int confirmed_nodes_total;
   int pending_nodes_total;
   int hooks_total;
   int events_total;
   int visible_events_total;
   int hidden_events_total;
   int f1_total;
   int f2_total;
   int f3_total;
   int nd_total;

   int input_events;
   int input_hooks;
   int visible_hooks_seen;

   bool export_attempted;
   bool export_ok;
   int export_files_written;
   int export_file_errors;

   bool render_attempted;
   bool render_ok;
   int render_objects_created;
   int render_object_errors;
   int render_objects_deleted;
   string render_reason;

   bool validation_attempted;
   bool validation_ok;
   int validation_failed;
   int validation_warned;

   string latest_visible_event_id;
   int latest_visible_event_level;
   int latest_visible_event_L;
   int latest_visible_event_direction;
   int latest_visible_event_status;

   string latest_visible_hook_id;
   int latest_visible_hook_L;
   int latest_visible_hook_direction;
   int latest_visible_hook_status;
   bool latest_visible_hook_is_nd;
   int latest_visible_hook_node_count;

   string state_status;
   string state_key;
   string no_touch_contract;
};

struct FP_Level19StateGateReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool ledger_written;
   bool ledger_skipped_duplicate_bar;
   int panel_objects_created;
   int panel_object_errors;
   int panel_objects_deleted;
};

void FP_ResetLevel19StateGateConfig(FP_Level19StateGateConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.export_closed_bar_ledger_csv = true;
   cfg.panel_enabled = false;
   cfg.panel_clean_on_init = false;
   cfg.panel_clean_on_deinit = true;
   cfg.print_summary = false;

   cfg.folder = FP_LEVEL19_STATE_GATE_DEFAULT_FOLDER;
   cfg.object_prefix = FP_LEVEL19_STATE_GATE_DEFAULT_PANEL_PREFIX;

   cfg.panel_corner = CORNER_RIGHT_UPPER;
   cfg.panel_x = 16;
   cfg.panel_y = 32;
   cfg.panel_width = 420;
   cfg.panel_font_size = 8;
}

void FP_ResetLevel19StateGateSnapshot(FP_Level19StateGateSnapshot &s)
{
   s.generated_at = 0;
   s.version = FP_LEVEL19_STATE_GATE_VERSION;
   s.symbol = "";
   s.period = PERIOD_CURRENT;
   s.period_label = "";

   s.bars = 0;
   s.scale_count = 0;

   s.timebase_ok = false;
   s.timebase_status = "not_available";
   s.timebase_reason = "not_available";
   s.first_bar_time = 0;
   s.last_bar_time = 0;

   s.raw_nodes_total = 0;
   s.nodes_total = 0;
   s.confirmed_nodes_total = 0;
   s.pending_nodes_total = 0;
   s.hooks_total = 0;
   s.events_total = 0;
   s.visible_events_total = 0;
   s.hidden_events_total = 0;
   s.f1_total = 0;
   s.f2_total = 0;
   s.f3_total = 0;
   s.nd_total = 0;

   s.input_events = 0;
   s.input_hooks = 0;
   s.visible_hooks_seen = 0;

   s.export_attempted = false;
   s.export_ok = false;
   s.export_files_written = 0;
   s.export_file_errors = 0;

   s.render_attempted = false;
   s.render_ok = false;
   s.render_objects_created = 0;
   s.render_object_errors = 0;
   s.render_objects_deleted = 0;
   s.render_reason = "";

   s.validation_attempted = false;
   s.validation_ok = false;
   s.validation_failed = 0;
   s.validation_warned = 0;

   s.latest_visible_event_id = "NO_VISIBLE_EVENT";
   s.latest_visible_event_level = -1;
   s.latest_visible_event_L = -1;
   s.latest_visible_event_direction = 0;
   s.latest_visible_event_status = -1;

   s.latest_visible_hook_id = "NO_VISIBLE_HOOK";
   s.latest_visible_hook_L = -1;
   s.latest_visible_hook_direction = 0;
   s.latest_visible_hook_status = -1;
   s.latest_visible_hook_is_nd = false;
   s.latest_visible_hook_node_count = 0;

   s.state_status = "LEVEL19_STATE_GATE_RESET";
   s.state_key = "LEVEL19_STATE_GATE_KEY_RESET";
   s.no_touch_contract = "READ_ONLY_NO_RENDERER_MUTATION_NO_F_HOOK_NODE_LINE_CHANGES";
}

void FP_ResetLevel19StateGateReport(FP_Level19StateGateReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.ledger_written = false;
   r.ledger_skipped_duplicate_bar = false;
   r.panel_objects_created = 0;
   r.panel_object_errors = 0;
   r.panel_objects_deleted = 0;
}

#endif // __FP_STATE_GATE_TYPES_MQH__
