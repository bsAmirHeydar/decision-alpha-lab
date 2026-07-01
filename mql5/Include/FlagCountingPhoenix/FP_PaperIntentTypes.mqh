#ifndef __FP_PAPER_INTENT_TYPES_MQH__
#define __FP_PAPER_INTENT_TYPES_MQH__
#property strict

#include "FP_EntryBridgeTypes.mqh"

#define FP_LEVEL21_PAPER_INTENT_VERSION "21.00-paper-intent-no-order"
#define FP_LEVEL21_PAPER_INTENT_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 21 Paper Intent Types
// ----------------------------------------------------------------------------
// Contract:
// - paper intent only
// - no order
// - no broker request
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Level21PaperIntentConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool require_entry_bridge_ready;
   bool require_directional_geometry;

   int expiry_bars;
   string folder;
};

struct FP_Level21PaperIntentRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool allowed;
   string intent_status;
   string block_reason;
   string intent_id;
   string intent_key;

   string source_bridge_key;
   string source_kind;
   string source_id;
   int source_level;
   int source_L;

   int direction;
   string direction_label;

   double entry_price;
   double stop_price;
   double target_price;
   double risk_distance;
   double reward_distance;
   double rr_like;

   datetime entry_anchor_time;
   datetime stop_anchor_time;
   datetime target_anchor_time;

   string entry_anchor_id;
   string stop_anchor_id;
   string target_anchor_id;

   string entry_anchor_kind;
   string stop_anchor_kind;
   string target_anchor_kind;

   string geometry_status;
   string lifecycle_seed_status;
   int expiry_bars;

   string no_touch_contract;
   string execution_status;
};

struct FP_Level21PaperIntentReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool intent_written;
};

void FP_ResetLevel21PaperIntentConfig(FP_Level21PaperIntentConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.require_entry_bridge_ready = true;
   cfg.require_directional_geometry = true;
   cfg.expiry_bars = 20;
   cfg.folder = FP_LEVEL21_PAPER_INTENT_DEFAULT_FOLDER;
}

void FP_ResetLevel21PaperIntentRow(FP_Level21PaperIntentRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL21_PAPER_INTENT_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.allowed = false;
   r.intent_status = "PAPER_INTENT_RESET";
   r.block_reason = "RESET";
   r.intent_id = "";
   r.intent_key = "";

   r.source_bridge_key = "";
   r.source_kind = "NONE";
   r.source_id = "";
   r.source_level = 0;
   r.source_L = 0;

   r.direction = FP_DIR_NONE;
   r.direction_label = "DIRECTION_NONE";

   r.entry_price = 0.0;
   r.stop_price = 0.0;
   r.target_price = 0.0;
   r.risk_distance = 0.0;
   r.reward_distance = 0.0;
   r.rr_like = 0.0;

   r.entry_anchor_time = 0;
   r.stop_anchor_time = 0;
   r.target_anchor_time = 0;

   r.entry_anchor_id = "";
   r.stop_anchor_id = "";
   r.target_anchor_id = "";

   r.entry_anchor_kind = "";
   r.stop_anchor_kind = "";
   r.target_anchor_kind = "";

   r.geometry_status = "GEOMETRY_NOT_EVALUATED";
   r.lifecycle_seed_status = "PAPER_INTENT_SEED_ONLY";
   r.expiry_bars = 20;

   r.no_touch_contract = "PAPER_INTENT_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL21_PAPER_INTENT_ONLY";
}

void FP_ResetLevel21PaperIntentReport(FP_Level21PaperIntentReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.intent_written = false;
}

#endif // __FP_PAPER_INTENT_TYPES_MQH__
