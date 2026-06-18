#ifndef __DAL_M0003_REPORTS_MQH__
#define __DAL_M0003_REPORTS_MQH__

#include <DecisionAlphaLab/M0002/DAL_M0002Reports.mqh>

string DAL_M0003Prefix(
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

double DAL_M0003SafeRatio(const double numerator, const double denominator)
{
   if(denominator == 0.0)
      return 0.0;
   return numerator / denominator;
}

double DAL_M0003LagCorr(const DALM0001PairedLogRtv &pairs[], const int lag)
{
   int count = ArraySize(pairs);
   if(lag <= 0 || count <= lag + 2)
      return 0.0;

   int n = count - lag;
   double mean_x = 0.0;
   double mean_y = 0.0;
   for(int i = lag; i < count; i++)
   {
      mean_x += pairs[i].delta_log;
      mean_y += pairs[i - lag].delta_log;
   }
   mean_x /= n;
   mean_y /= n;

   double cov = 0.0;
   double vx = 0.0;
   double vy = 0.0;
   for(int i = lag; i < count; i++)
   {
      double x = pairs[i].delta_log - mean_x;
      double y = pairs[i - lag].delta_log - mean_y;
      cov += x * y;
      vx += x * x;
      vy += y * y;
   }
   if(vx <= 0.0 || vy <= 0.0)
      return 0.0;
   return cov / MathSqrt(vx * vy);
}

string DAL_M0003HighRunText(const DALM0001PairedLogRtv &pairs[], const string label)
{
   int count = ArraySize(pairs);
   if(count <= 0)
      return "HIGH_RUNS*branch=" + label + "*n=0";

   double deltas[];
   ArrayResize(deltas, count);
   for(int i = 0; i < count; i++)
      deltas[i] = pairs[i].delta_log;
   ArraySort(deltas);

   double med = DAL_M0001NullPercentileSorted(deltas, 0.50);
   double p75 = DAL_M0001NullPercentileSorted(deltas, 0.75);

   int high_med = 0;
   int high_p75 = 0;
   int current_run = 0;
   int max_run = 0;
   int run_count = 0;
   int run_total = 0;
   for(int i = 0; i < count; i++)
   {
      if(pairs[i].delta_log > med)
         high_med++;
      if(pairs[i].delta_log > p75)
      {
         high_p75++;
         current_run++;
      }
      else
      {
         if(current_run > 0)
         {
            run_count++;
            run_total += current_run;
            if(current_run > max_run)
               max_run = current_run;
         }
         current_run = 0;
      }
   }
   if(current_run > 0)
   {
      run_count++;
      run_total += current_run;
      if(current_run > max_run)
         max_run = current_run;
   }

   double avg_run = run_count > 0 ? run_total / (double)run_count : 0.0;
   return "HIGH_RUNS"
      + "*branch=" + label
      + "*n=" + IntegerToString(count)
      + "*medianDelta=" + DAL_M0001Fmt4(med)
      + "*p75Delta=" + DAL_M0001Fmt4(p75)
      + "*gtMedianPct=" + DAL_M0001FmtPct(100.0 * high_med / count)
      + "*gtP75Pct=" + DAL_M0001FmtPct(100.0 * high_p75 / count)
      + "*p75RunCount=" + IntegerToString(run_count)
      + "*p75MaxRun=" + IntegerToString(max_run)
      + "*p75AvgRun=" + DAL_M0001Fmt4(avg_run);
}

string DAL_M0003InertiaText(
   const DALM0001LogRtvStats &reversal_stats,
   const DALM0001LogRtvStats &continuation_stats,
   const DALM0001PairedLogRtv &reversal_pairs[],
   const DALM0001PairedLogRtv &continuation_pairs[],
   const DALBar &bars[],
   const int bars_count,
   const datetime min_entry_time,
   const DALM0002Config &config
)
{
   int analysis_start_index = DAL_M0001FirstIndexAtOrAfter(bars, bars_count, min_entry_time);
   int hs[4];
   hs[0] = config.horizon_bars_1;
   hs[1] = config.horizon_bars_2;
   hs[2] = config.horizon_bars_3;
   hs[3] = config.horizon_bars_4;

   string out = "INERTIA_MEMORY";
   out += "*revEventDLog=" + DAL_M0001Fmt4(reversal_stats.log_mean);
   out += "*contEventDLog=" + DAL_M0001Fmt4(continuation_stats.log_mean);
   out += "*contMinusRevEventDLog=" + DAL_M0001Fmt4(continuation_stats.log_mean - reversal_stats.log_mean);
   out += "*contOverRevEventRatio=" + DAL_M0001Fmt4(MathExp(continuation_stats.log_mean - reversal_stats.log_mean));

   int cont_higher = 0;
   int cont_higher_carry = 0;
   for(int i = 0; i < 4; i++)
   {
      int h = hs[i];
      double rev_h_mean = 0.0;
      double rev_h_win = 0.0;
      int rev_h_n = 0;
      double cont_h_mean = 0.0;
      double cont_h_win = 0.0;
      int cont_h_n = 0;
      DAL_M0001HorizonOne(reversal_pairs, bars, bars_count, analysis_start_index, h, rev_h_mean, rev_h_win, rev_h_n);
      DAL_M0001HorizonOne(continuation_pairs, bars, bars_count, analysis_start_index, h, cont_h_mean, cont_h_win, cont_h_n);
      double rev_carry = DAL_M0003SafeRatio(rev_h_mean, reversal_stats.log_mean);
      double cont_carry = DAL_M0003SafeRatio(cont_h_mean, continuation_stats.log_mean);
      if(cont_h_n > 0 && rev_h_n > 0 && cont_h_mean > rev_h_mean)
         cont_higher++;
      if(cont_carry > rev_carry)
         cont_higher_carry++;
      out += "*h" + IntegerToString(h) + "RevDLog=" + DAL_M0001Fmt4(rev_h_mean);
      out += "*h" + IntegerToString(h) + "ContDLog=" + DAL_M0001Fmt4(cont_h_mean);
      out += "*h" + IntegerToString(h) + "ContMinusRev=" + DAL_M0001Fmt4(cont_h_mean - rev_h_mean);
      out += "*h" + IntegerToString(h) + "RevCarry=" + DAL_M0001Fmt4(rev_carry);
      out += "*h" + IntegerToString(h) + "ContCarry=" + DAL_M0001Fmt4(cont_carry);
   }

   string memory_model = "mixed_or_unavailable";
   if(cont_higher == 4 && cont_higher_carry >= 2)
      memory_model = "continuation_higher_inertia_and_memory";
   else if(cont_higher >= 2)
      memory_model = "continuation_higher_inertia_mixed_memory";

   out += "*continuationHigherHorizons=" + IntegerToString(cont_higher);
   out += "*continuationHigherCarryHorizons=" + IntegerToString(cont_higher_carry);
   out += "*memoryModel=" + memory_model;
   return out;
}

string DAL_M0003ClusterText(const DALM0001PairedLogRtv &pairs[], const string label)
{
   int day_n = 0;
   double day_mean = 0.0;
   double day_t = 0.0;
   double day_p = 1.0;
   DAL_M0001ClusterTStats(pairs, 86400, day_n, day_mean, day_t, day_p);

   int week_n = 0;
   double week_mean = 0.0;
   double week_t = 0.0;
   double week_p = 1.0;
   DAL_M0001ClusterTStats(pairs, 604800, week_n, week_mean, week_t, week_p);

   double lag1 = DAL_M0003LagCorr(pairs, 1);
   double lag2 = DAL_M0003LagCorr(pairs, 2);

   string cluster_model = "positive_cluster_robust_memory";
   if(day_mean <= 0.0 && week_mean <= 0.0)
      cluster_model = "weak_or_no_cluster_memory";

   return "CLUSTER_MEMORY"
      + "*branch=" + label
      + "*n=" + IntegerToString(ArraySize(pairs))
      + "*lag1DeltaCorr=" + DAL_M0001Fmt4(lag1)
      + "*lag2DeltaCorr=" + DAL_M0001Fmt4(lag2)
      + "*dayClusters=" + IntegerToString(day_n)
      + "*dayMean=" + DAL_M0001Fmt4(day_mean)
      + "*dayT=" + DAL_M0001Fmt4(day_t)
      + "*dayPapprox=" + DAL_M0001Fmt4(day_p)
      + "*weekClusters=" + IntegerToString(week_n)
      + "*weekMean=" + DAL_M0001Fmt4(week_mean)
      + "*weekT=" + DAL_M0001Fmt4(week_t)
      + "*weekPapprox=" + DAL_M0001Fmt4(week_p)
      + "*clusterModel=" + cluster_model;
}

string DAL_M0003SummaryText(
   const DALM0002Audit &audit,
   const DALM0001LogRtvStats &reversal_stats,
   const DALM0001LogRtvStats &continuation_stats,
   const DALM0001PairedLogRtv &reversal_pairs[],
   const DALM0001PairedLogRtv &continuation_pairs[],
   const DALBar &bars[],
   const int bars_count,
   const datetime min_entry_time,
   const DALM0002Config &config
)
{
   int analysis_start_index = DAL_M0001FirstIndexAtOrAfter(bars, bars_count, min_entry_time);
   int hs[4];
   hs[0] = config.horizon_bars_1;
   hs[1] = config.horizon_bars_2;
   hs[2] = config.horizon_bars_3;
   hs[3] = config.horizon_bars_4;

   int cont_higher = 0;
   for(int i = 0; i < 4; i++)
   {
      int h = hs[i];
      double rev_h_mean = 0.0, rev_h_win = 0.0, cont_h_mean = 0.0, cont_h_win = 0.0;
      int rev_h_n = 0, cont_h_n = 0;
      DAL_M0001HorizonOne(reversal_pairs, bars, bars_count, analysis_start_index, h, rev_h_mean, rev_h_win, rev_h_n);
      DAL_M0001HorizonOne(continuation_pairs, bars, bars_count, analysis_start_index, h, cont_h_mean, cont_h_win, cont_h_n);
      if(cont_h_n > 0 && rev_h_n > 0 && cont_h_mean > rev_h_mean)
         cont_higher++;
   }

   string summary = "mixed_h3";
   if(audit.reversal_count > audit.continuation_count && continuation_stats.log_mean > reversal_stats.log_mean && cont_higher >= 2)
      summary = "continuation_lower_frequency_higher_zone_volatility_higher_inertia_memory";
   if(audit.reversal_count > audit.continuation_count && continuation_stats.log_mean > reversal_stats.log_mean && cont_higher == 4 && continuation_stats.raw_cvar95 > reversal_stats.raw_cvar95)
      summary = "continuation_lower_frequency_higher_zone_volatility_higher_inertia_memory_fatter_tail";

   return "H0003_SUMMARY"
      + "*paired=" + IntegerToString(audit.paired_count)
      + "*reversalN=" + IntegerToString(audit.reversal_count)
      + "*continuationN=" + IntegerToString(audit.continuation_count)
      + "*reversalPct=" + DAL_M0001FmtPct(audit.paired_count > 0 ? 100.0 * audit.reversal_count / audit.paired_count : 0.0)
      + "*continuationPct=" + DAL_M0001FmtPct(audit.paired_count > 0 ? 100.0 * audit.continuation_count / audit.paired_count : 0.0)
      + "*contMinusRevEventDLog=" + DAL_M0001Fmt4(continuation_stats.log_mean - reversal_stats.log_mean)
      + "*contOverRevEventRatio=" + DAL_M0001Fmt4(MathExp(continuation_stats.log_mean - reversal_stats.log_mean))
      + "*contOverRevCVaR95Ratio=" + DAL_M0001Fmt4(DAL_M0003SafeRatio(continuation_stats.raw_cvar95, reversal_stats.raw_cvar95))
      + "*continuationHigherHorizons=" + IntegerToString(cont_higher)
      + "*hypothesisState=" + summary;
}

void DAL_M0003PrintFinalReports(
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

   double reversal_logs[];
   double continuation_logs[];
   DAL_M0002SamplesToLogs(reversal_samples, reversal_logs);
   DAL_M0002SamplesToLogs(continuation_samples, continuation_logs);

   DALM0001LogRtvStats reversal_stats;
   DALM0001LogRtvStats continuation_stats;
   DAL_M0001ComputeLogRtvStats(reversal_logs, reversal_stats);
   DAL_M0001ComputeLogRtvStats(continuation_logs, continuation_stats);

   DALM0001PairedLogRtv reversal_pairs[];
   DALM0001PairedLogRtv continuation_pairs[];
   double reversal_random_logs[];
   double continuation_random_logs[];
   DAL_M0002SamplesToM0001Pairs(reversal_samples, reversal_pairs, reversal_logs, reversal_random_logs);
   DAL_M0002SamplesToM0001Pairs(continuation_samples, continuation_pairs, continuation_logs, continuation_random_logs);

   Print(DAL_M0003Prefix("DAL_M0003_FINAL_AUDIT", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0002AuditText(audit, config));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_SUMMARY", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003SummaryText(audit, reversal_stats, continuation_stats, reversal_pairs, continuation_pairs, bars, bars_count, min_entry_time, config));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_INERTIA_MEMORY", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003InertiaText(reversal_stats, continuation_stats, reversal_pairs, continuation_pairs, bars, bars_count, min_entry_time, config));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_REVERSAL_CLUSTER", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003ClusterText(reversal_pairs, "REVERSAL"));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_CONTINUATION_CLUSTER", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003ClusterText(continuation_pairs, "CONTINUATION"));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_REVERSAL_HIGH_RUNS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003HighRunText(reversal_pairs, "REVERSAL"));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_CONTINUATION_HIGH_RUNS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003HighRunText(continuation_pairs, "CONTINUATION"));
}

#endif
