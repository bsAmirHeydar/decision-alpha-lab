#ifndef __FP_NO_SEND_CONTEXT_TYPES_MQH__
#define __FP_NO_SEND_CONTEXT_TYPES_MQH__
#property strict

#define FP_CONSOLIDATION01_NO_SEND_CONTEXT_VERSION "C01.00-no-send-context"
#define FP_CONSOLIDATION01_NO_SEND_CONTEXT_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Consolidation Patch 01 No-Send Context Types
// ----------------------------------------------------------------------------
// Contract:
// - no new trading feature level
// - latest-row consolidation snapshot only
// - no CTrade
// - no OrderSend
// - no OrderCheck
// - no broker request
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Consolidation01NoSendContextConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool write_latest_csv;
   string folder;
};

struct FP_Consolidation01NoSendContextRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool context_ready;
   string context_status;
   string context_block_reason;
   string context_key;

   bool has_entry_bridge;
   bool has_paper_intent;
   bool has_safety_gate;
   bool has_dry_run;
   bool has_validator;
   bool has_ledger;
   bool has_audit;
   bool has_adapter;
   bool has_lifecycle;

   bool entry_bridge_ready;
   string entry_bridge_status;

   bool paper_intent_allowed;
   string paper_intent_status;

   bool safety_gate_passed;
   string safety_gate_status;
   string safety_gate_block_reason;

   bool dry_run_request_built;
   string dry_run_status;
   string request_id;
   string request_key;

   bool validator_passed;
   string validator_status;
   string validator_block_reason;

   bool audit_passed;
   string audit_status;
   string audit_block_reason;

   bool adapter_registered;
   string adapter_status;
   string adapter_block_reason;
   string virtual_ticket;

   bool lifecycle_tracked;
   string lifecycle_status;
   string lifecycle_block_reason;
   string paper_order_state;
   double realized_r_like;

   string request_direction;
   double request_price;
   double request_sl;
   double request_tp;
   double request_volume;

   string no_send_contract;
   string no_touch_contract;
   string execution_status;
};

struct FP_Consolidation01NoSendContextReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool latest_written;
};

void FP_ResetConsolidation01NoSendContextConfig(FP_Consolidation01NoSendContextConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.write_latest_csv = true;
   cfg.folder = FP_CONSOLIDATION01_NO_SEND_CONTEXT_DEFAULT_FOLDER;
}

void FP_ResetConsolidation01NoSendContextRow(FP_Consolidation01NoSendContextRow &r)
{
   r.generated_at = 0;
   r.version = FP_CONSOLIDATION01_NO_SEND_CONTEXT_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.context_ready = false;
   r.context_status = "NO_SEND_CONTEXT_RESET";
   r.context_block_reason = "RESET";
   r.context_key = "";

   r.has_entry_bridge = false;
   r.has_paper_intent = false;
   r.has_safety_gate = false;
   r.has_dry_run = false;
   r.has_validator = false;
   r.has_ledger = false;
   r.has_audit = false;
   r.has_adapter = false;
   r.has_lifecycle = false;

   r.entry_bridge_ready = false;
   r.entry_bridge_status = "";

   r.paper_intent_allowed = false;
   r.paper_intent_status = "";

   r.safety_gate_passed = false;
   r.safety_gate_status = "";
   r.safety_gate_block_reason = "";

   r.dry_run_request_built = false;
   r.dry_run_status = "";
   r.request_id = "";
   r.request_key = "";

   r.validator_passed = false;
   r.validator_status = "";
   r.validator_block_reason = "";

   r.audit_passed = false;
   r.audit_status = "";
   r.audit_block_reason = "";

   r.adapter_registered = false;
   r.adapter_status = "";
   r.adapter_block_reason = "";
   r.virtual_ticket = "";

   r.lifecycle_tracked = false;
   r.lifecycle_status = "";
   r.lifecycle_block_reason = "";
   r.paper_order_state = "";
   r.realized_r_like = 0.0;

   r.request_direction = "";
   r.request_price = 0.0;
   r.request_sl = 0.0;
   r.request_tp = 0.0;
   r.request_volume = 0.0;

   r.no_send_contract = "CONSOLIDATION01_CONTEXT_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE";
   r.no_touch_contract = "CONSOLIDATION01_CONTEXT_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_CONSOLIDATION01_CONTEXT_ONLY";
}

void FP_ResetConsolidation01NoSendContextReport(FP_Consolidation01NoSendContextReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.latest_written = false;
}

#endif // __FP_NO_SEND_CONTEXT_TYPES_MQH__
