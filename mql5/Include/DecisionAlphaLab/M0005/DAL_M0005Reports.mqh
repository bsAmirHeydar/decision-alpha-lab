#ifndef __DAL_M0005_REPORTS_MQH__
#define __DAL_M0005_REPORTS_MQH__

#include <DecisionAlphaLab/M0004/DAL_M0004Reports.mqh>

enum ENUM_DALM0005RegimeSource
{
   DAL_M0005_REGIME_LAST_ONLY = 0,
   DAL_M0005_REGIME_EWMA_CONTEXT = 1,
   DAL_M0005_REGIME_EWMA_CONSENSUS = 2,
   DAL_M0005_REGIME_LAST_WITH_CONTEXT_CONFIDENCE = 3
};

enum ENUM_DALM0005PathType
{
   DAL_M0005_PATH_REVERSAL = 0,
   DAL_M0005_PATH_CONTINUATION = 1
};

enum ENUM_DALM0005ExitReason
{
   DAL_M0005_EXIT_TARGET = 0,
   DAL_M0005_EXIT_INVALIDATION = 1,
   DAL_M0005_EXIT_REGIME_CHANGE = 2,
   DAL_M0005_EXIT_MAX_BARS = 3,
   DAL_M0005_EXIT_END_OF_DATA = 4,
   DAL_M0005_EXIT_NO_ENTRY = 5,
   DAL_M0005_EXIT_NO_DESTINATION = 6,
   DAL_M0005_EXIT_UNKNOWN = 7
};

struct DALM0005Config
{
   ENUM_DALM0005RegimeSource regime_source;
   int context_lookback;
   double context_ewma_alpha;
   double context_strong_threshold;
   bool break_uses_close;
   int max_path_bars;
   int max_path_events;
   double continuation_success_zone_multiple;
   double follow_zone_mult_1;
   double follow_zone_mult_2;
   double follow_zone_mult_3;
   double follow_zone_mult_4;
   int random_samples_per_path;
   int stress_iterations;
   int block_size;
};

struct DALM0005Path
{
   bool valid;
   ENUM_DALM0005PathType path_type;
   ENUM_DALM0005ExitReason exit_reason;
   int source_index;
   int regime_label;
   int direction;
   int entry_index;
   int exit_index;
   int target_index;
   int events_to_exit;
   int bars_to_exit;
   datetime entry_time;
   datetime exit_time;
   double entry_price;
   double exit_price;
   double zone_width;
   double mfe;
   double mae;
   double mfe_zone;
   double mae_zone;
   double net_move;
   double net_zone;
   bool target_success;
   bool follow_success;
   bool follow_05;
   bool follow_10;
   bool follow_15;
   bool follow_20;
   bool positive_net;
   double flipped_mfe_zone;
   double flipped_mae_zone;
   bool flipped_follow_10;
   double random_mfe_zone;
   double random_mae_zone;
   bool random_follow_10;
   double context_p;
   double context_confidence;
   int context_dominant;
   int last_label;
   int session;
   int prevol_bucket;
   int revisit_bucket;
   int spacing_bucket;
   double delta_log;
};

struct DALM0005PathStats
{
   string name;
   int n;
   int valid;
   int reversal_n;
   int continuation_n;
   int target_success_n;
   int follow_success_n;
   int follow05_n;
   int follow10_n;
   int follow15_n;
   int follow20_n;
   int positive_net_n;
   int invalidation_n;
   int regime_change_n;
   int no_entry_n;
   int no_destination_n;
   int max_exit_n;
   int end_data_n;
   int bars_sum;
   int events_sum;
   double mfe_sum;
   double mae_sum;
   double mfe_zone_sum;
   double mae_zone_sum;
   double net_zone_sum;
   double flipped_mfe_zone_sum;
   double flipped_mae_zone_sum;
   int flipped_follow10_n;
   double random_mfe_zone_sum;
   double random_mae_zone_sum;
   int random_follow10_n;
   double delta_log_sum;
   double mfe_zone_vals[];
   double mae_zone_vals[];
   double net_zone_vals[];
};

string DAL_M0005RegimeSourceToString(const ENUM_DALM0005RegimeSource src)
{
   if(src == DAL_M0005_REGIME_EWMA_CONTEXT) return "EWMA_CONTEXT";
   if(src == DAL_M0005_REGIME_EWMA_CONSENSUS) return "EWMA_CONSENSUS";
   if(src == DAL_M0005_REGIME_LAST_WITH_CONTEXT_CONFIDENCE) return "LAST_WITH_CONTEXT_CONFIDENCE";
   return "LAST_ONLY";
}

string DAL_M0005PathTypeToString(const ENUM_DALM0005PathType type)
{
   if(type == DAL_M0005_PATH_CONTINUATION) return "CONTINUATION_PATH";
   return "REVERSAL_PATH";
}

string DAL_M0005ExitReasonToString(const ENUM_DALM0005ExitReason reason)
{
   if(reason == DAL_M0005_EXIT_TARGET) return "TARGET";
   if(reason == DAL_M0005_EXIT_INVALIDATION) return "INVALIDATION";
   if(reason == DAL_M0005_EXIT_REGIME_CHANGE) return "REGIME_CHANGE";
   if(reason == DAL_M0005_EXIT_MAX_BARS) return "MAX_BARS";
   if(reason == DAL_M0005_EXIT_END_OF_DATA) return "END_OF_DATA";
   if(reason == DAL_M0005_EXIT_NO_ENTRY) return "NO_ENTRY";
   if(reason == DAL_M0005_EXIT_NO_DESTINATION) return "NO_DESTINATION";
   return "UNKNOWN";
}

string DAL_M0005Prefix(
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

double DAL_M0005SafeDiv(const double a, const double b)
{
   if(MathAbs(b) <= 0.000000000001)
      return 0.0;
   return a / b;
}

int DAL_M0005BucketRevisit(const int revisit_id)
{
   if(revisit_id <= 0) return 0;
   if(revisit_id == 1) return 1;
   if(revisit_id == 2) return 2;
   return 3;
}

double DAL_M0005ZoneWidth(const DALM0002BranchSample &sample)
{
   double w = MathAbs(sample.territory_upper - sample.territory_lower);
   if(w <= 0.0)
      w = MathAbs(sample.node_price) * 0.0001;
   if(w <= 0.0)
      w = 0.0001;
   return w;
}

int DAL_M0005DirectionForRegime(const DALM0002BranchSample &sample, const int regime_label)
{
   bool low = (sample.node_type == DAL_NODE_LOW);
   if(regime_label == DAL_M0004_LABEL_REVERSAL)
      return low ? 1 : -1;
   return low ? -1 : 1;
}

bool DAL_M0005IsContinuationBreak(
   const DALBar &bar,
   const DALM0002BranchSample &sample,
   const int direction,
   const bool break_uses_close
)
{
   if(direction > 0)
   {
      if(break_uses_close)
         return bar.close > sample.territory_upper;
      return bar.high > sample.territory_upper;
   }
   if(break_uses_close)
      return bar.close < sample.territory_lower;
   return bar.low < sample.territory_lower;
}

bool DAL_M0005IsReversalInvalidation(
   const DALBar &bar,
   const DALM0002BranchSample &sample,
   const int direction,
   const bool break_uses_close
)
{
   if(direction > 0)
   {
      if(break_uses_close)
         return bar.close < sample.territory_lower;
      return bar.low < sample.territory_lower;
   }
   if(break_uses_close)
      return bar.close > sample.territory_upper;
   return bar.high > sample.territory_upper;
}

int DAL_M0005FindNextOppositeNodeEntry(
   const DALM0002BranchSample &samples[],
   const int count,
   const int index
)
{
   if(index < 0 || index >= count)
      return -1;
   ENUM_DALNodeType node_type = samples[index].node_type;
   int entry = samples[index].entry_index;
   for(int j = index + 1; j < count; j++)
   {
      if(samples[j].entry_index <= entry)
         continue;
      if(samples[j].node_type != node_type)
         return j;
   }
   return -1;
}

int DAL_M0005RegimeAt(
   const int &labels[],
   const int count,
   const int index,
   const DALM0005Config &config,
   double &context_p,
   double &context_confidence,
   int &context_dominant
)
{
   context_p = 0.0;
   context_confidence = 0.0;
   context_dominant = -1;
   if(index <= 0 || index >= count)
      return -1;

   int last_label = labels[index - 1];
   if(config.regime_source == DAL_M0005_REGIME_LAST_ONLY)
      return last_label;

   context_dominant = DAL_M0004ContextDominantAt(
      labels,
      count,
      index,
      config.context_lookback,
      config.context_ewma_alpha,
      config.context_strong_threshold,
      true,
      context_p,
      context_confidence
   );

   if(config.regime_source == DAL_M0005_REGIME_EWMA_CONTEXT)
      return context_dominant;

   if(config.regime_source == DAL_M0005_REGIME_EWMA_CONSENSUS)
   {
      if(context_dominant >= 0 && context_dominant == last_label)
         return last_label;
      return -1;
   }

   return last_label;
}

int DAL_M0005FindContinuationEntry(
   const DALM0002BranchSample &sample,
   const DALBar &bars[],
   const int bars_count,
   const int direction,
   const bool break_uses_close
)
{
   int start = sample.entry_index;
   int end = sample.exit_index;
   if(end < start) end = sample.outcome_index;
   if(end < start) end = start;
   if(end >= bars_count) end = bars_count - 1;
   if(start < 0) start = 0;

   for(int i = start; i <= end; i++)
      if(DAL_M0005IsContinuationBreak(bars[i], sample, direction, break_uses_close))
         return i;

   if(sample.outcome_index >= 0 && sample.outcome_index < bars_count)
      if(DAL_M0005IsContinuationBreak(bars[sample.outcome_index], sample, direction, break_uses_close))
         return sample.outcome_index;

   return -1;
}

int DAL_M0005FindRegimeExitSample(
   const int &labels[],
   const int count,
   const int index,
   const int current_regime,
   const DALM0005Config &config
)
{
   int max_events = config.max_path_events;
   if(max_events < 1) max_events = 1000000000;
   int end = index + max_events;
   if(end >= count) end = count - 1;

   for(int j = index + 1; j <= end; j++)
   {
      double p = 0.0;
      double conf = 0.0;
      int dom = -1;
      int r = DAL_M0005RegimeAt(labels, count, j, config, p, conf, dom);
      if(r != current_regime)
         return j;
   }
   return -1;
}

void DAL_M0005ComputeExcursions(
   const DALBar &bars[],
   const int bars_count,
   const int entry_index,
   const int exit_index,
   const int direction,
   const double entry_price,
   double &mfe,
   double &mae,
   double &net_move
)
{
   mfe = 0.0;
   mae = 0.0;
   net_move = 0.0;
   if(entry_index < 0 || entry_index >= bars_count || exit_index < entry_index)
      return;
   int end = exit_index;
   if(end >= bars_count) end = bars_count - 1;
   for(int i = entry_index; i <= end; i++)
   {
      double favorable = 0.0;
      double adverse = 0.0;
      if(direction > 0)
      {
         favorable = bars[i].high - entry_price;
         adverse = entry_price - bars[i].low;
      }
      else
      {
         favorable = entry_price - bars[i].low;
         adverse = bars[i].high - entry_price;
      }
      if(favorable > mfe) mfe = favorable;
      if(adverse > mae) mae = adverse;
   }
   if(direction > 0)
      net_move = bars[end].close - entry_price;
   else
      net_move = entry_price - bars[end].close;
}

void DAL_M0005ComputeRandomExcursion(
   const DALBar &bars[],
   const int bars_count,
   const int min_start,
   const int length,
   const int direction,
   const int seed_a,
   const int seed_b,
   double &mfe_zone,
   double &mae_zone,
   const double zone_width
)
{
   mfe_zone = 0.0;
   mae_zone = 0.0;
   if(length <= 0 || bars_count <= length + 5)
      return;
   int low = min_start;
   if(low < 1) low = 1;
   int high = bars_count - length - 1;
   if(high <= low) high = low;
   double frac = DAL_M0001RandomFractionK(seed_a + 211, seed_b + 503, length + 809, direction > 0 ? 1 : 2);
   int start = low + (int)MathFloor(frac * (high - low + 1));
   if(start < low) start = low;
   if(start > high) start = high;
   int end = start + length - 1;
   double mfe = 0.0, mae = 0.0, net = 0.0;
   DAL_M0005ComputeExcursions(bars, bars_count, start, end, direction, bars[start].close, mfe, mae, net);
   mfe_zone = DAL_M0005SafeDiv(mfe, zone_width);
   mae_zone = DAL_M0005SafeDiv(mae, zone_width);
}

void DAL_M0005FinalizePath(
   DALM0005Path &path,
   const DALM0002BranchSample &sample,
   const DALBar &bars[],
   const int bars_count,
   const int min_random_start,
   const DALM0005Config &config
)
{
   if(path.entry_index < 0 || path.entry_index >= bars_count || path.exit_index < path.entry_index)
   {
      path.valid = false;
      return;
   }
   if(path.exit_index >= bars_count)
      path.exit_index = bars_count - 1;

   path.valid = true;
   path.entry_time = bars[path.entry_index].time;
   path.exit_time = bars[path.exit_index].time;
   path.entry_price = bars[path.entry_index].close;
   path.exit_price = bars[path.exit_index].close;
   path.zone_width = DAL_M0005ZoneWidth(sample);
   path.bars_to_exit = path.exit_index - path.entry_index + 1;
   if(path.bars_to_exit < 0) path.bars_to_exit = 0;

   DAL_M0005ComputeExcursions(bars, bars_count, path.entry_index, path.exit_index, path.direction, path.entry_price, path.mfe, path.mae, path.net_move);
   path.mfe_zone = DAL_M0005SafeDiv(path.mfe, path.zone_width);
   path.mae_zone = DAL_M0005SafeDiv(path.mae, path.zone_width);
   path.net_zone = DAL_M0005SafeDiv(path.net_move, path.zone_width);
   path.follow_05 = (path.mfe_zone >= config.follow_zone_mult_1);
   path.follow_10 = (path.mfe_zone >= config.follow_zone_mult_2);
   path.follow_15 = (path.mfe_zone >= config.follow_zone_mult_3);
   path.follow_20 = (path.mfe_zone >= config.follow_zone_mult_4);
   path.follow_success = (path.mfe_zone >= config.continuation_success_zone_multiple);
   path.positive_net = (path.net_zone > 0.0);

   double fm = 0.0, fa = 0.0, fn = 0.0;
   DAL_M0005ComputeExcursions(bars, bars_count, path.entry_index, path.exit_index, -path.direction, path.entry_price, fm, fa, fn);
   path.flipped_mfe_zone = DAL_M0005SafeDiv(fm, path.zone_width);
   path.flipped_mae_zone = DAL_M0005SafeDiv(fa, path.zone_width);
   path.flipped_follow_10 = (path.flipped_mfe_zone >= config.follow_zone_mult_2);

   double random_mfe_sum = 0.0;
   double random_mae_sum = 0.0;
   int random_follow_sum = 0;
   int rk = config.random_samples_per_path;
   if(rk < 1) rk = 1;
   for(int r = 0; r < rk; r++)
   {
      double rm = 0.0, ra = 0.0;
      DAL_M0005ComputeRandomExcursion(bars, bars_count, min_random_start, path.bars_to_exit, path.direction, path.source_index + 811 + r * 17, path.entry_index + 991 + r * 31, rm, ra, path.zone_width);
      random_mfe_sum += rm;
      random_mae_sum += ra;
      if(rm >= config.follow_zone_mult_2)
         random_follow_sum++;
   }
   path.random_mfe_zone = random_mfe_sum / rk;
   path.random_mae_zone = random_mae_sum / rk;
   path.random_follow_10 = (random_follow_sum > rk / 2);
}

bool DAL_M0005BuildReversalPath(
   const DALM0002BranchSample &samples[],
   const int count,
   const int index,
   const int regime_label,
   const DALBar &bars[],
   const int bars_count,
   const int &labels[],
   const DALM0005Config &config,
   const int min_random_start,
   DALM0005Path &path
)
{
   path.valid = false;
   path.path_type = DAL_M0005_PATH_REVERSAL;
   path.exit_reason = DAL_M0005_EXIT_UNKNOWN;
   path.source_index = index;
   path.regime_label = regime_label;
   path.last_label = index > 0 ? labels[index - 1] : -1;
   path.direction = DAL_M0005DirectionForRegime(samples[index], DAL_M0004_LABEL_REVERSAL);
   path.entry_index = samples[index].entry_index;
   path.target_index = -1;
   path.events_to_exit = 0;
   path.context_p = 0.0;
   path.context_confidence = 0.0;
   path.context_dominant = -1;
   path.session = samples[index].utc_session;
   path.revisit_bucket = DAL_M0005BucketRevisit(samples[index].revisit_id);
   path.prevol_bucket = 0;
   path.spacing_bucket = 0;
   path.delta_log = samples[index].delta_log;

   if(path.entry_index < 0 || path.entry_index >= bars_count)
   {
      path.exit_reason = DAL_M0005_EXIT_NO_ENTRY;
      return false;
   }

   int target_sample = DAL_M0005FindNextOppositeNodeEntry(samples, count, index);
   if(target_sample < 0)
   {
      path.exit_reason = DAL_M0005_EXIT_NO_DESTINATION;
      path.exit_index = MathMin(bars_count - 1, path.entry_index + MathMax(1, config.max_path_bars));
      DAL_M0005FinalizePath(path, samples[index], bars, bars_count, min_random_start, config);
      path.valid = false;
      return false;
   }

   path.target_index = samples[target_sample].entry_index;
   path.events_to_exit = target_sample - index;
   int max_exit = path.target_index;
   if(config.max_path_bars > 0 && path.entry_index + config.max_path_bars < max_exit)
      max_exit = path.entry_index + config.max_path_bars;
   if(max_exit >= bars_count) max_exit = bars_count - 1;

   int invalidation = -1;
   for(int b = path.entry_index + 1; b <= max_exit; b++)
   {
      if(DAL_M0005IsReversalInvalidation(bars[b], samples[index], path.direction, config.break_uses_close))
      {
         invalidation = b;
         break;
      }
   }

   if(invalidation >= 0 && invalidation < path.target_index)
   {
      path.exit_index = invalidation;
      path.exit_reason = DAL_M0005_EXIT_INVALIDATION;
      path.target_success = false;
   }
   else if(path.target_index <= max_exit)
   {
      path.exit_index = path.target_index;
      path.exit_reason = DAL_M0005_EXIT_TARGET;
      path.target_success = true;
   }
   else
   {
      path.exit_index = max_exit;
      path.exit_reason = DAL_M0005_EXIT_MAX_BARS;
      path.target_success = false;
   }

   DAL_M0005FinalizePath(path, samples[index], bars, bars_count, min_random_start, config);
   return path.valid;
}

bool DAL_M0005BuildContinuationPath(
   const DALM0002BranchSample &samples[],
   const int count,
   const int index,
   const int regime_label,
   const DALBar &bars[],
   const int bars_count,
   const int &labels[],
   const DALM0005Config &config,
   const int min_random_start,
   DALM0005Path &path
)
{
   path.valid = false;
   path.path_type = DAL_M0005_PATH_CONTINUATION;
   path.exit_reason = DAL_M0005_EXIT_UNKNOWN;
   path.source_index = index;
   path.regime_label = regime_label;
   path.last_label = index > 0 ? labels[index - 1] : -1;
   path.direction = DAL_M0005DirectionForRegime(samples[index], DAL_M0004_LABEL_CONTINUATION);
   path.target_index = -1;
   path.events_to_exit = 0;
   path.context_p = 0.0;
   path.context_confidence = 0.0;
   path.context_dominant = -1;
   path.session = samples[index].utc_session;
   path.revisit_bucket = DAL_M0005BucketRevisit(samples[index].revisit_id);
   path.prevol_bucket = 0;
   path.spacing_bucket = 0;
   path.delta_log = samples[index].delta_log;

   path.entry_index = DAL_M0005FindContinuationEntry(samples[index], bars, bars_count, path.direction, config.break_uses_close);
   if(path.entry_index < 0 || path.entry_index >= bars_count)
   {
      path.exit_reason = DAL_M0005_EXIT_NO_ENTRY;
      return false;
   }

   int exit_sample = DAL_M0005FindRegimeExitSample(labels, count, index, DAL_M0004_LABEL_CONTINUATION, config);
   if(exit_sample > index)
   {
      path.exit_index = samples[exit_sample].entry_index;
      path.events_to_exit = exit_sample - index;
      path.exit_reason = DAL_M0005_EXIT_REGIME_CHANGE;
   }
   else
   {
      path.exit_index = bars_count - 1;
      path.events_to_exit = count - 1 - index;
      path.exit_reason = DAL_M0005_EXIT_END_OF_DATA;
   }

   if(config.max_path_bars > 0 && path.entry_index + config.max_path_bars < path.exit_index)
   {
      path.exit_index = path.entry_index + config.max_path_bars;
      path.exit_reason = DAL_M0005_EXIT_MAX_BARS;
   }
   if(path.exit_index >= bars_count) path.exit_index = bars_count - 1;
   if(path.exit_index < path.entry_index) path.exit_index = path.entry_index;

   path.target_success = false;
   DAL_M0005FinalizePath(path, samples[index], bars, bars_count, min_random_start, config);
   return path.valid;
}

void DAL_M0005AppendPath(DALM0005Path &paths[], const DALM0005Path &path)
{
   int n = ArraySize(paths);
   ArrayResize(paths, n + 1);
   paths[n] = path;
}

void DAL_M0005BuildPaths(
   const DALM0002BranchSample &samples[],
   const int count,
   const DALBar &bars[],
   const int bars_count,
   const int &labels[],
   const DALM0005Config &config,
   const int min_random_start,
   DALM0005Path &all_paths[],
   DALM0005Path &reversal_paths[],
   DALM0005Path &continuation_paths[]
)
{
   ArrayResize(all_paths, 0);
   ArrayResize(reversal_paths, 0);
   ArrayResize(continuation_paths, 0);
   for(int i = 1; i < count; i++)
   {
      double p = 0.0;
      double conf = 0.0;
      int dom = -1;
      int regime = DAL_M0005RegimeAt(labels, count, i, config, p, conf, dom);
      if(regime < 0)
         continue;

      DALM0005Path path;
      bool ok = false;
      if(regime == DAL_M0004_LABEL_REVERSAL)
         ok = DAL_M0005BuildReversalPath(samples, count, i, regime, bars, bars_count, labels, config, min_random_start, path);
      else
         ok = DAL_M0005BuildContinuationPath(samples, count, i, regime, bars, bars_count, labels, config, min_random_start, path);

      if(!ok)
         continue;

      path.context_p = p;
      path.context_confidence = conf;
      path.context_dominant = dom;
      DAL_M0005AppendPath(all_paths, path);
      if(path.path_type == DAL_M0005_PATH_REVERSAL)
         DAL_M0005AppendPath(reversal_paths, path);
      else
         DAL_M0005AppendPath(continuation_paths, path);
   }
}

void DAL_M0005ResetStats(DALM0005PathStats &st, const string name)
{
   st.name = name;
   st.n = 0;
   st.valid = 0;
   st.reversal_n = 0;
   st.continuation_n = 0;
   st.target_success_n = 0;
   st.follow_success_n = 0;
   st.follow05_n = 0;
   st.follow10_n = 0;
   st.follow15_n = 0;
   st.follow20_n = 0;
   st.positive_net_n = 0;
   st.invalidation_n = 0;
   st.regime_change_n = 0;
   st.no_entry_n = 0;
   st.no_destination_n = 0;
   st.max_exit_n = 0;
   st.end_data_n = 0;
   st.bars_sum = 0;
   st.events_sum = 0;
   st.mfe_sum = 0.0;
   st.mae_sum = 0.0;
   st.mfe_zone_sum = 0.0;
   st.mae_zone_sum = 0.0;
   st.net_zone_sum = 0.0;
   st.flipped_mfe_zone_sum = 0.0;
   st.flipped_mae_zone_sum = 0.0;
   st.flipped_follow10_n = 0;
   st.random_mfe_zone_sum = 0.0;
   st.random_mae_zone_sum = 0.0;
   st.random_follow10_n = 0;
   st.delta_log_sum = 0.0;
   ArrayResize(st.mfe_zone_vals, 0);
   ArrayResize(st.mae_zone_vals, 0);
   ArrayResize(st.net_zone_vals, 0);
}

void DAL_M0005StatsAdd(DALM0005PathStats &st, const DALM0005Path &p)
{
   st.n++;
   if(!p.valid)
      return;
   st.valid++;
   if(p.path_type == DAL_M0005_PATH_REVERSAL) st.reversal_n++; else st.continuation_n++;
   if(p.target_success) st.target_success_n++;
   if(p.follow_success) st.follow_success_n++;
   if(p.follow_05) st.follow05_n++;
   if(p.follow_10) st.follow10_n++;
   if(p.follow_15) st.follow15_n++;
   if(p.follow_20) st.follow20_n++;
   if(p.positive_net) st.positive_net_n++;
   if(p.exit_reason == DAL_M0005_EXIT_INVALIDATION) st.invalidation_n++;
   if(p.exit_reason == DAL_M0005_EXIT_REGIME_CHANGE) st.regime_change_n++;
   if(p.exit_reason == DAL_M0005_EXIT_NO_ENTRY) st.no_entry_n++;
   if(p.exit_reason == DAL_M0005_EXIT_NO_DESTINATION) st.no_destination_n++;
   if(p.exit_reason == DAL_M0005_EXIT_MAX_BARS) st.max_exit_n++;
   if(p.exit_reason == DAL_M0005_EXIT_END_OF_DATA) st.end_data_n++;
   st.bars_sum += p.bars_to_exit;
   st.events_sum += p.events_to_exit;
   st.mfe_sum += p.mfe;
   st.mae_sum += p.mae;
   st.mfe_zone_sum += p.mfe_zone;
   st.mae_zone_sum += p.mae_zone;
   st.net_zone_sum += p.net_zone;
   st.flipped_mfe_zone_sum += p.flipped_mfe_zone;
   st.flipped_mae_zone_sum += p.flipped_mae_zone;
   if(p.flipped_follow_10) st.flipped_follow10_n++;
   st.random_mfe_zone_sum += p.random_mfe_zone;
   st.random_mae_zone_sum += p.random_mae_zone;
   if(p.random_follow_10) st.random_follow10_n++;
   st.delta_log_sum += p.delta_log;
   DAL_M0004AppendDouble(st.mfe_zone_vals, p.mfe_zone);
   DAL_M0004AppendDouble(st.mae_zone_vals, p.mae_zone);
   DAL_M0004AppendDouble(st.net_zone_vals, p.net_zone);
}

void DAL_M0005ComputeStats(const string name, const DALM0005Path &paths[], DALM0005PathStats &st)
{
   DAL_M0005ResetStats(st, name);
   int n = ArraySize(paths);
   for(int i = 0; i < n; i++)
      DAL_M0005StatsAdd(st, paths[i]);
}

string DAL_M0005PathCountsText(const string tag, const DALM0005Config &config, const DALM0005PathStats &st, const int evaluated)
{
   double coverage = evaluated > 0 ? 100.0 * st.valid / evaluated : 0.0;
   return tag
      + "*regimeSource=" + DAL_M0005RegimeSourceToString(config.regime_source)
      + "*name=" + st.name
      + "*evaluated=" + IntegerToString(evaluated)
      + "*pathN=" + IntegerToString(st.valid)
      + "*coveragePct=" + DAL_M0001FmtPct(coverage)
      + "*reversalPathN=" + IntegerToString(st.reversal_n)
      + "*continuationPathN=" + IntegerToString(st.continuation_n)
      + "*reversalPathPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.reversal_n / st.valid : 0.0)
      + "*continuationPathPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.continuation_n / st.valid : 0.0);
}

string DAL_M0005PathOutcomeText(const string tag, const DALM0005Config &config, const DALM0005PathStats &st)
{
   return tag
      + "*regimeSource=" + DAL_M0005RegimeSourceToString(config.regime_source)
      + "*name=" + st.name
      + "*pathN=" + IntegerToString(st.valid)
      + "*targetSuccessPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.target_success_n / st.valid : 0.0)
      + "*followSuccessPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.follow_success_n / st.valid : 0.0)
      + "*follow0_5ZonePct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.follow05_n / st.valid : 0.0)
      + "*follow1_0ZonePct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.follow10_n / st.valid : 0.0)
      + "*follow1_5ZonePct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.follow15_n / st.valid : 0.0)
      + "*follow2_0ZonePct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.follow20_n / st.valid : 0.0)
      + "*positiveNetPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.positive_net_n / st.valid : 0.0)
      + "*invalidationPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.invalidation_n / st.valid : 0.0)
      + "*regimeChangeExitPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.regime_change_n / st.valid : 0.0)
      + "*maxBarsExitPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.max_exit_n / st.valid : 0.0)
      + "*endDataExitPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.end_data_n / st.valid : 0.0);
}

string DAL_M0005PathExcursionText(const string tag, const DALM0005Config &config, const DALM0005PathStats &st)
{
   return tag
      + "*regimeSource=" + DAL_M0005RegimeSourceToString(config.regime_source)
      + "*name=" + st.name
      + "*pathN=" + IntegerToString(st.valid)
      + "*meanMfeZone=" + DAL_M0001Fmt4(st.valid > 0 ? st.mfe_zone_sum / st.valid : 0.0)
      + "*medianMfeZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mfe_zone_vals, 0.50))
      + "*p90MfeZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mfe_zone_vals, 0.90))
      + "*p95MfeZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mfe_zone_vals, 0.95))
      + "*meanMaeZone=" + DAL_M0001Fmt4(st.valid > 0 ? st.mae_zone_sum / st.valid : 0.0)
      + "*medianMaeZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mae_zone_vals, 0.50))
      + "*p90MaeZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mae_zone_vals, 0.90))
      + "*p95MaeZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mae_zone_vals, 0.95))
      + "*mfeMaeRatio=" + DAL_M0001Fmt4(DAL_M0005SafeDiv(st.mfe_zone_sum, st.mae_zone_sum))
      + "*meanNetZone=" + DAL_M0001Fmt4(st.valid > 0 ? st.net_zone_sum / st.valid : 0.0)
      + "*medianNetZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.net_zone_vals, 0.50))
      + "*meanBarsToExit=" + DAL_M0001Fmt4(st.valid > 0 ? (double)st.bars_sum / st.valid : 0.0)
      + "*meanEventsToExit=" + DAL_M0001Fmt4(st.valid > 0 ? (double)st.events_sum / st.valid : 0.0)
      + "*meanDLog=" + DAL_M0001Fmt4(st.valid > 0 ? st.delta_log_sum / st.valid : 0.0);
}

string DAL_M0005PathStressText(const string tag, const DALM0005Config &config, const DALM0005PathStats &st)
{
   double actual_mfe = st.valid > 0 ? st.mfe_zone_sum / st.valid : 0.0;
   double flip_mfe = st.valid > 0 ? st.flipped_mfe_zone_sum / st.valid : 0.0;
   double random_mfe = st.valid > 0 ? st.random_mfe_zone_sum / st.valid : 0.0;
   double actual_follow = st.valid > 0 ? 100.0 * st.follow10_n / st.valid : 0.0;
   double flip_follow = st.valid > 0 ? 100.0 * st.flipped_follow10_n / st.valid : 0.0;
   double random_follow = st.valid > 0 ? 100.0 * st.random_follow10_n / st.valid : 0.0;
   return tag
      + "*regimeSource=" + DAL_M0005RegimeSourceToString(config.regime_source)
      + "*name=" + st.name
      + "*pathN=" + IntegerToString(st.valid)
      + "*actualMeanMfeZone=" + DAL_M0001Fmt4(actual_mfe)
      + "*flippedMeanMfeZone=" + DAL_M0001Fmt4(flip_mfe)
      + "*actualMinusFlippedMfeZone=" + DAL_M0001Fmt4(actual_mfe - flip_mfe)
      + "*randomMatchedMeanMfeZone=" + DAL_M0001Fmt4(random_mfe)
      + "*actualMinusRandomMfeZone=" + DAL_M0001Fmt4(actual_mfe - random_mfe)
      + "*actualFollow1xPct=" + DAL_M0001FmtPct(actual_follow)
      + "*flippedFollow1xPct=" + DAL_M0001FmtPct(flip_follow)
      + "*actualMinusFlippedFollow1xPct=" + DAL_M0001FmtPct(actual_follow - flip_follow)
      + "*randomMatchedFollow1xPct=" + DAL_M0001FmtPct(random_follow)
      + "*actualMinusRandomFollow1xPct=" + DAL_M0001FmtPct(actual_follow - random_follow)
      + "*stressModel=direction_flip_and_matched_random_entry";
}

string DAL_M0005PathCompareText(
   const string tag,
   const DALM0005Config &config,
   const DALM0005PathStats &all_stats,
   const DALM0005PathStats &rev_stats,
   const DALM0005PathStats &cont_stats
)
{
   double rev_mfe = rev_stats.valid > 0 ? rev_stats.mfe_zone_sum / rev_stats.valid : 0.0;
   double cont_mfe = cont_stats.valid > 0 ? cont_stats.mfe_zone_sum / cont_stats.valid : 0.0;
   double rev_mae = rev_stats.valid > 0 ? rev_stats.mae_zone_sum / rev_stats.valid : 0.0;
   double cont_mae = cont_stats.valid > 0 ? cont_stats.mae_zone_sum / cont_stats.valid : 0.0;
   double rev_follow = rev_stats.valid > 0 ? 100.0 * rev_stats.follow10_n / rev_stats.valid : 0.0;
   double cont_follow = cont_stats.valid > 0 ? 100.0 * cont_stats.follow10_n / cont_stats.valid : 0.0;
   return tag
      + "*regimeSource=" + DAL_M0005RegimeSourceToString(config.regime_source)
      + "*allPathN=" + IntegerToString(all_stats.valid)
      + "*reversalPathN=" + IntegerToString(rev_stats.valid)
      + "*continuationPathN=" + IntegerToString(cont_stats.valid)
      + "*revFollow1xPct=" + DAL_M0001FmtPct(rev_follow)
      + "*contFollow1xPct=" + DAL_M0001FmtPct(cont_follow)
      + "*contMinusRevFollow1xPct=" + DAL_M0001FmtPct(cont_follow - rev_follow)
      + "*revMeanMfeZone=" + DAL_M0001Fmt4(rev_mfe)
      + "*contMeanMfeZone=" + DAL_M0001Fmt4(cont_mfe)
      + "*contMinusRevMfeZone=" + DAL_M0001Fmt4(cont_mfe - rev_mfe)
      + "*revMeanMaeZone=" + DAL_M0001Fmt4(rev_mae)
      + "*contMeanMaeZone=" + DAL_M0001Fmt4(cont_mae)
      + "*contMinusRevMaeZone=" + DAL_M0001Fmt4(cont_mae - rev_mae)
      + "*directionalMemoryModel=structural_destination_for_reversal_state_change_for_continuation";
}

void DAL_M0005PrintFinalReports(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const string symbol,
   const string timeframe,
   const string source_mode,
   const datetime min_entry_time,
   const DALM0002Config &h2_config,
   const DALM0005Config &h5_config
)
{
   DALM0002BranchSample all_samples[];
   DALM0002BranchSample reversal_samples[];
   DALM0002BranchSample continuation_samples[];
   DALM0002Audit audit;
   DAL_M0002CollectBranchSamples(events, events_count, bars, bars_count, min_entry_time, h2_config, all_samples, reversal_samples, continuation_samples, audit);
   DAL_M0004SortSamplesByOutcome(all_samples);

   int count = ArraySize(all_samples);
   int labels[];
   int sessions[];
   int trends[];
   int revisits[];
   double prevols[];
   datetime times[];
   DAL_M0004BuildLabelArrays(all_samples, labels, sessions, trends, revisits, prevols, times);

   int min_random_start = DAL_M0001FirstIndexAtOrAfter(bars, bars_count, min_entry_time);
   if(min_random_start < 1) min_random_start = 1;

   DALM0005Path all_paths[];
   DALM0005Path rev_paths[];
   DALM0005Path cont_paths[];
   DAL_M0005BuildPaths(all_samples, count, bars, bars_count, labels, h5_config, min_random_start, all_paths, rev_paths, cont_paths);

   DALM0005PathStats all_stats;
   DALM0005PathStats rev_stats;
   DALM0005PathStats cont_stats;
   DAL_M0005ComputeStats("all_paths", all_paths, all_stats);
   DAL_M0005ComputeStats("reversal_paths", rev_paths, rev_stats);
   DAL_M0005ComputeStats("continuation_paths", cont_paths, cont_stats);

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_AUDIT", symbol, timeframe, source_mode, events_count, min_entry_time),
      "AUDIT*sourceEvents=", events_count,
      "*m0002Paired=", count,
      "*pathN=", all_stats.valid,
      "*reversalPathN=", rev_stats.valid,
      "*continuationPathN=", cont_stats.valid,
      "*regimeSource=", DAL_M0005RegimeSourceToString(h5_config.regime_source),
      "*contextK=", h5_config.context_lookback,
      "*contextEwmaAlpha=", DAL_M0001Fmt4(h5_config.context_ewma_alpha),
      "*contextThreshold=", DAL_M0001Fmt4(h5_config.context_strong_threshold),
      "*breakMode=", (h5_config.break_uses_close ? "close_break" : "wick_break"),
      "*continuationSuccessZoneMultiple=", DAL_M0001Fmt4(h5_config.continuation_success_zone_multiple),
      "*mfeMaeStopGuard=stop_at_path_exit");

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_COUNTS_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathCountsText("PATH_COUNTS", h5_config, all_stats, MathMax(0, count - 1)));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_COUNTS_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathCountsText("PATH_COUNTS", h5_config, rev_stats, MathMax(0, count - 1)));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_COUNTS_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathCountsText("PATH_COUNTS", h5_config, cont_stats, MathMax(0, count - 1)));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_OUTCOME_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathOutcomeText("PATH_OUTCOME", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_OUTCOME_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathOutcomeText("PATH_OUTCOME", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_OUTCOME_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathOutcomeText("PATH_OUTCOME", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_EXCURSION_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathExcursionText("PATH_MFE_MAE", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_EXCURSION_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathExcursionText("PATH_MFE_MAE", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_EXCURSION_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathExcursionText("PATH_MFE_MAE", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_STRESS_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathStressText("PATH_RANDOM_STRESS", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_STRESS_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathStressText("PATH_RANDOM_STRESS", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_STRESS_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathStressText("PATH_RANDOM_STRESS", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_REV_CONT_COMPARE", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathCompareText("PATH_BRANCH_COMPARE", h5_config, all_stats, rev_stats, cont_stats));
}

#endif
