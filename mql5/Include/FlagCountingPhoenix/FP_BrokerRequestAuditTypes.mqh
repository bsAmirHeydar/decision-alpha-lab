#ifndef __FP_BROKER_REQUEST_AUDIT_TYPES_MQH__
#define __FP_BROKER_REQUEST_AUDIT_TYPES_MQH__
#property strict

#include "FP_BrokerRequestLedgerTypes.mqh"
#include "FP_BrokerValidatorTypes.mqh"
#include "FP_BrokerDryRunTypes.mqh"

#define FP_LEVEL28_BROKER_REQUEST_AUDIT_VERSION "28.00-broker-request-audit-no-send"
#define FP_LEVEL28_BROKER_REQUEST_AUDIT_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 28 Broker Request Audit Types
// ----------------------------------------------------------------------------
// Contract:
// - audit broker request preview chain only
// - CSV only
// - no CTrade
// - no OrderSend
// - no OrderCheck
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Level28BrokerRequestAuditConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool append_audit_csv;
   bool write_latest_csv;
   bool skip_duplicate_audit_key;

   bool require_dry_run_only;
   bool require_zero_volume;
   bool require_no_send_contract;
   bool require_request_validator_coherence;
   bool require_safety_intent_coherence;

   string folder;
};

struct FP_Level28BrokerRequestAuditRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool audit_passed;
   bool audit_written;
   bool latest_written;
   bool duplicate_skipped;

   string audit_status;
   string audit_block_reason;
   string audit_id;
   string audit_key;

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

   bool safety_gate_passed;
   string safety_gate_status;
   string safety_gate_block_reason;

   bool intent_allowed;
   string intent_id;
   string intent_status;

   string request_order_type;
   string request_direction;
   double request_volume;
   double request_price;
   double request_sl;
   double request_tp;

   bool dry_run_only_ok;
   bool zero_volume_ok;
   bool no_send_contract_ok;
   bool request_validator_coherence_ok;
   bool safety_intent_coherence_ok;
   bool ledger_runtime_seen;

   int ledger_sequence_current;
   string ledger_last_request_key;

   string validator_readiness;
   string request_chain_state;
   string no_send_contract;
   string no_touch_contract;
   string execution_status;
};

struct FP_Level28BrokerRequestAuditReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool audit_written;
   bool latest_written;
   bool duplicate_skipped;
};

void FP_ResetLevel28BrokerRequestAuditConfig(FP_Level28BrokerRequestAuditConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.append_audit_csv = true;
   cfg.write_latest_csv = true;
   cfg.skip_duplicate_audit_key = true;

   cfg.require_dry_run_only = true;
   cfg.require_zero_volume = true;
   cfg.require_no_send_contract = true;
   cfg.require_request_validator_coherence = true;
   cfg.require_safety_intent_coherence = true;

   cfg.folder = FP_LEVEL28_BROKER_REQUEST_AUDIT_DEFAULT_FOLDER;
}

void FP_ResetLevel28BrokerRequestAuditRow(FP_Level28BrokerRequestAuditRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL28_BROKER_REQUEST_AUDIT_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.audit_passed = false;
   r.audit_written = false;
   r.latest_written = false;
   r.duplicate_skipped = false;

   r.audit_status = "BROKER_REQUEST_AUDIT_RESET";
   r.audit_block_reason = "RESET";
   r.audit_id = "";
   r.audit_key = "";

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

   r.safety_gate_passed = false;
   r.safety_gate_status = "";
   r.safety_gate_block_reason = "";

   r.intent_allowed = false;
   r.intent_id = "";
   r.intent_status = "";

   r.request_order_type = "ORDER_TYPE_NONE";
   r.request_direction = "DIRECTION_NONE";
   r.request_volume = 0.0;
   r.request_price = 0.0;
   r.request_sl = 0.0;
   r.request_tp = 0.0;

   r.dry_run_only_ok = false;
   r.zero_volume_ok = false;
   r.no_send_contract_ok = false;
   r.request_validator_coherence_ok = false;
   r.safety_intent_coherence_ok = false;
   r.ledger_runtime_seen = false;

   r.ledger_sequence_current = 0;
   r.ledger_last_request_key = "";

   r.validator_readiness = "VALIDATOR_READINESS_UNKNOWN";
   r.request_chain_state = "REQUEST_CHAIN_UNKNOWN";
   r.no_send_contract = "AUDIT_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE";
   r.no_touch_contract = "BROKER_REQUEST_AUDIT_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL28_BROKER_REQUEST_AUDIT_ONLY";
}

void FP_ResetLevel28BrokerRequestAuditReport(FP_Level28BrokerRequestAuditReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.audit_written = false;
   r.latest_written = false;
   r.duplicate_skipped = false;
}

#endif // __FP_BROKER_REQUEST_AUDIT_TYPES_MQH__
