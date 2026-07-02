#ifndef __FP_FINAL_CSV_NORMALIZATION_TYPES_MQH__
#define __FP_FINAL_CSV_NORMALIZATION_TYPES_MQH__
#property strict

#include "FP_FinalDecisionStateTypes.mqh"

#define FP_CONSOLIDATION04_FINAL_CSV_NORMALIZATION_VERSION "C04.00-final-csv-normalization"
#define FP_CONSOLIDATION04_FINAL_CSV_SCHEMA_VERSION "final-no-send-v1"
#define FP_CONSOLIDATION04_FINAL_CSV_NORMALIZATION_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Consolidation Patch 04 Final CSV Normalization Types
// ----------------------------------------------------------------------------
// Contract:
// - machine-friendly CSV snapshot from final no-send decision only
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

struct FP_Consolidation04FinalCsvNormalizationConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool write_latest_csv;
   bool require_no_send_integrity;
   string folder;
};

struct FP_Consolidation04FinalCsvNormalizationRow
{
   datetime generated_at;
   string version;
   string schema_version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   int attempted_i;
   int decision_ready_i;
   int context_ready_i;
   int no_send_integrity_i;

   int entry_bridge_ready_i;
   int paper_intent_allowed_i;
   int safety_gate_passed_i;
   int dry_run_request_built_i;
   int validator_passed_i;
   int audit_passed_i;
   int adapter_registered_i;
   int lifecycle_tracked_i;

   string decision_state;
   string decision_block_reason;
   string setup_state;
   string chain_stage;
   string next_action_hint;
   string blocker_layer;
   string blocker_reason;

   string request_id;
   string request_key;
   string virtual_ticket;

   string direction_label;
   int direction_sign;

   double entry_price;
   double stop_price;
   double target_price;
   double request_volume;
   double risk_distance;
   double reward_distance;
   double rr_like;

   string lifecycle_status;
   string paper_order_state;
   double realized_r_like;

   string normalized_quality_status;
   string normalized_block_reason;
   string no_send_contract;
   string no_touch_contract;
   string execution_status;
};

struct FP_Consolidation04FinalCsvNormalizationReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool latest_written;
};

void FP_ResetConsolidation04FinalCsvNormalizationConfig(FP_Consolidation04FinalCsvNormalizationConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.write_latest_csv = true;
   cfg.require_no_send_integrity = true;
   cfg.folder = FP_CONSOLIDATION04_FINAL_CSV_NORMALIZATION_DEFAULT_FOLDER;
}

void FP_ResetConsolidation04FinalCsvNormalizationRow(FP_Consolidation04FinalCsvNormalizationRow &r)
{
   r.generated_at = 0;
   r.version = FP_CONSOLIDATION04_FINAL_CSV_NORMALIZATION_VERSION;
   r.schema_version = FP_CONSOLIDATION04_FINAL_CSV_SCHEMA_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted_i = 0;
   r.decision_ready_i = 0;
   r.context_ready_i = 0;
   r.no_send_integrity_i = 0;

   r.entry_bridge_ready_i = 0;
   r.paper_intent_allowed_i = 0;
   r.safety_gate_passed_i = 0;
   r.dry_run_request_built_i = 0;
   r.validator_passed_i = 0;
   r.audit_passed_i = 0;
   r.adapter_registered_i = 0;
   r.lifecycle_tracked_i = 0;

   r.decision_state = "";
   r.decision_block_reason = "";
   r.setup_state = "";
   r.chain_stage = "";
   r.next_action_hint = "";
   r.blocker_layer = "";
   r.blocker_reason = "";

   r.request_id = "";
   r.request_key = "";
   r.virtual_ticket = "";

   r.direction_label = "";
   r.direction_sign = 0;

   r.entry_price = 0.0;
   r.stop_price = 0.0;
   r.target_price = 0.0;
   r.request_volume = 0.0;
   r.risk_distance = 0.0;
   r.reward_distance = 0.0;
   r.rr_like = 0.0;

   r.lifecycle_status = "";
   r.paper_order_state = "";
   r.realized_r_like = 0.0;

   r.normalized_quality_status = "FINAL_CSV_NORMALIZATION_RESET";
   r.normalized_block_reason = "RESET";
   r.no_send_contract = "FINAL_CSV_NORMALIZATION_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE";
   r.no_touch_contract = "FINAL_CSV_NORMALIZATION_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_CONSOLIDATION04_FINAL_CSV_NORMALIZATION_ONLY";
}

void FP_ResetConsolidation04FinalCsvNormalizationReport(FP_Consolidation04FinalCsvNormalizationReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.latest_written = false;
}

#endif // __FP_FINAL_CSV_NORMALIZATION_TYPES_MQH__
