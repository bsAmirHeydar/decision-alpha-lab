#ifndef __DAL_M0003_REPORTS_MQH__
#define __DAL_M0003_REPORTS_MQH__

#include <M0002/DAL_M0002Reports.mqh>

struct DALM0003Config
{
   int cluster_stress_iterations;
   int cluster_block_size;
   double high_run_percentile;
};

struct DALM0003RunStats
{
   int n;
   double threshold;
   double high_pct;
   int run_count;
   int max_run;
   double avg_run;
   double iid_expected_avg_run;
   double avg_run_over_iid;
};

struct DALM0003HorizonStats
{
   int h;
   int rev_n;
   int cont_n;
   double rev_mean;
   double rev_win;
   double cont_mean;
   double cont_win;
   double cont_minus_rev;
   double cont_over_rev;
   double rev_carry;
   double cont_carry;
   double cont_minus_rev_carry;
};

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
   if(MathAbs(denominator) <= 0.000000000001)
      return 0.0;
   return numerator / denominator;
}

// Deterministic Fisher-Yates permutation using the shared M0001 hash RNG.
// This avoids replacement bias in cluster/run nulls and keeps all H0003 stress tests reproducible.
void DAL_M0003BuildPermutation(const int count, const int iter, const int salt, int &perm[])
{
   ArrayResize(perm, count);
   for(int i = 0; i < count; i++)
      perm[i] = i;

   for(int i = count - 1; i > 0; i--)
   {
      double frac = DAL_M0001RandomFractionK(iter + salt, count, count + salt * 17, i + salt * 31);
      int j = (int)MathFloor(frac * (i + 1));
      if(j < 0) j = 0;
      if(j > i) j = i;

      int tmp = perm[i];
      perm[i] = perm[j];
      perm[j] = tmp;
   }
}

double DAL_M0003MeanDelta(const DALM0001PairedLogRtv &pairs[])
{
   int count = ArraySize(pairs);
   if(count <= 0)
      return 0.0;
   double sum = 0.0;
   for(int i = 0; i < count; i++)
      sum += pairs[i].delta_log;
   return sum / count;
}

void DAL_M0003Deltas(const DALM0001PairedLogRtv &pairs[], double &deltas[])
{
   int count = ArraySize(pairs);
   ArrayResize(deltas, count);
   for(int i = 0; i < count; i++)
      deltas[i] = pairs[i].delta_log;
}

double DAL_M0003LagCorrValues(const double &values[], const int lag)
{
   int count = ArraySize(values);
   if(lag <= 0 || count <= lag + 2)
      return 0.0;

   int n = count - lag;
   double mean_x = 0.0;
   double mean_y = 0.0;
   for(int i = lag; i < count; i++)
   {
      mean_x += values[i];
      mean_y += values[i - lag];
   }
   mean_x /= n;
   mean_y /= n;

   double cov = 0.0;
   double vx = 0.0;
   double vy = 0.0;
   for(int i = lag; i < count; i++)
   {
      double x = values[i] - mean_x;
      double y = values[i - lag] - mean_y;
      cov += x * y;
      vx += x * x;
      vy += y * y;
   }
   if(vx <= 0.0 || vy <= 0.0)
      return 0.0;
   return cov / MathSqrt(vx * vy);
}

double DAL_M0003LagCorr(const DALM0001PairedLogRtv &pairs[], const int lag)
{
   double deltas[];
   DAL_M0003Deltas(pairs, deltas);
   return DAL_M0003LagCorrValues(deltas, lag);
}

void DAL_M0003ComputeHorizonStats(
   const int h,
   const DALM0001LogRtvStats &reversal_stats,
   const DALM0001LogRtvStats &continuation_stats,
   const DALM0001PairedLogRtv &reversal_pairs[],
   const DALM0001PairedLogRtv &continuation_pairs[],
   const DALBar &bars[],
   const int bars_count,
   const int analysis_start_index,
   DALM0003HorizonStats &hs
)
{
   hs.h = h;
   hs.rev_mean = 0.0;
   hs.rev_win = 0.0;
   hs.rev_n = 0;
   hs.cont_mean = 0.0;
   hs.cont_win = 0.0;
   hs.cont_n = 0;

   DAL_M0001HorizonOne(reversal_pairs, bars, bars_count, analysis_start_index, h, hs.rev_mean, hs.rev_win, hs.rev_n);
   DAL_M0001HorizonOne(continuation_pairs, bars, bars_count, analysis_start_index, h, hs.cont_mean, hs.cont_win, hs.cont_n);

   hs.cont_minus_rev = hs.cont_mean - hs.rev_mean;
   hs.cont_over_rev = DAL_M0003SafeRatio(hs.cont_mean, hs.rev_mean);
   hs.rev_carry = DAL_M0003SafeRatio(hs.rev_mean, reversal_stats.log_mean);
   hs.cont_carry = DAL_M0003SafeRatio(hs.cont_mean, continuation_stats.log_mean);
   hs.cont_minus_rev_carry = hs.cont_carry - hs.rev_carry;
}

void DAL_M0003ComputeRunStats(const DALM0001PairedLogRtv &pairs[], const double percentile, DALM0003RunStats &stats)
{
   int count = ArraySize(pairs);
   stats.n = count;
   stats.threshold = 0.0;
   stats.high_pct = 0.0;
   stats.run_count = 0;
   stats.max_run = 0;
   stats.avg_run = 0.0;
   stats.iid_expected_avg_run = 0.0;
   stats.avg_run_over_iid = 0.0;
   if(count <= 0)
      return;

   double deltas[];
   DAL_M0003Deltas(pairs, deltas);
   ArraySort(deltas);
   stats.threshold = DAL_M0001NullPercentileSorted(deltas, percentile);

   int high_count = 0;
   int current_run = 0;
   int run_total = 0;
   for(int i = 0; i < count; i++)
   {
      bool high = pairs[i].delta_log > stats.threshold;
      if(high)
      {
         high_count++;
         current_run++;
      }
      else
      {
         if(current_run > 0)
         {
            stats.run_count++;
            run_total += current_run;
            if(current_run > stats.max_run)
               stats.max_run = current_run;
         }
         current_run = 0;
      }
   }
   if(current_run > 0)
   {
      stats.run_count++;
      run_total += current_run;
      if(current_run > stats.max_run)
         stats.max_run = current_run;
   }

   stats.high_pct = 100.0 * high_count / count;
   stats.avg_run = stats.run_count > 0 ? run_total / (double)stats.run_count : 0.0;

   double p_high = high_count / (double)count;
   if(p_high > 0.0 && p_high < 1.0)
      stats.iid_expected_avg_run = 1.0 / (1.0 - p_high);
   stats.avg_run_over_iid = DAL_M0003SafeRatio(stats.avg_run, stats.iid_expected_avg_run);
}

void DAL_M0003ComputeRunStatsFromSampledFlags(
   const DALM0001PairedLogRtv &pairs[],
   const double threshold,
   const int iter,
   int &max_run,
   double &avg_run
)
{
   int count = ArraySize(pairs);
   max_run = 0;
   avg_run = 0.0;
   if(count <= 0)
      return;

   int perm[];
   DAL_M0003BuildPermutation(count, iter, 7703, perm);

   int current_run = 0;
   int run_count = 0;
   int run_total = 0;
   for(int i = 0; i < count; i++)
   {
      int j = perm[i];
      bool high = pairs[j].delta_log > threshold;
      if(high)
      {
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

   avg_run = run_count > 0 ? run_total / (double)run_count : 0.0;
}

string DAL_M0003EventText(
   const DALM0002Audit &audit,
   const DALM0001LogRtvStats &reversal_stats,
   const DALM0001LogRtvStats &continuation_stats
)
{
   return "EVENT_INERTIA"
      + "*paired=" + IntegerToString(audit.paired_count)
      + "*reversalN=" + IntegerToString(audit.reversal_count)
      + "*continuationN=" + IntegerToString(audit.continuation_count)
      + "*reversalPct=" + DAL_M0001FmtPct(audit.paired_count > 0 ? 100.0 * audit.reversal_count / audit.paired_count : 0.0)
      + "*continuationPct=" + DAL_M0001FmtPct(audit.paired_count > 0 ? 100.0 * audit.continuation_count / audit.paired_count : 0.0)
      + "*revEventDLog=" + DAL_M0001Fmt4(reversal_stats.log_mean)
      + "*contEventDLog=" + DAL_M0001Fmt4(continuation_stats.log_mean)
      + "*contMinusRevEventDLog=" + DAL_M0001Fmt4(continuation_stats.log_mean - reversal_stats.log_mean)
      + "*contOverRevEventRatio=" + DAL_M0001Fmt4(MathExp(continuation_stats.log_mean - reversal_stats.log_mean))
      + "*revRawMean=" + DAL_M0001Fmt4(reversal_stats.raw_mean)
      + "*contRawMean=" + DAL_M0001Fmt4(continuation_stats.raw_mean)
      + "*revRawMed=" + DAL_M0001Fmt4(reversal_stats.raw_median)
      + "*contRawMed=" + DAL_M0001Fmt4(continuation_stats.raw_median);
}

string DAL_M0003TailText(const DALM0001LogRtvStats &reversal_stats, const DALM0001LogRtvStats &continuation_stats)
{
   return "TAIL_INERTIA"
      + "*revP90=" + DAL_M0001Fmt4(reversal_stats.raw_p90)
      + "*contP90=" + DAL_M0001Fmt4(continuation_stats.raw_p90)
      + "*contOverRevP90=" + DAL_M0001Fmt4(DAL_M0003SafeRatio(continuation_stats.raw_p90, reversal_stats.raw_p90))
      + "*revP95=" + DAL_M0001Fmt4(reversal_stats.raw_p95)
      + "*contP95=" + DAL_M0001Fmt4(continuation_stats.raw_p95)
      + "*contOverRevP95=" + DAL_M0001Fmt4(DAL_M0003SafeRatio(continuation_stats.raw_p95, reversal_stats.raw_p95))
      + "*revCVaR90=" + DAL_M0001Fmt4(reversal_stats.raw_cvar90)
      + "*contCVaR90=" + DAL_M0001Fmt4(continuation_stats.raw_cvar90)
      + "*contOverRevCVaR90=" + DAL_M0001Fmt4(DAL_M0003SafeRatio(continuation_stats.raw_cvar90, reversal_stats.raw_cvar90))
      + "*revCVaR95=" + DAL_M0001Fmt4(reversal_stats.raw_cvar95)
      + "*contCVaR95=" + DAL_M0001Fmt4(continuation_stats.raw_cvar95)
      + "*contOverRevCVaR95=" + DAL_M0001Fmt4(DAL_M0003SafeRatio(continuation_stats.raw_cvar95, reversal_stats.raw_cvar95))
      + "*tailModel=" + (continuation_stats.raw_cvar95 > reversal_stats.raw_cvar95 ? "continuation_fatter_right_tail" : "mixed_or_no_continuation_tail_advantage");
}

string DAL_M0003MemoryHorizonText(
   const int h,
   const DALM0001LogRtvStats &reversal_stats,
   const DALM0001LogRtvStats &continuation_stats,
   const DALM0001PairedLogRtv &reversal_pairs[],
   const DALM0001PairedLogRtv &continuation_pairs[],
   const DALBar &bars[],
   const int bars_count,
   const int analysis_start_index
)
{
   DALM0003HorizonStats hs;
   DAL_M0003ComputeHorizonStats(h, reversal_stats, continuation_stats, reversal_pairs, continuation_pairs, bars, bars_count, analysis_start_index, hs);
   return "MEMORY_HORIZON"
      + "*h=" + IntegerToString(h)
      + "*revN=" + IntegerToString(hs.rev_n)
      + "*contN=" + IntegerToString(hs.cont_n)
      + "*revDLog=" + DAL_M0001Fmt4(hs.rev_mean)
      + "*contDLog=" + DAL_M0001Fmt4(hs.cont_mean)
      + "*contMinusRev=" + DAL_M0001Fmt4(hs.cont_minus_rev)
      + "*contOverRev=" + DAL_M0001Fmt4(hs.cont_over_rev)
      + "*revCarry=" + DAL_M0001Fmt4(hs.rev_carry)
      + "*contCarry=" + DAL_M0001Fmt4(hs.cont_carry)
      + "*contMinusRevCarry=" + DAL_M0001Fmt4(hs.cont_minus_rev_carry)
      + "*revWin=" + DAL_M0001FmtPct(hs.rev_win)
      + "*contWin=" + DAL_M0001FmtPct(hs.cont_win)
      + "*memorySide=" + (hs.cont_mean > hs.rev_mean ? "continuation" : "reversal_or_mixed");
}

string DAL_M0003MemorySummaryText(
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
   int hs_in[4];
   hs_in[0] = config.horizon_bars_1;
   hs_in[1] = config.horizon_bars_2;
   hs_in[2] = config.horizon_bars_3;
   hs_in[3] = config.horizon_bars_4;

   int cont_higher = 0;
   int cont_higher_carry = 0;
   double rev_auc = 0.0;
   double cont_auc = 0.0;
   double rev_carry_auc = 0.0;
   double cont_carry_auc = 0.0;
   int valid = 0;
   for(int i = 0; i < 4; i++)
   {
      DALM0003HorizonStats hs;
      DAL_M0003ComputeHorizonStats(hs_in[i], reversal_stats, continuation_stats, reversal_pairs, continuation_pairs, bars, bars_count, analysis_start_index, hs);
      if(hs.rev_n > 0 && hs.cont_n > 0)
      {
         valid++;
         rev_auc += hs.rev_mean;
         cont_auc += hs.cont_mean;
         rev_carry_auc += hs.rev_carry;
         cont_carry_auc += hs.cont_carry;
         if(hs.cont_mean > hs.rev_mean)
            cont_higher++;
         if(hs.cont_carry > hs.rev_carry)
            cont_higher_carry++;
      }
   }

   string memory_model = "mixed_or_unavailable_memory";
   if(cont_higher == valid && valid > 0 && cont_higher_carry >= 2)
      memory_model = "continuation_higher_inertia_and_memory_all_tested_horizons";
   else if(cont_higher >= 2)
      memory_model = "continuation_higher_inertia_most_horizons";

   return "MEMORY_SUMMARY"
      + "*testedHorizons=" + IntegerToString(valid)
      + "*continuationHigherHorizons=" + IntegerToString(cont_higher)
      + "*continuationHigherCarryHorizons=" + IntegerToString(cont_higher_carry)
      + "*revHorizonAuc=" + DAL_M0001Fmt4(rev_auc)
      + "*contHorizonAuc=" + DAL_M0001Fmt4(cont_auc)
      + "*contMinusRevHorizonAuc=" + DAL_M0001Fmt4(cont_auc - rev_auc)
      + "*contOverRevHorizonAuc=" + DAL_M0001Fmt4(DAL_M0003SafeRatio(cont_auc, rev_auc))
      + "*revCarryAuc=" + DAL_M0001Fmt4(rev_carry_auc)
      + "*contCarryAuc=" + DAL_M0001Fmt4(cont_carry_auc)
      + "*contMinusRevCarryAuc=" + DAL_M0001Fmt4(cont_carry_auc - rev_carry_auc)
      + "*memoryModel=" + memory_model;
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

string DAL_M0003ClusterCompareText(const DALM0001PairedLogRtv &reversal_pairs[], const DALM0001PairedLogRtv &continuation_pairs[])
{
   int rev_day_n = 0, cont_day_n = 0, rev_week_n = 0, cont_week_n = 0;
   double rev_day_mean = 0.0, rev_day_t = 0.0, rev_day_p = 1.0;
   double cont_day_mean = 0.0, cont_day_t = 0.0, cont_day_p = 1.0;
   double rev_week_mean = 0.0, rev_week_t = 0.0, rev_week_p = 1.0;
   double cont_week_mean = 0.0, cont_week_t = 0.0, cont_week_p = 1.0;
   DAL_M0001ClusterTStats(reversal_pairs, 86400, rev_day_n, rev_day_mean, rev_day_t, rev_day_p);
   DAL_M0001ClusterTStats(continuation_pairs, 86400, cont_day_n, cont_day_mean, cont_day_t, cont_day_p);
   DAL_M0001ClusterTStats(reversal_pairs, 604800, rev_week_n, rev_week_mean, rev_week_t, rev_week_p);
   DAL_M0001ClusterTStats(continuation_pairs, 604800, cont_week_n, cont_week_mean, cont_week_t, cont_week_p);

   double rev_lag1 = DAL_M0003LagCorr(reversal_pairs, 1);
   double cont_lag1 = DAL_M0003LagCorr(continuation_pairs, 1);
   double rev_lag2 = DAL_M0003LagCorr(reversal_pairs, 2);
   double cont_lag2 = DAL_M0003LagCorr(continuation_pairs, 2);

   string cluster_side = "mixed_cluster_strength";
   if(cont_lag1 > rev_lag1 && cont_lag2 > rev_lag2 && cont_day_mean > rev_day_mean && cont_week_mean > rev_week_mean)
      cluster_side = "continuation_stronger_cluster_memory";

   return "CLUSTER_COMPARE"
      + "*revLag1=" + DAL_M0001Fmt4(rev_lag1)
      + "*contLag1=" + DAL_M0001Fmt4(cont_lag1)
      + "*contMinusRevLag1=" + DAL_M0001Fmt4(cont_lag1 - rev_lag1)
      + "*revLag2=" + DAL_M0001Fmt4(rev_lag2)
      + "*contLag2=" + DAL_M0001Fmt4(cont_lag2)
      + "*contMinusRevLag2=" + DAL_M0001Fmt4(cont_lag2 - rev_lag2)
      + "*revDayMean=" + DAL_M0001Fmt4(rev_day_mean)
      + "*contDayMean=" + DAL_M0001Fmt4(cont_day_mean)
      + "*contMinusRevDayMean=" + DAL_M0001Fmt4(cont_day_mean - rev_day_mean)
      + "*revWeekMean=" + DAL_M0001Fmt4(rev_week_mean)
      + "*contWeekMean=" + DAL_M0001Fmt4(cont_week_mean)
      + "*contMinusRevWeekMean=" + DAL_M0001Fmt4(cont_week_mean - rev_week_mean)
      + "*clusterSide=" + cluster_side;
}

string DAL_M0003BranchClusterPermStressText(
   const DALM0001PairedLogRtv &reversal_pairs[],
   const DALM0001PairedLogRtv &continuation_pairs[],
   const int iterations
)
{
   int rev_n = ArraySize(reversal_pairs);
   int cont_n = ArraySize(continuation_pairs);
   int total = rev_n + cont_n;
   if(rev_n <= 5 || cont_n <= 5 || iterations <= 0)
      return "BRANCH_CLUSTER_PERM_STRESS*revN=" + IntegerToString(rev_n) + "*contN=" + IntegerToString(cont_n) + "*iters=0";

   double all[];
   ArrayResize(all, total);
   for(int i = 0; i < rev_n; i++)
      all[i] = reversal_pairs[i].delta_log;
   for(int i = 0; i < cont_n; i++)
      all[rev_n + i] = continuation_pairs[i].delta_log;

   double rev_values[];
   double cont_values[];
   ArrayResize(rev_values, rev_n);
   ArrayResize(cont_values, cont_n);

   double obs_diff_lag1 = DAL_M0003LagCorr(continuation_pairs, 1) - DAL_M0003LagCorr(reversal_pairs, 1);
   double obs_diff_lag2 = DAL_M0003LagCorr(continuation_pairs, 2) - DAL_M0003LagCorr(reversal_pairs, 2);

   int perm[];
   double sum1 = 0.0, sum2 = 0.0, sumsq1 = 0.0, sumsq2 = 0.0;
   int ge1 = 0, ge2 = 0;
   for(int iter = 0; iter < iterations; iter++)
   {
      DAL_M0003BuildPermutation(total, iter, 3301, perm);
      for(int i = 0; i < rev_n; i++)
         rev_values[i] = all[perm[i]];
      for(int i = 0; i < cont_n; i++)
         cont_values[i] = all[perm[rev_n + i]];

      double d1 = DAL_M0003LagCorrValues(cont_values, 1) - DAL_M0003LagCorrValues(rev_values, 1);
      double d2 = DAL_M0003LagCorrValues(cont_values, 2) - DAL_M0003LagCorrValues(rev_values, 2);
      if(d1 >= obs_diff_lag1) ge1++;
      if(d2 >= obs_diff_lag2) ge2++;
      sum1 += d1;
      sum2 += d2;
      sumsq1 += d1 * d1;
      sumsq2 += d2 * d2;
   }

   double mean1 = sum1 / iterations;
   double mean2 = sum2 / iterations;
   double sd1 = MathSqrt(MathMax(0.0, sumsq1 / iterations - mean1 * mean1));
   double sd2 = MathSqrt(MathMax(0.0, sumsq2 / iterations - mean2 * mean2));
   double z1 = sd1 > 0.0 ? (obs_diff_lag1 - mean1) / sd1 : 0.0;
   double z2 = sd2 > 0.0 ? (obs_diff_lag2 - mean2) / sd2 : 0.0;
   double p1 = (ge1 + 1.0) / (iterations + 1.0);
   double p2 = (ge2 + 1.0) / (iterations + 1.0);

   string verdict = "branch_cluster_difference_not_above_label_permutation";
   if(z1 > 2.0 && obs_diff_lag1 > 0.0)
      verdict = "continuation_cluster_memory_above_label_permutation";

   return "BRANCH_CLUSTER_PERM_STRESS"
      + "*revN=" + IntegerToString(rev_n)
      + "*contN=" + IntegerToString(cont_n)
      + "*iters=" + IntegerToString(iterations)
      + "*obsDiffLag1=" + DAL_M0001Fmt4(obs_diff_lag1)
      + "*permMeanDiffLag1=" + DAL_M0001Fmt4(mean1)
      + "*permSdDiffLag1=" + DAL_M0001Fmt4(sd1)
      + "*diffLag1Z=" + DAL_M0001Fmt4(z1)
      + "*diffLag1EmpP=" + DAL_M0001Fmt4(p1)
      + "*obsDiffLag2=" + DAL_M0001Fmt4(obs_diff_lag2)
      + "*permMeanDiffLag2=" + DAL_M0001Fmt4(mean2)
      + "*permSdDiffLag2=" + DAL_M0001Fmt4(sd2)
      + "*diffLag2Z=" + DAL_M0001Fmt4(z2)
      + "*diffLag2EmpP=" + DAL_M0001Fmt4(p2)
      + "*stressVerdict=" + verdict;
}

string DAL_M0003LagShuffleStressText(const DALM0001PairedLogRtv &pairs[], const string label, const int iterations)
{
   int count = ArraySize(pairs);
   if(count <= 5 || iterations <= 0)
      return "LAG_SHUFFLE_STRESS*branch=" + label + "*n=" + IntegerToString(count) + "*iters=0";

   double obs_lag1 = DAL_M0003LagCorr(pairs, 1);
   double obs_lag2 = DAL_M0003LagCorr(pairs, 2);
   double tmp[];
   ArrayResize(tmp, count);

   double sum1 = 0.0, sum2 = 0.0, sumsq1 = 0.0, sumsq2 = 0.0;
   int ge1 = 0, ge2 = 0;
   int perm[];
   for(int iter = 0; iter < iterations; iter++)
   {
      DAL_M0003BuildPermutation(count, iter, 1103, perm);
      for(int i = 0; i < count; i++)
         tmp[i] = pairs[perm[i]].delta_log;

      double l1 = DAL_M0003LagCorrValues(tmp, 1);
      double l2 = DAL_M0003LagCorrValues(tmp, 2);
      if(l1 >= obs_lag1) ge1++;
      if(l2 >= obs_lag2) ge2++;
      sum1 += l1;
      sum2 += l2;
      sumsq1 += l1 * l1;
      sumsq2 += l2 * l2;
   }

   double mean1 = sum1 / iterations;
   double mean2 = sum2 / iterations;
   double sd1 = MathSqrt(MathMax(0.0, sumsq1 / iterations - mean1 * mean1));
   double sd2 = MathSqrt(MathMax(0.0, sumsq2 / iterations - mean2 * mean2));
   double z1 = sd1 > 0.0 ? (obs_lag1 - mean1) / sd1 : 0.0;
   double z2 = sd2 > 0.0 ? (obs_lag2 - mean2) / sd2 : 0.0;
   double emp_p1 = (ge1 + 1.0) / (iterations + 1.0);
   double emp_p2 = (ge2 + 1.0) / (iterations + 1.0);

   string verdict = "serial_memory_not_above_shuffle";
   if(z1 > 2.0 && z2 > 1.0)
      verdict = "serial_memory_above_iid_shuffle";

   return "LAG_SHUFFLE_STRESS"
      + "*branch=" + label
      + "*n=" + IntegerToString(count)
      + "*iters=" + IntegerToString(iterations)
      + "*obsLag1=" + DAL_M0001Fmt4(obs_lag1)
      + "*shuffleMeanLag1=" + DAL_M0001Fmt4(mean1)
      + "*shuffleSdLag1=" + DAL_M0001Fmt4(sd1)
      + "*lag1Z=" + DAL_M0001Fmt4(z1)
      + "*lag1EmpP=" + DAL_M0001Fmt4(emp_p1)
      + "*obsLag2=" + DAL_M0001Fmt4(obs_lag2)
      + "*shuffleMeanLag2=" + DAL_M0001Fmt4(mean2)
      + "*shuffleSdLag2=" + DAL_M0001Fmt4(sd2)
      + "*lag2Z=" + DAL_M0001Fmt4(z2)
      + "*lag2EmpP=" + DAL_M0001Fmt4(emp_p2)
      + "*stressVerdict=" + verdict;
}

string DAL_M0003BlockStressText(const DALM0001PairedLogRtv &pairs[], const string label, const int block_size)
{
   int count = ArraySize(pairs);
   int bs = block_size;
   if(bs < 2)
      bs = 2;
   if(count < bs * 2)
      return "BLOCK_CLUSTER_STRESS*branch=" + label + "*n=" + IntegerToString(count) + "*blockSize=" + IntegerToString(bs) + "*blocks=0";

   int blocks = (count + bs - 1) / bs;
   double means[];
   ArrayResize(means, blocks);
   int valid = 0;
   for(int start = 0; start < count; start += bs)
   {
      int end = start + bs;
      if(end > count)
         end = count;
      int n = end - start;
      if(n <= 0)
         continue;
      double sum = 0.0;
      for(int i = start; i < end; i++)
         sum += pairs[i].delta_log;
      means[valid] = sum / n;
      valid++;
   }
   ArrayResize(means, valid);

   double mean = 0.0;
   double min_mean = DBL_MAX;
   int positive = 0;
   for(int i = 0; i < valid; i++)
   {
      mean += means[i];
      if(means[i] < min_mean)
         min_mean = means[i];
      if(means[i] > 0.0)
         positive++;
   }
   mean = valid > 0 ? mean / valid : 0.0;

   double var = 0.0;
   for(int i = 0; i < valid; i++)
   {
      double d = means[i] - mean;
      var += d * d;
   }
   double sd = valid > 1 ? MathSqrt(var / (valid - 1)) : 0.0;
   double t = sd > 0.0 && valid > 1 ? mean / (sd / MathSqrt(valid)) : 0.0;

   string verdict = "positive_across_contiguous_blocks";
   if(mean <= 0.0 || positive < valid * 0.75)
      verdict = "weak_or_mixed_contiguous_blocks";

   return "BLOCK_CLUSTER_STRESS"
      + "*branch=" + label
      + "*n=" + IntegerToString(count)
      + "*blockSize=" + IntegerToString(bs)
      + "*blocks=" + IntegerToString(valid)
      + "*blockMean=" + DAL_M0001Fmt4(mean)
      + "*blockSd=" + DAL_M0001Fmt4(sd)
      + "*blockT=" + DAL_M0001Fmt4(t)
      + "*blockMin=" + DAL_M0001Fmt4(min_mean == DBL_MAX ? 0.0 : min_mean)
      + "*positiveBlockPct=" + DAL_M0001FmtPct(valid > 0 ? 100.0 * positive / valid : 0.0)
      + "*stressVerdict=" + verdict;
}

string DAL_M0003HighRunText(const DALM0001PairedLogRtv &pairs[], const string label, const double percentile)
{
   DALM0003RunStats rs;
   DAL_M0003ComputeRunStats(pairs, percentile, rs);
   return "HIGH_RUNS"
      + "*branch=" + label
      + "*n=" + IntegerToString(rs.n)
      + "*thresholdPct=" + DAL_M0001FmtPct(100.0 * percentile)
      + "*thresholdDelta=" + DAL_M0001Fmt4(rs.threshold)
      + "*gtThresholdPct=" + DAL_M0001FmtPct(rs.high_pct)
      + "*runCount=" + IntegerToString(rs.run_count)
      + "*maxRun=" + IntegerToString(rs.max_run)
      + "*avgRun=" + DAL_M0001Fmt4(rs.avg_run)
      + "*iidExpectedAvgRun=" + DAL_M0001Fmt4(rs.iid_expected_avg_run)
      + "*avgRunOverIid=" + DAL_M0001Fmt4(rs.avg_run_over_iid);
}

string DAL_M0003RunShuffleStressText(const DALM0001PairedLogRtv &pairs[], const string label, const double percentile, const int iterations)
{
   int count = ArraySize(pairs);
   if(count <= 0 || iterations <= 0)
      return "RUN_SHUFFLE_STRESS*branch=" + label + "*n=" + IntegerToString(count) + "*iters=0";

   DALM0003RunStats obs;
   DAL_M0003ComputeRunStats(pairs, percentile, obs);

   double max_sum = 0.0, max_sumsq = 0.0;
   double avg_sum = 0.0, avg_sumsq = 0.0;
   int max_ge = 0, avg_ge = 0;
   for(int iter = 0; iter < iterations; iter++)
   {
      int max_run = 0;
      double avg_run = 0.0;
      DAL_M0003ComputeRunStatsFromSampledFlags(pairs, obs.threshold, iter, max_run, avg_run);
      if(max_run >= obs.max_run) max_ge++;
      if(avg_run >= obs.avg_run) avg_ge++;
      max_sum += max_run;
      max_sumsq += max_run * max_run;
      avg_sum += avg_run;
      avg_sumsq += avg_run * avg_run;
   }

   double max_mean = max_sum / iterations;
   double avg_mean = avg_sum / iterations;
   double max_sd = MathSqrt(MathMax(0.0, max_sumsq / iterations - max_mean * max_mean));
   double avg_sd = MathSqrt(MathMax(0.0, avg_sumsq / iterations - avg_mean * avg_mean));
   double max_z = max_sd > 0.0 ? (obs.max_run - max_mean) / max_sd : 0.0;
   double avg_z = avg_sd > 0.0 ? (obs.avg_run - avg_mean) / avg_sd : 0.0;
   double max_emp_p = (max_ge + 1.0) / (iterations + 1.0);
   double avg_emp_p = (avg_ge + 1.0) / (iterations + 1.0);

   string verdict = "high_run_not_above_iid_shuffle";
   if(max_z > 2.0 || avg_z > 2.0)
      verdict = "high_run_clustering_above_iid_shuffle";

   return "RUN_SHUFFLE_STRESS"
      + "*branch=" + label
      + "*n=" + IntegerToString(count)
      + "*iters=" + IntegerToString(iterations)
      + "*thresholdPct=" + DAL_M0001FmtPct(100.0 * percentile)
      + "*obsMaxRun=" + IntegerToString(obs.max_run)
      + "*shuffleMaxRunMean=" + DAL_M0001Fmt4(max_mean)
      + "*shuffleMaxRunSd=" + DAL_M0001Fmt4(max_sd)
      + "*maxRunZ=" + DAL_M0001Fmt4(max_z)
      + "*maxRunEmpP=" + DAL_M0001Fmt4(max_emp_p)
      + "*obsAvgRun=" + DAL_M0001Fmt4(obs.avg_run)
      + "*shuffleAvgRunMean=" + DAL_M0001Fmt4(avg_mean)
      + "*shuffleAvgRunSd=" + DAL_M0001Fmt4(avg_sd)
      + "*avgRunZ=" + DAL_M0001Fmt4(avg_z)
      + "*avgRunEmpP=" + DAL_M0001Fmt4(avg_emp_p)
      + "*stressVerdict=" + verdict;
}

string DAL_M0003RunCompareText(const DALM0001PairedLogRtv &reversal_pairs[], const DALM0001PairedLogRtv &continuation_pairs[], const double percentile)
{
   DALM0003RunStats rev;
   DALM0003RunStats cont;
   DAL_M0003ComputeRunStats(reversal_pairs, percentile, rev);
   DAL_M0003ComputeRunStats(continuation_pairs, percentile, cont);

   string run_side = "mixed_run_clustering";
   if(cont.max_run > rev.max_run && cont.avg_run > rev.avg_run)
      run_side = "continuation_longer_high_volatility_runs";

   return "RUN_COMPARE"
      + "*thresholdPct=" + DAL_M0001FmtPct(100.0 * percentile)
      + "*revMaxRun=" + IntegerToString(rev.max_run)
      + "*contMaxRun=" + IntegerToString(cont.max_run)
      + "*contMinusRevMaxRun=" + IntegerToString(cont.max_run - rev.max_run)
      + "*revAvgRun=" + DAL_M0001Fmt4(rev.avg_run)
      + "*contAvgRun=" + DAL_M0001Fmt4(cont.avg_run)
      + "*contMinusRevAvgRun=" + DAL_M0001Fmt4(cont.avg_run - rev.avg_run)
      + "*contOverRevAvgRun=" + DAL_M0001Fmt4(DAL_M0003SafeRatio(cont.avg_run, rev.avg_run))
      + "*revAvgRunOverIid=" + DAL_M0001Fmt4(rev.avg_run_over_iid)
      + "*contAvgRunOverIid=" + DAL_M0001Fmt4(cont.avg_run_over_iid)
      + "*runSide=" + run_side;
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
   const DALM0002Config &config,
   const DALM0003Config &h3_config
)
{
   int analysis_start_index = DAL_M0001FirstIndexAtOrAfter(bars, bars_count, min_entry_time);
   int hs_in[4];
   hs_in[0] = config.horizon_bars_1;
   hs_in[1] = config.horizon_bars_2;
   hs_in[2] = config.horizon_bars_3;
   hs_in[3] = config.horizon_bars_4;

   int cont_higher = 0;
   int cont_higher_carry = 0;
   for(int i = 0; i < 4; i++)
   {
      DALM0003HorizonStats hs;
      DAL_M0003ComputeHorizonStats(hs_in[i], reversal_stats, continuation_stats, reversal_pairs, continuation_pairs, bars, bars_count, analysis_start_index, hs);
      if(hs.rev_n > 0 && hs.cont_n > 0 && hs.cont_mean > hs.rev_mean)
         cont_higher++;
      if(hs.rev_n > 0 && hs.cont_n > 0 && hs.cont_carry > hs.rev_carry)
         cont_higher_carry++;
   }

   DALM0003RunStats rev_run;
   DALM0003RunStats cont_run;
   DAL_M0003ComputeRunStats(reversal_pairs, h3_config.high_run_percentile, rev_run);
   DAL_M0003ComputeRunStats(continuation_pairs, h3_config.high_run_percentile, cont_run);

   double rev_lag1 = DAL_M0003LagCorr(reversal_pairs, 1);
   double cont_lag1 = DAL_M0003LagCorr(continuation_pairs, 1);
   double rev_lag2 = DAL_M0003LagCorr(reversal_pairs, 2);
   double cont_lag2 = DAL_M0003LagCorr(continuation_pairs, 2);

   string summary = "mixed_h3";
   bool lower_freq = audit.reversal_count > audit.continuation_count;
   bool higher_event = continuation_stats.log_mean > reversal_stats.log_mean;
   bool higher_memory = cont_higher >= 2;
   bool fatter_tail = continuation_stats.raw_cvar95 > reversal_stats.raw_cvar95;
   bool stronger_cluster = (cont_lag1 > rev_lag1 && cont_lag2 > rev_lag2);
   bool longer_runs = (cont_run.max_run > rev_run.max_run && cont_run.avg_run > rev_run.avg_run);

   if(lower_freq && higher_event && higher_memory)
      summary = "continuation_lower_frequency_higher_zone_volatility_higher_inertia_memory";
   if(lower_freq && higher_event && higher_memory && fatter_tail)
      summary = "continuation_lower_frequency_higher_zone_volatility_higher_inertia_memory_fatter_tail";
   if(lower_freq && higher_event && higher_memory && fatter_tail && stronger_cluster && longer_runs)
      summary = "continuation_lower_frequency_higher_zone_volatility_higher_inertia_memory_fatter_tail_stronger_cluster_runs";

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
      + "*continuationHigherCarryHorizons=" + IntegerToString(cont_higher_carry)
      + "*contMinusRevLag1=" + DAL_M0001Fmt4(cont_lag1 - rev_lag1)
      + "*contMinusRevLag2=" + DAL_M0001Fmt4(cont_lag2 - rev_lag2)
      + "*contMinusRevMaxRun=" + IntegerToString(cont_run.max_run - rev_run.max_run)
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
   const DALM0002Config &config,
   const DALM0003Config &h3_config
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

   int analysis_start_index = DAL_M0001FirstIndexAtOrAfter(bars, bars_count, min_entry_time);

   int hs[4];
   hs[0] = config.horizon_bars_1;
   hs[1] = config.horizon_bars_2;
   hs[2] = config.horizon_bars_3;
   hs[3] = config.horizon_bars_4;

   Print(DAL_M0003Prefix("DAL_M0003_FINAL_AUDIT", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0002AuditText(audit, config));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_SUMMARY", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003SummaryText(audit, reversal_stats, continuation_stats, reversal_pairs, continuation_pairs, bars, bars_count, min_entry_time, config, h3_config));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_EVENT_INERTIA", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003EventText(audit, reversal_stats, continuation_stats));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_TAIL_INERTIA", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003TailText(reversal_stats, continuation_stats));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_MEMORY_SUMMARY", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003MemorySummaryText(reversal_stats, continuation_stats, reversal_pairs, continuation_pairs, bars, bars_count, min_entry_time, config));

   for(int i = 0; i < 4; i++)
      Print(DAL_M0003Prefix("DAL_M0003_FINAL_MEMORY_H" + IntegerToString(hs[i]), symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003MemoryHorizonText(hs[i], reversal_stats, continuation_stats, reversal_pairs, continuation_pairs, bars, bars_count, analysis_start_index));

   Print(DAL_M0003Prefix("DAL_M0003_FINAL_REVERSAL_CLUSTER", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003ClusterText(reversal_pairs, "REVERSAL"));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_CONTINUATION_CLUSTER", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003ClusterText(continuation_pairs, "CONTINUATION"));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_CLUSTER_COMPARE", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003ClusterCompareText(reversal_pairs, continuation_pairs));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_BRANCH_CLUSTER_PERM_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003BranchClusterPermStressText(reversal_pairs, continuation_pairs, h3_config.cluster_stress_iterations));

   Print(DAL_M0003Prefix("DAL_M0003_FINAL_REVERSAL_LAG_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003LagShuffleStressText(reversal_pairs, "REVERSAL", h3_config.cluster_stress_iterations));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_CONTINUATION_LAG_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003LagShuffleStressText(continuation_pairs, "CONTINUATION", h3_config.cluster_stress_iterations));

   Print(DAL_M0003Prefix("DAL_M0003_FINAL_REVERSAL_BLOCK_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003BlockStressText(reversal_pairs, "REVERSAL", h3_config.cluster_block_size));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_CONTINUATION_BLOCK_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003BlockStressText(continuation_pairs, "CONTINUATION", h3_config.cluster_block_size));

   Print(DAL_M0003Prefix("DAL_M0003_FINAL_REVERSAL_HIGH_RUNS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003HighRunText(reversal_pairs, "REVERSAL", h3_config.high_run_percentile));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_CONTINUATION_HIGH_RUNS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003HighRunText(continuation_pairs, "CONTINUATION", h3_config.high_run_percentile));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_RUN_COMPARE", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003RunCompareText(reversal_pairs, continuation_pairs, h3_config.high_run_percentile));

   Print(DAL_M0003Prefix("DAL_M0003_FINAL_REVERSAL_RUN_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003RunShuffleStressText(reversal_pairs, "REVERSAL", h3_config.high_run_percentile, h3_config.cluster_stress_iterations));
   Print(DAL_M0003Prefix("DAL_M0003_FINAL_CONTINUATION_RUN_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0003RunShuffleStressText(continuation_pairs, "CONTINUATION", h3_config.high_run_percentile, h3_config.cluster_stress_iterations));
}

#endif
