#ifndef __DAL_M0001_RTV_NULL_COMPARISON_MQH__
#define __DAL_M0001_RTV_NULL_COMPARISON_MQH__

#include <DecisionAlphaLab/Common/DAL_Math.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Types.mqh>

struct DALM0001LogRtvStats
{
   int count;

   double raw_mean;
   double raw_median;
   double raw_p90;
   double raw_p95;

   double log_mean;
   double log_median;
   double log_stdev;
   double log_p05;
   double log_p25;
   double log_p75;
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
   double paired_win_pct;
   double paired_mean_delta;
   double paired_t_stat;
   double cohen_d;
   double ks_real_vs_random;
};

string DAL_M0001_NULL_LAST_SIGNATURE = "";

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

void DAL_M0001NullResetStats(DALM0001LogRtvStats &stats)
{
   stats.count = 0;

   stats.raw_mean = 0.0;
   stats.raw_median = 0.0;
   stats.raw_p90 = 0.0;
   stats.raw_p95 = 0.0;

   stats.log_mean = 0.0;
   stats.log_median = 0.0;
   stats.log_stdev = 0.0;
   stats.log_p05 = 0.0;
   stats.log_p25 = 0.0;
   stats.log_p75 = 0.0;
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

int DAL_M0001CollectNodeLogRtvs(
   const DALM0001Event &events[],
   const int events_count,
   double &log_values[]
)
{
   ArrayResize(log_values, 0);

   for(int i = 0; i < events_count; i++)
   {
      if(!events[i].closed)
         continue;

      if(!events[i].rtv_ready)
         continue;

      if(events[i].rtv <= 0.0)
         continue;

      if(!DAL_M0001NullValidNumber(events[i].rtv))
         continue;

      int size = ArraySize(log_values);
      ArrayResize(log_values, size + 1);
      log_values[size] = MathLog(events[i].rtv);
   }

   return ArraySize(log_values);
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

double DAL_M0001RandomFraction(
   const int event_id,
   const int sample_length,
   const int bars_count
)
{
   double x = MathSin((event_id + 1) * 12.9898 + (sample_length + 3) * 78.233 + bars_count * 0.0174532925199433) * 43758.5453123;
   return x - MathFloor(x);
}

int DAL_M0001CollectRandomLogRtvs(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   double &log_values[]
)
{
   ArrayResize(log_values, 0);

   for(int i = 0; i < events_count; i++)
   {
      if(!events[i].closed)
         continue;

      if(!events[i].rtv_ready)
         continue;

      int n = events[i].rtv_sample_length;
      if(n <= 0)
         continue;

      int min_entry = n;
      int max_entry = bars_count - n;
      if(max_entry < min_entry)
         continue;

      int span = max_entry - min_entry + 1;
      double frac = DAL_M0001RandomFraction(events[i].id, n, bars_count);
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

      int size = ArraySize(log_values);
      ArrayResize(log_values, size + 1);
      log_values[size] = MathLog(rtv);
   }

   return ArraySize(log_values);
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
   stats.log_p95 = DAL_M0001NullPercentileSorted(sorted_log, 0.95);
   stats.log_iqr = stats.log_p75 - stats.log_p25;

   stats.raw_median = DAL_M0001NullPercentileSorted(sorted_raw, 0.50);
   stats.raw_p90 = DAL_M0001NullPercentileSorted(sorted_raw, 0.90);
   stats.raw_p95 = DAL_M0001NullPercentileSorted(sorted_raw, 0.95);

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

void DAL_M0001ComputeLogRtvComparison(
   const double &node_logs[],
   const double &random_logs[],
   const DALM0001LogRtvStats &node_stats,
   const DALM0001LogRtvStats &random_stats,
   DALM0001LogRtvComparison &cmp
)
{
   cmp.paired_count = MathMin(ArraySize(node_logs), ArraySize(random_logs));
   cmp.delta_log_mean = node_stats.log_mean - random_stats.log_mean;
   cmp.delta_log_median = node_stats.log_median - random_stats.log_median;
   cmp.delta_pct_log_gt_zero = node_stats.pct_log_gt_zero - random_stats.pct_log_gt_zero;
   cmp.paired_win_pct = 0.0;
   cmp.paired_mean_delta = 0.0;
   cmp.paired_t_stat = 0.0;
   cmp.cohen_d = 0.0;
   cmp.ks_real_vs_random = DAL_M0001KsTwoSample(node_logs, random_logs);

   if(cmp.paired_count <= 0)
      return;

   int wins = 0;
   double sum_delta = 0.0;

   for(int i = 0; i < cmp.paired_count; i++)
   {
      double d = node_logs[i] - random_logs[i];
      sum_delta += d;

      if(d > 0.0)
         wins++;
   }

   cmp.paired_win_pct = 100.0 * wins / cmp.paired_count;
   cmp.paired_mean_delta = sum_delta / cmp.paired_count;

   if(cmp.paired_count > 1)
   {
      double var = 0.0;
      for(int i = 0; i < cmp.paired_count; i++)
      {
         double d = node_logs[i] - random_logs[i] - cmp.paired_mean_delta;
         var += d * d;
      }

      var /= (cmp.paired_count - 1);
      double sd = MathSqrt(var);

      if(sd > 0.0)
         cmp.paired_t_stat = cmp.paired_mean_delta / (sd / MathSqrt(cmp.paired_count));
   }

   double pooled_var = (node_stats.log_stdev * node_stats.log_stdev + random_stats.log_stdev * random_stats.log_stdev) / 2.0;
   if(pooled_var > 0.0)
      cmp.cohen_d = cmp.delta_log_mean / MathSqrt(pooled_var);
}

string DAL_M0001Fmt4(const double value)
{
   return DoubleToString(value, 4);
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
   const DALM0001LogRtvStats &stats,
   const double &log_values[]
)
{
   return label
      + "*n=" + IntegerToString(stats.count)
      + "*rawMean=" + DAL_M0001Fmt4(stats.raw_mean)
      + "*rawMed=" + DAL_M0001Fmt4(stats.raw_median)
      + "*rawP90=" + DAL_M0001Fmt4(stats.raw_p90)
      + "*rawP95=" + DAL_M0001Fmt4(stats.raw_p95)
      + "*logMean=" + DAL_M0001Fmt4(stats.log_mean)
      + "*logMed=" + DAL_M0001Fmt4(stats.log_median)
      + "*logGt0Pct=" + DAL_M0001Fmt4(stats.pct_log_gt_zero)
      + "*skew=" + DAL_M0001Fmt4(stats.log_skewness)
      + "*exKurt=" + DAL_M0001Fmt4(stats.log_excess_kurtosis)
      + "*JB=" + DAL_M0001Fmt4(stats.log_jarque_bera)
      + "*KSnorm=" + DAL_M0001Fmt4(stats.log_ks_normal)
      + "*tail2xN=" + DAL_M0001Fmt4(stats.tail2_ratio_normal)
      + "*tail3xN=" + DAL_M0001Fmt4(stats.tail3_ratio_normal)
      + "*histRaw=" + DAL_M0001CompactHistCounts(log_values);
}

string DAL_M0001ComparisonCompactText(const DALM0001LogRtvComparison &cmp)
{
   return "COMPARE"
      + "*pairs=" + IntegerToString(cmp.paired_count)
      + "*dLogMean=" + DAL_M0001Fmt4(cmp.delta_log_mean)
      + "*dLogMed=" + DAL_M0001Fmt4(cmp.delta_log_median)
      + "*dGt0Pct=" + DAL_M0001Fmt4(cmp.delta_pct_log_gt_zero)
      + "*winPct=" + DAL_M0001Fmt4(cmp.paired_win_pct)
      + "*pairedMeanDelta=" + DAL_M0001Fmt4(cmp.paired_mean_delta)
      + "*pairedT=" + DAL_M0001Fmt4(cmp.paired_t_stat)
      + "*cohenD=" + DAL_M0001Fmt4(cmp.cohen_d)
      + "*KS_node_vs_random=" + DAL_M0001Fmt4(cmp.ks_real_vs_random);
}

string DAL_M0001BuildLogRtvNullComparisonLine(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const string symbol,
   const string timeframe
)
{
   double node_logs[];
   double random_logs[];

   DAL_M0001CollectNodeLogRtvs(events, events_count, node_logs);
   DAL_M0001CollectRandomLogRtvs(events, events_count, bars, bars_count, random_logs);

   DALM0001LogRtvStats node_stats;
   DALM0001LogRtvStats random_stats;

   DAL_M0001ComputeLogRtvStats(node_logs, node_stats);
   DAL_M0001ComputeLogRtvStats(random_logs, random_stats);

   DALM0001LogRtvComparison cmp;
   DAL_M0001ComputeLogRtvComparison(node_logs, random_logs, node_stats, random_stats, cmp);

   return "DAL_M0001_LOGRTV_NULL"
      + " *** symbol=" + symbol
      + "*tf=" + timeframe
      + "*events=" + IntegerToString(events_count)
      + " *** " + DAL_M0001StatsCompactText("NODES", node_stats, node_logs)
      + " *** " + DAL_M0001StatsCompactText("RANDOM", random_stats, random_logs)
      + " *** " + DAL_M0001ComparisonCompactText(cmp);
}

string DAL_M0001LogRtvNullSignature(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count
)
{
   double node_logs[];
   double random_logs[];

   DAL_M0001CollectNodeLogRtvs(events, events_count, node_logs);
   DAL_M0001CollectRandomLogRtvs(events, events_count, bars, bars_count, random_logs);

   DALM0001LogRtvStats node_stats;
   DALM0001LogRtvStats random_stats;

   DAL_M0001ComputeLogRtvStats(node_logs, node_stats);
   DAL_M0001ComputeLogRtvStats(random_logs, random_stats);

   return "n=" + IntegerToString(node_stats.count)
      + "|r=" + IntegerToString(random_stats.count)
      + "|nMean=" + DAL_M0001Fmt4(node_stats.log_mean)
      + "|rMean=" + DAL_M0001Fmt4(random_stats.log_mean)
      + "|nMed=" + DAL_M0001Fmt4(node_stats.log_median)
      + "|rMed=" + DAL_M0001Fmt4(random_stats.log_median);
}

void DAL_M0001PrintLogRtvNullComparisonWhenChanged(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const string symbol,
   const string timeframe
)
{
   string signature = DAL_M0001LogRtvNullSignature(events, events_count, bars, bars_count);
   if(signature == DAL_M0001_NULL_LAST_SIGNATURE)
      return;

   double node_logs[];
   int node_count = DAL_M0001CollectNodeLogRtvs(events, events_count, node_logs);
   if(node_count <= 0)
      return;

   DAL_M0001_NULL_LAST_SIGNATURE = signature;

   Print(DAL_M0001BuildLogRtvNullComparisonLine(events, events_count, bars, bars_count, symbol, timeframe));
}


string DAL_M0001FinalLinePrefix(
   const string tag,
   const string symbol,
   const string timeframe,
   const string source_mode,
   const int events_count
)
{
   return tag
      + " *** symbol=" + symbol
      + "*tf=" + timeframe
      + "*source=" + source_mode
      + "*events=" + IntegerToString(events_count)
      + " *** ";
}

void DAL_M0001PrintFinalNodeRandomReports(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const string symbol,
   const string timeframe,
   const string source_mode
)
{
   double node_logs[];
   double random_logs[];

   DAL_M0001CollectNodeLogRtvs(events, events_count, node_logs);
   DAL_M0001CollectRandomLogRtvs(events, events_count, bars, bars_count, random_logs);

   DALM0001LogRtvStats node_stats;
   DALM0001LogRtvStats random_stats;

   DAL_M0001ComputeLogRtvStats(node_logs, node_stats);
   DAL_M0001ComputeLogRtvStats(random_logs, random_stats);

   DALM0001LogRtvComparison cmp;
   DAL_M0001ComputeLogRtvComparison(node_logs, random_logs, node_stats, random_stats, cmp);

   Print(
      DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_NODES", symbol, timeframe, source_mode, events_count),
      DAL_M0001StatsCompactText("NODES", node_stats, node_logs)
   );

   Print(
      DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_RANDOM", symbol, timeframe, source_mode, events_count),
      DAL_M0001StatsCompactText("RANDOM", random_stats, random_logs),
      " *** ",
      DAL_M0001ComparisonCompactText(cmp)
   );
}


#endif
