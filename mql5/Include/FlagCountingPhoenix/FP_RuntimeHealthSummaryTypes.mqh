#ifndef __FP_RUNTIME_HEALTH_SUMMARY_TYPES_MQH__
#define __FP_RUNTIME_HEALTH_SUMMARY_TYPES_MQH__
#property strict

#include "FP_FinalCsvNormalizationTypes.mqh"

#define FP_CONSOLIDATION05_RUNTIME_HEALTH_VERSION "C05.00-runtime-health-summary"
#define FP_CONSOLIDATION05_RUNTIME_HEALTH_SCHEMA_VERSION "runtime-health-v1"
#define FP_CONSOLIDATION05_RUNTIME_HEALTH_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Consolidation Patch 05 Runtime Health Summary Types
// ----------------------------------------------------------------------------
// Contract:
// - runtime health/dashboard snapshot only
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

struct FP_Consolidation05RuntimeHealthConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool write_latest_csv;

   bool require_context_ready;
   bool require_final_decision_export;
   bool require_normalized_export;
   bool require_no_send_integrity;

   string folder;
};

struct FP_Consolidation05RuntimeHealthRow
{
   datetime generated_at;
   string version;
   string schema_version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool health_ok;
   string health_status;
   string health_block_reason;
   string health_key;

   bool context_enabled;
   bool context_export_enabled;
   bool context_ready;
   string context_status;
   string context_block_reason;

   bool final_decision_enabled;
   bool final_decision_export_enabled;
   bool final_decision_ready;
   string final_decision_state;
   string final_decision_block_reason;

   bool normalized_enabled;
   bool normalized_export_enabled;
   bool normalized_ready;
   string normalized_quality_status;
   string normalized_block_reason;

   bool no_send_integrity_ok;
   bool expected_outputs_enabled;
   int expected_outputs_enabled_count;
   int expected_outputs_required_count;

   string setup_state;
   string chain_stage;
   string blocker_layer;
   string blocker_reason;
   string request_id;
   string virtual_ticket;
   string request_direction;
   double entry_price;
   double stop_price;
   double target_price;
   double request_volume;
   double realized_r_like;

   string no_send_contract;
   string no_touch_contract;
   string execution_status;
};

struct FP_Consolidation05RuntimeHealthReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool latest_written;
};

void FP_ResetConsolidation05RuntimeHealthConfig(FP_Consolidation05RuntimeHealthConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.write_latest_csv = true;

   cfg.require_context_ready = false;
   cfg.require_final_decision_export = true;
   cfg.require_normalized_export = true;
   cfg.require_no_send_integrity = true;

   cfg.folder = FP_CONSOLIDATION05_RUNTIME_HEALTH_DEFAULT_FOLDER;
}

void FP_ResetConsolidation05RuntimeHealthRow(FP_Consolidation05RuntimeHealthRow &r)
{
   r.generated_at = 0;
   r.version = FP_CONSOLIDATION05_RUNTIME_HEALTH_VERSION;
   r.schema_version = FP_CONSOLIDATION05_RUNTIME_HEALTH_SCHEMA_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.health_ok = false;
   r.health_status = "RUNTIME_HEALTH_RESET";
   r.health_block_reason = "RESET";
   r.health_key = "";

   r.context_enabled = false;
   r.context_export_enabled = false;
   r.context_ready = false;
   r.context_status = "";
   r.context_block_reason = "";

   r.final_decision_enabled = false;
   r.final_decision_export_enabled = false;
   r.final_decision_ready = false;
   r.final_decision_state = "";
   r.final_decision_block_reason = "";

   r.normalized_enabled = false;
   r.normalized_export_enabled = false;
   r.normalized_ready = false;
   r.normalized_quality_status = "";
   r.normalized_block_reason = "";

   r.no_send_integrity_ok = false;
   r.expected_outputs_enabled = false;
   r.expected_outputs_enabled_count = 0;
   r.expected_outputs_required_count = 3;

   r.setup_state = "";
   r.chain_stage = "";
   r.blocker_layer = "";
   r.blocker_reason = "";
   r.request_id = "";
   r.virtual_ticket = "";
   r.request_direction = "";
   r.entry_price = 0.0;
   r.stop_price = 0.0;
   r.target_price = 0.0;
   r.request_volume = 0.0;
   r.realized_r_like = 0.0;

   r.no_send_contract = "RUNTIME_HEALTH_SUMMARY_ONLY_NO_ORDER_SEND_NO_ORDER_CHECK_NO_CTRADE";
   r.no_touch_contract = "RUNTIME_HEALTH_SUMMARY_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_CONSOLIDATION05_RUNTIME_HEALTH_ONLY";
}

void FP_ResetConsolidation05RuntimeHealthReport(FP_Consolidation05RuntimeHealthReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.latest_written = false;
}

#endif // __FP_RUNTIME_HEALTH_SUMMARY_TYPES_MQH__
