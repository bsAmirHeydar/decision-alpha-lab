#ifndef __DAL_M0001_RTV_NULL_COMPARISON_MQH__
#define __DAL_M0001_RTV_NULL_COMPARISON_MQH__

#include <DecisionAlphaLab/Common/DAL_Math.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Types.mqh>

struct DALM0001RtvReportConfig
{
   bool print_histogram;
   int random_samples_per_event;
   int bootstrap_iterations;
   int permutation_iterations;
   int validation_splits;
};

struct DALM0001PairedLogRtv
{
   int event_id;
   int sample_length;
   datetime entry_time;
   double node_log;
   double random_log;
   double delta_log;
};

struct DALM0001LogRtvStats
{
   int count;

   double raw_mean;
   double raw_median;
   double raw_p75;
   double raw_p90;
   double raw_p95;
   double raw_cvar90;
   double raw_cvar95;

   double log_mean;
   double log_median;
   double log_stdev;
   double log_p05;
   double log_p25;
   double log_p75;
   double log_p90;
   double log_p95;
   double log_iqr;

   double log_skewness;
   double log_excess_kurtosis;
   double log_jarque_bera;
   double log_ks_normal;

   double pct_log_gt_zero;
   double tail2_pct;
   double tail3_pct;
   double tail2_ratio_normal;
   double tail3_ratio_normal;
};

struct DALM0001LogRtvComparison
{
   int paired_count;

   double delta_log_mean;
   double delta_log_median;
   double delta_pct_log_gt_zero;
   double geo_ratio;
   double median_ratio;

   double paired_win_pct;
   double paired_mean_delta;
   double paired_median_delta;
   double paired_t_stat;
   double paired_t_p_approx;
   double cohen_d;
   double sign_test_p_approx;

   double cliff_delta;
   double ks_real_vs_random;
   double cvm_real_vs_random;
   double wasserstein_log;

   double delta_raw_q50;
   double delta_raw_q75;
   double delta_raw_q90;
   double delta_raw_q95;
   double delta_raw_cvar90;
   double delta_raw_cvar95;
   double right_tail_odds_ratio;
};

struct DALM0001RobustnessStats
{
   int bootstrap_iterations;
   int permutation_iterations;
   int validation_splits;

   double boot_mean_delta_low95;
   double boot_mean_delta_high95;
   double boot_win_pct_low95;
   double boot_win_pct_high95;
   double permutation_p;

   int split_valid_count;
   double split_positive_pct;
   double split_min_delta_log_mean;
   double split_mean_delta_log_mean;
   double split_stdev_delta_log_mean;
   double split_min_win_pct;
   double stability_score;
};

struct DALM0001IntegrityAudit
{
   int closed_events;
   int events_after_analysis_start;
   int rtv_ready_events;
   int paired_events;
   int full_baseline_events;
   int touch_confirmed_events;
   int warmup_excluded_events;
};

string DAL_M0001_NULL_LAST_SIGNATURE = "";

void DAL_M0001DefaultRtvReportConfig(DALM0001RtvReportConfig &config)
{
   config.print_histogram = false;
   config.random_samples_per_event = 20;
   config.bootstrap_iterations = 300;
   config.permutation_iterations = 500;
   config.validation_splits = 5;
}

bool DAL_M0001NullValidNumber(const double value)
{
   if(!(value == value))
      return false;

   if(value == DBL_MAX || value == -DBL_MAX)
      return false;

   return true;
}

double DAL_M0001NullSafeDiv(const double numerator, const double denominator)
{
   if(MathAbs(denominator) <= DBL_EPSILON)
      return 0.0;

   return numerator / denominator;
}

int DAL_M0001IntMin(const int a, const int b)
{
   return (a < b ? a : b);
}

int DAL_M0001IntMax(const int a, const int b)
{
   return (a > b ? a : b);
}

int DAL_M0001FirstIndexAtOrAfter(
   const DALBar &bars[],
   const int bars_count,
   const datetime min_time
)
{
   if(min_time <= 0)
      return 0;

   for(int i = 0; i < bars_count; i++)
   {
      if(bars[i].time >= min_time)
         return i;
   }

   return bars_count;
}

bool DAL_M0001EventPassesAnalysisStart(
   const DALM0001Event &event,
   const datetime min_entry_time
)
{
   if(min_entry_time <= 0)
      return true;

   return event.entry_time >= min_entry_time;
}

string DAL_M0001AnalysisStartText(const datetime min_entry_time)
{
   if(min_entry_time <= 0)
      return "all";

   return TimeToString(min_entry_time, TIME_DATE | TIME_MINUTES);
}

double DAL_M0001NullPercentileSorted(const double &sorted[], const double percentile)
{
   int count = ArraySize(sorted);
   if(count <= 0)
      return 0.0;

   if(count == 1)
      return sorted[0];

   double p = percentile;
   if(p < 0.0)
      p = 0.0;
   if(p > 1.0)
      p = 1.0;

   double pos = (count - 1) * p;
   int lo = (int)MathFloor(pos);
   int hi = (int)MathCeil(pos);

   if(lo < 0)
      lo = 0;
   if(hi < 0)
      hi = 0;
   if(lo >= count)
      lo = count - 1;
   if(hi >= count)
      hi = count - 1;

   if(lo == hi)
      return sorted[lo];

   double weight = pos - lo;
   return sorted[lo] * (1.0 - weight) + sorted[hi] * weight;
}

double DAL_M0001NullNormalCdf(const double z)
{
   double x = z;
   double a = MathAbs(x);
   double t = 1.0 / (1.0 + 0.2316419 * a);

   double poly =
      0.319381530 * t
      - 0.356563782 * MathPow(t, 2)
      + 1.781477937 * MathPow(t, 3)
      - 1.821255978 * MathPow(t, 4)
      + 1.330274429 * MathPow(t, 5);

   double pdf = 0.3989422804014327 * MathExp(-0.5 * a * a);
   double cdf = 1.0 - pdf * poly;

   if(x < 0.0)
      return 1.0 - cdf;

   return cdf;
}

double DAL_M0001TwoSidedNormalP(const double z)
{
   double a = MathAbs(z);
   double p = 2.0 * (1.0 - DAL_M0001NullNormalCdf(a));
   if(p < 0.0)
      p = 0.0;
   if(p > 1.0)
      p = 1.0;
   return p;
}

void DAL_M0001NullResetStats(DALM0001LogRtvStats &stats)
{
   stats.count = 0;

   stats.raw_mean = 0.0;
   stats.raw_median = 0.0;
   stats.raw_p75 = 0.0;
   stats.raw_p90 = 0.0;
   stats.raw_p95 = 0.0;
   stats.raw_cvar90 = 0.0;
   stats.raw_cvar95 = 0.0;

   stats.log_mean = 0.0;
   stats.log_median = 0.0;
   stats.log_stdev = 0.0;
   stats.log_p05 = 0.0;
   stats.log_p25 = 0.0;
   stats.log_p75 = 0.0;
   stats.log_p90 = 0.0;
   stats.log_p95 = 0.0;
   stats.log_iqr = 0.0;

   stats.log_skewness = 0.0;
   stats.log_excess_kurtosis = 0.0;
   stats.log_jarque_bera = 0.0;
   stats.log_ks_normal = 0.0;

   stats.pct_log_gt_zero = 0.0;
   stats.tail2_pct = 0.0;
   stats.tail3_pct = 0.0;
   stats.tail2_ratio_normal = 0.0;
   stats.tail3_ratio_normal = 0.0;
}

void DAL_M0001ResetComparison(DALM0001LogRtvComparison &cmp)
{
   cmp.paired_count = 0;
   cmp.delta_log_mean = 0.0;
   cmp.delta_log_median = 0.0;
   cmp.delta_pct_log_gt_zero = 0.0;
   cmp.geo_ratio = 0.0;
   cmp.median_ratio = 0.0;
   cmp.paired_win_pct = 0.0;
   cmp.paired_mean_delta = 0.0;
   cmp.paired_median_delta = 0.0;
   cmp.paired_t_stat = 0.0;
   cmp.paired_t_p_approx = 1.0;
   cmp.cohen_d = 0.0;
   cmp.sign_test_p_approx = 1.0;
   cmp.cliff_delta = 0.0;
   cmp.ks_real_vs_random = 0.0;
   cmp.cvm_real_vs_random = 0.0;
   cmp.wasserstein_log = 0.0;
   cmp.delta_raw_q50 = 0.0;
   cmp.delta_raw_q75 = 0.0;
   cmp.delta_raw_q90 = 0.0;
   cmp.delta_raw_q95 = 0.0;
   cmp.delta_raw_cvar90 = 0.0;
   cmp.delta_raw_cvar95 = 0.0;
   cmp.right_tail_odds_ratio = 0.0;
}

void DAL_M0001ResetRobustness(DALM0001RobustnessStats &rob)
{
   rob.bootstrap_iterations = 0;
   rob.permutation_iterations = 0;
   rob.validation_splits = 0;
   rob.boot_mean_delta_low95 = 0.0;
   rob.boot_mean_delta_high95 = 0.0;
   rob.boot_win_pct_low95 = 0.0;
   rob.boot_win_pct_high95 = 0.0;
   rob.permutation_p = 1.0;
   rob.split_valid_count = 0;
   rob.split_positive_pct = 0.0;
   rob.split_min_delta_log_mean = 0.0;
   rob.split_mean_delta_log_mean = 0.0;
   rob.split_stdev_delta_log_mean = 0.0;
   rob.split_min_win_pct = 0.0;
   rob.stability_score = 0.0;
}

void DAL_M0001ResetIntegrityAudit(DALM0001IntegrityAudit &audit)
{
   audit.closed_events = 0;
   audit.events_after_analysis_start = 0;
   audit.rtv_ready_events = 0;
   audit.paired_events = 0;
   audit.full_baseline_events = 0;
   audit.touch_confirmed_events = 0;
   audit.warmup_excluded_events = 0;
}

double DAL_M0001MeanLogMoveWindow(
   const DALBar &bars[],
   const int bars_count,
   const int start,
   const int length
)
{
   if(length <= 0)
      return 0.0;

   if(start < 0 || start + length > bars_count)
      return 0.0;

   double total = 0.0;
   int used = 0;

   for(int i = 0; i < length; i++)
   {
      int idx = start + i;
      double v = DAL_LogRange(bars[idx].high, bars[idx].low);

      if(!DAL_M0001NullValidNumber(v))
         continue;

      total += v;
      used++;
   }

   if(used <= 0)
      return 0.0;

   return total / used;
}

double DAL_M0001RandomFractionK(
   const int event_id,
   const int sample_length,
   const int bars_count,
   const int k
)
{
   double x = MathSin((event_id + 1) * 12.9898 + (sample_length + 3) * 78.233 + bars_count * 0.0174532925199433 + (k + 1) * 19.191919) * 43758.5453123;
   return x - MathFloor(x);
}

bool DAL_M0001RandomLogForEvent(
   const DALM0001Event &event,
   const DALBar &bars[],
   const int bars_count,
   const int analysis_start_index,
   const int random_k,
   double &random_log
)
{
   random_log = 0.0;

   int n = event.rtv_sample_length;
   if(n <= 0)
      return false;

   int min_entry = DAL_M0001IntMax(n, analysis_start_index);
   int max_entry = bars_count - n;
   if(max_entry < min_entry)
      return false;

   int k_count = random_k;
   if(k_count <= 0)
      k_count = 1;

   int valid = 0;
   double total = 0.0;
   int span = max_entry - min_entry + 1;

   for(int k = 0; k < k_count; k++)
   {
      double frac = DAL_M0001RandomFractionK(event.id, n, bars_count, k);
      int random_entry = min_entry + (int)MathFloor(frac * span);

      if(random_entry < min_entry)
         random_entry = min_entry;
      if(random_entry > max_entry)
         random_entry = max_entry;

      double mean_inside = DAL_M0001MeanLogMoveWindow(bars, bars_count, random_entry, n);
      double mean_before = DAL_M0001MeanLogMoveWindow(bars, bars_count, random_entry - n, n);

      if(mean_inside <= 0.0 || mean_before <= 0.0)
         continue;

      double rtv = mean_inside / mean_before;
      if(rtv <= 0.0 || !DAL_M0001NullValidNumber(rtv))
         continue;

      total += MathLog(rtv);
      valid++;
   }

   if(valid <= 0)
      return false;

   random_log = total / valid;
   return true;
}

int DAL_M0001CollectPairedLogRtvs(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const datetime min_entry_time,
   const int random_k,
   DALM0001PairedLogRtv &pairs[],
   double &node_logs[],
   double &random_logs[],
   DALM0001IntegrityAudit &audit
)
{
   ArrayResize(pairs, 0);
   ArrayResize(node_logs, 0);
   ArrayResize(random_logs, 0);
   DAL_M0001ResetIntegrityAudit(audit);

   int analysis_start_index = DAL_M0001FirstIndexAtOrAfter(bars, bars_count, min_entry_time);

   for(int i = 0; i < events_count; i++)
   {
      if(events[i].closed)
         audit.closed_events++;

      if(events[i].closed && !DAL_M0001EventPassesAnalysisStart(events[i], min_entry_time))
         audit.warmup_excluded_events++;

      if(!events[i].closed)
         continue;

      if(!DAL_M0001EventPassesAnalysisStart(events[i], min_entry_time))
         continue;

      audit.events_after_analysis_start++;

      if(events[i].touch_confirmed)
         audit.touch_confirmed_events++;

      if(events[i].rtv_before_start_index >= 0)
         audit.full_baseline_events++;

      if(!events[i].rtv_ready)
         continue;

      audit.rtv_ready_events++;

      if(events[i].rtv <= 0.0 || !DAL_M0001NullValidNumber(events[i].rtv))
         continue;

      double node_log = MathLog(events[i].rtv);
      double random_log = 0.0;
      if(!DAL_M0001RandomLogForEvent(events[i], bars, bars_count, analysis_start_index, random_k, random_log))
         continue;

      int size = ArraySize(pairs);
      ArrayResize(pairs, size + 1);
      ArrayResize(node_logs, size + 1);
      ArrayResize(random_logs, size + 1);

      pairs[size].event_id = events[i].id;
      pairs[size].sample_length = events[i].rtv_sample_length;
      pairs[size].entry_time = events[i].entry_time;
      pairs[size].node_log = node_log;
      pairs[size].random_log = random_log;
      pairs[size].delta_log = node_log - random_log;

      node_logs[size] = node_log;
      random_logs[size] = random_log;
   }

   audit.paired_events = ArraySize(pairs);
   return ArraySize(pairs);
}

void DAL_M0001ComputeLogRtvStats(
   const double &log_values[],
   DALM0001LogRtvStats &stats
)
{
   DAL_M0001NullResetStats(stats);

   int count = ArraySize(log_values);
   if(count <= 0)
      return;

   stats.count = count;

   double sorted_log[];
   double sorted_raw[];
   ArrayResize(sorted_log, count);
   ArrayResize(sorted_raw, count);

   double total_log = 0.0;
   double total_raw = 0.0;

   for(int i = 0; i < count; i++)
   {
      double lv = log_values[i];
      double rv = MathExp(lv);

      sorted_log[i] = lv;
      sorted_raw[i] = rv;

      total_log += lv;
      total_raw += rv;
   }

   ArraySort(sorted_log);
   ArraySort(sorted_raw);

   stats.log_mean = total_log / count;
   stats.raw_mean = total_raw / count;

   stats.log_median = DAL_M0001NullPercentileSorted(sorted_log, 0.50);
   stats.log_p05 = DAL_M0001NullPercentileSorted(sorted_log, 0.05);
   stats.log_p25 = DAL_M0001NullPercentileSorted(sorted_log, 0.25);
   stats.log_p75 = DAL_M0001NullPercentileSorted(sorted_log, 0.75);
   stats.log_p90 = DAL_M0001NullPercentileSorted(sorted_log, 0.90);
   stats.log_p95 = DAL_M0001NullPercentileSorted(sorted_log, 0.95);
   stats.log_iqr = stats.log_p75 - stats.log_p25;

   stats.raw_median = DAL_M0001NullPercentileSorted(sorted_raw, 0.50);
   stats.raw_p75 = DAL_M0001NullPercentileSorted(sorted_raw, 0.75);
   stats.raw_p90 = DAL_M0001NullPercentileSorted(sorted_raw, 0.90);
   stats.raw_p95 = DAL_M0001NullPercentileSorted(sorted_raw, 0.95);

   double cvar90_total = 0.0;
   double cvar95_total = 0.0;
   int cvar90_count = 0;
   int cvar95_count = 0;

   for(int i = 0; i < count; i++)
   {
      if(sorted_raw[i] >= stats.raw_p90)
      {
         cvar90_total += sorted_raw[i];
         cvar90_count++;
      }

      if(sorted_raw[i] >= stats.raw_p95)
      {
         cvar95_total += sorted_raw[i];
         cvar95_count++;
      }
   }

   stats.raw_cvar90 = cvar90_count > 0 ? cvar90_total / cvar90_count : 0.0;
   stats.raw_cvar95 = cvar95_count > 0 ? cvar95_total / cvar95_count : 0.0;

   double m2 = 0.0;
   double m3 = 0.0;
   double m4 = 0.0;

   int gt0 = 0;

   for(int i = 0; i < count; i++)
   {
      double d = log_values[i] - stats.log_mean;
      double d2 = d * d;

      m2 += d2;
      m3 += d2 * d;
      m4 += d2 * d2;

      if(log_values[i] > 0.0)
         gt0++;
   }

   m2 /= count;
   m3 /= count;
   m4 /= count;

   stats.log_stdev = MathSqrt(m2);
   stats.pct_log_gt_zero = 100.0 * gt0 / count;

   if(stats.log_stdev > 0.0)
   {
      stats.log_skewness = m3 / MathPow(stats.log_stdev, 3);
      stats.log_excess_kurtosis = m4 / MathPow(stats.log_stdev, 4) - 3.0;
      stats.log_jarque_bera = count / 6.0 * (stats.log_skewness * stats.log_skewness + 0.25 * stats.log_excess_kurtosis * stats.log_excess_kurtosis);

      int tail2 = 0;
      int tail3 = 0;
      double max_ks = 0.0;

      for(int i = 0; i < count; i++)
      {
         double z = (log_values[i] - stats.log_mean) / stats.log_stdev;

         if(MathAbs(z) >= 2.0)
            tail2++;
         if(MathAbs(z) >= 3.0)
            tail3++;
      }

      for(int i = 0; i < count; i++)
      {
         double z = (sorted_log[i] - stats.log_mean) / stats.log_stdev;
         double f = DAL_M0001NullNormalCdf(z);

         double d_plus = (i + 1.0) / count - f;
         double d_minus = f - i / (double)count;

         if(d_plus > max_ks)
            max_ks = d_plus;
         if(d_minus > max_ks)
            max_ks = d_minus;
      }

      stats.log_ks_normal = max_ks;
      stats.tail2_pct = 100.0 * tail2 / count;
      stats.tail3_pct = 100.0 * tail3 / count;
      stats.tail2_ratio_normal = DAL_M0001NullSafeDiv(stats.tail2_pct, 4.550026);
      stats.tail3_ratio_normal = DAL_M0001NullSafeDiv(stats.tail3_pct, 0.269980);
   }
}

double DAL_M0001KsTwoSample(
   const double &a_values[],
   const double &b_values[]
)
{
   int a_count = ArraySize(a_values);
   int b_count = ArraySize(b_values);

   if(a_count <= 0 || b_count <= 0)
      return 0.0;

   double a[];
   double b[];
   ArrayResize(a, a_count);
   ArrayResize(b, b_count);

   for(int i = 0; i < a_count; i++)
      a[i] = a_values[i];

   for(int i = 0; i < b_count; i++)
      b[i] = b_values[i];

   ArraySort(a);
   ArraySort(b);

   int ia = 0;
   int ib = 0;
   double max_d = 0.0;

   while(ia < a_count || ib < b_count)
   {
      double x;

      if(ib >= b_count || (ia < a_count && a[ia] <= b[ib]))
         x = a[ia];
      else
         x = b[ib];

      while(ia < a_count && a[ia] <= x)
         ia++;

      while(ib < b_count && b[ib] <= x)
         ib++;

      double fa = ia / (double)a_count;
      double fb = ib / (double)b_count;
      double d = MathAbs(fa - fb);

      if(d > max_d)
         max_d = d;
   }

   return max_d;
}

double DAL_M0001CvmTwoSample(
   const double &a_values[],
   const double &b_values[]
)
{
   int a_count = ArraySize(a_values);
   int b_count = ArraySize(b_values);
   if(a_count <= 0 || b_count <= 0)
      return 0.0;

   double a[];
   double b[];
   ArrayResize(a, a_count);
   ArrayResize(b, b_count);

   for(int i = 0; i < a_count; i++)
      a[i] = a_values[i];
   for(int i = 0; i < b_count; i++)
      b[i] = b_values[i];

   ArraySort(a);
   ArraySort(b);

   int ia = 0;
   int ib = 0;
   double sum_sq = 0.0;
   int steps = 0;

   while(ia < a_count || ib < b_count)
   {
      double x;
      if(ib >= b_count || (ia < a_count && a[ia] <= b[ib]))
         x = a[ia];
      else
         x = b[ib];

      while(ia < a_count && a[ia] <= x)
         ia++;
      while(ib < b_count && b[ib] <= x)
         ib++;

      double d = ia / (double)a_count - ib / (double)b_count;
      sum_sq += d * d;
      steps++;
   }

   if(steps <= 0)
      return 0.0;

   return sum_sq / steps;
}

double DAL_M0001WassersteinLogDistance(
   const double &a_values[],
   const double &b_values[]
)
{
   int a_count = ArraySize(a_values);
   int b_count = ArraySize(b_values);
   if(a_count <= 0 || b_count <= 0)
      return 0.0;

   double a[];
   double b[];
   ArrayResize(a, a_count);
   ArrayResize(b, b_count);

   for(int i = 0; i < a_count; i++)
      a[i] = a_values[i];
   for(int i = 0; i < b_count; i++)
      b[i] = b_values[i];

   ArraySort(a);
   ArraySort(b);

   int grid = 101;
   double total = 0.0;
   for(int i = 0; i < grid; i++)
   {
      double q = i / (double)(grid - 1);
      total += MathAbs(DAL_M0001NullPercentileSorted(a, q) - DAL_M0001NullPercentileSorted(b, q));
   }

   return total / grid;
}

double DAL_M0001CliffDelta(
   const double &a_values[],
   const double &b_values[]
)
{
   int a_count = ArraySize(a_values);
   int b_count = ArraySize(b_values);
   if(a_count <= 0 || b_count <= 0)
      return 0.0;

   int a_step = 1;
   int b_step = 1;
   double full_product = (double)a_count * (double)b_count;

   // Keep final-only validation fast on very large samples. For normal sample sizes
   // this is exact; for very large samples it becomes a deterministic grid estimate.
   if(full_product > 2000000.0)
   {
      a_step = (int)MathCeil(a_count / 1200.0);
      b_step = (int)MathCeil(b_count / 1200.0);
      if(a_step < 1)
         a_step = 1;
      if(b_step < 1)
         b_step = 1;
   }

   long greater = 0;
   long less = 0;
   long used = 0;

   for(int i = 0; i < a_count; i += a_step)
   {
      for(int j = 0; j < b_count; j += b_step)
      {
         if(a_values[i] > b_values[j])
            greater++;
         else if(a_values[i] < b_values[j])
            less++;
         used++;
      }
   }

   if(used <= 0)
      return 0.0;

   return (greater - less) / (double)used;
}

void DAL_M0001ComputeLogRtvComparison(
   const double &node_logs[],
   const double &random_logs[],
   const DALM0001LogRtvStats &node_stats,
   const DALM0001LogRtvStats &random_stats,
   DALM0001LogRtvComparison &cmp
)
{
   DAL_M0001ResetComparison(cmp);

   cmp.paired_count = DAL_M0001IntMin(ArraySize(node_logs), ArraySize(random_logs));
   cmp.delta_log_mean = node_stats.log_mean - random_stats.log_mean;
   cmp.delta_log_median = node_stats.log_median - random_stats.log_median;
   cmp.delta_pct_log_gt_zero = node_stats.pct_log_gt_zero - random_stats.pct_log_gt_zero;
   cmp.geo_ratio = MathExp(cmp.delta_log_mean);
   cmp.median_ratio = MathExp(cmp.delta_log_median);
   cmp.ks_real_vs_random = DAL_M0001KsTwoSample(node_logs, random_logs);
   cmp.cvm_real_vs_random = DAL_M0001CvmTwoSample(node_logs, random_logs);
   cmp.wasserstein_log = DAL_M0001WassersteinLogDistance(node_logs, random_logs);
   cmp.cliff_delta = DAL_M0001CliffDelta(node_logs, random_logs);

   cmp.delta_raw_q50 = node_stats.raw_median - random_stats.raw_median;
   cmp.delta_raw_q75 = node_stats.raw_p75 - random_stats.raw_p75;
   cmp.delta_raw_q90 = node_stats.raw_p90 - random_stats.raw_p90;
   cmp.delta_raw_q95 = node_stats.raw_p95 - random_stats.raw_p95;
   cmp.delta_raw_cvar90 = node_stats.raw_cvar90 - random_stats.raw_cvar90;
   cmp.delta_raw_cvar95 = node_stats.raw_cvar95 - random_stats.raw_cvar95;
   cmp.right_tail_odds_ratio = DAL_M0001NullSafeDiv(node_stats.tail3_pct, random_stats.tail3_pct);

   if(cmp.paired_count <= 0)
      return;

   int wins = 0;
   int losses = 0;
   double sum_delta = 0.0;
   double deltas[];
   ArrayResize(deltas, cmp.paired_count);

   for(int i = 0; i < cmp.paired_count; i++)
   {
      double d = node_logs[i] - random_logs[i];
      deltas[i] = d;
      sum_delta += d;

      if(d > 0.0)
         wins++;
      else if(d < 0.0)
         losses++;
   }

   ArraySort(deltas);

   cmp.paired_win_pct = 100.0 * wins / cmp.paired_count;
   cmp.paired_mean_delta = sum_delta / cmp.paired_count;
   cmp.paired_median_delta = DAL_M0001NullPercentileSorted(deltas, 0.50);

   int sign_n = wins + losses;
   if(sign_n > 0)
   {
      double z_sign = (wins - sign_n * 0.5) / MathSqrt(sign_n * 0.25);
      cmp.sign_test_p_approx = DAL_M0001TwoSidedNormalP(z_sign);
   }

   if(cmp.paired_count > 1)
   {
      double var = 0.0;
      for(int i = 0; i < cmp.paired_count; i++)
      {
         double d = deltas[i] - cmp.paired_mean_delta;
         var += d * d;
      }

      var /= (cmp.paired_count - 1);
      double sd = MathSqrt(var);

      if(sd > 0.0)
      {
         cmp.paired_t_stat = cmp.paired_mean_delta / (sd / MathSqrt(cmp.paired_count));
         cmp.paired_t_p_approx = DAL_M0001TwoSidedNormalP(cmp.paired_t_stat);
      }
   }

   double pooled_var = (node_stats.log_stdev * node_stats.log_stdev + random_stats.log_stdev * random_stats.log_stdev) / 2.0;
   if(pooled_var > 0.0)
      cmp.cohen_d = cmp.delta_log_mean / MathSqrt(pooled_var);
}

double DAL_M0001PseudoFraction(const int a, const int b, const int c)
{
   double x = MathSin((a + 1) * 12.9898 + (b + 3) * 78.233 + (c + 7) * 37.719) * 43758.5453123;
   return x - MathFloor(x);
}

void DAL_M0001ComputeRobustnessStats(
   const DALM0001PairedLogRtv &pairs[],
   const int bootstrap_iterations,
   const int permutation_iterations,
   const int validation_splits,
   DALM0001RobustnessStats &rob
)
{
   DAL_M0001ResetRobustness(rob);

   int count = ArraySize(pairs);
   if(count <= 1)
      return;

   int boot_iters = bootstrap_iterations;
   if(boot_iters < 0)
      boot_iters = 0;
   int perm_iters = permutation_iterations;
   if(perm_iters < 0)
      perm_iters = 0;
   int splits = validation_splits;
   if(splits < 1)
      splits = 1;
   if(splits > count)
      splits = count;

   rob.bootstrap_iterations = boot_iters;
   rob.permutation_iterations = perm_iters;
   rob.validation_splits = splits;

   double observed_sum = 0.0;
   int observed_wins = 0;
   for(int i = 0; i < count; i++)
   {
      observed_sum += pairs[i].delta_log;
      if(pairs[i].delta_log > 0.0)
         observed_wins++;
   }
   double observed_mean = observed_sum / count;
   double observed_abs = MathAbs(observed_mean);

   if(boot_iters > 0)
   {
      double boot_means[];
      double boot_wins[];
      ArrayResize(boot_means, boot_iters);
      ArrayResize(boot_wins, boot_iters);

      for(int it = 0; it < boot_iters; it++)
      {
         double sum = 0.0;
         int wins = 0;
         for(int j = 0; j < count; j++)
         {
            double frac = DAL_M0001PseudoFraction(it, j, count);
            int idx = (int)MathFloor(frac * count);
            if(idx < 0)
               idx = 0;
            if(idx >= count)
               idx = count - 1;

            double d = pairs[idx].delta_log;
            sum += d;
            if(d > 0.0)
               wins++;
         }

         boot_means[it] = sum / count;
         boot_wins[it] = 100.0 * wins / count;
      }

      ArraySort(boot_means);
      ArraySort(boot_wins);
      rob.boot_mean_delta_low95 = DAL_M0001NullPercentileSorted(boot_means, 0.025);
      rob.boot_mean_delta_high95 = DAL_M0001NullPercentileSorted(boot_means, 0.975);
      rob.boot_win_pct_low95 = DAL_M0001NullPercentileSorted(boot_wins, 0.025);
      rob.boot_win_pct_high95 = DAL_M0001NullPercentileSorted(boot_wins, 0.975);
   }

   if(perm_iters > 0)
   {
      int extreme = 0;
      for(int it = 0; it < perm_iters; it++)
      {
         double sum = 0.0;
         for(int j = 0; j < count; j++)
         {
            double frac = DAL_M0001PseudoFraction(it, j, count + 97);
            double sign = (frac < 0.5 ? -1.0 : 1.0);
            sum += sign * pairs[j].delta_log;
         }

         double perm_mean = sum / count;
         if(MathAbs(perm_mean) >= observed_abs)
            extreme++;
      }

      rob.permutation_p = (extreme + 1.0) / (perm_iters + 1.0);
   }

   if(splits > 0)
   {
      datetime sorted_times[];
      double sorted_pair_deltas[];
      ArrayResize(sorted_times, count);
      ArrayResize(sorted_pair_deltas, count);

      for(int i = 0; i < count; i++)
      {
         sorted_times[i] = pairs[i].entry_time;
         sorted_pair_deltas[i] = pairs[i].delta_log;
      }

      // Chronological split stability: sort pair deltas by entry_time.
      // MQL5 cannot ArraySort a struct array here, so use deterministic insertion sort.
      for(int i = 1; i < count; i++)
      {
         datetime key_time = sorted_times[i];
         double key_delta = sorted_pair_deltas[i];
         int j = i - 1;
         while(j >= 0 && sorted_times[j] > key_time)
         {
            sorted_times[j + 1] = sorted_times[j];
            sorted_pair_deltas[j + 1] = sorted_pair_deltas[j];
            j--;
         }
         sorted_times[j + 1] = key_time;
         sorted_pair_deltas[j + 1] = key_delta;
      }

      double split_deltas[];
      ArrayResize(split_deltas, 0);
      int positive = 0;
      double total_delta = 0.0;
      double min_delta = 0.0;
      double min_win = 100.0;

      for(int s = 0; s < splits; s++)
      {
         int start = (int)MathFloor(s * count / (double)splits);
         int end = (int)MathFloor((s + 1) * count / (double)splits) - 1;
         if(end < start)
            continue;

         double sum = 0.0;
         int wins = 0;
         int n = 0;
         for(int i = start; i <= end; i++)
         {
            double d = sorted_pair_deltas[i];
            sum += d;
            if(d > 0.0)
               wins++;
            n++;
         }

         if(n <= 0)
            continue;

         double split_mean = sum / n;
         double split_win = 100.0 * wins / n;

         int size = ArraySize(split_deltas);
         ArrayResize(split_deltas, size + 1);
         split_deltas[size] = split_mean;

         if(size == 0 || split_mean < min_delta)
            min_delta = split_mean;
         if(split_win < min_win)
            min_win = split_win;

         if(split_mean > 0.0)
            positive++;

         total_delta += split_mean;
      }

      int valid_splits = ArraySize(split_deltas);
      rob.split_valid_count = valid_splits;
      if(valid_splits > 0)
      {
         rob.split_positive_pct = 100.0 * positive / valid_splits;
         rob.split_min_delta_log_mean = min_delta;
         rob.split_mean_delta_log_mean = total_delta / valid_splits;
         rob.split_min_win_pct = min_win;

         double var = 0.0;
         for(int i = 0; i < valid_splits; i++)
         {
            double d = split_deltas[i] - rob.split_mean_delta_log_mean;
            var += d * d;
         }
         if(valid_splits > 1)
            var /= (valid_splits - 1);

         rob.split_stdev_delta_log_mean = MathSqrt(var);

         double positivity_component = rob.split_positive_pct / 100.0;
         double min_component = (rob.split_min_delta_log_mean > 0.0 ? 1.0 : 0.0);
         double dispersion_component = 1.0 / (1.0 + DAL_M0001NullSafeDiv(rob.split_stdev_delta_log_mean, MathAbs(rob.split_mean_delta_log_mean) + 0.000001));
         rob.stability_score = 100.0 * (0.50 * positivity_component + 0.25 * min_component + 0.25 * dispersion_component);
      }
   }
}

string DAL_M0001Fmt4(const double value)
{
   return DoubleToString(value, 4);
}

string DAL_M0001FmtPct(const double value)
{
   return DoubleToString(value, 2);
}

string DAL_M0001CompactHistCounts(const double &log_values[])
{
   int count = ArraySize(log_values);
   if(count <= 0)
      return "empty";

   double raw[];
   ArrayResize(raw, count);

   for(int i = 0; i < count; i++)
      raw[i] = MathExp(log_values[i]);

   ArraySort(raw);

   double min_v = raw[0];
   double max_v = raw[count - 1];

   if(max_v <= min_v)
      return DAL_M0001Fmt4(min_v) + "-" + DAL_M0001Fmt4(max_v) + ":" + IntegerToString(count);

   int bins = 10;
   int counts[];
   ArrayResize(counts, bins);
   ArrayInitialize(counts, 0);

   double width = (max_v - min_v) / bins;

   for(int i = 0; i < count; i++)
   {
      int b = (int)MathFloor((raw[i] - min_v) / width);

      if(b < 0)
         b = 0;
      if(b >= bins)
         b = bins - 1;

      counts[b]++;
   }

   string out = "";
   for(int b = 0; b < bins; b++)
   {
      if(b > 0)
         out += ",";

      double from = min_v + width * b;
      double to = from + width;
      out += DAL_M0001Fmt4(from) + "-" + DAL_M0001Fmt4(to) + ":" + IntegerToString(counts[b]);
   }

   return out;
}

string DAL_M0001StatsCompactText(
   const string label,
   const DALM0001LogRtvStats &stats
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
      + "*JB=" + DAL_M0001Fmt4(stats.log_jarque_bera)
      + "*KSnorm=" + DAL_M0001Fmt4(stats.log_ks_normal)
      + "*tail2xN=" + DAL_M0001Fmt4(stats.tail2_ratio_normal)
      + "*tail3xN=" + DAL_M0001Fmt4(stats.tail3_ratio_normal);
}

string DAL_M0001ComparisonCompactText(const DALM0001LogRtvComparison &cmp)
{
   return "COMPARE"
      + "*pairs=" + IntegerToString(cmp.paired_count)
      + "*dLogMean=" + DAL_M0001Fmt4(cmp.delta_log_mean)
      + "*geoRatio=" + DAL_M0001Fmt4(cmp.geo_ratio)
      + "*dLogMed=" + DAL_M0001Fmt4(cmp.delta_log_median)
      + "*medianRatio=" + DAL_M0001Fmt4(cmp.median_ratio)
      + "*dGt0Pct=" + DAL_M0001FmtPct(cmp.delta_pct_log_gt_zero)
      + "*pairedWinPct=" + DAL_M0001FmtPct(cmp.paired_win_pct)
      + "*pairedMeanDelta=" + DAL_M0001Fmt4(cmp.paired_mean_delta)
      + "*pairedMedDelta=" + DAL_M0001Fmt4(cmp.paired_median_delta)
      + "*pairedT=" + DAL_M0001Fmt4(cmp.paired_t_stat)
      + "*tPapprox=" + DAL_M0001Fmt4(cmp.paired_t_p_approx)
      + "*cohenD=" + DAL_M0001Fmt4(cmp.cohen_d)
      + "*signPapprox=" + DAL_M0001Fmt4(cmp.sign_test_p_approx)
      + "*cliffDelta=" + DAL_M0001Fmt4(cmp.cliff_delta)
      + "*KS=" + DAL_M0001Fmt4(cmp.ks_real_vs_random)
      + "*CvM=" + DAL_M0001Fmt4(cmp.cvm_real_vs_random)
      + "*W1log=" + DAL_M0001Fmt4(cmp.wasserstein_log);
}

string DAL_M0001QuantileTailText(const DALM0001LogRtvComparison &cmp)
{
   return "QUANT_TAIL"
      + "*dQ50=" + DAL_M0001Fmt4(cmp.delta_raw_q50)
      + "*dQ75=" + DAL_M0001Fmt4(cmp.delta_raw_q75)
      + "*dQ90=" + DAL_M0001Fmt4(cmp.delta_raw_q90)
      + "*dQ95=" + DAL_M0001Fmt4(cmp.delta_raw_q95)
      + "*dCVaR90=" + DAL_M0001Fmt4(cmp.delta_raw_cvar90)
      + "*dCVaR95=" + DAL_M0001Fmt4(cmp.delta_raw_cvar95)
      + "*rightTailOdds=" + DAL_M0001Fmt4(cmp.right_tail_odds_ratio);
}

string DAL_M0001RobustnessText(const DALM0001RobustnessStats &rob)
{
   return "ROBUST"
      + "*bootN=" + IntegerToString(rob.bootstrap_iterations)
      + "*dMeanCI95=" + DAL_M0001Fmt4(rob.boot_mean_delta_low95) + ".." + DAL_M0001Fmt4(rob.boot_mean_delta_high95)
      + "*winCI95=" + DAL_M0001FmtPct(rob.boot_win_pct_low95) + ".." + DAL_M0001FmtPct(rob.boot_win_pct_high95)
      + "*permN=" + IntegerToString(rob.permutation_iterations)
      + "*permP=" + DAL_M0001Fmt4(rob.permutation_p)
      + "*splits=" + IntegerToString(rob.split_valid_count)
      + "*splitPositivePct=" + DAL_M0001FmtPct(rob.split_positive_pct)
      + "*splitMinDLog=" + DAL_M0001Fmt4(rob.split_min_delta_log_mean)
      + "*splitMeanDLog=" + DAL_M0001Fmt4(rob.split_mean_delta_log_mean)
      + "*splitSdDLog=" + DAL_M0001Fmt4(rob.split_stdev_delta_log_mean)
      + "*splitMinWin=" + DAL_M0001FmtPct(rob.split_min_win_pct)
      + "*stabilityScore=" + DAL_M0001FmtPct(rob.stability_score);
}


string DAL_M0001SessionRegimeText(
   const DALM0001PairedLogRtv &pairs[],
   const double &random_logs[]
)
{
   int count = ArraySize(pairs);
   if(count <= 0)
      return "SESSION_REGIME*empty=1";

   double random_sorted[];
   ArrayResize(random_sorted, ArraySize(random_logs));
   for(int i = 0; i < ArraySize(random_logs); i++)
      random_sorted[i] = random_logs[i];
   ArraySort(random_sorted);

   double r33 = ArraySize(random_sorted) > 0 ? DAL_M0001NullPercentileSorted(random_sorted, 0.3333) : 0.0;
   double r66 = ArraySize(random_sorted) > 0 ? DAL_M0001NullPercentileSorted(random_sorted, 0.6667) : 0.0;

   int session_count[3];
   int session_wins[3];
   double session_sum[3];
   ArrayInitialize(session_count, 0);
   ArrayInitialize(session_wins, 0);
   ArrayInitialize(session_sum, 0.0);

   int regime_count[3];
   int regime_wins[3];
   double regime_sum[3];
   ArrayInitialize(regime_count, 0);
   ArrayInitialize(regime_wins, 0);
   ArrayInitialize(regime_sum, 0.0);

   for(int i = 0; i < count; i++)
   {
      MqlDateTime dt;
      TimeToStruct(pairs[i].entry_time, dt);
      int hour = dt.hour;

      int session = 0;
      if(hour >= 8 && hour < 16)
         session = 1;
      else if(hour >= 16)
         session = 2;

      session_count[session]++;
      session_sum[session] += pairs[i].delta_log;
      if(pairs[i].delta_log > 0.0)
         session_wins[session]++;

      int regime = 1;
      if(pairs[i].random_log <= r33)
         regime = 0;
      else if(pairs[i].random_log >= r66)
         regime = 2;

      regime_count[regime]++;
      regime_sum[regime] += pairs[i].delta_log;
      if(pairs[i].delta_log > 0.0)
         regime_wins[regime]++;
   }

   double asia_mean = session_count[0] > 0 ? session_sum[0] / session_count[0] : 0.0;
   double london_mean = session_count[1] > 0 ? session_sum[1] / session_count[1] : 0.0;
   double ny_mean = session_count[2] > 0 ? session_sum[2] / session_count[2] : 0.0;

   double asia_win = session_count[0] > 0 ? 100.0 * session_wins[0] / session_count[0] : 0.0;
   double london_win = session_count[1] > 0 ? 100.0 * session_wins[1] / session_count[1] : 0.0;
   double ny_win = session_count[2] > 0 ? 100.0 * session_wins[2] / session_count[2] : 0.0;

   double low_mean = regime_count[0] > 0 ? regime_sum[0] / regime_count[0] : 0.0;
   double mid_mean = regime_count[1] > 0 ? regime_sum[1] / regime_count[1] : 0.0;
   double high_mean = regime_count[2] > 0 ? regime_sum[2] / regime_count[2] : 0.0;

   double low_win = regime_count[0] > 0 ? 100.0 * regime_wins[0] / regime_count[0] : 0.0;
   double mid_win = regime_count[1] > 0 ? 100.0 * regime_wins[1] / regime_count[1] : 0.0;
   double high_win = regime_count[2] > 0 ? 100.0 * regime_wins[2] / regime_count[2] : 0.0;

   return "SESSION_REGIME"
      + "*sessionClock=brokerHour"
      + "*asiaN=" + IntegerToString(session_count[0])
      + "*asiaDLog=" + DAL_M0001Fmt4(asia_mean)
      + "*asiaWin=" + DAL_M0001FmtPct(asia_win)
      + "*londonN=" + IntegerToString(session_count[1])
      + "*londonDLog=" + DAL_M0001Fmt4(london_mean)
      + "*londonWin=" + DAL_M0001FmtPct(london_win)
      + "*nyN=" + IntegerToString(session_count[2])
      + "*nyDLog=" + DAL_M0001Fmt4(ny_mean)
      + "*nyWin=" + DAL_M0001FmtPct(ny_win)
      + "*regimeBy=randomLogTercile"
      + "*lowRegN=" + IntegerToString(regime_count[0])
      + "*lowRegDLog=" + DAL_M0001Fmt4(low_mean)
      + "*lowRegWin=" + DAL_M0001FmtPct(low_win)
      + "*midRegN=" + IntegerToString(regime_count[1])
      + "*midRegDLog=" + DAL_M0001Fmt4(mid_mean)
      + "*midRegWin=" + DAL_M0001FmtPct(mid_win)
      + "*highRegN=" + IntegerToString(regime_count[2])
      + "*highRegDLog=" + DAL_M0001Fmt4(high_mean)
      + "*highRegWin=" + DAL_M0001FmtPct(high_win);
}

string DAL_M0001IntegrityAuditText(
   const DALM0001IntegrityAudit &audit,
   const int random_k,
   const bool print_histogram,
   const datetime min_entry_time
)
{
   double baseline_pct = audit.events_after_analysis_start > 0 ? 100.0 * audit.full_baseline_events / audit.events_after_analysis_start : 0.0;
   double touch_pct = audit.events_after_analysis_start > 0 ? 100.0 * audit.touch_confirmed_events / audit.events_after_analysis_start : 0.0;
   double paired_pct = audit.rtv_ready_events > 0 ? 100.0 * audit.paired_events / audit.rtv_ready_events : 0.0;

   return "AUDIT"
      + "*analysisStart=" + DAL_M0001AnalysisStartText(min_entry_time)
      + "*closed=" + IntegerToString(audit.closed_events)
      + "*afterStart=" + IntegerToString(audit.events_after_analysis_start)
      + "*warmupExcluded=" + IntegerToString(audit.warmup_excluded_events)
      + "*rtvReady=" + IntegerToString(audit.rtv_ready_events)
      + "*paired=" + IntegerToString(audit.paired_events)
      + "*baselineOkPct=" + DAL_M0001FmtPct(baseline_pct)
      + "*touchConfirmedPct=" + DAL_M0001FmtPct(touch_pct)
      + "*pairedPctOfReady=" + DAL_M0001FmtPct(paired_pct)
      + "*randomK=" + IntegerToString(random_k)
      + "*histogram=" + (print_histogram ? "on" : "off")
      + "*lookaheadGuard=activeFrom_nodeIndexPlusL"
      + "*baselineGuard=beforeEntryOnly"
      + "*exitGapGuard=excludedFromRTV";
}

string DAL_M0001FinalLinePrefix(
   const string tag,
   const string symbol,
   const string timeframe,
   const string source_mode,
   const int events_count,
   const datetime min_entry_time
)
{
   return tag
      + " *** symbol=" + symbol
      + "*tf=" + timeframe
      + "*source=" + source_mode
      + "*events=" + IntegerToString(events_count)
      + "*analysisStart=" + DAL_M0001AnalysisStartText(min_entry_time)
      + " *** ";
}

void DAL_M0001PrintFinalNodeRandomReports(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const string symbol,
   const string timeframe,
   const string source_mode,
   const datetime min_entry_time,
   const DALM0001RtvReportConfig &report_config
)
{
   DALM0001PairedLogRtv pairs[];
   double node_logs[];
   double random_logs[];
   DALM0001IntegrityAudit audit;

   int random_k = report_config.random_samples_per_event;
   if(random_k <= 0)
      random_k = 1;

   DAL_M0001CollectPairedLogRtvs(events, events_count, bars, bars_count, min_entry_time, random_k, pairs, node_logs, random_logs, audit);

   DALM0001LogRtvStats node_stats;
   DALM0001LogRtvStats random_stats;
   DAL_M0001ComputeLogRtvStats(node_logs, node_stats);
   DAL_M0001ComputeLogRtvStats(random_logs, random_stats);

   DALM0001LogRtvComparison cmp;
   DAL_M0001ComputeLogRtvComparison(node_logs, random_logs, node_stats, random_stats, cmp);

   DALM0001RobustnessStats rob;
   DAL_M0001ComputeRobustnessStats(pairs, report_config.bootstrap_iterations, report_config.permutation_iterations, report_config.validation_splits, rob);

   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_NODES", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0001StatsCompactText("NODES", node_stats));
   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_RANDOM", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0001StatsCompactText("RANDOM", random_stats));
   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_COMPARE", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0001ComparisonCompactText(cmp));
   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_QUANT_TAIL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0001QuantileTailText(cmp));
   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_ROBUST", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0001RobustnessText(rob));
   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_SESSION_REGIME", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0001SessionRegimeText(pairs, random_logs));
   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_AUDIT", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0001IntegrityAuditText(audit, random_k, report_config.print_histogram, min_entry_time));

   if(report_config.print_histogram)
   {
      Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_HIST_NODES", symbol, timeframe, source_mode, events_count, min_entry_time), "HIST_NODES*histRaw=", DAL_M0001CompactHistCounts(node_logs));
      Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_HIST_RANDOM", symbol, timeframe, source_mode, events_count, min_entry_time), "HIST_RANDOM*histRaw=", DAL_M0001CompactHistCounts(random_logs));
   }
}

string DAL_M0001LogRtvNullSignature(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const datetime min_entry_time,
   const DALM0001RtvReportConfig &report_config
)
{
   DALM0001PairedLogRtv pairs[];
   double node_logs[];
   double random_logs[];
   DALM0001IntegrityAudit audit;
   DAL_M0001CollectPairedLogRtvs(events, events_count, bars, bars_count, min_entry_time, report_config.random_samples_per_event, pairs, node_logs, random_logs, audit);

   DALM0001LogRtvStats node_stats;
   DALM0001LogRtvStats random_stats;
   DAL_M0001ComputeLogRtvStats(node_logs, node_stats);
   DAL_M0001ComputeLogRtvStats(random_logs, random_stats);

   return "n=" + IntegerToString(node_stats.count)
      + "|r=" + IntegerToString(random_stats.count)
      + "|nMean=" + DAL_M0001Fmt4(node_stats.log_mean)
      + "|rMean=" + DAL_M0001Fmt4(random_stats.log_mean)
      + "|k=" + IntegerToString(report_config.random_samples_per_event);
}

#endif
