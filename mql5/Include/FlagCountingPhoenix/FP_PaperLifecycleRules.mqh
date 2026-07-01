#ifndef __FP_PAPER_LIFECYCLE_RULES_MQH__
#define __FP_PAPER_LIFECYCLE_RULES_MQH__
#property strict

#include "FP_PaperLifecycleTypes.mqh"
#include "FP_PaperIntentRules.mqh"

string FP_L22Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L22Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L22SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L22TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

double FP_L22AbsDouble(const double value)
{
   if(value < 0.0) return -value;
   return value;
}

string FP_L22DirectionLabel(const int direction)
{
   if(direction == FP_DIR_BULLISH) return "DIRECTION_BULLISH";
   if(direction == FP_DIR_BEARISH) return "DIRECTION_BEARISH";
   return "DIRECTION_NONE";
}

bool FP_L22CloseTouchesEntry(const int direction,const double close_price,const double entry_price)
{
   if(direction == FP_DIR_BULLISH) return close_price <= entry_price;
   if(direction == FP_DIR_BEARISH) return close_price >= entry_price;
   return false;
}

bool FP_L22CloseHitsTarget(const int direction,const double close_price,const double target_price)
{
   if(direction == FP_DIR_BULLISH) return close_price >= target_price;
   if(direction == FP_DIR_BEARISH) return close_price <= target_price;
   return false;
}

bool FP_L22CloseHitsStop(const int direction,const double close_price,const double stop_price)
{
   if(direction == FP_DIR_BULLISH) return close_price <= stop_price;
   if(direction == FP_DIR_BEARISH) return close_price >= stop_price;
   return false;
}

int FP_L22FindFirstBarAtOrAfter(const MqlRates &rates[],const int bars,const datetime t)
{
   if(t <= 0 || bars <= 0)
      return -1;

   for(int i=0; i<bars; i++)
   {
      if(rates[i].time >= t)
         return i;
   }

   return -1;
}

string FP_L22BuildLifecycleId(const FP_Level21PaperIntentRow &intent)
{
   string id = "PLC";
   id += "_" + intent.symbol;
   id += "_" + intent.period_label;
   id += "_" + intent.intent_id;
   return id;
}

void FP_L22SeedFromIntent(const FP_Level22PaperLifecycleConfig &cfg,
                          const FP_Level21PaperIntentRow &intent,
                          FP_Level22PaperLifecycleRow &row)
{
   FP_ResetLevel22PaperLifecycleRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = intent.symbol;
   row.period = intent.period;
   row.period_label = intent.period_label;
   row.attempted = cfg.enabled;

   row.intent_id = intent.intent_id;
   row.intent_status = intent.intent_status;
   row.intent_allowed = intent.allowed;

   row.direction = intent.direction;
   row.direction_label = intent.direction_label;

   row.entry_price = intent.entry_price;
   row.stop_price = intent.stop_price;
   row.target_price = intent.target_price;
   row.risk_distance = intent.risk_distance;
   row.reward_distance = intent.reward_distance;
   row.rr_like = intent.rr_like;

   row.seed_time = intent.generated_at;
   row.expiry_bars = intent.expiry_bars;
   if(row.expiry_bars <= 0)
      row.expiry_bars = cfg.default_expiry_bars;

   row.lifecycle_id = FP_L22BuildLifecycleId(intent);
}

void FP_L22FinalizeMetrics(FP_Level22PaperLifecycleRow &row)
{
   if(row.risk_distance > 0.0)
   {
      if(row.direction == FP_DIR_BULLISH)
         row.realized_r_like = (row.exit_close - row.entry_price) / row.risk_distance;
      else if(row.direction == FP_DIR_BEARISH)
         row.realized_r_like = (row.entry_price - row.exit_close) / row.risk_distance;
   }

   row.lifecycle_key = row.symbol;
   row.lifecycle_key += "|TF=" + row.period_label;
   row.lifecycle_key += "|ID=" + row.lifecycle_id;
   row.lifecycle_key += "|STATUS=" + row.lifecycle_status;
   row.lifecycle_key += "|DIR=" + row.direction_label;
   row.lifecycle_key += "|R=" + DoubleToString(row.realized_r_like, 2);
   row.lifecycle_key += "|EXEC=NO";
}

void FP_L22EvaluateCloseOnlyLifecycle(const FP_Level22PaperLifecycleConfig &cfg,
                                      const MqlRates &rates[],
                                      const int bars,
                                      FP_Level22PaperLifecycleRow &row)
{
   if(cfg.require_intent_allowed && !row.intent_allowed)
   {
      row.tracked = false;
      row.lifecycle_status = "PAPER_LIFECYCLE_BLOCKED_INTENT_NOT_ALLOWED";
      row.block_reason = row.intent_status;
      row.close_only_path_status = "CLOSE_ONLY_PATH_BLOCKED";
      FP_L22FinalizeMetrics(row);
      return;
   }

   if(row.direction == FP_DIR_NONE)
   {
      row.lifecycle_status = "PAPER_LIFECYCLE_BLOCKED_NO_DIRECTION";
      row.block_reason = "direction_missing";
      row.close_only_path_status = "CLOSE_ONLY_PATH_BLOCKED";
      FP_L22FinalizeMetrics(row);
      return;
   }

   if(row.entry_price <= 0.0 || row.stop_price <= 0.0 || row.target_price <= 0.0)
   {
      row.lifecycle_status = "PAPER_LIFECYCLE_BLOCKED_MISSING_PRICE";
      row.block_reason = "entry_stop_or_target_missing";
      row.close_only_path_status = "CLOSE_ONLY_PATH_BLOCKED";
      FP_L22FinalizeMetrics(row);
      return;
   }

   if(bars <= 0)
   {
      row.lifecycle_status = "PAPER_LIFECYCLE_BLOCKED_NO_BARS";
      row.block_reason = "no_rates_available";
      row.close_only_path_status = "CLOSE_ONLY_PATH_BLOCKED";
      FP_L22FinalizeMetrics(row);
      return;
   }

   int seed_index = FP_L22FindFirstBarAtOrAfter(rates, bars, row.seed_time);
   if(seed_index < 0)
      seed_index = bars - 1;

   row.seed_index = seed_index;
   row.tracked = true;
   row.lifecycle_status = "PAPER_LIFECYCLE_PENDING";
   row.block_reason = "none";
   row.entry_condition = "WAITING_FOR_ENTRY_CLOSE_TOUCH";
   row.exit_condition = "WAITING_FOR_EXIT_CLOSE";
   row.close_only_path_status = "CLOSE_ONLY_PATH_ACTIVE";

   int last_index = bars - 1;
   int max_index = seed_index + row.expiry_bars;
   if(max_index > last_index)
      max_index = last_index;

   for(int i=seed_index; i<=max_index; i++)
   {
      double c = rates[i].close;
      if(FP_L22CloseTouchesEntry(row.direction, c, row.entry_price))
      {
         row.entry_index = i;
         row.entry_time = rates[i].time;
         row.entry_close = c;
         row.entry_condition = "ENTERED_BY_CLOSE_TOUCH";
         row.lifecycle_status = "PAPER_LIFECYCLE_ENTERED_BY_CLOSE";
         break;
      }
   }

   if(row.entry_index < 0)
   {
      row.bars_elapsed = last_index - seed_index;
      if(row.bars_elapsed >= row.expiry_bars)
      {
         row.lifecycle_status = "PAPER_LIFECYCLE_EXPIRED_BEFORE_ENTRY";
         row.exit_condition = "EXPIRED_BEFORE_ENTRY";
         row.close_only_path_status = "CLOSE_ONLY_PATH_EXPIRED";
      }
      FP_L22FinalizeMetrics(row);
      return;
   }

   row.best_close = row.entry_close;
   row.worst_close = row.entry_close;

   for(int i=row.entry_index; i<=max_index; i++)
   {
      double c = rates[i].close;

      if(row.direction == FP_DIR_BULLISH)
      {
         if(c > row.best_close) row.best_close = c;
         if(c < row.worst_close) row.worst_close = c;
      }
      else if(row.direction == FP_DIR_BEARISH)
      {
         if(c < row.best_close) row.best_close = c;
         if(c > row.worst_close) row.worst_close = c;
      }

      bool hit_target = FP_L22CloseHitsTarget(row.direction, c, row.target_price);
      bool hit_stop = FP_L22CloseHitsStop(row.direction, c, row.stop_price);

      if(hit_target && hit_stop)
      {
         row.exit_index = i;
         row.exit_time = rates[i].time;
         row.exit_close = c;
         row.lifecycle_status = "PAPER_LIFECYCLE_AMBIGUOUS_TARGET_AND_STOP_SAME_CLOSE";
         row.exit_condition = "AMBIGUOUS_TARGET_AND_STOP_SAME_CLOSE";
         row.ambiguity_status = "AMBIGUOUS_SAME_CLOSE";
         row.close_only_path_status = "CLOSE_ONLY_PATH_AMBIGUOUS";
         break;
      }

      if(hit_target)
      {
         row.exit_index = i;
         row.exit_time = rates[i].time;
         row.exit_close = c;
         row.lifecycle_status = "PAPER_LIFECYCLE_HIT_TARGET_BY_CLOSE";
         row.exit_condition = "TARGET_BY_CLOSE";
         row.close_only_path_status = "CLOSE_ONLY_PATH_RESOLVED_TARGET";
         break;
      }

      if(hit_stop)
      {
         row.exit_index = i;
         row.exit_time = rates[i].time;
         row.exit_close = c;
         row.lifecycle_status = "PAPER_LIFECYCLE_HIT_STOP_BY_CLOSE";
         row.exit_condition = "STOP_BY_CLOSE";
         row.close_only_path_status = "CLOSE_ONLY_PATH_RESOLVED_STOP";
         break;
      }
   }

   if(row.exit_index < 0)
   {
      row.bars_elapsed = last_index - row.entry_index;
      if(row.bars_elapsed >= row.expiry_bars)
      {
         row.exit_index = max_index;
         row.exit_time = rates[max_index].time;
         row.exit_close = rates[max_index].close;
         row.lifecycle_status = "PAPER_LIFECYCLE_EXPIRED_AFTER_ENTRY";
         row.exit_condition = "EXPIRED_AFTER_ENTRY";
         row.close_only_path_status = "CLOSE_ONLY_PATH_EXPIRED";
      }
      else
      {
         row.exit_close = rates[last_index].close;
         row.lifecycle_status = "PAPER_LIFECYCLE_OPEN_CLOSE_ONLY";
         row.exit_condition = "OPEN_WAITING_FOR_TARGET_OR_STOP";
         row.close_only_path_status = "CLOSE_ONLY_PATH_OPEN";
      }
   }
   else
   {
      row.bars_elapsed = row.exit_index - row.entry_index;
   }

   if(row.direction == FP_DIR_BULLISH)
   {
      row.mfe_close_distance = row.best_close - row.entry_price;
      row.mae_close_distance = row.entry_price - row.worst_close;
   }
   else if(row.direction == FP_DIR_BEARISH)
   {
      row.mfe_close_distance = row.entry_price - row.best_close;
      row.mae_close_distance = row.worst_close - row.entry_price;
   }

   FP_L22FinalizeMetrics(row);
}

#endif // __FP_PAPER_LIFECYCLE_RULES_MQH__
