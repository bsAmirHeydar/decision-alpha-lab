#ifndef __FP_PAPER_PERFORMANCE_ENGINE_MQH__
#define __FP_PAPER_PERFORMANCE_ENGINE_MQH__
#property strict

#include "FP_PaperPerformanceExport.mqh"

string g_fp_l23_last_sample_key = "";
int g_fp_l23_sample_total = 0;
int g_fp_l23_counted_total = 0;
int g_fp_l23_duplicate_total = 0;
int g_fp_l23_blocked_count = 0;
int g_fp_l23_tracked_count = 0;
int g_fp_l23_entered_count = 0;
int g_fp_l23_target_count = 0;
int g_fp_l23_stop_count = 0;
int g_fp_l23_expired_count = 0;
int g_fp_l23_open_count = 0;
int g_fp_l23_ambiguous_count = 0;
int g_fp_l23_resolved_count = 0;
int g_fp_l23_win_like_count = 0;
int g_fp_l23_loss_like_count = 0;
int g_fp_l23_neutral_like_count = 0;
double g_fp_l23_sum_r_like = 0.0;
double g_fp_l23_best_r_like = 0.0;
double g_fp_l23_worst_r_like = 0.0;
bool g_fp_l23_has_r_sample = false;

void FP_L23ApplyLifecycleSample(const FP_Level23PaperPerformanceConfig &cfg,
                                const FP_Level22PaperLifecycleRow &life,
                                FP_Level23PaperPerformanceRow &row)
{
   string sample_key = FP_L23BuildSampleKey(life);
   string outcome_class = FP_L23OutcomeClass(life);

   row.current_lifecycle_id = life.lifecycle_id;
   row.current_lifecycle_status = life.lifecycle_status;
   row.current_outcome_class = outcome_class;
   row.current_r_like = life.realized_r_like;
   row.current_bars_elapsed = life.bars_elapsed;

   if(sample_key == g_fp_l23_last_sample_key)
   {
      g_fp_l23_duplicate_total++;
      row.duplicate_skipped = true;
      row.updated = false;
   }
   else
   {
      g_fp_l23_last_sample_key = sample_key;
      g_fp_l23_sample_total++;
      row.updated = true;

      bool should_count = true;
      if(FP_L23OutcomeIsBlocked(outcome_class) && !cfg.count_blocked_samples)
         should_count = false;
      if(FP_L23OutcomeIsOpen(outcome_class) && !cfg.count_open_samples)
         should_count = false;

      if(should_count)
      {
         g_fp_l23_counted_total++;

         if(FP_L23OutcomeIsBlocked(outcome_class))
            g_fp_l23_blocked_count++;
         if(life.tracked)
            g_fp_l23_tracked_count++;
         if(life.entry_index >= 0)
            g_fp_l23_entered_count++;

         if(outcome_class == "OUTCOME_TARGET")
         {
            g_fp_l23_target_count++;
            g_fp_l23_win_like_count++;
         }
         else if(outcome_class == "OUTCOME_STOP")
         {
            g_fp_l23_stop_count++;
            g_fp_l23_loss_like_count++;
         }
         else if(outcome_class == "OUTCOME_EXPIRED_BEFORE_ENTRY" ||
                 outcome_class == "OUTCOME_EXPIRED_AFTER_ENTRY")
         {
            g_fp_l23_expired_count++;
            g_fp_l23_neutral_like_count++;
         }
         else if(outcome_class == "OUTCOME_OPEN" ||
                 outcome_class == "OUTCOME_PENDING" ||
                 outcome_class == "OUTCOME_ENTERED_OPEN")
         {
            g_fp_l23_open_count++;
            g_fp_l23_neutral_like_count++;
         }
         else if(outcome_class == "OUTCOME_AMBIGUOUS")
         {
            g_fp_l23_ambiguous_count++;
            g_fp_l23_neutral_like_count++;
         }
         else
         {
            g_fp_l23_neutral_like_count++;
         }

         if(FP_L23OutcomeIsResolved(outcome_class, cfg))
         {
            g_fp_l23_resolved_count++;
            g_fp_l23_sum_r_like += life.realized_r_like;

            if(!g_fp_l23_has_r_sample)
            {
               g_fp_l23_best_r_like = life.realized_r_like;
               g_fp_l23_worst_r_like = life.realized_r_like;
               g_fp_l23_has_r_sample = true;
            }
            else
            {
               if(life.realized_r_like > g_fp_l23_best_r_like)
                  g_fp_l23_best_r_like = life.realized_r_like;
               if(life.realized_r_like < g_fp_l23_worst_r_like)
                  g_fp_l23_worst_r_like = life.realized_r_like;
            }
         }
      }
   }

   row.sample_total = g_fp_l23_sample_total;
   row.counted_total = g_fp_l23_counted_total;
   row.duplicate_total = g_fp_l23_duplicate_total;

   row.blocked_count = g_fp_l23_blocked_count;
   row.tracked_count = g_fp_l23_tracked_count;
   row.entered_count = g_fp_l23_entered_count;
   row.target_count = g_fp_l23_target_count;
   row.stop_count = g_fp_l23_stop_count;
   row.expired_count = g_fp_l23_expired_count;
   row.open_count = g_fp_l23_open_count;
   row.ambiguous_count = g_fp_l23_ambiguous_count;
   row.resolved_count = g_fp_l23_resolved_count;

   row.win_like_count = g_fp_l23_win_like_count;
   row.loss_like_count = g_fp_l23_loss_like_count;
   row.neutral_like_count = g_fp_l23_neutral_like_count;
   row.sum_r_like = g_fp_l23_sum_r_like;
   row.best_r_like = g_fp_l23_best_r_like;
   row.worst_r_like = g_fp_l23_worst_r_like;

   if(g_fp_l23_resolved_count > 0)
      row.avg_r_like = g_fp_l23_sum_r_like / (double)g_fp_l23_resolved_count;
   if(g_fp_l23_resolved_count > 0)
      row.hit_rate_like = (double)g_fp_l23_target_count / (double)g_fp_l23_resolved_count;
   if(g_fp_l23_resolved_count > 0)
      row.loss_rate_like = (double)g_fp_l23_stop_count / (double)g_fp_l23_resolved_count;

   row.performance_status = (row.updated ? "PAPER_PERFORMANCE_UPDATED" : "PAPER_PERFORMANCE_DUPLICATE_SKIPPED");
   row.performance_key = row.symbol;
   row.performance_key += "|TF=" + row.period_label;
   row.performance_key += "|SAMPLES=" + IntegerToString(row.sample_total);
   row.performance_key += "|RESOLVED=" + IntegerToString(row.resolved_count);
   row.performance_key += "|HIT_RATE=" + DoubleToString(row.hit_rate_like, 2);
   row.performance_key += "|AVG_R=" + DoubleToString(row.avg_r_like, 2);
   row.performance_key += "|EXEC=NO";
}

void FP_RunLevel23PaperPerformance(const string symbol,
                                   const ENUM_TIMEFRAMES period,
                                   const MqlRates &rates[],
                                   const int bars,
                                   const FP_FlagEvent &events[],
                                   const FP_HookBranch &hooks[],
                                   const FP_TimebaseReport &timebase_report,
                                   const FP_RenderReport &render_report,
                                   const FP_ValidationReport &validation_report,
                                   const FP_Level20EntryBridgeConfig &entry_bridge_cfg,
                                   const FP_Level21PaperIntentConfig &intent_cfg,
                                   const FP_Level22PaperLifecycleConfig &lifecycle_cfg,
                                   const FP_Level23PaperPerformanceConfig &cfg,
                                   FP_Level23PaperPerformanceReport &report)
{
   FP_ResetLevel23PaperPerformanceReport(report);
   report.attempted = cfg.enabled;

   if(!cfg.enabled)
   {
      report.ok = true;
      report.status = "LEVEL23_PAPER_PERFORMANCE_DISABLED";
      report.reason = "InpLevel23PaperPerformanceEnabled_false";
      return;
   }

   FP_Level20EntryBridgeRow bridge_row;
   FP_L20BuildEntryBridgeRow(symbol, period, rates, bars, events, hooks,
                             timebase_report, render_report, validation_report,
                             entry_bridge_cfg, bridge_row);

   FP_Level21PaperIntentRow intent_row;
   FP_L21FillFromEntryBridge(intent_cfg, bridge_row, intent_row);

   FP_Level22PaperLifecycleRow lifecycle_row;
   FP_L22SeedFromIntent(lifecycle_cfg, intent_row, lifecycle_row);
   FP_L22EvaluateCloseOnlyLifecycle(lifecycle_cfg, rates, bars, lifecycle_row);

   FP_Level23PaperPerformanceRow row;
   FP_ResetLevel23PaperPerformanceRow(row);
   row.generated_at = TimeCurrent();
   row.symbol = symbol;
   row.period = period;
   row.period_label = FP_L23TfLabel(period);
   row.attempted = cfg.enabled;

   FP_L23ApplyLifecycleSample(cfg, lifecycle_row, row);

   bool export_ok = FP_L23ExportPaperPerformance(cfg, row, report);

   report.ok = (export_ok && report.file_errors == 0);
   report.status = row.performance_status;
   report.reason = row.current_outcome_class;
   report.duplicate_skipped = row.duplicate_skipped;
}

void FP_PrintLevel23PaperPerformanceReport(const string tag,
                                           const FP_Level23PaperPerformanceReport &report)
{
   string line = tag;
   line += " attempted=" + FP_L23Bool(report.attempted);
   line += " ok=" + FP_L23Bool(report.ok);
   line += " status=" + report.status;
   line += " reason=" + report.reason;
   line += " files_written=" + IntegerToString(report.files_written);
   line += " file_errors=" + IntegerToString(report.file_errors);
   line += " performance_written=" + FP_L23Bool(report.performance_written);
   line += " duplicate_skipped=" + FP_L23Bool(report.duplicate_skipped);
   line += " execution=NO";
   Print(line);
}

#endif // __FP_PAPER_PERFORMANCE_ENGINE_MQH__
