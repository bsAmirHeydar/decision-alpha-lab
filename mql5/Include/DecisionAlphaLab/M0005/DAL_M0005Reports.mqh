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

enum ENUM_DALM0005ReversalStopMode
{
   DAL_M0005_REV_STOP_ZONE_EDGE = 0,
   DAL_M0005_REV_STOP_ZONE_OR_HUNT_EXTREME = 1
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
   ENUM_DALM0005ReversalStopMode reversal_stop_mode;
   bool reversal_stop_uses_wick;
   bool reversal_same_bar_stop_first;
   double reversal_hunt_lock_zone_multiple;
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
   double base_stop_price;
   double adaptive_stop_price;
   double stop_distance;
   double stop_distance_zone;
   double base_stop_distance_zone;
   double hunt_depth_zone;
   double target_distance_zone;
   double mfe_r;
   double mae_r;
   double net_r;
   double target_distance_r;
   bool hunt_occurred;
   bool stop_expanded_by_hunt;
   bool stop_hit;
   bool stop_locked;
   bool same_bar_target_stop;
   int hunt_start_index;
   int hunt_extreme_index;
   int stop_lock_index;
   int stop_hit_index;
   int first_mfe10_index;
   int first_mae10_index;
   bool mfe10_before_mae10;
   bool mae10_before_mfe10;
   int first_mfe1r_index;
   int first_mae1r_index;
   bool mfe1r_before_mae1r;
   bool mae1r_before_mfe1r;
   bool hit_mfe_1r;
   bool hit_mfe_2r;
   bool hit_mfe_3r;
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
   double random_net_zone;
   double random_mfe_r;
   double random_mae_r;
   double random_net_r;
   bool random_follow_10;
   bool random_positive_net;
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
   int hunt_n;
   int stop_expanded_n;
   int stop_hit_n;
   int stop_locked_n;
   int same_bar_target_stop_n;
   int mfe10_before_mae10_n;
   int mae10_before_mfe10_n;
   int mfe1r_before_mae1r_n;
   int mae1r_before_mfe1r_n;
   int hit_mfe_1r_n;
   int hit_mfe_2r_n;
   int hit_mfe_3r_n;
   int realized_win_n;
   int realized_loss_n;
   int realized_flat_n;
   int random_win_n;
   int random_loss_n;
   int random_flat_n;
   int random_hit_mfe_1r_n;
   int random_hit_mfe_2r_n;
   int random_hit_mfe_3r_n;
   int max_exit_n;
   int end_data_n;
   int bars_sum;
   int events_sum;
   double mfe_sum;
   double mae_sum;
   double mfe_zone_sum;
   double mae_zone_sum;
   double net_zone_sum;
   double stop_distance_zone_sum;
   double base_stop_distance_zone_sum;
   double hunt_depth_zone_sum;
   double target_distance_zone_sum;
   double mfe_r_sum;
   double mae_r_sum;
   double net_r_sum;
   double target_distance_r_sum;
   double gross_win_r_sum;
   double gross_loss_r_sum;
   double win_r_sum;
   double loss_r_abs_sum;
   double random_mfe_r_sum;
   double random_mae_r_sum;
   double random_net_zone_sum;
   double random_net_r_sum;
   double random_gross_win_r_sum;
   double random_gross_loss_r_sum;
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
   double net_r_vals[];
   double stop_distance_zone_vals[];
   double hunt_depth_zone_vals[];
   double mfe_r_vals[];
   double mae_r_vals[];
   double random_net_r_vals[];
   double random_mfe_r_vals[];
   double random_mae_r_vals[];
};

string DAL_M0005RegimeSourceToString(const ENUM_DALM0005RegimeSource src)
{
   if(src == DAL_M0005_REGIME_EWMA_CONTEXT) return "EWMA_CONTEXT";
   if(src == DAL_M0005_REGIME_EWMA_CONSENSUS) return "EWMA_CONSENSUS";
   if(src == DAL_M0005_REGIME_LAST_WITH_CONTEXT_CONFIDENCE) return "LAST_WITH_CONTEXT_CONFIDENCE";
   return "LAST_ONLY";
}

string DAL_M0005ReversalStopModeToString(const ENUM_DALM0005ReversalStopMode mode)
{
   if(mode == DAL_M0005_REV_STOP_ZONE_OR_HUNT_EXTREME) return "ZONE_OR_HUNT_EXTREME_FARTHER";
   return "ZONE_EDGE";
}


void DAL_M0005ResetPath(DALM0005Path &p)
{
   p.valid = false;
   p.path_type = DAL_M0005_PATH_REVERSAL;
   p.exit_reason = DAL_M0005_EXIT_UNKNOWN;
   p.source_index = -1;
   p.regime_label = -1;
   p.direction = 0;
   p.entry_index = -1;
   p.exit_index = -1;
   p.target_index = -1;
   p.events_to_exit = 0;
   p.bars_to_exit = 0;
   p.entry_time = 0;
   p.exit_time = 0;
   p.entry_price = 0.0;
   p.exit_price = 0.0;
   p.zone_width = 0.0;
   p.base_stop_price = 0.0;
   p.adaptive_stop_price = 0.0;
   p.stop_distance = 0.0;
   p.stop_distance_zone = 0.0;
   p.base_stop_distance_zone = 0.0;
   p.hunt_depth_zone = 0.0;
   p.target_distance_zone = 0.0;
   p.mfe_r = 0.0;
   p.mae_r = 0.0;
   p.net_r = 0.0;
   p.target_distance_r = 0.0;
   p.hunt_occurred = false;
   p.stop_expanded_by_hunt = false;
   p.stop_hit = false;
   p.stop_locked = false;
   p.same_bar_target_stop = false;
   p.hunt_start_index = -1;
   p.hunt_extreme_index = -1;
   p.stop_lock_index = -1;
   p.stop_hit_index = -1;
   p.first_mfe10_index = -1;
   p.first_mae10_index = -1;
   p.mfe10_before_mae10 = false;
   p.mae10_before_mfe10 = false;
   p.first_mfe1r_index = -1;
   p.first_mae1r_index = -1;
   p.mfe1r_before_mae1r = false;
   p.mae1r_before_mfe1r = false;
   p.hit_mfe_1r = false;
   p.hit_mfe_2r = false;
   p.hit_mfe_3r = false;
   p.mfe = 0.0;
   p.mae = 0.0;
   p.mfe_zone = 0.0;
   p.mae_zone = 0.0;
   p.net_move = 0.0;
   p.net_zone = 0.0;
   p.target_success = false;
   p.follow_success = false;
   p.follow_05 = false;
   p.follow_10 = false;
   p.follow_15 = false;
   p.follow_20 = false;
   p.positive_net = false;
   p.flipped_mfe_zone = 0.0;
   p.flipped_mae_zone = 0.0;
   p.flipped_follow_10 = false;
   p.random_mfe_zone = 0.0;
   p.random_mae_zone = 0.0;
   p.random_net_zone = 0.0;
   p.random_mfe_r = 0.0;
   p.random_mae_r = 0.0;
   p.random_net_r = 0.0;
   p.random_follow_10 = false;
   p.random_positive_net = false;
   p.context_p = 0.0;
   p.context_confidence = 0.0;
   p.context_dominant = -1;
   p.last_label = -1;
   p.session = 0;
   p.prevol_bucket = 0;
   p.revisit_bucket = 0;
   p.spacing_bucket = 0;
   p.delta_log = 0.0;
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


double DAL_M0005StructuralStopPrice(const DALM0002BranchSample &sample, const int direction)
{
   return direction > 0 ? sample.territory_lower : sample.territory_upper;
}

double DAL_M0005AdverseExtremePrice(const DALBar &bar, const int direction)
{
   return direction > 0 ? bar.low : bar.high;
}

double DAL_M0005FavorableExtremePrice(const DALBar &bar, const int direction)
{
   return direction > 0 ? bar.high : bar.low;
}

bool DAL_M0005IsFurtherAdverse(const double candidate, const double current, const int direction)
{
   if(direction > 0)
      return candidate < current;
   return candidate > current;
}

bool DAL_M0005IsAdverseBeyondStop(const double adverse_price, const double stop_price, const int direction)
{
   if(direction > 0)
      return adverse_price < stop_price;
   return adverse_price > stop_price;
}

bool DAL_M0005StopTouched(const DALBar &bar, const double stop_price, const int direction, const bool use_wick)
{
   if(direction > 0)
      return use_wick ? (bar.low <= stop_price) : (bar.close <= stop_price);
   return use_wick ? (bar.high >= stop_price) : (bar.close >= stop_price);
}

bool DAL_M0005ReversalZoneReclaimed(const DALBar &bar, const DALM0002BranchSample &sample, const int direction)
{
   if(direction > 0)
      return bar.close >= sample.territory_lower;
   return bar.close <= sample.territory_upper;
}

double DAL_M0005FavorableMoveFromEntry(const DALBar &bar, const int direction, const double entry_price)
{
   if(direction > 0)
      return bar.high - entry_price;
   return entry_price - bar.low;
}

double DAL_M0005AdverseMoveFromEntry(const DALBar &bar, const int direction, const double entry_price)
{
   if(direction > 0)
      return entry_price - bar.low;
   return bar.high - entry_price;
}

void DAL_M0005ComputeFirstHitOrder(
   const DALBar &bars[],
   const int bars_count,
   const int entry_index,
   const int exit_index,
   const int direction,
   const double entry_price,
   const double zone_width,
   int &first_mfe10_index,
   int &first_mae10_index,
   bool &mfe10_before_mae10,
   bool &mae10_before_mfe10
)
{
   first_mfe10_index = -1;
   first_mae10_index = -1;
   mfe10_before_mae10 = false;
   mae10_before_mfe10 = false;
   if(entry_index < 0 || exit_index < entry_index || zone_width <= 0.0)
      return;
   int end = exit_index;
   if(end >= bars_count) end = bars_count - 1;
   for(int i = entry_index; i <= end; i++)
   {
      double fm = DAL_M0005FavorableMoveFromEntry(bars[i], direction, entry_price);
      double am = DAL_M0005AdverseMoveFromEntry(bars[i], direction, entry_price);
      if(first_mfe10_index < 0 && fm >= zone_width)
         first_mfe10_index = i;
      if(first_mae10_index < 0 && am >= zone_width)
         first_mae10_index = i;
      if(first_mfe10_index >= 0 && first_mae10_index >= 0)
         break;
   }
   if(first_mfe10_index >= 0 && (first_mae10_index < 0 || first_mfe10_index < first_mae10_index))
      mfe10_before_mae10 = true;
   if(first_mae10_index >= 0 && (first_mfe10_index < 0 || first_mae10_index < first_mfe10_index))
      mae10_before_mfe10 = true;
}

void DAL_M0005ComputeFirstHitOrderByDistance(
   const DALBar &bars[],
   const int bars_count,
   const int entry_index,
   const int exit_index,
   const int direction,
   const double entry_price,
   const double distance,
   int &first_mfe_index,
   int &first_mae_index,
   bool &mfe_before_mae,
   bool &mae_before_mfe
)
{
   first_mfe_index = -1;
   first_mae_index = -1;
   mfe_before_mae = false;
   mae_before_mfe = false;
   if(entry_index < 0 || exit_index < entry_index || distance <= 0.0)
      return;
   int end = exit_index;
   if(end >= bars_count) end = bars_count - 1;
   for(int i = entry_index; i <= end; i++)
   {
      double fm = DAL_M0005FavorableMoveFromEntry(bars[i], direction, entry_price);
      double am = DAL_M0005AdverseMoveFromEntry(bars[i], direction, entry_price);
      if(first_mfe_index < 0 && fm >= distance)
         first_mfe_index = i;
      if(first_mae_index < 0 && am >= distance)
         first_mae_index = i;
      if(first_mfe_index >= 0 && first_mae_index >= 0)
         break;
   }
   if(first_mfe_index >= 0 && (first_mae_index < 0 || first_mfe_index < first_mae_index))
      mfe_before_mae = true;
   if(first_mae_index >= 0 && (first_mfe_index < 0 || first_mae_index < first_mfe_index))
      mae_before_mfe = true;
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
   double &net_zone,
   const double zone_width
)
{
   mfe_zone = 0.0;
   mae_zone = 0.0;
   net_zone = 0.0;
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
   net_zone = DAL_M0005SafeDiv(net, zone_width);
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
   if(path.base_stop_price == 0.0 && path.adaptive_stop_price == 0.0)
   {
      path.base_stop_price = DAL_M0005StructuralStopPrice(sample, path.direction);
      path.adaptive_stop_price = path.base_stop_price;
   }
   if(path.adaptive_stop_price == 0.0)
      path.adaptive_stop_price = path.base_stop_price;
   path.bars_to_exit = path.exit_index - path.entry_index + 1;
   if(path.bars_to_exit < 0) path.bars_to_exit = 0;

   DAL_M0005ComputeExcursions(bars, bars_count, path.entry_index, path.exit_index, path.direction, path.entry_price, path.mfe, path.mae, path.net_move);
   path.mfe_zone = DAL_M0005SafeDiv(path.mfe, path.zone_width);
   path.mae_zone = DAL_M0005SafeDiv(path.mae, path.zone_width);
   path.net_zone = DAL_M0005SafeDiv(path.net_move, path.zone_width);
   path.stop_distance = MathAbs(path.entry_price - path.adaptive_stop_price);
   double base_stop_distance = MathAbs(path.entry_price - path.base_stop_price);
   if(path.stop_distance <= 0.0) path.stop_distance = path.zone_width;
   path.stop_distance_zone = DAL_M0005SafeDiv(path.stop_distance, path.zone_width);
   path.base_stop_distance_zone = DAL_M0005SafeDiv(base_stop_distance, path.zone_width);
   path.hunt_depth_zone = MathMax(0.0, path.stop_distance_zone - path.base_stop_distance_zone);
   path.target_distance_zone = path.target_index >= path.entry_index ? DAL_M0005SafeDiv(MathAbs(bars[MathMin(path.target_index, bars_count - 1)].close - path.entry_price), path.zone_width) : 0.0;
   path.mfe_r = DAL_M0005SafeDiv(path.mfe, path.stop_distance);
   path.mae_r = DAL_M0005SafeDiv(path.mae, path.stop_distance);
   path.net_r = DAL_M0005SafeDiv(path.net_move, path.stop_distance);
   path.target_distance_r = DAL_M0005SafeDiv(path.target_distance_zone, path.stop_distance_zone);
   DAL_M0005ComputeFirstHitOrder(bars, bars_count, path.entry_index, path.exit_index, path.direction, path.entry_price, path.zone_width, path.first_mfe10_index, path.first_mae10_index, path.mfe10_before_mae10, path.mae10_before_mfe10);
   DAL_M0005ComputeFirstHitOrderByDistance(bars, bars_count, path.entry_index, path.exit_index, path.direction, path.entry_price, path.stop_distance, path.first_mfe1r_index, path.first_mae1r_index, path.mfe1r_before_mae1r, path.mae1r_before_mfe1r);
   path.hit_mfe_1r = (path.mfe_r >= 1.0);
   path.hit_mfe_2r = (path.mfe_r >= 2.0);
   path.hit_mfe_3r = (path.mfe_r >= 3.0);
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
   double random_net_sum = 0.0;
   int random_follow_sum = 0;
   int rk = config.random_samples_per_path;
   if(rk < 1) rk = 1;
   for(int r = 0; r < rk; r++)
   {
      double rm = 0.0, ra = 0.0, rn = 0.0;
      DAL_M0005ComputeRandomExcursion(bars, bars_count, min_random_start, path.bars_to_exit, path.direction, path.source_index + 811 + r * 17, path.entry_index + 991 + r * 31, rm, ra, rn, path.zone_width);
      random_mfe_sum += rm;
      random_mae_sum += ra;
      random_net_sum += rn;
      if(rm >= config.follow_zone_mult_2)
         random_follow_sum++;
   }
   path.random_mfe_zone = random_mfe_sum / rk;
   path.random_mae_zone = random_mae_sum / rk;
   path.random_net_zone = random_net_sum / rk;
   path.random_mfe_r = DAL_M0005SafeDiv(path.random_mfe_zone, path.stop_distance_zone);
   path.random_mae_r = DAL_M0005SafeDiv(path.random_mae_zone, path.stop_distance_zone);
   path.random_net_r = DAL_M0005SafeDiv(path.random_net_zone, path.stop_distance_zone);
   path.random_follow_10 = (random_follow_sum > rk / 2);
   path.random_positive_net = (path.random_net_r > 0.0);
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
   DAL_M0005ResetPath(path);
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

   double base_stop = DAL_M0005StructuralStopPrice(samples[index], path.direction);
   double entry_price = bars[path.entry_index].close;
   double zone_width = DAL_M0005ZoneWidth(samples[index]);
   double adverse_extreme = base_stop;
   int first_hunt_index = -1;
   int hunt_extreme_index = -1;
   int stop_lock_index = -1;
   int stop_hit_index = -1;
   bool hunt_active = false;
   bool stop_locked = false;
   bool same_bar_target_stop = false;
   double lock_threshold = config.reversal_hunt_lock_zone_multiple;
   if(lock_threshold <= 0.0) lock_threshold = 0.5;

   if(config.reversal_stop_mode == DAL_M0005_REV_STOP_ZONE_EDGE)
   {
      stop_locked = true;
      stop_lock_index = path.entry_index;
      adverse_extreme = base_stop;
   }

   for(int b = path.entry_index + 1; b <= max_exit; b++)
   {
      bool target_bar = (path.target_index <= max_exit && b >= path.target_index);
      double adverse_price = DAL_M0005AdverseExtremePrice(bars[b], path.direction);
      double favorable_move_zone = DAL_M0005SafeDiv(DAL_M0005FavorableMoveFromEntry(bars[b], path.direction, entry_price), zone_width);

      if(!stop_locked)
      {
         if(DAL_M0005IsAdverseBeyondStop(adverse_price, base_stop, path.direction))
         {
            if(!hunt_active)
               first_hunt_index = b;
            hunt_active = true;
            if(hunt_extreme_index < 0 || DAL_M0005IsFurtherAdverse(adverse_price, adverse_extreme, path.direction))
            {
               adverse_extreme = adverse_price;
               hunt_extreme_index = b;
            }
         }

         if(hunt_active)
         {
            if(DAL_M0005ReversalZoneReclaimed(bars[b], samples[index], path.direction) || favorable_move_zone >= lock_threshold)
            {
               stop_locked = true;
               stop_lock_index = b;
            }
         }
         else if(favorable_move_zone >= lock_threshold)
         {
            stop_locked = true;
            stop_lock_index = b;
            adverse_extreme = base_stop;
         }
      }
      else
      {
         if(b > stop_lock_index && DAL_M0005StopTouched(bars[b], adverse_extreme, path.direction, config.reversal_stop_uses_wick))
         {
            stop_hit_index = b;
            if(target_bar)
               same_bar_target_stop = true;
            break;
         }
      }

      if(target_bar)
         break;
   }

   path.base_stop_price = base_stop;
   path.adaptive_stop_price = adverse_extreme;
   path.hunt_occurred = hunt_active;
   path.stop_expanded_by_hunt = hunt_active && MathAbs(adverse_extreme - base_stop) > 0.0;
   path.stop_locked = stop_locked;
   path.hunt_start_index = first_hunt_index;
   path.hunt_extreme_index = hunt_extreme_index;
   path.stop_lock_index = stop_lock_index;
   path.stop_hit_index = stop_hit_index;
   path.same_bar_target_stop = same_bar_target_stop;

   if(stop_hit_index >= 0 && (stop_hit_index < path.target_index || (stop_hit_index == path.target_index && config.reversal_same_bar_stop_first)))
   {
      path.exit_index = stop_hit_index;
      path.exit_reason = DAL_M0005_EXIT_INVALIDATION;
      path.target_success = false;
      path.stop_hit = true;
   }
   else if(path.target_index <= max_exit)
   {
      path.exit_index = path.target_index;
      path.exit_reason = DAL_M0005_EXIT_TARGET;
      path.target_success = true;
      path.stop_hit = false;
   }
   else if(hunt_active && !stop_locked && hunt_extreme_index >= 0)
   {
      path.exit_index = hunt_extreme_index;
      path.exit_reason = DAL_M0005_EXIT_INVALIDATION;
      path.target_success = false;
      path.stop_hit = true;
   }
   else
   {
      path.exit_index = max_exit;
      path.exit_reason = DAL_M0005_EXIT_MAX_BARS;
      path.target_success = false;
      path.stop_hit = false;
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
   DAL_M0005ResetPath(path);
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
   DALM0005Path &continuation_paths[],
   int &attempted_n,
   int &no_regime_n,
   int &no_entry_n,
   int &no_destination_n,
   int &reversal_attempts,
   int &continuation_attempts
)
{
   attempted_n = 0;
   no_regime_n = 0;
   no_entry_n = 0;
   no_destination_n = 0;
   reversal_attempts = 0;
   continuation_attempts = 0;
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
      {
         no_regime_n++;
         continue;
      }

      attempted_n++;
      if(regime == DAL_M0004_LABEL_REVERSAL) reversal_attempts++; else continuation_attempts++;
      DALM0005Path path;
      bool ok = false;
      if(regime == DAL_M0004_LABEL_REVERSAL)
         ok = DAL_M0005BuildReversalPath(samples, count, i, regime, bars, bars_count, labels, config, min_random_start, path);
      else
         ok = DAL_M0005BuildContinuationPath(samples, count, i, regime, bars, bars_count, labels, config, min_random_start, path);

      if(!ok)
      {
         if(path.exit_reason == DAL_M0005_EXIT_NO_ENTRY) no_entry_n++;
         if(path.exit_reason == DAL_M0005_EXIT_NO_DESTINATION) no_destination_n++;
         continue;
      }

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
   st.hunt_n = 0;
   st.stop_expanded_n = 0;
   st.stop_hit_n = 0;
   st.stop_locked_n = 0;
   st.same_bar_target_stop_n = 0;
   st.mfe10_before_mae10_n = 0;
   st.mae10_before_mfe10_n = 0;
   st.mfe1r_before_mae1r_n = 0;
   st.mae1r_before_mfe1r_n = 0;
   st.hit_mfe_1r_n = 0;
   st.hit_mfe_2r_n = 0;
   st.hit_mfe_3r_n = 0;
   st.realized_win_n = 0;
   st.realized_loss_n = 0;
   st.realized_flat_n = 0;
   st.random_win_n = 0;
   st.random_loss_n = 0;
   st.random_flat_n = 0;
   st.random_hit_mfe_1r_n = 0;
   st.random_hit_mfe_2r_n = 0;
   st.random_hit_mfe_3r_n = 0;
   st.max_exit_n = 0;
   st.end_data_n = 0;
   st.bars_sum = 0;
   st.events_sum = 0;
   st.mfe_sum = 0.0;
   st.mae_sum = 0.0;
   st.mfe_zone_sum = 0.0;
   st.mae_zone_sum = 0.0;
   st.net_zone_sum = 0.0;
   st.stop_distance_zone_sum = 0.0;
   st.base_stop_distance_zone_sum = 0.0;
   st.hunt_depth_zone_sum = 0.0;
   st.target_distance_zone_sum = 0.0;
   st.mfe_r_sum = 0.0;
   st.mae_r_sum = 0.0;
   st.net_r_sum = 0.0;
   st.target_distance_r_sum = 0.0;
   st.gross_win_r_sum = 0.0;
   st.gross_loss_r_sum = 0.0;
   st.win_r_sum = 0.0;
   st.loss_r_abs_sum = 0.0;
   st.random_mfe_r_sum = 0.0;
   st.random_mae_r_sum = 0.0;
   st.random_net_zone_sum = 0.0;
   st.random_net_r_sum = 0.0;
   st.random_gross_win_r_sum = 0.0;
   st.random_gross_loss_r_sum = 0.0;
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
   ArrayResize(st.net_r_vals, 0);
   ArrayResize(st.stop_distance_zone_vals, 0);
   ArrayResize(st.hunt_depth_zone_vals, 0);
   ArrayResize(st.mfe_r_vals, 0);
   ArrayResize(st.mae_r_vals, 0);
   ArrayResize(st.random_net_r_vals, 0);
   ArrayResize(st.random_mfe_r_vals, 0);
   ArrayResize(st.random_mae_r_vals, 0);
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
   if(p.hunt_occurred) st.hunt_n++;
   if(p.stop_expanded_by_hunt) st.stop_expanded_n++;
   if(p.stop_hit) st.stop_hit_n++;
   if(p.stop_locked) st.stop_locked_n++;
   if(p.same_bar_target_stop) st.same_bar_target_stop_n++;
   if(p.mfe10_before_mae10) st.mfe10_before_mae10_n++;
   if(p.mae10_before_mfe10) st.mae10_before_mfe10_n++;
   if(p.mfe1r_before_mae1r) st.mfe1r_before_mae1r_n++;
   if(p.mae1r_before_mfe1r) st.mae1r_before_mfe1r_n++;
   if(p.hit_mfe_1r) st.hit_mfe_1r_n++;
   if(p.hit_mfe_2r) st.hit_mfe_2r_n++;
   if(p.hit_mfe_3r) st.hit_mfe_3r_n++;
   if(p.net_r > 0.0) st.realized_win_n++;
   else if(p.net_r < 0.0) st.realized_loss_n++;
   else st.realized_flat_n++;
   if(p.random_net_r > 0.0) st.random_win_n++;
   else if(p.random_net_r < 0.0) st.random_loss_n++;
   else st.random_flat_n++;
   if(p.random_mfe_r >= 1.0) st.random_hit_mfe_1r_n++;
   if(p.random_mfe_r >= 2.0) st.random_hit_mfe_2r_n++;
   if(p.random_mfe_r >= 3.0) st.random_hit_mfe_3r_n++;
   if(p.exit_reason == DAL_M0005_EXIT_MAX_BARS) st.max_exit_n++;
   if(p.exit_reason == DAL_M0005_EXIT_END_OF_DATA) st.end_data_n++;
   st.bars_sum += p.bars_to_exit;
   st.events_sum += p.events_to_exit;
   st.mfe_sum += p.mfe;
   st.mae_sum += p.mae;
   st.mfe_zone_sum += p.mfe_zone;
   st.mae_zone_sum += p.mae_zone;
   st.net_zone_sum += p.net_zone;
   st.stop_distance_zone_sum += p.stop_distance_zone;
   st.base_stop_distance_zone_sum += p.base_stop_distance_zone;
   st.hunt_depth_zone_sum += p.hunt_depth_zone;
   st.target_distance_zone_sum += p.target_distance_zone;
   st.mfe_r_sum += p.mfe_r;
   st.mae_r_sum += p.mae_r;
   st.net_r_sum += p.net_r;
   st.target_distance_r_sum += p.target_distance_r;
   if(p.net_r > 0.0) { st.gross_win_r_sum += p.net_r; st.win_r_sum += p.net_r; }
   if(p.net_r < 0.0) { st.gross_loss_r_sum += -p.net_r; st.loss_r_abs_sum += -p.net_r; }
   st.random_mfe_r_sum += p.random_mfe_r;
   st.random_mae_r_sum += p.random_mae_r;
   st.random_net_zone_sum += p.random_net_zone;
   st.random_net_r_sum += p.random_net_r;
   if(p.random_net_r > 0.0) st.random_gross_win_r_sum += p.random_net_r;
   if(p.random_net_r < 0.0) st.random_gross_loss_r_sum += -p.random_net_r;
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
   DAL_M0004AppendDouble(st.net_r_vals, p.net_r);
   DAL_M0004AppendDouble(st.stop_distance_zone_vals, p.stop_distance_zone);
   DAL_M0004AppendDouble(st.hunt_depth_zone_vals, p.hunt_depth_zone);
   DAL_M0004AppendDouble(st.mfe_r_vals, p.mfe_r);
   DAL_M0004AppendDouble(st.mae_r_vals, p.mae_r);
   DAL_M0004AppendDouble(st.random_net_r_vals, p.random_net_r);
   DAL_M0004AppendDouble(st.random_mfe_r_vals, p.random_mfe_r);
   DAL_M0004AppendDouble(st.random_mae_r_vals, p.random_mae_r);
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


string DAL_M0005PathStopRiskText(const string tag, const DALM0005Config &config, const DALM0005PathStats &st)
{
   return tag
      + "*regimeSource=" + DAL_M0005RegimeSourceToString(config.regime_source)
      + "*name=" + st.name
      + "*pathN=" + IntegerToString(st.valid)
      + "*reversalStopMode=" + DAL_M0005ReversalStopModeToString(config.reversal_stop_mode)
      + "*huntOccurredPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.hunt_n / st.valid : 0.0)
      + "*stopExpandedByHuntPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.stop_expanded_n / st.valid : 0.0)
      + "*stopHitPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.stop_hit_n / st.valid : 0.0)
      + "*stopLockedPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.stop_locked_n / st.valid : 0.0)
      + "*sameBarTargetStopPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.same_bar_target_stop_n / st.valid : 0.0)
      + "*meanBaseStopDistZone=" + DAL_M0001Fmt4(st.valid > 0 ? st.base_stop_distance_zone_sum / st.valid : 0.0)
      + "*meanStopDistZone=" + DAL_M0001Fmt4(st.valid > 0 ? st.stop_distance_zone_sum / st.valid : 0.0)
      + "*medianStopDistZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.stop_distance_zone_vals, 0.50))
      + "*p90StopDistZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.stop_distance_zone_vals, 0.90))
      + "*meanHuntDepthZone=" + DAL_M0001Fmt4(st.valid > 0 ? st.hunt_depth_zone_sum / st.valid : 0.0)
      + "*medianHuntDepthZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.hunt_depth_zone_vals, 0.50))
      + "*p90HuntDepthZone=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.hunt_depth_zone_vals, 0.90))
      + "*meanTargetDistZone=" + DAL_M0001Fmt4(st.valid > 0 ? st.target_distance_zone_sum / st.valid : 0.0)
      + "*meanTargetDistR=" + DAL_M0001Fmt4(st.valid > 0 ? st.target_distance_r_sum / st.valid : 0.0);
}

string DAL_M0005PathRiskRewardText(const string tag, const DALM0005Config &config, const DALM0005PathStats &st)
{
   return tag
      + "*regimeSource=" + DAL_M0005RegimeSourceToString(config.regime_source)
      + "*name=" + st.name
      + "*pathN=" + IntegerToString(st.valid)
      + "*meanMfeR=" + DAL_M0001Fmt4(st.valid > 0 ? st.mfe_r_sum / st.valid : 0.0)
      + "*medianMfeR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mfe_r_vals, 0.50))
      + "*p90MfeR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mfe_r_vals, 0.90))
      + "*p95MfeR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mfe_r_vals, 0.95))
      + "*meanMaeR=" + DAL_M0001Fmt4(st.valid > 0 ? st.mae_r_sum / st.valid : 0.0)
      + "*medianMaeR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mae_r_vals, 0.50))
      + "*p90MaeR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mae_r_vals, 0.90))
      + "*meanNetR=" + DAL_M0001Fmt4(st.valid > 0 ? st.net_r_sum / st.valid : 0.0)
      + "*mfeRoverMaeR=" + DAL_M0001Fmt4(DAL_M0005SafeDiv(st.mfe_r_sum, st.mae_r_sum))
      + "*mfe1xBeforeMae1xPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.mfe10_before_mae10_n / st.valid : 0.0)
      + "*mae1xBeforeMfe1xPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.mae10_before_mfe10_n / st.valid : 0.0)
      + "*firstHitEdgePct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * (st.mfe10_before_mae10_n - st.mae10_before_mfe10_n) / st.valid : 0.0);
}


string DAL_M0005PathRealizedRText(const string tag, const DALM0005Config &config, const DALM0005PathStats &st)
{
   double win_rate = st.valid > 0 ? 100.0 * st.realized_win_n / st.valid : 0.0;
   double loss_rate = st.valid > 0 ? 100.0 * st.realized_loss_n / st.valid : 0.0;
   double flat_rate = st.valid > 0 ? 100.0 * st.realized_flat_n / st.valid : 0.0;
   double avg_win = st.realized_win_n > 0 ? st.win_r_sum / st.realized_win_n : 0.0;
   double avg_loss = st.realized_loss_n > 0 ? st.loss_r_abs_sum / st.realized_loss_n : 0.0;
   double rr = DAL_M0005SafeDiv(avg_win, avg_loss);
   double pf = DAL_M0005SafeDiv(st.gross_win_r_sum, st.gross_loss_r_sum);
   double expectancy = st.valid > 0 ? st.net_r_sum / st.valid : 0.0;
   double be_win = (avg_win + avg_loss) > 0.0 ? 100.0 * avg_loss / (avg_win + avg_loss) : 0.0;
   return tag
      + "*regimeSource=" + DAL_M0005RegimeSourceToString(config.regime_source)
      + "*name=" + st.name
      + "*pathN=" + IntegerToString(st.valid)
      + "*realizedWinRatePct=" + DAL_M0001FmtPct(win_rate)
      + "*realizedLossRatePct=" + DAL_M0001FmtPct(loss_rate)
      + "*realizedFlatRatePct=" + DAL_M0001FmtPct(flat_rate)
      + "*avgWinR=" + DAL_M0001Fmt4(avg_win)
      + "*avgLossR=" + DAL_M0001Fmt4(avg_loss)
      + "*realizedRR=" + DAL_M0001Fmt4(rr)
      + "*realizedProfitFactor=" + DAL_M0001Fmt4(pf)
      + "*realizedExpectancyR=" + DAL_M0001Fmt4(expectancy)
      + "*medianNetR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.net_r_vals, 0.50))
      + "*p10NetR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.net_r_vals, 0.10))
      + "*p90NetR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.net_r_vals, 0.90))
      + "*breakEvenWinRatePct=" + DAL_M0001FmtPct(be_win)
      + "*grossWinR=" + DAL_M0001Fmt4(st.gross_win_r_sum)
      + "*grossLossR=" + DAL_M0001Fmt4(st.gross_loss_r_sum);
}

string DAL_M0005PathFloatingRText(const string tag, const DALM0005Config &config, const DALM0005PathStats &st)
{
   double mean_mfe_r = st.valid > 0 ? st.mfe_r_sum / st.valid : 0.0;
   double mean_mae_r = st.valid > 0 ? st.mae_r_sum / st.valid : 0.0;
   double float_rr = DAL_M0005SafeDiv(st.mfe_r_sum, st.mae_r_sum);
   return tag
      + "*regimeSource=" + DAL_M0005RegimeSourceToString(config.regime_source)
      + "*name=" + st.name
      + "*pathN=" + IntegerToString(st.valid)
      + "*floatHit1RPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.hit_mfe_1r_n / st.valid : 0.0)
      + "*floatHit2RPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.hit_mfe_2r_n / st.valid : 0.0)
      + "*floatHit3RPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.hit_mfe_3r_n / st.valid : 0.0)
      + "*meanMfeR=" + DAL_M0001Fmt4(mean_mfe_r)
      + "*medianMfeR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mfe_r_vals, 0.50))
      + "*p90MfeR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mfe_r_vals, 0.90))
      + "*p95MfeR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mfe_r_vals, 0.95))
      + "*meanMaeR=" + DAL_M0001Fmt4(mean_mae_r)
      + "*medianMaeR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mae_r_vals, 0.50))
      + "*p90MaeR=" + DAL_M0001Fmt4(DAL_M0004QuantileFromArray(st.mae_r_vals, 0.90))
      + "*floatingRR=" + DAL_M0001Fmt4(float_rr)
      + "*mfe1RBeforeMae1RPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.mfe1r_before_mae1r_n / st.valid : 0.0)
      + "*mae1RBeforeMfe1RPct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * st.mae1r_before_mfe1r_n / st.valid : 0.0)
      + "*firstHitREdgePct=" + DAL_M0001FmtPct(st.valid > 0 ? 100.0 * (st.mfe1r_before_mae1r_n - st.mae1r_before_mfe1r_n) / st.valid : 0.0);
}

string DAL_M0005PathRandomPerformanceText(const string tag, const DALM0005Config &config, const DALM0005PathStats &st)
{
   double actual_pf = DAL_M0005SafeDiv(st.gross_win_r_sum, st.gross_loss_r_sum);
   double random_pf = DAL_M0005SafeDiv(st.random_gross_win_r_sum, st.random_gross_loss_r_sum);
   double actual_win = st.valid > 0 ? 100.0 * st.realized_win_n / st.valid : 0.0;
   double random_win = st.valid > 0 ? 100.0 * st.random_win_n / st.valid : 0.0;
   double actual_exp = st.valid > 0 ? st.net_r_sum / st.valid : 0.0;
   double random_exp = st.valid > 0 ? st.random_net_r_sum / st.valid : 0.0;
   double actual_mfe_r = st.valid > 0 ? st.mfe_r_sum / st.valid : 0.0;
   double random_mfe_r = st.valid > 0 ? st.random_mfe_r_sum / st.valid : 0.0;
   double actual_float_rr = DAL_M0005SafeDiv(st.mfe_r_sum, st.mae_r_sum);
   double random_float_rr = DAL_M0005SafeDiv(st.random_mfe_r_sum, st.random_mae_r_sum);
   double actual_hit1r = st.valid > 0 ? 100.0 * st.hit_mfe_1r_n / st.valid : 0.0;
   double random_hit1r = st.valid > 0 ? 100.0 * st.random_hit_mfe_1r_n / st.valid : 0.0;
   return tag
      + "*regimeSource=" + DAL_M0005RegimeSourceToString(config.regime_source)
      + "*name=" + st.name
      + "*pathN=" + IntegerToString(st.valid)
      + "*randomDesign=matched_entry_same_duration_same_direction_same_actual_R_scale"
      + "*actualWinRatePct=" + DAL_M0001FmtPct(actual_win)
      + "*randomWinRatePct=" + DAL_M0001FmtPct(random_win)
      + "*actualMinusRandomWinRatePct=" + DAL_M0001FmtPct(actual_win - random_win)
      + "*actualProfitFactor=" + DAL_M0001Fmt4(actual_pf)
      + "*randomProfitFactor=" + DAL_M0001Fmt4(random_pf)
      + "*actualMinusRandomPF=" + DAL_M0001Fmt4(actual_pf - random_pf)
      + "*actualExpectancyR=" + DAL_M0001Fmt4(actual_exp)
      + "*randomExpectancyR=" + DAL_M0001Fmt4(random_exp)
      + "*actualMinusRandomExpectancyR=" + DAL_M0001Fmt4(actual_exp - random_exp)
      + "*actualMeanMfeR=" + DAL_M0001Fmt4(actual_mfe_r)
      + "*randomMeanMfeR=" + DAL_M0001Fmt4(random_mfe_r)
      + "*actualMinusRandomMfeR=" + DAL_M0001Fmt4(actual_mfe_r - random_mfe_r)
      + "*actualFloatingRR=" + DAL_M0001Fmt4(actual_float_rr)
      + "*randomFloatingRR=" + DAL_M0001Fmt4(random_float_rr)
      + "*actualMinusRandomFloatingRR=" + DAL_M0001Fmt4(actual_float_rr - random_float_rr)
      + "*actualHit1RPct=" + DAL_M0001FmtPct(actual_hit1r)
      + "*randomHit1RPct=" + DAL_M0001FmtPct(random_hit1r)
      + "*actualMinusRandomHit1RPct=" + DAL_M0001FmtPct(actual_hit1r - random_hit1r);
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
   int attempted_n = 0;
   int no_regime_n = 0;
   int no_entry_n = 0;
   int no_destination_n = 0;
   int reversal_attempts = 0;
   int continuation_attempts = 0;
   DAL_M0005BuildPaths(all_samples, count, bars, bars_count, labels, h5_config, min_random_start, all_paths, rev_paths, cont_paths, attempted_n, no_regime_n, no_entry_n, no_destination_n, reversal_attempts, continuation_attempts);

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
      "*attemptedN=", attempted_n,
      "*noRegimeN=", no_regime_n,
      "*noEntryN=", no_entry_n,
      "*noDestinationN=", no_destination_n,
      "*validPathPctOfAttempted=", DAL_M0001FmtPct(attempted_n > 0 ? 100.0 * all_stats.valid / attempted_n : 0.0),
      "*reversalAttemptN=", reversal_attempts,
      "*continuationAttemptN=", continuation_attempts,
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

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_BUILD_COVERAGE", symbol, timeframe, source_mode, events_count, min_entry_time),
      "PATH_BUILD_COVERAGE*regimeSource=", DAL_M0005RegimeSourceToString(h5_config.regime_source),
      "*evaluated=", MathMax(0, count - 1),
      "*attemptedN=", attempted_n,
      "*validPathN=", all_stats.valid,
      "*noRegimeN=", no_regime_n,
      "*noEntryN=", no_entry_n,
      "*noDestinationN=", no_destination_n,
      "*validPathPctOfEvaluated=", DAL_M0001FmtPct(MathMax(0, count - 1) > 0 ? 100.0 * all_stats.valid / MathMax(0, count - 1) : 0.0),
      "*validPathPctOfAttempted=", DAL_M0001FmtPct(attempted_n > 0 ? 100.0 * all_stats.valid / attempted_n : 0.0),
      "*noEntryPctOfAttempted=", DAL_M0001FmtPct(attempted_n > 0 ? 100.0 * no_entry_n / attempted_n : 0.0),
      "*noDestinationPctOfAttempted=", DAL_M0001FmtPct(attempted_n > 0 ? 100.0 * no_destination_n / attempted_n : 0.0));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_OUTCOME_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathOutcomeText("PATH_OUTCOME", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_OUTCOME_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathOutcomeText("PATH_OUTCOME", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_OUTCOME_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathOutcomeText("PATH_OUTCOME", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_EXCURSION_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathExcursionText("PATH_MFE_MAE", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_EXCURSION_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathExcursionText("PATH_MFE_MAE", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_EXCURSION_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathExcursionText("PATH_MFE_MAE", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_STOP_RISK_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathStopRiskText("PATH_STOP_RISK", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_STOP_RISK_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathStopRiskText("PATH_STOP_RISK", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_STOP_RISK_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathStopRiskText("PATH_STOP_RISK", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_RISK_REWARD_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathRiskRewardText("PATH_RISK_REWARD", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_RISK_REWARD_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathRiskRewardText("PATH_RISK_REWARD", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_RISK_REWARD_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathRiskRewardText("PATH_RISK_REWARD", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_REALIZED_R_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathRealizedRText("PATH_REALIZED_R", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_REALIZED_R_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathRealizedRText("PATH_REALIZED_R", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_REALIZED_R_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathRealizedRText("PATH_REALIZED_R", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_FLOATING_R_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathFloatingRText("PATH_FLOATING_R", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_FLOATING_R_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathFloatingRText("PATH_FLOATING_R", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_FLOATING_R_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathFloatingRText("PATH_FLOATING_R", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_RANDOM_PERFORMANCE_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathRandomPerformanceText("PATH_RANDOM_PERFORMANCE", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_RANDOM_PERFORMANCE_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathRandomPerformanceText("PATH_RANDOM_PERFORMANCE", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_RANDOM_PERFORMANCE_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathRandomPerformanceText("PATH_RANDOM_PERFORMANCE", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_STRESS_ALL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathStressText("PATH_RANDOM_STRESS", h5_config, all_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_STRESS_REVERSAL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathStressText("PATH_RANDOM_STRESS", h5_config, rev_stats));
   Print(DAL_M0005Prefix("DAL_M0005_FINAL_STRESS_CONTINUATION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathStressText("PATH_RANDOM_STRESS", h5_config, cont_stats));

   Print(DAL_M0005Prefix("DAL_M0005_FINAL_REV_CONT_COMPARE", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0005PathCompareText("PATH_BRANCH_COMPARE", h5_config, all_stats, rev_stats, cont_stats));
}

#endif
