#ifndef __DAL_M0001_RTV_DISTRIBUTION_MQH__
#define __DAL_M0001_RTV_DISTRIBUTION_MQH__

#include <M0001/DAL_M0001Types.mqh>

struct DALM0001RtvDistributionStats
{
   int count;

   double mean;
   double median;
   double min_value;
   double max_value;
   double range_value;

   double variance;
   double stdev;
   double sample_variance;
   double sample_stdev;
   double coeff_variation;

   double q1;
   double q3;
   double iqr;
   double mad;
   double robust_sigma_mad;
   double stdev_to_robust_sigma;

   double p01;
   double p05;
   double p10;
   double p25;
   double p50;
   double p75;
   double p90;
   double p95;
   double p99;

   double skewness;
   double excess_kurtosis;
   double jarque_bera;
   double ks_distance;
   double ad_statistic;

   double tail2_actual_pct;
   double tail3_actual_pct;
   double right_tail2_pct;
   double left_tail2_pct;
   double right_tail3_pct;
   double left_tail3_pct;

   double tail2_ratio_to_normal;
   double tail3_ratio_to_normal;
   double right_tail2_ratio_to_normal;
   double left_tail2_ratio_to_normal;
   double right_tail3_ratio_to_normal;
   double left_tail3_ratio_to_normal;

   double p95_p05_width;
   double p99_p01_width;
   double robust_tail90_ratio_to_normal;
   double robust_tail98_ratio_to_normal;
};

string DAL_M0001_DISTRIBUTION_LAST_SIGNATURE = "";

bool DAL_M0001DistIsValidNumber(const double value)
{
   if(!(value == value))
      return false;

   if(value == DBL_MAX || value == -DBL_MAX)
      return false;

   return true;
}

void DAL_M0001DistReset(DALM0001RtvDistributionStats &stats)
{
   stats.count = 0;

   stats.mean = 0.0;
   stats.median = 0.0;
   stats.min_value = 0.0;
   stats.max_value = 0.0;
   stats.range_value = 0.0;

   stats.variance = 0.0;
   stats.stdev = 0.0;
   stats.sample_variance = 0.0;
   stats.sample_stdev = 0.0;
   stats.coeff_variation = 0.0;

   stats.q1 = 0.0;
   stats.q3 = 0.0;
   stats.iqr = 0.0;
   stats.mad = 0.0;
   stats.robust_sigma_mad = 0.0;
   stats.stdev_to_robust_sigma = 0.0;

   stats.p01 = 0.0;
   stats.p05 = 0.0;
   stats.p10 = 0.0;
   stats.p25 = 0.0;
   stats.p50 = 0.0;
   stats.p75 = 0.0;
   stats.p90 = 0.0;
   stats.p95 = 0.0;
   stats.p99 = 0.0;

   stats.skewness = 0.0;
   stats.excess_kurtosis = 0.0;
   stats.jarque_bera = 0.0;
   stats.ks_distance = 0.0;
   stats.ad_statistic = 0.0;

   stats.tail2_actual_pct = 0.0;
   stats.tail3_actual_pct = 0.0;
   stats.right_tail2_pct = 0.0;
   stats.left_tail2_pct = 0.0;
   stats.right_tail3_pct = 0.0;
   stats.left_tail3_pct = 0.0;

   stats.tail2_ratio_to_normal = 0.0;
   stats.tail3_ratio_to_normal = 0.0;
   stats.right_tail2_ratio_to_normal = 0.0;
   stats.left_tail2_ratio_to_normal = 0.0;
   stats.right_tail3_ratio_to_normal = 0.0;
   stats.left_tail3_ratio_to_normal = 0.0;

   stats.p95_p05_width = 0.0;
   stats.p99_p01_width = 0.0;
   stats.robust_tail90_ratio_to_normal = 0.0;
   stats.robust_tail98_ratio_to_normal = 0.0;
}

int DAL_M0001DistCollectReadyRtvs(
   const DALM0001Event &events[],
   const int events_count,
   double &values[]
)
{
   ArrayResize(values, 0);

   for(int i = 0; i < events_count; i++)
   {
      if(!events[i].closed)
         continue;

      if(!events[i].rtv_ready)
         continue;

      double value = events[i].rtv;

      if(!DAL_M0001DistIsValidNumber(value))
         continue;

      if(value <= 0.0)
         continue;

      int size = ArraySize(values);
      ArrayResize(values, size + 1);
      values[size] = value;
   }

   return ArraySize(values);
}

double DAL_M0001DistPercentileSorted(const double &sorted[], const double percentile)
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

double DAL_M0001DistNormalCdf(const double z)
{
   // Abramowitz-Stegun style approximation for the standard normal CDF.
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

double DAL_M0001DistSafeDiv(const double numerator, const double denominator)
{
   if(MathAbs(denominator) <= DBL_EPSILON)
      return 0.0;

   return numerator / denominator;
}

void DAL_M0001DistCompute(
   const double &values[],
   DALM0001RtvDistributionStats &stats
)
{
   DAL_M0001DistReset(stats);

   int count = ArraySize(values);
   if(count <= 0)
      return;

   stats.count = count;

   double sorted[];
   ArrayResize(sorted, count);

   for(int i = 0; i < count; i++)
      sorted[i] = values[i];

   ArraySort(sorted);

   stats.min_value = sorted[0];
   stats.max_value = sorted[count - 1];
   stats.range_value = stats.max_value - stats.min_value;

   double total = 0.0;
   for(int i = 0; i < count; i++)
      total += values[i];

   stats.mean = total / count;

   stats.p01 = DAL_M0001DistPercentileSorted(sorted, 0.01);
   stats.p05 = DAL_M0001DistPercentileSorted(sorted, 0.05);
   stats.p10 = DAL_M0001DistPercentileSorted(sorted, 0.10);
   stats.p25 = DAL_M0001DistPercentileSorted(sorted, 0.25);
   stats.p50 = DAL_M0001DistPercentileSorted(sorted, 0.50);
   stats.p75 = DAL_M0001DistPercentileSorted(sorted, 0.75);
   stats.p90 = DAL_M0001DistPercentileSorted(sorted, 0.90);
   stats.p95 = DAL_M0001DistPercentileSorted(sorted, 0.95);
   stats.p99 = DAL_M0001DistPercentileSorted(sorted, 0.99);

   stats.median = stats.p50;
   stats.q1 = stats.p25;
   stats.q3 = stats.p75;
   stats.iqr = stats.q3 - stats.q1;
   stats.p95_p05_width = stats.p95 - stats.p05;
   stats.p99_p01_width = stats.p99 - stats.p01;

   double m2 = 0.0;
   double m3 = 0.0;
   double m4 = 0.0;

   for(int i = 0; i < count; i++)
   {
      double d = values[i] - stats.mean;
      double d2 = d * d;

      m2 += d2;
      m3 += d2 * d;
      m4 += d2 * d2;
   }

   m2 /= count;
   m3 /= count;
   m4 /= count;

   stats.variance = m2;
   stats.stdev = MathSqrt(stats.variance);

   if(count > 1)
   {
      stats.sample_variance = stats.variance * count / (count - 1);
      stats.sample_stdev = MathSqrt(stats.sample_variance);
   }

   stats.coeff_variation = DAL_M0001DistSafeDiv(stats.stdev, stats.mean);

   if(stats.stdev > 0.0)
   {
      stats.skewness = m3 / MathPow(stats.stdev, 3);
      stats.excess_kurtosis = m4 / MathPow(stats.stdev, 4) - 3.0;
      stats.jarque_bera = count / 6.0 * (stats.skewness * stats.skewness + 0.25 * stats.excess_kurtosis * stats.excess_kurtosis);
   }

   double deviations[];
   ArrayResize(deviations, count);

   for(int i = 0; i < count; i++)
      deviations[i] = MathAbs(values[i] - stats.median);

   ArraySort(deviations);
   stats.mad = DAL_M0001DistPercentileSorted(deviations, 0.50);
   stats.robust_sigma_mad = 1.4826 * stats.mad;
   stats.stdev_to_robust_sigma = DAL_M0001DistSafeDiv(stats.stdev, stats.robust_sigma_mad);

   if(stats.stdev > 0.0)
   {
      int tail2 = 0;
      int tail3 = 0;
      int right2 = 0;
      int left2 = 0;
      int right3 = 0;
      int left3 = 0;

      for(int i = 0; i < count; i++)
      {
         double z = (values[i] - stats.mean) / stats.stdev;

         if(MathAbs(z) >= 2.0)
            tail2++;
         if(MathAbs(z) >= 3.0)
            tail3++;

         if(z >= 2.0)
            right2++;
         if(z <= -2.0)
            left2++;

         if(z >= 3.0)
            right3++;
         if(z <= -3.0)
            left3++;
      }

      stats.tail2_actual_pct = 100.0 * tail2 / count;
      stats.tail3_actual_pct = 100.0 * tail3 / count;
      stats.right_tail2_pct = 100.0 * right2 / count;
      stats.left_tail2_pct = 100.0 * left2 / count;
      stats.right_tail3_pct = 100.0 * right3 / count;
      stats.left_tail3_pct = 100.0 * left3 / count;

      // Normal benchmarks:
      // Two-sided: |Z| >= 2 -> 4.5500%, |Z| >= 3 -> 0.2700%
      // One-sided: Z >= 2 or Z <= -2 -> 2.2750%, Z >= 3 or Z <= -3 -> 0.1350%
      stats.tail2_ratio_to_normal = DAL_M0001DistSafeDiv(stats.tail2_actual_pct, 4.550026);
      stats.tail3_ratio_to_normal = DAL_M0001DistSafeDiv(stats.tail3_actual_pct, 0.269980);
      stats.right_tail2_ratio_to_normal = DAL_M0001DistSafeDiv(stats.right_tail2_pct, 2.275013);
      stats.left_tail2_ratio_to_normal = DAL_M0001DistSafeDiv(stats.left_tail2_pct, 2.275013);
      stats.right_tail3_ratio_to_normal = DAL_M0001DistSafeDiv(stats.right_tail3_pct, 0.134990);
      stats.left_tail3_ratio_to_normal = DAL_M0001DistSafeDiv(stats.left_tail3_pct, 0.134990);

      // Normal percentile-width benchmarks:
      // p95-p05 = 3.289707 * sigma, p99-p01 = 4.652696 * sigma.
      stats.robust_tail90_ratio_to_normal = DAL_M0001DistSafeDiv(stats.p95_p05_width, 3.289707 * stats.stdev);
      stats.robust_tail98_ratio_to_normal = DAL_M0001DistSafeDiv(stats.p99_p01_width, 4.652696 * stats.stdev);
   }

   if(stats.stdev > 0.0)
   {
      double max_ks = 0.0;
      double ad_sum = 0.0;
      double eps = 0.000000000001;

      for(int i = 0; i < count; i++)
      {
         double z = (sorted[i] - stats.mean) / stats.stdev;
         double f = DAL_M0001DistNormalCdf(z);

         if(f < eps)
            f = eps;
         if(f > 1.0 - eps)
            f = 1.0 - eps;

         double d_plus = (i + 1.0) / count - f;
         double d_minus = f - i / (double)count;

         if(d_plus > max_ks)
            max_ks = d_plus;
         if(d_minus > max_ks)
            max_ks = d_minus;

         double z_rev = (sorted[count - 1 - i] - stats.mean) / stats.stdev;
         double f_rev = DAL_M0001DistNormalCdf(z_rev);

         if(f_rev < eps)
            f_rev = eps;
         if(f_rev > 1.0 - eps)
            f_rev = 1.0 - eps;

         ad_sum += (2.0 * (i + 1.0) - 1.0) * (MathLog(f) + MathLog(1.0 - f_rev));
      }

      stats.ks_distance = max_ks;
      stats.ad_statistic = -count - ad_sum / count;
      stats.ad_statistic *= (1.0 + 0.75 / count + 2.25 / (count * count));
   }
}

string DAL_M0001DistFmt(const double value, const int digits = 6)
{
   if(!DAL_M0001DistIsValidNumber(value))
      return "n/a";

   return DoubleToString(value, digits);
}

string DAL_M0001DistBar(const int length)
{
   string out = "";
   for(int i = 0; i < length; i++)
      out += "#";

   return out;
}

string DAL_M0001DistHistogramTsv(
   const double &values[],
   const DALM0001RtvDistributionStats &stats
)
{
   int count = ArraySize(values);
   if(count <= 0)
      return "";

   if(stats.max_value <= stats.min_value)
      return "histogram_bin\tfrom\tto\tcount\tpct\tbar\n1\t" + DAL_M0001DistFmt(stats.min_value, 6) + "\t" + DAL_M0001DistFmt(stats.max_value, 6) + "\t" + IntegerToString(count) + "\t100.00\t##############################\n";

   int bins = (int)MathCeil(MathSqrt(count));
   if(bins < 8)
      bins = 8;
   if(bins > 30)
      bins = 30;

   int counts[];
   ArrayResize(counts, bins);
   ArrayInitialize(counts, 0);

   double width = (stats.max_value - stats.min_value) / bins;

   for(int i = 0; i < count; i++)
   {
      int b = (int)MathFloor((values[i] - stats.min_value) / width);

      if(b < 0)
         b = 0;
      if(b >= bins)
         b = bins - 1;

      counts[b]++;
   }

   int max_count = 0;
   for(int b = 0; b < bins; b++)
   {
      if(counts[b] > max_count)
         max_count = counts[b];
   }

   string out = "histogram_bin\tfrom\tto\tcount\tpct\tbar\n";

   for(int b = 0; b < bins; b++)
   {
      double from = stats.min_value + width * b;
      double to = from + width;
      double pct = 100.0 * counts[b] / count;
      int bar_len = max_count > 0 ? (int)MathRound(30.0 * counts[b] / max_count) : 0;

      out += IntegerToString(b + 1)
         + "\t" + DAL_M0001DistFmt(from, 6)
         + "\t" + DAL_M0001DistFmt(to, 6)
         + "\t" + IntegerToString(counts[b])
         + "\t" + DAL_M0001DistFmt(pct, 2)
         + "\t" + DAL_M0001DistBar(bar_len)
         + "\n";
   }

   return out;
}

string DAL_M0001DistEvidenceText(const DALM0001RtvDistributionStats &stats)
{
   string out = "";

   if(stats.count < 30)
      out += "sample_warning\tn<30; distribution evidence is weak\n";
   else if(stats.count < 100)
      out += "sample_warning\tn<100; useful but still medium confidence\n";
   else
      out += "sample_warning\tn>=100; distribution evidence is more stable\n";

   if(stats.excess_kurtosis > 1.0)
      out += "fat_tail_kurtosis\tYES; excess_kurtosis>1\n";
   else
      out += "fat_tail_kurtosis\tNO_STRONG_SIGNAL_BY_KURTOSIS\n";

   if(stats.tail3_ratio_to_normal > 2.0)
      out += "fat_tail_3sigma\tYES; actual 3-sigma tail more than 2x normal\n";
   else
      out += "fat_tail_3sigma\tNO_STRONG_SIGNAL_BY_3SIGMA_RATIO\n";

   if(stats.ks_distance > 0.10)
      out += "normal_distance_ks\tLARGE; KS distance > 0.10\n";
   else if(stats.ks_distance > 0.05)
      out += "normal_distance_ks\tMEDIUM; KS distance > 0.05\n";
   else
      out += "normal_distance_ks\tLOW_BY_KS\n";

   if(MathAbs(stats.skewness) > 1.0)
      out += "skewness_signal\tSTRONG_ASYMMETRY\n";
   else if(MathAbs(stats.skewness) > 0.50)
      out += "skewness_signal\tMEDIUM_ASYMMETRY\n";
   else
      out += "skewness_signal\tLOW_ASYMMETRY\n";

   return out;
}

string DAL_M0001BuildRtvDistributionReport(
   const DALM0001Event &events[],
   const int events_count,
   const int bars_count,
   const int nodes_count,
   const int audit_states_count,
   const string source_mode,
   const string symbol,
   const string timeframe
)
{
   double values[];
   int ready_count = DAL_M0001DistCollectReadyRtvs(events, events_count, values);

   DALM0001RtvDistributionStats stats;
   DAL_M0001DistCompute(values, stats);

   string out = "";
   out += "DAL_M0001_RTV_DISTRIBUTION_REPORT_BEGIN\n";
   out += "symbol\t" + symbol + "\n";
   out += "timeframe\t" + timeframe + "\n";
   out += "source\t" + source_mode + "\n";
   out += "bars\t" + IntegerToString(bars_count) + "\n";
   out += "nodes\t" + IntegerToString(nodes_count) + "\n";
   out += "events\t" + IntegerToString(events_count) + "\n";
   out += "audit_states\t" + IntegerToString(audit_states_count) + "\n";
   out += "rtv_ready_count\t" + IntegerToString(ready_count) + "\n";
   out += "\n";

   out += "metric\tvalue\n";
   out += "mean\t" + DAL_M0001DistFmt(stats.mean, 8) + "\n";
   out += "median\t" + DAL_M0001DistFmt(stats.median, 8) + "\n";
   out += "min\t" + DAL_M0001DistFmt(stats.min_value, 8) + "\n";
   out += "max\t" + DAL_M0001DistFmt(stats.max_value, 8) + "\n";
   out += "range\t" + DAL_M0001DistFmt(stats.range_value, 8) + "\n";
   out += "variance\t" + DAL_M0001DistFmt(stats.variance, 8) + "\n";
   out += "stdev\t" + DAL_M0001DistFmt(stats.stdev, 8) + "\n";
   out += "sample_variance\t" + DAL_M0001DistFmt(stats.sample_variance, 8) + "\n";
   out += "sample_stdev\t" + DAL_M0001DistFmt(stats.sample_stdev, 8) + "\n";
   out += "coeff_variation\t" + DAL_M0001DistFmt(stats.coeff_variation, 8) + "\n";
   out += "p01\t" + DAL_M0001DistFmt(stats.p01, 8) + "\n";
   out += "p05\t" + DAL_M0001DistFmt(stats.p05, 8) + "\n";
   out += "p10\t" + DAL_M0001DistFmt(stats.p10, 8) + "\n";
   out += "p25_q1\t" + DAL_M0001DistFmt(stats.p25, 8) + "\n";
   out += "p50_median\t" + DAL_M0001DistFmt(stats.p50, 8) + "\n";
   out += "p75_q3\t" + DAL_M0001DistFmt(stats.p75, 8) + "\n";
   out += "p90\t" + DAL_M0001DistFmt(stats.p90, 8) + "\n";
   out += "p95\t" + DAL_M0001DistFmt(stats.p95, 8) + "\n";
   out += "p99\t" + DAL_M0001DistFmt(stats.p99, 8) + "\n";
   out += "iqr\t" + DAL_M0001DistFmt(stats.iqr, 8) + "\n";
   out += "mad\t" + DAL_M0001DistFmt(stats.mad, 8) + "\n";
   out += "robust_sigma_mad\t" + DAL_M0001DistFmt(stats.robust_sigma_mad, 8) + "\n";
   out += "stdev_to_robust_sigma\t" + DAL_M0001DistFmt(stats.stdev_to_robust_sigma, 8) + "\n";
   out += "skewness\t" + DAL_M0001DistFmt(stats.skewness, 8) + "\n";
   out += "excess_kurtosis\t" + DAL_M0001DistFmt(stats.excess_kurtosis, 8) + "\n";
   out += "jarque_bera\t" + DAL_M0001DistFmt(stats.jarque_bera, 8) + "\n";
   out += "ks_distance_to_fitted_normal\t" + DAL_M0001DistFmt(stats.ks_distance, 8) + "\n";
   out += "anderson_darling_to_fitted_normal\t" + DAL_M0001DistFmt(stats.ad_statistic, 8) + "\n";
   out += "tail2_actual_pct\t" + DAL_M0001DistFmt(stats.tail2_actual_pct, 6) + "\n";
   out += "tail2_normal_expected_pct\t4.550026\n";
   out += "tail2_ratio_to_normal\t" + DAL_M0001DistFmt(stats.tail2_ratio_to_normal, 8) + "\n";
   out += "tail3_actual_pct\t" + DAL_M0001DistFmt(stats.tail3_actual_pct, 6) + "\n";
   out += "tail3_normal_expected_pct\t0.269980\n";
   out += "tail3_ratio_to_normal\t" + DAL_M0001DistFmt(stats.tail3_ratio_to_normal, 8) + "\n";
   out += "right_tail2_pct\t" + DAL_M0001DistFmt(stats.right_tail2_pct, 6) + "\n";
   out += "left_tail2_pct\t" + DAL_M0001DistFmt(stats.left_tail2_pct, 6) + "\n";
   out += "right_tail3_pct\t" + DAL_M0001DistFmt(stats.right_tail3_pct, 6) + "\n";
   out += "left_tail3_pct\t" + DAL_M0001DistFmt(stats.left_tail3_pct, 6) + "\n";
   out += "right_tail2_ratio_to_normal\t" + DAL_M0001DistFmt(stats.right_tail2_ratio_to_normal, 8) + "\n";
   out += "left_tail2_ratio_to_normal\t" + DAL_M0001DistFmt(stats.left_tail2_ratio_to_normal, 8) + "\n";
   out += "right_tail3_ratio_to_normal\t" + DAL_M0001DistFmt(stats.right_tail3_ratio_to_normal, 8) + "\n";
   out += "left_tail3_ratio_to_normal\t" + DAL_M0001DistFmt(stats.left_tail3_ratio_to_normal, 8) + "\n";
   out += "p95_p05_width\t" + DAL_M0001DistFmt(stats.p95_p05_width, 8) + "\n";
   out += "p99_p01_width\t" + DAL_M0001DistFmt(stats.p99_p01_width, 8) + "\n";
   out += "robust_tail90_ratio_to_normal\t" + DAL_M0001DistFmt(stats.robust_tail90_ratio_to_normal, 8) + "\n";
   out += "robust_tail98_ratio_to_normal\t" + DAL_M0001DistFmt(stats.robust_tail98_ratio_to_normal, 8) + "\n";
   out += "\n";

   out += "evidence\tresult\n";
   out += DAL_M0001DistEvidenceText(stats);
   out += "\n";

   out += DAL_M0001DistHistogramTsv(values, stats);
   out += "DAL_M0001_RTV_DISTRIBUTION_REPORT_END";

   return out;
}

string DAL_M0001RtvDistributionSignature(
   const DALM0001Event &events[],
   const int events_count
)
{
   double values[];
   int ready_count = DAL_M0001DistCollectReadyRtvs(events, events_count, values);

   DALM0001RtvDistributionStats stats;
   DAL_M0001DistCompute(values, stats);

   return "ready=" + IntegerToString(ready_count)
      + "|mean=" + DAL_M0001DistFmt(stats.mean, 8)
      + "|median=" + DAL_M0001DistFmt(stats.median, 8)
      + "|kurt=" + DAL_M0001DistFmt(stats.excess_kurtosis, 8)
      + "|ks=" + DAL_M0001DistFmt(stats.ks_distance, 8);
}

void DAL_M0001PrintRtvDistributionReportWhenChanged(
   const DALM0001Event &events[],
   const int events_count,
   const int bars_count,
   const int nodes_count,
   const int audit_states_count,
   const string source_mode,
   const string symbol,
   const string timeframe
)
{
   string signature = DAL_M0001RtvDistributionSignature(events, events_count);
   if(signature == DAL_M0001_DISTRIBUTION_LAST_SIGNATURE)
      return;

   double values[];
   int ready_count = DAL_M0001DistCollectReadyRtvs(events, events_count, values);
   if(ready_count <= 0)
      return;

   DAL_M0001_DISTRIBUTION_LAST_SIGNATURE = signature;

   string report = DAL_M0001BuildRtvDistributionReport(
      events,
      events_count,
      bars_count,
      nodes_count,
      audit_states_count,
      source_mode,
      symbol,
      timeframe
   );

   Print(report);
}

#endif
