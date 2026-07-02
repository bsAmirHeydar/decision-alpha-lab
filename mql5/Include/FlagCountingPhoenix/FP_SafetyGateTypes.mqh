#ifndef __FP_SAFETY_GATE_TYPES_MQH__
#define __FP_SAFETY_GATE_TYPES_MQH__
#property strict

#include "FP_PaperPerformanceTypes.mqh"

#define FP_LEVEL24_SAFETY_GATE_VERSION "24.00-safety-gate-pre-broker"
#define FP_LEVEL24_SAFETY_GATE_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 24 Safety Gate Types
// ----------------------------------------------------------------------------
// Contract:
// - safety gate only
// - no order
// - no broker request
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Level24SafetyGateConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;

   bool manual_arm;
   bool real_execution_enabled;

   bool require_license_ok;
   bool require_symbol_allowed;
   bool require_timeframe_allowed;
   bool require_spread_ok;
   bool require_performance_ok;
   bool require_manual_arm;
   bool require_real_execution_disabled;

   string allowed_symbols;
   string allowed_timeframes;

   int max_spread_points;
   int min_resolved_samples;
   double min_hit_rate_like;
   double min_avg_r_like;

   string folder;
};

struct FP_Level24SafetyGateRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool gate_passed;
   string gate_status;
   string gate_block_reason;
   string gate_key;

   bool license_ok;
   bool symbol_allowed;
   bool timeframe_allowed;
   bool spread_ok;
   bool performance_ok;
   bool manual_arm_ok;
   bool real_execution_disabled_ok;

   int current_spread_points;
   int max_spread_points;

   int performance_sample_total;
   int performance_resolved_count;
   int performance_target_count;
   int performance_stop_count;
   double performance_hit_rate_like;
   double performance_avg_r_like;
   double performance_best_r_like;
   double performance_worst_r_like;

   int min_resolved_samples;
   double min_hit_rate_like;
   double min_avg_r_like;

   string allowed_symbols;
   string allowed_timeframes;

   string next_step;
   string no_touch_contract;
   string execution_status;
};

struct FP_Level24SafetyGateReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool safety_gate_written;
};

void FP_ResetLevel24SafetyGateConfig(FP_Level24SafetyGateConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;

   cfg.manual_arm = false;
   cfg.real_execution_enabled = false;

   cfg.require_license_ok = true;
   cfg.require_symbol_allowed = true;
   cfg.require_timeframe_allowed = true;
   cfg.require_spread_ok = true;
   cfg.require_performance_ok = false;
   cfg.require_manual_arm = false;
   cfg.require_real_execution_disabled = true;

   cfg.allowed_symbols = "*";
   cfg.allowed_timeframes = "*";

   cfg.max_spread_points = 0;
   cfg.min_resolved_samples = 30;
   cfg.min_hit_rate_like = 0.50;
   cfg.min_avg_r_like = 0.00;

   cfg.folder = FP_LEVEL24_SAFETY_GATE_DEFAULT_FOLDER;
}

void FP_ResetLevel24SafetyGateRow(FP_Level24SafetyGateRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL24_SAFETY_GATE_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.gate_passed = false;
   r.gate_status = "SAFETY_GATE_RESET";
   r.gate_block_reason = "RESET";
   r.gate_key = "";

   r.license_ok = false;
   r.symbol_allowed = false;
   r.timeframe_allowed = false;
   r.spread_ok = false;
   r.performance_ok = false;
   r.manual_arm_ok = false;
   r.real_execution_disabled_ok = false;

   r.current_spread_points = 0;
   r.max_spread_points = 0;

   r.performance_sample_total = 0;
   r.performance_resolved_count = 0;
   r.performance_target_count = 0;
   r.performance_stop_count = 0;
   r.performance_hit_rate_like = 0.0;
   r.performance_avg_r_like = 0.0;
   r.performance_best_r_like = 0.0;
   r.performance_worst_r_like = 0.0;

   r.min_resolved_samples = 0;
   r.min_hit_rate_like = 0.0;
   r.min_avg_r_like = 0.0;

   r.allowed_symbols = "";
   r.allowed_timeframes = "";

   r.next_step = "NEXT_BLOCKED";
   r.no_touch_contract = "SAFETY_GATE_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL24_SAFETY_GATE_ONLY";
}

void FP_ResetLevel24SafetyGateReport(FP_Level24SafetyGateReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.safety_gate_written = false;
}

#endif // __FP_SAFETY_GATE_TYPES_MQH__
