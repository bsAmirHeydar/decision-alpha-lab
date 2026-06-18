#ifndef __DAL_M0002_REPORTS_MQH__
#define __DAL_M0002_REPORTS_MQH__

#include <DecisionAlphaLab/M0001/DAL_M0001RtvNullComparison.mqh>
#include <DecisionAlphaLab/M0002/DAL_M0002Engine.mqh>

string DAL_M0002Prefix(
   const string tag,
   const string symbol,
   const string timeframe,
   const string source_mode,
   const int source_events,
   const datetime min_entry_time
)
{
   return tag
      + " *** symbol=" + symbol
      + "*tf=" + timeframe
      + "*source=" + source_mode
      + "*sourceEvents=" + IntegerToString(source_events)
      + "*analysisStart=" + DAL_M0001AnalysisStartText(min_entry_time)
      + " *** ";
}

string DAL_M0002AuditText(const DALM0002Audit &audit, const DALM0002Config &config)
{
   return "AUDIT"
      + "*measureMode=" + DAL_M0002MeasureModeToString(config.measure_mode)
      + "*sampleWindow=" + (config.measure_mode == DAL_M0002_MEASURE_POST_OUTCOME_FIXED ? "postOutcome" : "m0001EventRtv")
      + "*eventRtvMode=" + IntegerToString(audit.event_rtv_mode_count)
      + "*postOutcomeMode=" + IntegerToString(audit.post_outcome_mode_count)
      + "*sourceEvents=" + IntegerToString(audit.source_events)
      + "*afterStart=" + IntegerToString(audit.after_start)
      + "*exitCompleted=" + IntegerToString(audit.touch_confirmed)
      + "*paired=" + IntegerToString(audit.paired_count)
      + "*reversal=" + IntegerToString(audit.reversal_count)
      + "*continuation=" + IntegerToString(audit.continuation_count)
      + "*unknown=" + IntegerToString(audit.unknown_outcome)
      + "*skippedNoBaseline=" + IntegerToString(audit.skipped_no_baseline)
      + "*skippedNoFuture=" + IntegerToString(audit.skipped_no_future)
      + "*reversalPct=" + DAL_M0001FmtPct(audit.paired_count > 0 ? 100.0 * audit.reversal_count / audit.paired_count : 0.0)
      + "*continuationPct=" + DAL_M0001FmtPct(audit.paired_count > 0 ? 100.0 * audit.continuation_count / audit.paired_count : 0.0)
      + "*outcomeCandleOffsetAfterExit=" + IntegerToString(config.outcome_candle_offset_after_exit)
      + "*randomK=" + IntegerToString(config.random_samples_per_event)
      + "*sessionClock=UTC"
      + "*brokerUtcOffset=" + IntegerToString(config.broker_utc_offset_hours)
      + "*regimeBy=preEntryVolTercile"
      + "*baselineGuard=beforeEventEntry"
      + "*logic=neutralExitCompletion_nodeSide_branching_M0001EventRtvLocked_noHuntFiltering";
}

string DAL_M0002BranchDirectText(
   const string label,
   const DALM0001LogRtvStats &stats,
   const DALM0001LogRtvComparison &cmp
)
{
   return label
      + "*n=" + IntegerToString(stats.count)
      + "*rawMean=" + DAL_M0001Fmt4(stats.raw_mean)
      + "*rawMed=" + DAL_M0001Fmt4(stats.raw_median)
      + "*rawP75=" + DAL_M0001Fmt4(stats.raw_p75)
      + "*rawP90=" + DAL_M0001Fmt4(stats.raw_p90)
      + "*rawP95=" + DAL_M0001Fmt4(stats.raw_p95)
      + "*rawCVaR90=" + DAL_M0001Fmt4(stats.raw_cvar90)
      + "*rawCVaR95=" + DAL_M0001Fmt4(stats.raw_cvar95)
      + "*logMean=" + DAL_M0001Fmt4(stats.log_mean)
      + "*logMed=" + DAL_M0001Fmt4(stats.log_median)
      + "*logGt0Pct=" + DAL_M0001FmtPct(stats.pct_log_gt_zero)
      + "*logIQR=" + DAL_M0001Fmt4(stats.log_iqr)
      + "*skew=" + DAL_M0001Fmt4(stats.log_skewness)
      + "*exKurt=" + DAL_M0001Fmt4(stats.log_excess_kurtosis)
      + "*vsRandomDLog=" + DAL_M0001Fmt4(cmp.delta_log_mean)
      + "*vsRandomGeoRatio=" + DAL_M0001Fmt4(cmp.geo_ratio)
      + "*vsRandomWin=" + DAL_M0001FmtPct(cmp.paired_win_pct)
      + "*vsRandomT=" + DAL_M0001Fmt4(cmp.paired_t_stat)
      + "*vsRandomCohenD=" + DAL_M0001Fmt4(cmp.cohen_d)
      + "*vsRandomKS=" + DAL_M0001Fmt4(cmp.ks_real_vs_random)
      + "*vsRandomW1=" + DAL_M0001Fmt4(cmp.wasserstein_log);
}

string DAL_M0002DirectCompareText(
   const DALM0001LogRtvStats &reversal_stats,
   const DALM0001LogRtvStats &continuation_stats,
   const double &reversal_logs[],
   const double &continuation_logs[]
)
{
   double dlog = reversal_stats.log_mean - continuation_stats.log_mean;
   double dmed = reversal_stats.log_median - continuation_stats.log_median;
   double drawmean = reversal_stats.raw_mean - continuation_stats.raw_mean;
   double drawmed = reversal_stats.raw_median - continuation_stats.raw_median;
   double dgt0 = reversal_stats.pct_log_gt_zero - continuation_stats.pct_log_gt_zero;
   double ks = DAL_M0001KsTwoSample(reversal_logs, continuation_logs);
   double cvm = DAL_M0001CvmTwoSample(reversal_logs, continuation_logs);
   double w1 = DAL_M0001WassersteinLogDistance(reversal_logs, continuation_logs);
   double cliff = DAL_M0001CliffDelta(reversal_logs, continuation_logs);

   string interpretation = "balanced_or_mixed";
   if(dlog > 0.0)
      interpretation = "positive_means_reversal_more_volatile_than_continuation";
   else if(dlog < 0.0)
      interpretation = "negative_means_continuation_more_volatile_than_reversal";

   return "REVERSAL_VS_CONTINUATION"
      + "*reversalN=" + IntegerToString(reversal_stats.count)
      + "*continuationN=" + IntegerToString(continuation_stats.count)
      + "*reversalRawMean=" + DAL_M0001Fmt4(reversal_stats.raw_mean)
      + "*continuationRawMean=" + DAL_M0001Fmt4(continuation_stats.raw_mean)
      + "*dRawMean=" + DAL_M0001Fmt4(drawmean)
      + "*reversalRawMed=" + DAL_M0001Fmt4(reversal_stats.raw_median)
      + "*continuationRawMed=" + DAL_M0001Fmt4(continuation_stats.raw_median)
      + "*dRawMed=" + DAL_M0001Fmt4(drawmed)
      + "*dLogMean=" + DAL_M0001Fmt4(dlog)
      + "*geoRatio=" + DAL_M0001Fmt4(MathExp(dlog))
      + "*dLogMed=" + DAL_M0001Fmt4(dmed)
      + "*medianRatio=" + DAL_M0001Fmt4(MathExp(dmed))
      + "*dGt0Pct=" + DAL_M0001FmtPct(dgt0)
      + "*reversalLogMean=" + DAL_M0001Fmt4(reversal_stats.log_mean)
      + "*continuationLogMean=" + DAL_M0001Fmt4(continuation_stats.log_mean)
      + "*reversalWinRaw=" + DAL_M0001FmtPct(reversal_stats.pct_log_gt_zero)
      + "*continuationWinRaw=" + DAL_M0001FmtPct(continuation_stats.pct_log_gt_zero)
      + "*cliffDelta=" + DAL_M0001Fmt4(cliff)
      + "*KS=" + DAL_M0001Fmt4(ks)
      + "*CvM=" + DAL_M0001Fmt4(cvm)
      + "*W1log=" + DAL_M0001Fmt4(w1)
      + "*interpretation=" + interpretation;
}

void DAL_M0002PrintBranchReport(
   const string label,
   const DALM0002BranchSample &samples[],
   const string symbol,
   const string timeframe,
   const string source_mode,
   const int source_events,
   const datetime min_entry_time,
   const DALM0002Config &config
)
{
   DALM0001PairedLogRtv pairs[];
   double logs[];
   double random_logs[];
   DAL_M0002SamplesToM0001Pairs(samples, pairs, logs, random_logs);

   DALM0001LogRtvStats stats;
   DALM0001LogRtvStats random_stats;
   DAL_M0001ComputeLogRtvStats(logs, stats);
   DAL_M0001ComputeLogRtvStats(random_logs, random_stats);

   DALM0001LogRtvComparison cmp;
   DAL_M0001ComputeLogRtvComparison(logs, random_logs, stats, random_stats, cmp);

   DALM0001RobustnessStats rob;
   DAL_M0001ComputeRobustnessStats(pairs, config.bootstrap_iterations, config.permutation_iterations, config.validation_splits, rob);

   Print(DAL_M0002Prefix("DAL_M0002_FINAL_" + label, symbol, timeframe, source_mode, source_events, min_entry_time), DAL_M0002BranchDirectText(label, stats, cmp));
   Print(DAL_M0002Prefix("DAL_M0002_FINAL_" + label + "_RANDOM", symbol, timeframe, source_mode, source_events, min_entry_time), DAL_M0001StatsCompactText(label + "_RANDOM", random_stats));
   Print(DAL_M0002Prefix("DAL_M0002_FINAL_" + label + "_COMPARE", symbol, timeframe, source_mode, source_events, min_entry_time), DAL_M0001ComparisonCompactText(cmp));
   Print(DAL_M0002Prefix("DAL_M0002_FINAL_" + label + "_ROBUST", symbol, timeframe, source_mode, source_events, min_entry_time), DAL_M0001RobustnessText(rob));

   if(config.print_group_session_regime)
      Print(DAL_M0002Prefix("DAL_M0002_FINAL_" + label + "_SESSION_REGIME", symbol, timeframe, source_mode, source_events, min_entry_time), DAL_M0001SessionRegimeText(pairs, config.broker_utc_offset_hours));
}

void DAL_M0002PrintFinalReports(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const string symbol,
   const string timeframe,
   const string source_mode,
   const datetime min_entry_time,
   const DALM0002Config &config
)
{
   DALM0002BranchSample all_samples[];
   DALM0002BranchSample reversal_samples[];
   DALM0002BranchSample continuation_samples[];
   DALM0002Audit audit;

   DAL_M0002CollectBranchSamples(events, events_count, bars, bars_count, min_entry_time, config, all_samples, reversal_samples, continuation_samples, audit);

   Print(DAL_M0002Prefix("DAL_M0002_FINAL_AUDIT", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0002AuditText(audit, config));

   DAL_M0002PrintBranchReport("REVERSAL_AFTER_EXIT", reversal_samples, symbol, timeframe, source_mode, events_count, min_entry_time, config);
   DAL_M0002PrintBranchReport("CONTINUATION_AFTER_EXIT", continuation_samples, symbol, timeframe, source_mode, events_count, min_entry_time, config);

   double reversal_logs[];
   double continuation_logs[];
   DAL_M0002SamplesToLogs(reversal_samples, reversal_logs);
   DAL_M0002SamplesToLogs(continuation_samples, continuation_logs);

   DALM0001LogRtvStats reversal_stats;
   DALM0001LogRtvStats continuation_stats;
   DAL_M0001ComputeLogRtvStats(reversal_logs, reversal_stats);
   DAL_M0001ComputeLogRtvStats(continuation_logs, continuation_stats);

   Print(DAL_M0002Prefix("DAL_M0002_FINAL_REVERSAL_VS_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0002DirectCompareText(reversal_stats, continuation_stats, reversal_logs, continuation_logs));
}

#endif
