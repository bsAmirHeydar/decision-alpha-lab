#ifndef __FP_PAPER_BROKER_ADAPTER_TYPES_MQH__
#define __FP_PAPER_BROKER_ADAPTER_TYPES_MQH__
#property strict

#include "FP_BrokerRequestAuditTypes.mqh"
#include "FP_BrokerValidatorTypes.mqh"
#include "FP_BrokerDryRunTypes.mqh"

#define FP_LEVEL29_PAPER_BROKER_ADAPTER_VERSION "29.00-paper-broker-adapter-no-send"
#define FP_LEVEL29_PAPER_BROKER_ADAPTER_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 29 Paper Broker Adapter Types
// ----------------------------------------------------------------------------
// Contract:
// - internal paper-broker adapter record only
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

struct FP_Level29PaperBrokerAdapterConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool append_adapter_csv;
   bool write_latest_csv;
   bool skip_duplicate_adapter_key;

   bool require_audit_passed;
   bool require_validator_passed;
   bool require_request_built;
   bool require_dry_run_only;
   bool require_zero_volume;
   bool adapter_dry_run_only;

   string folder;
};

struct FP_Level29PaperBrokerAdapterRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool adapter_registered;
   bool adapter_written;
   bool latest_written;
   bool duplicate_skipped;

   string adapter_status;
   string adapter_block_reason;
   string adapter_id;
   string adapter_key;

   string virtual_ticket;
   int adapter_sequence;
   string paper_order_state;
   string paper_order_lifecycle_hint;

   string request_id;
   string request_key;
   bool request_built;
   bool dry_run_only;
   string dry_run_status;

   bool validator_passed;
   string validator_status;
   string validator_block_reason;

   bool audit_passed;
   string audit_status;
   string audit_block_reason;

   string request_order_type;
   string request_direction;
   double request_volume;
   double request_price;
   double request_sl;
   double request_tp;
   long request_magic;
   string request_comment;

   bool zero_volume_ok;
   bool dry_run_only_ok;
   bool no_send_contract_ok;
   bool adapter_chain_coherence_ok;

   string adapter_runtime_state;
   string no_send_contract;
   string no_touch_contract;
   string execution_status;
};

struct FP_Level29PaperBrokerAdapterReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool adapter_written;
   bool latest_written;
   bool duplicate_skipped;
};

void FP_ResetLevel29PaperBrokerAdapterConfig(FP_Level29PaperBrokerAdapterConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.append_adapter_csv = true;
   cfg.write_latest_csv = true;
   cfg.skip_duplicate_adapter_key = true;

   cfg.require_audit_passed = true;
   cfg.require_validator_passed = true;
   cfg.require_request_built = true;
   cfg.require_dry_run_only = true;
   cfg.require_zero_volume = true;
   cfg.adapter_dry_run_only = true;

   cfg.folder = FP_LEVEL29_PAPER_BROKER_ADAPTER_DEFAULT_FOLDER;
}

void FP_ResetLevel29PaperBrokerAdapterRow(FP_Level29PaperBrokerAdapterRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL29_PAPER_BROKER_ADAPTER_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.adapter_registered = false;
   r.adapter_written = false;
   r.latest_written = false;
   r.duplicate_skipped = false;

   r.adapter_status = "PAPER_BROKER_ADAPTER_RESET";
   r.adapter_block_reason = "RESET";
   r.adapter_id = "";
   r.adapter_key = "";

   r.virtual_ticket = "";
   r.adapter_sequence = 0;
   r.paper_order_state = "PAPER_ORDER_STATE_NONE";
   r.paper_order_lifecycle_hint = "PAPER_ORDER_LIFECYCLE_NOT_STARTED";

   r.request_id = "";
   r.request_key = "";
   r.request_built = false;
   r.dry_run_only = true;
   r.dry_run_status = "";

   r.validator_passed = false;
   r.validator_status = "";
   r.validator_block_reason = "";

   r.audit_passed = false;
   r.audit_status = "";
   r.audit_block_reason = "";

   r.request_order_type = "ORDER_TYPE_NONE";
   r.request_direction = "DIRECTION_NONE";
   r.request_volume = 0.0;
   r.request_price = 0.0;
   r.request_sl = 0.0;
   r.request_tp = 0.0;
   r.request_magic = 0;
   r.request_comment = "";

   r.zero_volume_ok = false;
   r.dry_run_only_ok = false;
   r.no_send_contract_ok = false;
   r.adapter_chain_coherence_ok = false;

   r.adapter_runtime_state = "ADAPTER_RUNTIME_IDLE";
   r.no_send_contract = "PAPER_BROKER_ADAPTER_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE";
   r.no_touch_contract = "PAPER_BROKER_ADAPTER_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL29_PAPER_BROKER_ADAPTER_ONLY";
}

void FP_ResetLevel29PaperBrokerAdapterReport(FP_Level29PaperBrokerAdapterReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.adapter_written = false;
   r.latest_written = false;
   r.duplicate_skipped = false;
}

#endif // __FP_PAPER_BROKER_ADAPTER_TYPES_MQH__
