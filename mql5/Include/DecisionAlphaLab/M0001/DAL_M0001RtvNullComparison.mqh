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

   bool run_stress_suite;
   int broker_utc_offset_hours;
   int regime_lookback_bars;
   int hard_random_candidates;
   int placebo_shift_bars;
   int nonoverlap_gap_bars;
   int block_bootstrap_iterations;
   int block_bootstrap_block_pairs;
   int horizon_bars_1;
   int horizon_bars_2;
   int horizon_bars_3;
   int horizon_bars_4;
};

struct DALM0001PairedLogRtv
{
   int event_id;
   int sample_length;
   datetime entry_time;
   int entry_index;
   double pre_entry_vol;
   int utc_hour;
   int utc_session;
   int trend_regime;
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
   config.run_stress_suite = true;
   config.broker_utc_offset_hours = 0;
   config.regime_lookback_bars = 100;
   config.hard_random_candidates = 80;
   config.placebo_shift_bars = 50;
   config.nonoverlap_gap_bars = 0;
   config.block_bootstrap_iterations = 300;
   config.block_bootstrap_block_pairs = 25;
   config.horizon_bars_1 = 5;
   config.horizon_bars_2 = 10;
   config.horizon_bars_3 = 20;
   config.horizon_bars_4 = 50;
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


int DAL_M0001NormalizeHour(const int hour)
{
   int h = hour % 24;
   if(h < 0)
      h += 24;
   return h;
}

int DAL_M0001UtcHourFromBrokerTime(
   const datetime broker_time,
   const int broker_utc_offset_hours
)
{
   MqlDateTime dt;
   TimeToStruct(broker_time, dt);
   return DAL_M0001NormalizeHour(dt.hour - broker_utc_offset_hours);
}

int DAL_M0001UtcSessionFromHour(const int utc_hour)
{
   int h = DAL_M0001NormalizeHour(utc_hour);
   if(h >= 0 && h < 7)
      return 0; // Asia / early UTC
   if(h >= 7 && h < 13)
      return 1; // London core
   if(h >= 13 && h < 21)
      return 2; // New York core
   return 3; // late/rollover/other
}

string DAL_M0001SessionName(const int session)
{
   if(session == 0)
      return "asia";
   if(session == 1)
      return "london";
   if(session == 2)
      return "ny";
   return "other";
}

int DAL_M0001BarIndexByTime(
   const DALBar &bars[],
   const int bars_count,
   const datetime time
)
{
   if(bars_count <= 0)
      return -1;

   int idx = DAL_M0001FirstIndexAtOrAfter(bars, bars_count, time);
   if(idx >= 0 && idx < bars_count)
      return idx;

   return -1;
}

double DAL_M0001PreEntryVol(
   const DALBar &bars[],
   const int bars_count,
   const int entry_index,
   const int lookback_bars
)
{
   int lookback = lookback_bars;
   if(lookback < 1)
      lookback = 1;

   int start = entry_index - lookback;
   if(start < 0)
      start = 0;

   int end = entry_index - 1;
   if(end < start || end >= bars_count)
      return 0.0;

   double sum = 0.0;
   int used = 0;
   for(int i = start; i <= end; i++)
   {
      double v = DAL_LogRange(bars[i].high, bars[i].low);
      if(!DAL_M0001NullValidNumber(v) || v <= 0.0)
         continue;
      sum += v;
      used++;
   }

   if(used <= 0)
      return 0.0;
   return sum / used;
}

int DAL_M0001PreEntryTrendRegime(
   const DALBar &bars[],
   const int bars_count,
   const int entry_index,
   const int lookback_bars
)
{
   int lookback = lookback_bars;
   if(lookback < 1)
      lookback = 1;

   int start = entry_index - lookback;
   if(start < 0)
      start = 0;

   int end = entry_index - 1;
   if(start < 0 || end <= start || end >= bars_count)
      return 0;

   if(bars[start].close <= 0.0 || bars[end].close <= 0.0)
      return 0;

   double ret = MathLog(bars[end].close / bars[start].close);
   double pre_vol = DAL_M0001PreEntryVol(bars, bars_count, entry_index, lookback);
   double threshold = pre_vol * MathSqrt((double)(end - start + 1));
   if(threshold <= 0.0)
      threshold = 0.0;

   if(ret > threshold)
      return 1;
   if(ret < -threshold)
      return -1;
   return 0;
}

int DAL_M0001ClassifyTercile(
   const double value,
   const double low_threshold,
   const double high_threshold
)
{
   if(value <= low_threshold)
      return 0;
   if(value >= high_threshold)
      return 2;
   return 1;
}

bool DAL_M0001LogRtvAtEntryIndex(
   const DALBar &bars[],
   const int bars_count,
   const int entry_index,
   const int sample_length,
   double &log_rtv
)
{
   log_rtv = 0.0;
   int n = sample_length;
   if(n <= 0)
      return false;

   if(entry_index - n < 0 || entry_index + n > bars_count)
      return false;

   double mean_inside = DAL_M0001MeanLogMoveWindow(bars, bars_count, entry_index, n);
   double mean_before = DAL_M0001MeanLogMoveWindow(bars, bars_count, entry_index - n, n);
   if(mean_inside <= 0.0 || mean_before <= 0.0)
      return false;

   double rtv = mean_inside / mean_before;
   if(rtv <= 0.0 || !DAL_M0001NullValidNumber(rtv))
      return false;

   log_rtv = MathLog(rtv);
   return true;
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
   const int broker_utc_offset_hours,
   const int regime_lookback_bars,
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
      int entry_index = DAL_M0001BarIndexByTime(bars, bars_count, events[i].entry_time);
      if(entry_index < 0)
         continue;

      double pre_vol = DAL_M0001PreEntryVol(bars, bars_count, entry_index, regime_lookback_bars);
      int utc_hour = DAL_M0001UtcHourFromBrokerTime(events[i].entry_time, broker_utc_offset_hours);
      int utc_session = DAL_M0001UtcSessionFromHour(utc_hour);
      int trend_regime = DAL_M0001PreEntryTrendRegime(bars, bars_count, entry_index, regime_lookback_bars);

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
      pairs[size].entry_index = entry_index;
      pairs[size].pre_entry_vol = pre_vol;
      pairs[size].utc_hour = utc_hour;
      pairs[size].utc_session = utc_session;
      pairs[size].trend_regime = trend_regime;
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
   const int broker_utc_offset_hours
)
{
   int count = ArraySize(pairs);
   if(count <= 0)
      return "SESSION_REGIME*empty=1";

   double pre_vols[];
   ArrayResize(pre_vols, count);
   for(int i = 0; i < count; i++)
      pre_vols[i] = pairs[i].pre_entry_vol;
   ArraySort(pre_vols);

   double v33 = DAL_M0001NullPercentileSorted(pre_vols, 0.3333);
   double v66 = DAL_M0001NullPercentileSorted(pre_vols, 0.6667);

   int session_count[4];
   int session_wins[4];
   double session_sum[4];
   ArrayInitialize(session_count, 0);
   ArrayInitialize(session_wins, 0);
   ArrayInitialize(session_sum, 0.0);

   int regime_count[3];
   int regime_wins[3];
   double regime_sum[3];
   ArrayInitialize(regime_count, 0);
   ArrayInitialize(regime_wins, 0);
   ArrayInitialize(regime_sum, 0.0);

   int trend_count[3];
   int trend_wins[3];
   double trend_sum[3];
   ArrayInitialize(trend_count, 0);
   ArrayInitialize(trend_wins, 0);
   ArrayInitialize(trend_sum, 0.0);

   for(int i = 0; i < count; i++)
   {
      int session = pairs[i].utc_session;
      if(session < 0 || session > 3)
         session = 3;

      session_count[session]++;
      session_sum[session] += pairs[i].delta_log;
      if(pairs[i].delta_log > 0.0)
         session_wins[session]++;

      int regime = DAL_M0001ClassifyTercile(pairs[i].pre_entry_vol, v33, v66);
      regime_count[regime]++;
      regime_sum[regime] += pairs[i].delta_log;
      if(pairs[i].delta_log > 0.0)
         regime_wins[regime]++;

      int trend = pairs[i].trend_regime + 1;
      if(trend < 0)
         trend = 0;
      if(trend > 2)
         trend = 2;
      trend_count[trend]++;
      trend_sum[trend] += pairs[i].delta_log;
      if(pairs[i].delta_log > 0.0)
         trend_wins[trend]++;
   }

   double asia_mean = session_count[0] > 0 ? session_sum[0] / session_count[0] : 0.0;
   double london_mean = session_count[1] > 0 ? session_sum[1] / session_count[1] : 0.0;
   double ny_mean = session_count[2] > 0 ? session_sum[2] / session_count[2] : 0.0;
   double other_mean = session_count[3] > 0 ? session_sum[3] / session_count[3] : 0.0;

   double asia_win = session_count[0] > 0 ? 100.0 * session_wins[0] / session_count[0] : 0.0;
   double london_win = session_count[1] > 0 ? 100.0 * session_wins[1] / session_count[1] : 0.0;
   double ny_win = session_count[2] > 0 ? 100.0 * session_wins[2] / session_count[2] : 0.0;
   double other_win = session_count[3] > 0 ? 100.0 * session_wins[3] / session_count[3] : 0.0;

   double low_mean = regime_count[0] > 0 ? regime_sum[0] / regime_count[0] : 0.0;
   double mid_mean = regime_count[1] > 0 ? regime_sum[1] / regime_count[1] : 0.0;
   double high_mean = regime_count[2] > 0 ? regime_sum[2] / regime_count[2] : 0.0;

   double low_win = regime_count[0] > 0 ? 100.0 * regime_wins[0] / regime_count[0] : 0.0;
   double mid_win = regime_count[1] > 0 ? 100.0 * regime_wins[1] / regime_count[1] : 0.0;
   double high_win = regime_count[2] > 0 ? 100.0 * regime_wins[2] / regime_count[2] : 0.0;

   double down_mean = trend_count[0] > 0 ? trend_sum[0] / trend_count[0] : 0.0;
   double flat_mean = trend_count[1] > 0 ? trend_sum[1] / trend_count[1] : 0.0;
   double up_mean = trend_count[2] > 0 ? trend_sum[2] / trend_count[2] : 0.0;

   double down_win = trend_count[0] > 0 ? 100.0 * trend_wins[0] / trend_count[0] : 0.0;
   double flat_win = trend_count[1] > 0 ? 100.0 * trend_wins[1] / trend_count[1] : 0.0;
   double up_win = trend_count[2] > 0 ? 100.0 * trend_wins[2] / trend_count[2] : 0.0;

   return "SESSION_REGIME"
      + "*sessionClock=UTC"
      + "*brokerUtcOffset=" + IntegerToString(broker_utc_offset_hours)
      + "*asiaN=" + IntegerToString(session_count[0])
      + "*asiaDLog=" + DAL_M0001Fmt4(asia_mean)
      + "*asiaWin=" + DAL_M0001FmtPct(asia_win)
      + "*londonN=" + IntegerToString(session_count[1])
      + "*londonDLog=" + DAL_M0001Fmt4(london_mean)
      + "*londonWin=" + DAL_M0001FmtPct(london_win)
      + "*nyN=" + IntegerToString(session_count[2])
      + "*nyDLog=" + DAL_M0001Fmt4(ny_mean)
      + "*nyWin=" + DAL_M0001FmtPct(ny_win)
      + "*otherN=" + IntegerToString(session_count[3])
      + "*otherDLog=" + DAL_M0001Fmt4(other_mean)
      + "*otherWin=" + DAL_M0001FmtPct(other_win)
      + "*regimeBy=preEntryVolTercile"
      + "*lowRegN=" + IntegerToString(regime_count[0])
      + "*lowRegDLog=" + DAL_M0001Fmt4(low_mean)
      + "*lowRegWin=" + DAL_M0001FmtPct(low_win)
      + "*midRegN=" + IntegerToString(regime_count[1])
      + "*midRegDLog=" + DAL_M0001Fmt4(mid_mean)
      + "*midRegWin=" + DAL_M0001FmtPct(mid_win)
      + "*highRegN=" + IntegerToString(regime_count[2])
      + "*highRegDLog=" + DAL_M0001Fmt4(high_mean)
      + "*highRegWin=" + DAL_M0001FmtPct(high_win)
      + "*trendBy=preEntryCloseReturn"
      + "*downN=" + IntegerToString(trend_count[0])
      + "*downDLog=" + DAL_M0001Fmt4(down_mean)
      + "*downWin=" + DAL_M0001FmtPct(down_win)
      + "*flatN=" + IntegerToString(trend_count[1])
      + "*flatDLog=" + DAL_M0001Fmt4(flat_mean)
      + "*flatWin=" + DAL_M0001FmtPct(flat_win)
      + "*upN=" + IntegerToString(trend_count[2])
      + "*upDLog=" + DAL_M0001Fmt4(up_mean)
      + "*upWin=" + DAL_M0001FmtPct(up_win);
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


// -----------------------------------------------------------------------------
// M0001 final stress-validation suite
// -----------------------------------------------------------------------------

double DAL_M0001MeanOfArray(const double &values[])
{
   int count = ArraySize(values);
   if(count <= 0)
      return 0.0;
   double sum = 0.0;
   for(int i = 0; i < count; i++)
      sum += values[i];
   return sum / count;
}

double DAL_M0001WinPctOfArray(const double &values[])
{
   int count = ArraySize(values);
   if(count <= 0)
      return 0.0;
   int wins = 0;
   for(int i = 0; i < count; i++)
      if(values[i] > 0.0)
         wins++;
   return 100.0 * wins / count;
}

double DAL_M0001TStatOfArray(const double &values[])
{
   int count = ArraySize(values);
   if(count <= 1)
      return 0.0;
   double mean = DAL_M0001MeanOfArray(values);
   double var = 0.0;
   for(int i = 0; i < count; i++)
   {
      double d = values[i] - mean;
      var += d * d;
   }
   var /= (count - 1);
   double sd = MathSqrt(var);
   if(sd <= 0.0)
      return 0.0;
   return mean / (sd / MathSqrt(count));
}

string DAL_M0001CompactDeltaSummary(
   const string label,
   const double &deltas[]
)
{
   int count = ArraySize(deltas);
   if(count <= 0)
      return label + "*n=0";

   double sorted[];
   ArrayResize(sorted, count);
   for(int i = 0; i < count; i++)
      sorted[i] = deltas[i];
   ArraySort(sorted);

   double mean = DAL_M0001MeanOfArray(deltas);
   double median = DAL_M0001NullPercentileSorted(sorted, 0.50);
   double win = DAL_M0001WinPctOfArray(deltas);
   double t = DAL_M0001TStatOfArray(deltas);
   double p = DAL_M0001TwoSidedNormalP(t);

   return label
      + "*n=" + IntegerToString(count)
      + "*mean=" + DAL_M0001Fmt4(mean)
      + "*med=" + DAL_M0001Fmt4(median)
      + "*win=" + DAL_M0001FmtPct(win)
      + "*t=" + DAL_M0001Fmt4(t)
      + "*pApprox=" + DAL_M0001Fmt4(p);
}

void DAL_M0001PreVolTercileThresholds(
   const DALM0001PairedLogRtv &pairs[],
   double &low_threshold,
   double &high_threshold
)
{
   low_threshold = 0.0;
   high_threshold = 0.0;
   int count = ArraySize(pairs);
   if(count <= 0)
      return;

   double vols[];
   ArrayResize(vols, count);
   for(int i = 0; i < count; i++)
      vols[i] = pairs[i].pre_entry_vol;
   ArraySort(vols);
   low_threshold = DAL_M0001NullPercentileSorted(vols, 0.3333);
   high_threshold = DAL_M0001NullPercentileSorted(vols, 0.6667);
}

bool DAL_M0001HardMatchedRandomLogForPair(
   const DALM0001PairedLogRtv &pair,
   const DALBar &bars[],
   const int bars_count,
   const int analysis_start_index,
   const DALM0001RtvReportConfig &config,
   const double pre_vol_low,
   const double pre_vol_high,
   double &random_log,
   int &accepted,
   int &attempts
)
{
   random_log = 0.0;
   accepted = 0;
   attempts = 0;

   int n = pair.sample_length;
   if(n <= 0)
      return false;

   int min_entry = DAL_M0001IntMax(n, analysis_start_index);
   int max_entry = bars_count - n;
   if(max_entry < min_entry)
      return false;

   int candidates = config.hard_random_candidates;
   if(candidates < 1)
      candidates = 1;

   int span = max_entry - min_entry + 1;
   double total = 0.0;

   for(int pass = 0; pass < 3; pass++)
   {
      for(int k = 0; k < candidates; k++)
      {
         attempts++;
         double frac = DAL_M0001RandomFractionK(pair.event_id + 9001 + pass * 131, n + 17, bars_count, k + pass * 1000);
         int random_entry = min_entry + (int)MathFloor(frac * span);
         if(random_entry < min_entry)
            random_entry = min_entry;
         if(random_entry > max_entry)
            random_entry = max_entry;

         int utc_hour = DAL_M0001UtcHourFromBrokerTime(bars[random_entry].time, config.broker_utc_offset_hours);
         int session = DAL_M0001UtcSessionFromHour(utc_hour);
         if(session != pair.utc_session)
            continue;

         double pre_vol = DAL_M0001PreEntryVol(bars, bars_count, random_entry, config.regime_lookback_bars);
         int regime = DAL_M0001ClassifyTercile(pre_vol, pre_vol_low, pre_vol_high);
         int pair_regime = DAL_M0001ClassifyTercile(pair.pre_entry_vol, pre_vol_low, pre_vol_high);
         if(regime != pair_regime)
            continue;

         if(pass == 0)
         {
            int trend = DAL_M0001PreEntryTrendRegime(bars, bars_count, random_entry, config.regime_lookback_bars);
            if(trend != pair.trend_regime)
               continue;
         }

         double log_rtv = 0.0;
         if(!DAL_M0001LogRtvAtEntryIndex(bars, bars_count, random_entry, n, log_rtv))
            continue;

         total += log_rtv;
         accepted++;
      }

      if(accepted > 0)
         break;
   }

   if(accepted <= 0)
      return false;

   random_log = total / accepted;
   return true;
}

string DAL_M0001HardMatchedNullText(
   const DALM0001PairedLogRtv &pairs[],
   const DALBar &bars[],
   const int bars_count,
   const int analysis_start_index,
   const DALM0001RtvReportConfig &config
)
{
   int count = ArraySize(pairs);
   if(count <= 0)
      return "HARD_NULL*n=0";

   double low_thr = 0.0;
   double high_thr = 0.0;
   DAL_M0001PreVolTercileThresholds(pairs, low_thr, high_thr);

   double hard_deltas[];
   ArrayResize(hard_deltas, 0);
   int total_attempts = 0;
   int total_accepts = 0;

   for(int i = 0; i < count; i++)
   {
      double hard_log = 0.0;
      int accepted = 0;
      int attempts = 0;
      if(!DAL_M0001HardMatchedRandomLogForPair(pairs[i], bars, bars_count, analysis_start_index, config, low_thr, high_thr, hard_log, accepted, attempts))
      {
         total_attempts += attempts;
         continue;
      }

      total_attempts += attempts;
      total_accepts += accepted;

      int size = ArraySize(hard_deltas);
      ArrayResize(hard_deltas, size + 1);
      hard_deltas[size] = pairs[i].node_log - hard_log;
   }

   double accept_rate = total_attempts > 0 ? 100.0 * total_accepts / total_attempts : 0.0;
   return DAL_M0001CompactDeltaSummary("HARD_NULL", hard_deltas)
      + "*constraints=sameUtcSession_preVolTercile_trendFirstPass"
      + "*preVolT1=" + DAL_M0001Fmt4(low_thr)
      + "*preVolT2=" + DAL_M0001Fmt4(high_thr)
      + "*candidates=" + IntegerToString(config.hard_random_candidates)
      + "*accepted=" + IntegerToString(total_accepts)
      + "*attempts=" + IntegerToString(total_attempts)
      + "*acceptRate=" + DAL_M0001FmtPct(accept_rate);
}

string DAL_M0001PlaceboText(
   const DALM0001PairedLogRtv &pairs[],
   const DALBar &bars[],
   const int bars_count,
   const int shift_bars
)
{
   int count = ArraySize(pairs);
   if(count <= 0)
      return "PLACEBO*n=0";

   int shift = shift_bars;
   if(shift < 1)
      shift = 1;

   double plus_deltas[];
   double minus_deltas[];
   ArrayResize(plus_deltas, 0);
   ArrayResize(minus_deltas, 0);

   for(int i = 0; i < count; i++)
   {
      double log_plus = 0.0;
      if(DAL_M0001LogRtvAtEntryIndex(bars, bars_count, pairs[i].entry_index + shift, pairs[i].sample_length, log_plus))
      {
         int size = ArraySize(plus_deltas);
         ArrayResize(plus_deltas, size + 1);
         plus_deltas[size] = log_plus - pairs[i].random_log;
      }

      double log_minus = 0.0;
      if(DAL_M0001LogRtvAtEntryIndex(bars, bars_count, pairs[i].entry_index - shift, pairs[i].sample_length, log_minus))
      {
         int size = ArraySize(minus_deltas);
         ArrayResize(minus_deltas, size + 1);
         minus_deltas[size] = log_minus - pairs[i].random_log;
      }
   }

   return "PLACEBO"
      + "*shiftBars=" + IntegerToString(shift)
      + "*" + DAL_M0001CompactDeltaSummary("plus", plus_deltas)
      + "*" + DAL_M0001CompactDeltaSummary("minus", minus_deltas);
}

string DAL_M0001OutlierStressText(const DALM0001PairedLogRtv &pairs[])
{
   int count = ArraySize(pairs);
   if(count <= 0)
      return "OUTLIER_STRESS*n=0";

   double deltas[];
   ArrayResize(deltas, count);
   for(int i = 0; i < count; i++)
      deltas[i] = pairs[i].delta_log;
   ArraySort(deltas);

   double full_mean = DAL_M0001MeanOfArray(deltas);
   int cut1 = (int)MathFloor(count * 0.01);
   int cut5 = (int)MathFloor(count * 0.05);

   double trim1_sum = 0.0;
   int trim1_n = 0;
   double trim5_sum = 0.0;
   int trim5_n = 0;
   for(int i = 0; i < count; i++)
   {
      if(i < count - cut1)
      {
         trim1_sum += deltas[i];
         trim1_n++;
      }
      if(i < count - cut5)
      {
         trim5_sum += deltas[i];
         trim5_n++;
      }
   }

   double trim1 = trim1_n > 0 ? trim1_sum / trim1_n : 0.0;
   double trim5 = trim5_n > 0 ? trim5_sum / trim5_n : 0.0;

   double p01 = DAL_M0001NullPercentileSorted(deltas, 0.01);
   double p99 = DAL_M0001NullPercentileSorted(deltas, 0.99);
   double p05 = DAL_M0001NullPercentileSorted(deltas, 0.05);
   double p95 = DAL_M0001NullPercentileSorted(deltas, 0.95);

   double winsor1_sum = 0.0;
   double winsor5_sum = 0.0;
   for(int i = 0; i < count; i++)
   {
      double w1 = deltas[i];
      if(w1 < p01) w1 = p01;
      if(w1 > p99) w1 = p99;
      winsor1_sum += w1;

      double w5 = deltas[i];
      if(w5 < p05) w5 = p05;
      if(w5 > p95) w5 = p95;
      winsor5_sum += w5;
   }

   int groups = 10;
   if(groups > count)
      groups = count;
   double group_means[];
   ArrayResize(group_means, groups);
   for(int g = 0; g < groups; g++)
   {
      int start = (int)MathFloor(g * count / (double)groups);
      int end = (int)MathFloor((g + 1) * count / (double)groups) - 1;
      double sum = 0.0;
      int n = 0;
      for(int i = start; i <= end; i++)
      {
         sum += deltas[i];
         n++;
      }
      group_means[g] = n > 0 ? sum / n : 0.0;
   }
   ArraySort(group_means);
   double mom10 = DAL_M0001NullPercentileSorted(group_means, 0.50);

   return "OUTLIER_STRESS"
      + "*n=" + IntegerToString(count)
      + "*fullMean=" + DAL_M0001Fmt4(full_mean)
      + "*removeTop1Mean=" + DAL_M0001Fmt4(trim1)
      + "*removeTop5Mean=" + DAL_M0001Fmt4(trim5)
      + "*winsor1Mean=" + DAL_M0001Fmt4(winsor1_sum / count)
      + "*winsor5Mean=" + DAL_M0001Fmt4(winsor5_sum / count)
      + "*medianOfMeans10=" + DAL_M0001Fmt4(mom10);
}

string DAL_M0001NonOverlapText(
   const DALM0001PairedLogRtv &pairs[],
   const int gap_bars
)
{
   int count = ArraySize(pairs);
   if(count <= 0)
      return "NONOVERLAP*n=0";

   int idxs[];
   ArrayResize(idxs, count);
   for(int i = 0; i < count; i++)
      idxs[i] = i;

   for(int i = 1; i < count; i++)
   {
      int key = idxs[i];
      int j = i - 1;
      while(j >= 0 && pairs[idxs[j]].entry_index > pairs[key].entry_index)
      {
         idxs[j + 1] = idxs[j];
         j--;
      }
      idxs[j + 1] = key;
   }

   int gap = gap_bars;
   if(gap < 0)
      gap = 0;

   double deltas[];
   ArrayResize(deltas, 0);
   int last_end = -2147483647;
   for(int n = 0; n < count; n++)
   {
      int i = idxs[n];
      int start = pairs[i].entry_index;
      int end = start + pairs[i].sample_length - 1;
      if(start <= last_end + gap)
         continue;

      int size = ArraySize(deltas);
      ArrayResize(deltas, size + 1);
      deltas[size] = pairs[i].delta_log;
      last_end = end;
   }

   return DAL_M0001CompactDeltaSummary("NONOVERLAP", deltas)
      + "*gapBars=" + IntegerToString(gap)
      + "*keptPct=" + DAL_M0001FmtPct(100.0 * ArraySize(deltas) / count);
}

void DAL_M0001ClusterTStats(
   const DALM0001PairedLogRtv &pairs[],
   const int divisor_seconds,
   int &cluster_count,
   double &cluster_mean,
   double &cluster_t,
   double &cluster_p
)
{
   cluster_count = 0;
   cluster_mean = 0.0;
   cluster_t = 0.0;
   cluster_p = 1.0;
   int count = ArraySize(pairs);
   if(count <= 0 || divisor_seconds <= 0)
      return;

   int keys[];
   double sums[];
   int counts[];
   ArrayResize(keys, 0);
   ArrayResize(sums, 0);
   ArrayResize(counts, 0);

   for(int i = 0; i < count; i++)
   {
      int key = (int)(((long)pairs[i].entry_time) / divisor_seconds);
      int pos = -1;
      for(int j = 0; j < ArraySize(keys); j++)
      {
         if(keys[j] == key)
         {
            pos = j;
            break;
         }
      }
      if(pos < 0)
      {
         pos = ArraySize(keys);
         ArrayResize(keys, pos + 1);
         ArrayResize(sums, pos + 1);
         ArrayResize(counts, pos + 1);
         keys[pos] = key;
         sums[pos] = 0.0;
         counts[pos] = 0;
      }
      sums[pos] += pairs[i].delta_log;
      counts[pos]++;
   }

   cluster_count = ArraySize(keys);
   if(cluster_count <= 0)
      return;

   double means[];
   ArrayResize(means, cluster_count);
   for(int i = 0; i < cluster_count; i++)
      means[i] = counts[i] > 0 ? sums[i] / counts[i] : 0.0;

   cluster_mean = DAL_M0001MeanOfArray(means);
   cluster_t = DAL_M0001TStatOfArray(means);
   cluster_p = DAL_M0001TwoSidedNormalP(cluster_t);
}

string DAL_M0001ClusterRobustText(const DALM0001PairedLogRtv &pairs[])
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

   return "CLUSTER_ROBUST"
      + "*dayClusters=" + IntegerToString(day_n)
      + "*dayMean=" + DAL_M0001Fmt4(day_mean)
      + "*dayT=" + DAL_M0001Fmt4(day_t)
      + "*dayPapprox=" + DAL_M0001Fmt4(day_p)
      + "*weekClusters=" + IntegerToString(week_n)
      + "*weekMean=" + DAL_M0001Fmt4(week_mean)
      + "*weekT=" + DAL_M0001Fmt4(week_t)
      + "*weekPapprox=" + DAL_M0001Fmt4(week_p);
}

string DAL_M0001BlockBootstrapText(
   const DALM0001PairedLogRtv &pairs[],
   const int iterations,
   const int block_pairs
)
{
   int count = ArraySize(pairs);
   int iters = iterations;
   if(iters < 0)
      iters = 0;
   int block = block_pairs;
   if(block < 1)
      block = 1;

   if(count <= 1 || iters <= 0)
      return "BLOCK_BOOT*n=" + IntegerToString(count) + "*iters=0";

   double boot[];
   ArrayResize(boot, iters);

   for(int it = 0; it < iters; it++)
   {
      double sum = 0.0;
      int used = 0;
      while(used < count)
      {
         double frac = DAL_M0001PseudoFraction(it, used, count + 333);
         int start = (int)MathFloor(frac * count);
         if(start < 0) start = 0;
         if(start >= count) start = count - 1;

         for(int b = 0; b < block && used < count; b++)
         {
            int idx = start + b;
            if(idx >= count)
               idx -= count;
            sum += pairs[idx].delta_log;
            used++;
         }
      }
      boot[it] = sum / count;
   }

   ArraySort(boot);
   double low = DAL_M0001NullPercentileSorted(boot, 0.025);
   double high = DAL_M0001NullPercentileSorted(boot, 0.975);
   double med = DAL_M0001NullPercentileSorted(boot, 0.50);

   return "BLOCK_BOOT"
      + "*n=" + IntegerToString(count)
      + "*iters=" + IntegerToString(iters)
      + "*blockPairs=" + IntegerToString(block)
      + "*dMeanCI95=" + DAL_M0001Fmt4(low) + ".." + DAL_M0001Fmt4(high)
      + "*bootMedian=" + DAL_M0001Fmt4(med);
}

bool DAL_M0001SimpleRandomLogAtHorizon(
   const DALM0001PairedLogRtv &pair,
   const DALBar &bars[],
   const int bars_count,
   const int analysis_start_index,
   const int horizon,
   double &log_rtv
)
{
   log_rtv = 0.0;
   if(horizon <= 0)
      return false;

   int min_entry = DAL_M0001IntMax(horizon, analysis_start_index);
   int max_entry = bars_count - horizon;
   if(max_entry < min_entry)
      return false;

   int span = max_entry - min_entry + 1;
   double frac = DAL_M0001RandomFractionK(pair.event_id + 707, horizon, bars_count, horizon);
   int random_entry = min_entry + (int)MathFloor(frac * span);
   if(random_entry < min_entry)
      random_entry = min_entry;
   if(random_entry > max_entry)
      random_entry = max_entry;

   return DAL_M0001LogRtvAtEntryIndex(bars, bars_count, random_entry, horizon, log_rtv);
}

void DAL_M0001HorizonOne(
   const DALM0001PairedLogRtv &pairs[],
   const DALBar &bars[],
   const int bars_count,
   const int analysis_start_index,
   const int horizon,
   double &mean,
   double &win,
   int &n
)
{
   mean = 0.0;
   win = 0.0;
   n = 0;
   if(horizon <= 0)
      return;

   double deltas[];
   ArrayResize(deltas, 0);
   for(int i = 0; i < ArraySize(pairs); i++)
   {
      double node_h = 0.0;
      if(!DAL_M0001LogRtvAtEntryIndex(bars, bars_count, pairs[i].entry_index, horizon, node_h))
         continue;

      double random_h = 0.0;
      if(!DAL_M0001SimpleRandomLogAtHorizon(pairs[i], bars, bars_count, analysis_start_index, horizon, random_h))
         continue;

      int size = ArraySize(deltas);
      ArrayResize(deltas, size + 1);
      deltas[size] = node_h - random_h;
   }

   n = ArraySize(deltas);
   mean = DAL_M0001MeanOfArray(deltas);
   win = DAL_M0001WinPctOfArray(deltas);
}

string DAL_M0001HorizonStressText(
   const DALM0001PairedLogRtv &pairs[],
   const DALBar &bars[],
   const int bars_count,
   const int analysis_start_index,
   const DALM0001RtvReportConfig &config
)
{
   int hs[4];
   hs[0] = config.horizon_bars_1;
   hs[1] = config.horizon_bars_2;
   hs[2] = config.horizon_bars_3;
   hs[3] = config.horizon_bars_4;

   string out = "HORIZON";
   double best_mean = -DBL_MAX;
   int best_h = 0;
   double first_positive_mean = 0.0;
   int first_positive_h = 0;

   for(int i = 0; i < 4; i++)
   {
      int h = hs[i];
      double mean = 0.0;
      double win = 0.0;
      int n = 0;
      DAL_M0001HorizonOne(pairs, bars, bars_count, analysis_start_index, h, mean, win, n);
      out += "*h" + IntegerToString(h) + "N=" + IntegerToString(n);
      out += "*h" + IntegerToString(h) + "DLog=" + DAL_M0001Fmt4(mean);
      out += "*h" + IntegerToString(h) + "Win=" + DAL_M0001FmtPct(win);

      if(n > 0 && (best_h == 0 || mean > best_mean))
      {
         best_mean = mean;
         best_h = h;
      }
      if(n > 0 && first_positive_h == 0 && mean > 0.0)
      {
         first_positive_h = h;
         first_positive_mean = mean;
      }
   }

   double half = best_mean * 0.5;
   int half_life_h = 0;
   if(best_h > 0)
   {
      for(int i = 0; i < 4; i++)
      {
         int h = hs[i];
         double mean = 0.0;
         double win = 0.0;
         int n = 0;
         DAL_M0001HorizonOne(pairs, bars, bars_count, analysis_start_index, h, mean, win, n);
         if(n > 0 && h >= best_h && mean <= half)
         {
            half_life_h = h;
            break;
         }
      }
   }

   out += "*peakH=" + IntegerToString(best_h);
   out += "*peakDLog=" + DAL_M0001Fmt4(best_mean == -DBL_MAX ? 0.0 : best_mean);
   out += "*halfLifeH=" + IntegerToString(half_life_h);
   out += "*firstPositiveH=" + IntegerToString(first_positive_h);
   out += "*firstPositiveDLog=" + DAL_M0001Fmt4(first_positive_mean);
   return out;
}

string DAL_M0001NegativeControlText(
   const DALM0001PairedLogRtv &pairs[],
   const DALBar &bars[],
   const int bars_count,
   const int analysis_start_index
)
{
   int count = ArraySize(pairs);
   if(count <= 0)
      return "NEG_CONTROL*n=0";

   double deltas[];
   ArrayResize(deltas, 0);

   for(int i = 0; i < count; i++)
   {
      int n = pairs[i].sample_length;
      int min_entry = DAL_M0001IntMax(n, analysis_start_index);
      int max_entry = bars_count - n;
      if(max_entry < min_entry)
         continue;

      int span = max_entry - min_entry + 1;
      double f1 = DAL_M0001RandomFractionK(pairs[i].event_id + 1111, n, bars_count, 1);
      double f2 = DAL_M0001RandomFractionK(pairs[i].event_id + 2222, n, bars_count, 2);
      int e1 = min_entry + (int)MathFloor(f1 * span);
      int e2 = min_entry + (int)MathFloor(f2 * span);
      if(e1 < min_entry) e1 = min_entry;
      if(e1 > max_entry) e1 = max_entry;
      if(e2 < min_entry) e2 = min_entry;
      if(e2 > max_entry) e2 = max_entry;

      double l1 = 0.0;
      double l2 = 0.0;
      if(!DAL_M0001LogRtvAtEntryIndex(bars, bars_count, e1, n, l1))
         continue;
      if(!DAL_M0001LogRtvAtEntryIndex(bars, bars_count, e2, n, l2))
         continue;

      int size = ArraySize(deltas);
      ArrayResize(deltas, size + 1);
      deltas[size] = l1 - l2;
   }

   return DAL_M0001CompactDeltaSummary("NEG_CONTROL_RANDOM_VS_RANDOM", deltas)
      + "*expectedMeanNearZero=1";
}

void DAL_M0001PrintStressSuiteReports(
   const DALM0001PairedLogRtv &pairs[],
   const DALBar &bars[],
   const int bars_count,
   const string symbol,
   const string timeframe,
   const string source_mode,
   const int events_count,
   const datetime min_entry_time,
   const DALM0001RtvReportConfig &report_config
)
{
   if(!report_config.run_stress_suite)
      return;

   int analysis_start_index = DAL_M0001FirstIndexAtOrAfter(bars, bars_count, min_entry_time);

   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_STRESS_NULLS", symbol, timeframe, source_mode, events_count, min_entry_time),
      DAL_M0001HardMatchedNullText(pairs, bars, bars_count, analysis_start_index, report_config));

   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_PLACEBO", symbol, timeframe, source_mode, events_count, min_entry_time),
      DAL_M0001PlaceboText(pairs, bars, bars_count, report_config.placebo_shift_bars));

   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_OUTLIER_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time),
      DAL_M0001OutlierStressText(pairs));

   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_NONOVERLAP", symbol, timeframe, source_mode, events_count, min_entry_time),
      DAL_M0001NonOverlapText(pairs, report_config.nonoverlap_gap_bars));

   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_CLUSTER_ROBUST", symbol, timeframe, source_mode, events_count, min_entry_time),
      DAL_M0001ClusterRobustText(pairs));

   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_BLOCK_BOOT", symbol, timeframe, source_mode, events_count, min_entry_time),
      DAL_M0001BlockBootstrapText(pairs, report_config.block_bootstrap_iterations, report_config.block_bootstrap_block_pairs));

   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_HORIZON", symbol, timeframe, source_mode, events_count, min_entry_time),
      DAL_M0001HorizonStressText(pairs, bars, bars_count, analysis_start_index, report_config));

   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_NEGATIVE_CONTROL", symbol, timeframe, source_mode, events_count, min_entry_time),
      DAL_M0001NegativeControlText(pairs, bars, bars_count, analysis_start_index));
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

   DAL_M0001CollectPairedLogRtvs(events, events_count, bars, bars_count, min_entry_time, random_k, report_config.broker_utc_offset_hours, report_config.regime_lookback_bars, pairs, node_logs, random_logs, audit);

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
   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_SESSION_REGIME", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0001SessionRegimeText(pairs, report_config.broker_utc_offset_hours));
   Print(DAL_M0001FinalLinePrefix("DAL_M0001_FINAL_AUDIT", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0001IntegrityAuditText(audit, random_k, report_config.print_histogram, min_entry_time));

   DAL_M0001PrintStressSuiteReports(pairs, bars, bars_count, symbol, timeframe, source_mode, events_count, min_entry_time, report_config);

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
   DAL_M0001CollectPairedLogRtvs(events, events_count, bars, bars_count, min_entry_time, report_config.random_samples_per_event, report_config.broker_utc_offset_hours, report_config.regime_lookback_bars, pairs, node_logs, random_logs, audit);

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
