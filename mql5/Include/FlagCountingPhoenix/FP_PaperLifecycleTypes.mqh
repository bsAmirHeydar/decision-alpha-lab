#ifndef __FP_PAPER_LIFECYCLE_TYPES_MQH__
#define __FP_PAPER_LIFECYCLE_TYPES_MQH__
#property strict

#include "FP_PaperIntentTypes.mqh"

#define FP_LEVEL22_PAPER_LIFECYCLE_VERSION "22.00-paper-lifecycle-close-only"
#define FP_LEVEL22_PAPER_LIFECYCLE_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 22 Paper Lifecycle Types
// ----------------------------------------------------------------------------
// Contract:
// - close-only paper lifecycle reconstruction
// - no order
// - no broker request
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Level22PaperLifecycleConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool require_intent_allowed;

   int default_expiry_bars;
   string folder;
};

struct FP_Level22PaperLifecycleRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool tracked;
   string lifecycle_status;
   string block_reason;
   string lifecycle_id;
   string lifecycle_key;

   string intent_id;
   string intent_status;
   bool intent_allowed;

   int direction;
   string direction_label;

   double entry_price;
   double stop_price;
   double target_price;
   double risk_distance;
   double reward_distance;
   double rr_like;

   datetime seed_time;
   datetime entry_time;
   datetime exit_time;

   int seed_index;
   int entry_index;
   int exit_index;
   int bars_elapsed;
   int expiry_bars;

   double entry_close;
   double exit_close;
   double best_close;
   double worst_close;
   double mfe_close_distance;
   double mae_close_distance;
   double realized_r_like;

   string entry_condition;
   string exit_condition;
   string close_only_path_status;
   string ambiguity_status;

   string no_touch_contract;
   string execution_status;
};

struct FP_Level22PaperLifecycleReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool lifecycle_written;
};

void FP_ResetLevel22PaperLifecycleConfig(FP_Level22PaperLifecycleConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.require_intent_allowed = true;
   cfg.default_expiry_bars = 20;
   cfg.folder = FP_LEVEL22_PAPER_LIFECYCLE_DEFAULT_FOLDER;
}

void FP_ResetLevel22PaperLifecycleRow(FP_Level22PaperLifecycleRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL22_PAPER_LIFECYCLE_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.tracked = false;
   r.lifecycle_status = "PAPER_LIFECYCLE_RESET";
   r.block_reason = "RESET";
   r.lifecycle_id = "";
   r.lifecycle_key = "";

   r.intent_id = "";
   r.intent_status = "";
   r.intent_allowed = false;

   r.direction = FP_DIR_NONE;
   r.direction_label = "DIRECTION_NONE";

   r.entry_price = 0.0;
   r.stop_price = 0.0;
   r.target_price = 0.0;
   r.risk_distance = 0.0;
   r.reward_distance = 0.0;
   r.rr_like = 0.0;

   r.seed_time = 0;
   r.entry_time = 0;
   r.exit_time = 0;

   r.seed_index = -1;
   r.entry_index = -1;
   r.exit_index = -1;
   r.bars_elapsed = 0;
   r.expiry_bars = 20;

   r.entry_close = 0.0;
   r.exit_close = 0.0;
   r.best_close = 0.0;
   r.worst_close = 0.0;
   r.mfe_close_distance = 0.0;
   r.mae_close_distance = 0.0;
   r.realized_r_like = 0.0;

   r.entry_condition = "ENTRY_NOT_EVALUATED";
   r.exit_condition = "EXIT_NOT_EVALUATED";
   r.close_only_path_status = "CLOSE_ONLY_PATH_NOT_EVALUATED";
   r.ambiguity_status = "AMBIGUITY_NONE";

   r.no_touch_contract = "PAPER_LIFECYCLE_CLOSE_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL22_PAPER_LIFECYCLE_ONLY";
}

void FP_ResetLevel22PaperLifecycleReport(FP_Level22PaperLifecycleReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.lifecycle_written = false;
}

#endif // __FP_PAPER_LIFECYCLE_TYPES_MQH__
