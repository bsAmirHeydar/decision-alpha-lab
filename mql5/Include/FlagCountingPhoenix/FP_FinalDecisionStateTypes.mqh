#ifndef __FP_FINAL_DECISION_STATE_TYPES_MQH__
#define __FP_FINAL_DECISION_STATE_TYPES_MQH__
#property strict

#include "FP_NoSendContextTypes.mqh"

#define FP_CONSOLIDATION02_FINAL_DECISION_VERSION "C02.00-final-no-send-decision-state"
#define FP_CONSOLIDATION02_FINAL_DECISION_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Consolidation Patch 02 Final Decision State Types
// ----------------------------------------------------------------------------
// Contract:
// - final decision/dashboard snapshot from no-send context only
// - no new feature level
// - no CTrade
// - no OrderSend
// - no OrderCheck
// - no broker request
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Consolidation02FinalDecisionConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool write_latest_csv;

   bool require_context_ready_for_ready_state;
   bool require_lifecycle_tracked_for_ready_state;
   bool require_no_send_integrity;

   string folder;
};

struct FP_Consolidation02FinalDecisionRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool decision_ready;
   string decision_state;
   string decision_block_reason;
   string decision_key;

   string setup_state;
   string chain_stage;
   string next_action_hint;

   bool context_ready;
   string context_status;
   string context_block_reason;

   bool entry_bridge_ready;
   bool paper_intent_allowed;
   bool safety_gate_passed;
   bool dry_run_request_built;
   bool validator_passed;
   bool audit_passed;
   bool adapter_registered;
   bool lifecycle_tracked;

   string request_id;
   string request_key;
   string virtual_ticket;
   string request_direction;
   double entry_price;
   double stop_price;
   double target_price;
   double request_volume;

   string lifecycle_status;
   string lifecycle_block_reason;
   string paper_order_state;
   double realized_r_like;

   string blocker_layer;
   string blocker_status;
   string blocker_reason;

   bool no_send_integrity_ok;
   string no_send_contract;
   string no_touch_contract;
   string execution_status;
};

struct FP_Consolidation02FinalDecisionReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool latest_written;
};

void FP_ResetConsolidation02FinalDecisionConfig(FP_Consolidation02FinalDecisionConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.write_latest_csv = true;

   cfg.require_context_ready_for_ready_state = true;
   cfg.require_lifecycle_tracked_for_ready_state = false;
   cfg.require_no_send_integrity = true;

   cfg.folder = FP_CONSOLIDATION02_FINAL_DECISION_DEFAULT_FOLDER;
}

void FP_ResetConsolidation02FinalDecisionRow(FP_Consolidation02FinalDecisionRow &r)
{
   r.generated_at = 0;
   r.version = FP_CONSOLIDATION02_FINAL_DECISION_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.decision_ready = false;
   r.decision_state = "FINAL_DECISION_RESET";
   r.decision_block_reason = "RESET";
   r.decision_key = "";

   r.setup_state = "SETUP_UNKNOWN";
   r.chain_stage = "CHAIN_UNKNOWN";
   r.next_action_hint = "NO_ACTION";

   r.context_ready = false;
   r.context_status = "";
   r.context_block_reason = "";

   r.entry_bridge_ready = false;
   r.paper_intent_allowed = false;
   r.safety_gate_passed = false;
   r.dry_run_request_built = false;
   r.validator_passed = false;
   r.audit_passed = false;
   r.adapter_registered = false;
   r.lifecycle_tracked = false;

   r.request_id = "";
   r.request_key = "";
   r.virtual_ticket = "";
   r.request_direction = "";
   r.entry_price = 0.0;
   r.stop_price = 0.0;
   r.target_price = 0.0;
   r.request_volume = 0.0;

   r.lifecycle_status = "";
   r.lifecycle_block_reason = "";
   r.paper_order_state = "";
   r.realized_r_like = 0.0;

   r.blocker_layer = "NONE";
   r.blocker_status = "none";
   r.blocker_reason = "none";

   r.no_send_integrity_ok = true;
   r.no_send_contract = "FINAL_DECISION_CONTEXT_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE";
   r.no_touch_contract = "FINAL_DECISION_CONTEXT_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_CONSOLIDATION02_FINAL_DECISION_ONLY";
}

void FP_ResetConsolidation02FinalDecisionReport(FP_Consolidation02FinalDecisionReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.latest_written = false;
}

#endif // __FP_FINAL_DECISION_STATE_TYPES_MQH__
