#ifndef __FP_ENTRY_BRIDGE_TYPES_MQH__
#define __FP_ENTRY_BRIDGE_TYPES_MQH__
#property strict

#define FP_LEVEL20_ENTRY_BRIDGE_VERSION "20.00-entry-bridge-xy-anchor-join"
#define FP_LEVEL20_ENTRY_BRIDGE_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 20 Entry Bridge Types
// ----------------------------------------------------------------------------
// Contract:
// - research / diagnostic only
// - no order
// - no broker request
// - no renderer mutation
// - no chart-object mutation
// - no F / Hook / Node logic mutation
// ============================================================================

struct FP_Level20EntryBridgeConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool prefer_latest_visible_event;
   bool allow_hook_fallback;

   double min_rr;
   string folder;
};

struct FP_Level20EntryBridgeRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool ready;
   string readiness_status;
   string block_reason;
   string bridge_status;
   string bridge_key;

   string source_kind;
   string source_id;
   int source_level;
   int source_L;
   int direction;

   string y_state_label;
   string y_context_label;

   string entry_anchor_kind;
   datetime entry_anchor_time;
   double entry_anchor_price;
   int entry_anchor_node_id;
   string entry_anchor_id;

   string invalidation_anchor_kind;
   datetime invalidation_anchor_time;
   double invalidation_anchor_price;
   int invalidation_anchor_node_id;
   string invalidation_anchor_id;

   string destination_anchor_kind;
   datetime destination_anchor_time;
   double destination_anchor_price;
   int destination_anchor_node_id;
   string destination_anchor_id;

   double current_close;
   double risk_distance;
   double reward_distance;
   double rr_like;
   double min_rr_required;

   bool timebase_ok;
   bool render_health_ok;
   bool validation_health_ok;

   string no_touch_contract;
   string execution_status;
};

struct FP_Level20EntryBridgeReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool bridge_written;
};

void FP_ResetLevel20EntryBridgeConfig(FP_Level20EntryBridgeConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.prefer_latest_visible_event = true;
   cfg.allow_hook_fallback = true;

   cfg.min_rr = 1.0;
   cfg.folder = FP_LEVEL20_ENTRY_BRIDGE_DEFAULT_FOLDER;
}

void FP_ResetLevel20EntryBridgeRow(FP_Level20EntryBridgeRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL20_ENTRY_BRIDGE_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.ready = false;
   r.readiness_status = "ENTRY_BRIDGE_RESET";
   r.block_reason = "RESET";
   r.bridge_status = "LEVEL20_ENTRY_BRIDGE_RESET";
   r.bridge_key = "LEVEL20_ENTRY_BRIDGE_KEY_RESET";

   r.source_kind = "NONE";
   r.source_id = "";
   r.source_level = 0;
   r.source_L = 0;
   r.direction = FP_DIR_NONE;

   r.y_state_label = "Y_STATE_UNKNOWN";
   r.y_context_label = "Y_CONTEXT_UNKNOWN";

   r.entry_anchor_kind = "ENTRY_ANCHOR_NONE";
   r.entry_anchor_time = 0;
   r.entry_anchor_price = 0.0;
   r.entry_anchor_node_id = -1;
   r.entry_anchor_id = "";

   r.invalidation_anchor_kind = "INVALIDATION_ANCHOR_NONE";
   r.invalidation_anchor_time = 0;
   r.invalidation_anchor_price = 0.0;
   r.invalidation_anchor_node_id = -1;
   r.invalidation_anchor_id = "";

   r.destination_anchor_kind = "DESTINATION_ANCHOR_NONE";
   r.destination_anchor_time = 0;
   r.destination_anchor_price = 0.0;
   r.destination_anchor_node_id = -1;
   r.destination_anchor_id = "";

   r.current_close = 0.0;
   r.risk_distance = 0.0;
   r.reward_distance = 0.0;
   r.rr_like = 0.0;
   r.min_rr_required = 1.0;

   r.timebase_ok = false;
   r.render_health_ok = false;
   r.validation_health_ok = false;

   r.no_touch_contract = "READ_ONLY_ENTRY_BRIDGE_NO_RENDERER_MUTATION_NO_ORDER";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL20_ENTRY_BRIDGE_ONLY";
}

void FP_ResetLevel20EntryBridgeReport(FP_Level20EntryBridgeReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.bridge_written = false;
}

#endif // __FP_ENTRY_BRIDGE_TYPES_MQH__
