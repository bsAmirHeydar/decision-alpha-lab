#ifndef __FP_PAPER_BROKER_LIFECYCLE_TYPES_MQH__
#define __FP_PAPER_BROKER_LIFECYCLE_TYPES_MQH__
#property strict

#include "FP_PaperBrokerAdapterTypes.mqh"

#define FP_LEVEL30_PAPER_BROKER_LIFECYCLE_VERSION "30.00-paper-broker-lifecycle-no-send"
#define FP_LEVEL30_PAPER_BROKER_LIFECYCLE_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 30 Paper Broker Lifecycle Types
// ----------------------------------------------------------------------------
// Contract:
// - internal paper-broker lifecycle only
// - CSV only
// - no CTrade
// - no OrderSend
// - no OrderCheck
// - no broker request
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Level30PaperBrokerLifecycleConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool append_lifecycle_csv;
   bool write_latest_csv;
   bool skip_duplicate_lifecycle_key;

   bool require_adapter_registered;
   bool require_zero_volume;
   bool close_only;
   int expiry_bars;

   string folder;
};

struct FP_Level30PaperBrokerLifecycleRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool lifecycle_tracked;
   bool lifecycle_written;
   bool latest_written;
   bool duplicate_skipped;

   string lifecycle_status;
   string lifecycle_block_reason;
   string lifecycle_id;
   string lifecycle_key;

   string virtual_ticket;
   int lifecycle_sequence;
   string adapter_status;
   bool adapter_registered;
   string adapter_block_reason;

   string request_id;
   string request_key;
   string request_order_type;
   string request_direction;
   double request_volume;
   double request_price;
   double request_sl;
   double request_tp;

   int seed_index;
   int entry_index;
   int exit_index;
   datetime seed_time;
   datetime entry_time;
   datetime exit_time;

   int expiry_bars;
   int bars_to_entry;
   int bars_in_trade;
   int bars_elapsed_total;

   double entry_close;
   double exit_close;
   double best_close;
   double worst_close;
   double mfe_close_distance;
   double mae_close_distance;
   double risk_distance;
   double reward_distance;
   double realized_r_like;

   string entry_condition;
   string exit_condition;
   string paper_order_state;
   string paper_order_event;
   string close_only_contract;

   string no_send_contract;
   string no_touch_contract;
   string execution_status;
};

struct FP_Level30PaperBrokerLifecycleReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool lifecycle_written;
   bool latest_written;
   bool duplicate_skipped;
};

void FP_ResetLevel30PaperBrokerLifecycleConfig(FP_Level30PaperBrokerLifecycleConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.append_lifecycle_csv = true;
   cfg.write_latest_csv = true;
   cfg.skip_duplicate_lifecycle_key = true;

   cfg.require_adapter_registered = true;
   cfg.require_zero_volume = true;
   cfg.close_only = true;
   cfg.expiry_bars = 20;

   cfg.folder = FP_LEVEL30_PAPER_BROKER_LIFECYCLE_DEFAULT_FOLDER;
}

void FP_ResetLevel30PaperBrokerLifecycleRow(FP_Level30PaperBrokerLifecycleRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL30_PAPER_BROKER_LIFECYCLE_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.lifecycle_tracked = false;
   r.lifecycle_written = false;
   r.latest_written = false;
   r.duplicate_skipped = false;

   r.lifecycle_status = "PAPER_BROKER_LIFECYCLE_RESET";
   r.lifecycle_block_reason = "RESET";
   r.lifecycle_id = "";
   r.lifecycle_key = "";

   r.virtual_ticket = "";
   r.lifecycle_sequence = 0;
   r.adapter_status = "";
   r.adapter_registered = false;
   r.adapter_block_reason = "";

   r.request_id = "";
   r.request_key = "";
   r.request_order_type = "ORDER_TYPE_NONE";
   r.request_direction = "DIRECTION_NONE";
   r.request_volume = 0.0;
   r.request_price = 0.0;
   r.request_sl = 0.0;
   r.request_tp = 0.0;

   r.seed_index = -1;
   r.entry_index = -1;
   r.exit_index = -1;
   r.seed_time = 0;
   r.entry_time = 0;
   r.exit_time = 0;

   r.expiry_bars = 20;
   r.bars_to_entry = 0;
   r.bars_in_trade = 0;
   r.bars_elapsed_total = 0;

   r.entry_close = 0.0;
   r.exit_close = 0.0;
   r.best_close = 0.0;
   r.worst_close = 0.0;
   r.mfe_close_distance = 0.0;
   r.mae_close_distance = 0.0;
   r.risk_distance = 0.0;
   r.reward_distance = 0.0;
   r.realized_r_like = 0.0;

   r.entry_condition = "PAPER_BROKER_ENTRY_NOT_EVALUATED";
   r.exit_condition = "PAPER_BROKER_EXIT_NOT_EVALUATED";
   r.paper_order_state = "PAPER_BROKER_STATE_NONE";
   r.paper_order_event = "PAPER_BROKER_EVENT_NONE";
   r.close_only_contract = "CLOSE_ONLY_PAPER_BROKER_LIFECYCLE";

   r.no_send_contract = "PAPER_BROKER_LIFECYCLE_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE";
   r.no_touch_contract = "PAPER_BROKER_LIFECYCLE_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL30_PAPER_BROKER_LIFECYCLE_ONLY";
}

void FP_ResetLevel30PaperBrokerLifecycleReport(FP_Level30PaperBrokerLifecycleReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.lifecycle_written = false;
   r.latest_written = false;
   r.duplicate_skipped = false;
}

#endif // __FP_PAPER_BROKER_LIFECYCLE_TYPES_MQH__
