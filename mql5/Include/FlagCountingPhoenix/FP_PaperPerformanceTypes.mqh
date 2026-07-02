#ifndef __FP_PAPER_PERFORMANCE_TYPES_MQH__
#define __FP_PAPER_PERFORMANCE_TYPES_MQH__
#property strict

#include "FP_PaperLifecycleTypes.mqh"

#define FP_LEVEL23_PAPER_PERFORMANCE_VERSION "23.00-paper-performance-close-only"
#define FP_LEVEL23_PAPER_PERFORMANCE_DEFAULT_FOLDER "FlagCountingPhoenix"

// ============================================================================
// FlagCounting Phoenix - Level 23 Paper Performance Types
// ----------------------------------------------------------------------------
// Contract:
// - performance summary only
// - close-only paper lifecycle input
// - no order
// - no broker request
// - no position
// - no volume / risk sizing
// - no renderer mutation
// - no chart-object mutation
// ============================================================================

struct FP_Level23PaperPerformanceConfig
{
   bool enabled;
   bool export_csv;
   bool print_summary;
   bool count_blocked_samples;
   bool count_open_samples;
   bool count_expired_as_resolved;
   string folder;
};

struct FP_Level23PaperPerformanceRow
{
   datetime generated_at;
   string version;
   string symbol;
   ENUM_TIMEFRAMES period;
   string period_label;

   bool attempted;
   bool updated;
   bool duplicate_skipped;
   string performance_status;
   string performance_key;

   string current_lifecycle_id;
   string current_lifecycle_status;
   string current_outcome_class;
   double current_r_like;
   int current_bars_elapsed;

   int sample_total;
   int counted_total;
   int duplicate_total;

   int blocked_count;
   int tracked_count;
   int entered_count;
   int target_count;
   int stop_count;
   int expired_count;
   int open_count;
   int ambiguous_count;
   int resolved_count;

   int win_like_count;
   int loss_like_count;
   int neutral_like_count;

   double hit_rate_like;
   double loss_rate_like;
   double avg_r_like;
   double best_r_like;
   double worst_r_like;
   double sum_r_like;

   string no_touch_contract;
   string execution_status;
};

struct FP_Level23PaperPerformanceReport
{
   bool attempted;
   bool ok;
   string status;
   string reason;
   int files_written;
   int file_errors;
   bool performance_written;
   bool duplicate_skipped;
};

void FP_ResetLevel23PaperPerformanceConfig(FP_Level23PaperPerformanceConfig &cfg)
{
   cfg.enabled = true;
   cfg.export_csv = true;
   cfg.print_summary = false;
   cfg.count_blocked_samples = true;
   cfg.count_open_samples = true;
   cfg.count_expired_as_resolved = true;
   cfg.folder = FP_LEVEL23_PAPER_PERFORMANCE_DEFAULT_FOLDER;
}

void FP_ResetLevel23PaperPerformanceRow(FP_Level23PaperPerformanceRow &r)
{
   r.generated_at = 0;
   r.version = FP_LEVEL23_PAPER_PERFORMANCE_VERSION;
   r.symbol = "";
   r.period = PERIOD_CURRENT;
   r.period_label = "";

   r.attempted = false;
   r.updated = false;
   r.duplicate_skipped = false;
   r.performance_status = "PAPER_PERFORMANCE_RESET";
   r.performance_key = "";

   r.current_lifecycle_id = "";
   r.current_lifecycle_status = "";
   r.current_outcome_class = "OUTCOME_NOT_EVALUATED";
   r.current_r_like = 0.0;
   r.current_bars_elapsed = 0;

   r.sample_total = 0;
   r.counted_total = 0;
   r.duplicate_total = 0;

   r.blocked_count = 0;
   r.tracked_count = 0;
   r.entered_count = 0;
   r.target_count = 0;
   r.stop_count = 0;
   r.expired_count = 0;
   r.open_count = 0;
   r.ambiguous_count = 0;
   r.resolved_count = 0;

   r.win_like_count = 0;
   r.loss_like_count = 0;
   r.neutral_like_count = 0;

   r.hit_rate_like = 0.0;
   r.loss_rate_like = 0.0;
   r.avg_r_like = 0.0;
   r.best_r_like = 0.0;
   r.worst_r_like = 0.0;
   r.sum_r_like = 0.0;

   r.no_touch_contract = "PAPER_PERFORMANCE_ONLY_NO_ORDER_NO_BROKER_NO_RENDERER_MUTATION";
   r.execution_status = "REAL_EXECUTION_DISABLED_LEVEL23_PAPER_PERFORMANCE_ONLY";
}

void FP_ResetLevel23PaperPerformanceReport(FP_Level23PaperPerformanceReport &r)
{
   r.attempted = false;
   r.ok = false;
   r.status = "not_attempted";
   r.reason = "not_attempted";
   r.files_written = 0;
   r.file_errors = 0;
   r.performance_written = false;
   r.duplicate_skipped = false;
}

#endif // __FP_PAPER_PERFORMANCE_TYPES_MQH__
