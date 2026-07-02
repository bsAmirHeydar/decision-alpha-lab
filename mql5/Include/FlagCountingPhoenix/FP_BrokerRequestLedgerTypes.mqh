#ifndef __FP_BROKER_REQUEST_LEDGER_TYPES_MQH__
#define __FP_BROKER_REQUEST_LEDGER_TYPES_MQH__
#property strict

#include "FP_BrokerValidatorTypes.mqh"
#include "FP_BrokerDryRunTypes.mqh"

#define FP_LEVEL27_BROKER_REQUEST_LEDGER_VERSION "27.00-broker-request-ledger-no-send"
#define FP_LEVEL27_BROKER_REQUEST_LEDGER_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 27 Broker Request Ledger Types
// ----------------------------------------------------------------------------
// Contract:
// - append-only broker request preview ledger
// - no CTrade
// - no OrderSend
// - no OrderCheck
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Level27BrokerRequestLedgerConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool append_ledger_csv;
   bool write_latest_csv;
   bool skip_duplicate_request_key;

   string folder;
};

struct FP_Level27BrokerRequestLedgerRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool ledger_written;
   bool latest_written;
   bool duplicate_skipped;

   string ledger_status;
   string ledger_reason;
   string ledger_id;
   string ledger_key;

   string request_id;
   string request_key;
   bool request_built;
   bool dry_run_only;
   string dry_run_status;
   string dry_run_block_reason;

   bool validator_passed;
   string validator_status;
   string validator_block_reason;
   string validator_key;

   string safety_gate_status;
   bool safety_gate_passed;
   string safety_gate_block_reason;

   string intent_id;
   bool intent_allowed;
   string intent_status;

   string request_order_type;
   string request_direction;
   double request_volume;
   double request_price;
   double request_sl;
   double request_tp;
   long request_magic;
   string request_comment;

   bool price_normalized;
   bool sl_normalized;
   bool tp_normalized;
   bool price_tick_aligned;
   bool sl_tick_aligned;
   bool tp_tick_aligned;
   bool stop_distance_ok;
   bool target_distance_ok;
   bool zero_volume_ok;
   bool price_geometry_ok;

   int ledger_sequence;
   string no_send_contract;
   string no_touch_contract;
   string execution_status;
};

struct FP_Level27BrokerRequestLedgerReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool ledger_written;
   bool latest_written;
   bool duplicate_skipped;
};

void FP_ResetLevel27BrokerRequestLedgerConfig(FP_Level27BrokerRequestLedgerConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.append_ledger_csv = true;
   cfg.write_latest_csv = true;
   cfg.skip_duplicate_request_key = true;

   cfg.folder = FP_LEVEL27_BROKER_REQUEST_LEDGER_DEFAULT_FOLDER;
}

void FP_ResetLevel27BrokerRequestLedgerRow(FP_Level27BrokerRequestLedgerRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL27_BROKER_REQUEST_LEDGER_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.ledger_written = false;
   r.latest_written = false;
   r.duplicate_skipped = false;

   r.ledger_status = "BROKER_REQUEST_LEDGER_RESET";
   r.ledger_reason = "RESET";
   r.ledger_id = "";
   r.ledger_key = "";

   r.request_id = "";
   r.request_key = "";
   r.request_built = false;
   r.dry_run_only = true;
   r.dry_run_status = "";
   r.dry_run_block_reason = "";

   r.validator_passed = false;
   r.validator_status = "";
   r.validator_block_reason = "";
   r.validator_key = "";

   r.safety_gate_status = "";
   r.safety_gate_passed = false;
   r.safety_gate_block_reason = "";

   r.intent_id = "";
   r.intent_allowed = false;
   r.intent_status = "";

   r.request_order_type = "ORDER_TYPE_NONE";
   r.request_direction = "DIRECTION_NONE";
   r.request_volume = 0.0;
   r.request_price = 0.0;
   r.request_sl = 0.0;
   r.request_tp = 0.0;
   r.request_magic = 0;
   r.request_comment = "";

   r.price_normalized = false;
   r.sl_normalized = false;
   r.tp_normalized = false;
   r.price_tick_aligned = false;
   r.sl_tick_aligned = false;
   r.tp_tick_aligned = false;
   r.stop_distance_ok = false;
   r.target_distance_ok = false;
   r.zero_volume_ok = false;
   r.price_geometry_ok = false;

   r.ledger_sequence = 0;
   r.no_send_contract = "LEDGER_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE";
   r.no_touch_contract = "BROKER_REQUEST_LEDGER_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL27_BROKER_REQUEST_LEDGER_ONLY";
}

void FP_ResetLevel27BrokerRequestLedgerReport(FP_Level27BrokerRequestLedgerReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.ledger_written = false;
   r.latest_written = false;
   r.duplicate_skipped = false;
}

#endif // __FP_BROKER_REQUEST_LEDGER_TYPES_MQH__
