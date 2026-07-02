#ifndef __FP_PAPER_BROKER_LIFECYCLE_RULES_MQH__
#define __FP_PAPER_BROKER_LIFECYCLE_RULES_MQH__
#property strict

#include "FP_PaperBrokerLifecycleTypes.mqh"
#include "FP_PaperBrokerAdapterRules.mqh"

string FP_L30Bool(const bool v){ return (v ? "true" : "false"); }
string FP_L30Time(const datetime t){ if(t <= 0) return ""; return TimeToString(t, TIME_DATE|TIME_SECONDS); }
string FP_L30SafeCsv(string v){ StringReplace(v, "\"", "\"\""); return "\"" + v + "\""; }
string FP_L30TfLabel(const ENUM_TIMEFRAMES tf){ return EnumToString(tf); }

string g_fp_l30_last_lifecycle_key = "";
int g_fp_l30_lifecycle_sequence = 0;

double FP_L30AbsDouble(const double v)
{
   if(v < 0.0) return -v;
   return v;
}

bool FP_L30IsBullishDirection(const string direction)
{
   return (direction == "DIRECTION_BULLISH");
}

bool FP_L30IsBearishDirection(const string direction)
{
   return (direction == "DIRECTION_BEARISH");
}

bool FP_L30CloseTouchesEntry(const string direction,const double close_price,const double entry_price)
{
   if(FP_L30IsBullishDirection(direction)) return close_price <= entry_price;
   if(FP_L30IsBearishDirection(direction)) return close_price >= entry_price;
   return false;
}

bool FP_L30CloseHitsTarget(const string direction,const double close_price,const double target_price)
{
   if(FP_L30IsBullishDirection(direction)) return close_price >= target_price;
   if(FP_L30IsBearishDirection(direction)) return close_price <= target_price;
   return false;
}

bool FP_L30CloseHitsStop(const string direction,const double close_price,const double stop_price)
{
   if(FP_L30IsBullishDirection(direction)) return close_price <= stop_price;
   if(FP_L30IsBearishDirection(direction)) return close_price >= stop_price;
   return false;
}

int FP_L30FindFirstBarAtOrAfter(const MqlRates &rates[],const int bars,const datetime t)
{
   if(bars <= 0)
      return -1;

   if(t <= 0)
      return bars - 1;

   for(int i=0; i<bars; i++)
   {
      if(rates[i].time >= t)
         return i;
   }

   return bars - 1;
}

string FP_L30BuildLifecycleId(const FP_Level29PaperBrokerAdapterRow &adapter)
{
   string id = "PBL";
   id += "_" + adapter.symbol;
   id += "_" + adapter.period_label;
   id += "_" + adapter.virtual_ticket;
   id += "_" + adapter.request_id;
   return id;
}

string FP_L30FirstBlockReason(const FP_Level30PaperBrokerLifecycleConfig &cfg,
                              const FP_Level30PaperBrokerLifecycleRow &row)
{
   if(!cfg.close_only)
      return "BLOCK_LIFECYCLE_CLOSE_ONLY_FALSE";
   if(cfg.require_adapter_registered && !row.adapter_registered)
      return "BLOCK_LIFECYCLE_ADAPTER_NOT_REGISTERED";
   if(cfg.require_zero_volume && row.request_volume != 0.0)
      return "BLOCK_LIFECYCLE_VOLUME_NOT_ZERO";
   if(row.request_price <= 0.0)
      return "BLOCK_LIFECYCLE_ENTRY_PRICE_MISSING";
   if(row.request_sl <= 0.0)
      return "BLOCK_LIFECYCLE_SL_MISSING";
   if(row.request_tp <= 0.0)
      return "BLOCK_LIFECYCLE_TP_MISSING";
   if(!FP_L30IsBullishDirection(row.request_direction) && !FP_L30IsBearishDirection(row.request_direction))
      return "BLOCK_LIFECYCLE_DIRECTION_MISSING";
   return "none";
}

void FP_L30SeedFromAdapter(const FP_Level30PaperBrokerLifecycleConfig &cfg,
                           const FP_Level29PaperBrokerAdapterRow &adapter,
                           FP_Level30PaperBrokerLifecycleRow &row)
{
   FP_ResetLevel30PaperBrokerLifecycleRow(row);

   row.generated_at = TimeCurrent();
   row.symbol = adapter.symbol;
   row.period = adapter.period;
   row.period_label = adapter.period_label;
   row.attempted = cfg.enabled;

   row.virtual_ticket = adapter.virtual_ticket;
   row.adapter_status = adapter.adapter_status;
   row.adapter_registered = adapter.adapter_registered;
   row.adapter_block_reason = adapter.adapter_block_reason;

   row.request_id = adapter.request_id;
   row.request_key = adapter.request_key;
   row.request_order_type = adapter.request_order_type;
   row.request_direction = adapter.request_direction;
   row.request_volume = adapter.request_volume;
   row.request_price = adapter.request_price;
   row.request_sl = adapter.request_sl;
   row.request_tp = adapter.request_tp;

   row.expiry_bars = cfg.expiry_bars;
   if(row.expiry_bars <= 0)
      row.expiry_bars = 20;

   row.lifecycle_id = FP_L30BuildLifecycleId(adapter);
   row.seed_time = adapter.generated_at;

   row.risk_distance = FP_L30AbsDouble(row.request_price - row.request_sl);
   row.reward_distance = FP_L30AbsDouble(row.request_tp - row.request_price);
}

void FP_L30FinalizeR(FP_Level30PaperBrokerLifecycleRow &row)
{
   if(row.risk_distance > 0.0)
   {
      if(FP_L30IsBullishDirection(row.request_direction))
         row.realized_r_like = (row.exit_close - row.request_price) / row.risk_distance;
      else if(FP_L30IsBearishDirection(row.request_direction))
         row.realized_r_like = (row.request_price - row.exit_close) / row.risk_distance;
   }
}

void FP_L30EvaluateLifecycle(const FP_Level30PaperBrokerLifecycleConfig &cfg,
                             const MqlRates &rates[],
                             const int bars,
                             FP_Level30PaperBrokerLifecycleRow &row)
{
   string block = FP_L30FirstBlockReason(cfg, row);
   if(block != "none")
   {
      row.lifecycle_tracked = false;
      row.lifecycle_status = "PAPER_BROKER_LIFECYCLE_BLOCKED";
      row.lifecycle_block_reason = block;
      row.paper_order_state = "PAPER_BROKER_STATE_BLOCKED";
      row.paper_order_event = "PAPER_BROKER_EVENT_BLOCKED";
      row.entry_condition = "ENTRY_BLOCKED";
      row.exit_condition = "EXIT_BLOCKED";
      return;
   }

   if(bars <= 0)
   {
      row.lifecycle_tracked = false;
      row.lifecycle_status = "PAPER_BROKER_LIFECYCLE_BLOCKED_NO_BARS";
      row.lifecycle_block_reason = "no_rates_available";
      row.paper_order_state = "PAPER_BROKER_STATE_BLOCKED";
      row.paper_order_event = "PAPER_BROKER_EVENT_NO_BARS";
      return;
   }

   int seed_index = FP_L30FindFirstBarAtOrAfter(rates, bars, row.seed_time);
   row.seed_index = seed_index;
   row.lifecycle_tracked = true;
   row.lifecycle_status = "PAPER_BROKER_LIFECYCLE_REGISTERED_PENDING";
   row.lifecycle_block_reason = "none";
   row.paper_order_state = "PAPER_BROKER_STATE_PENDING";
   row.paper_order_event = "PAPER_BROKER_EVENT_REGISTERED";
   row.entry_condition = "WAITING_FOR_CLOSE_TOUCH_ENTRY";
   row.exit_condition = "WAITING_FOR_CLOSE_TARGET_OR_STOP";

   int last_index = bars - 1;
   int max_index = seed_index + row.expiry_bars;
   if(max_index > last_index)
      max_index = last_index;

   for(int i=seed_index; i<=max_index; i++)
   {
      double c = rates[i].close;
      if(FP_L30CloseTouchesEntry(row.request_direction, c, row.request_price))
      {
         row.entry_index = i;
         row.entry_time = rates[i].time;
         row.entry_close = c;
         row.bars_to_entry = i - seed_index;
         row.lifecycle_status = "PAPER_BROKER_LIFECYCLE_ENTERED_BY_CLOSE";
         row.paper_order_state = "PAPER_BROKER_STATE_ACTIVE";
         row.paper_order_event = "PAPER_BROKER_EVENT_ENTRY_BY_CLOSE";
         row.entry_condition = "ENTRY_BY_CLOSE_TOUCH";
         break;
      }
   }

   if(row.entry_index < 0)
   {
      row.bars_elapsed_total = last_index - seed_index;
      if(row.bars_elapsed_total >= row.expiry_bars)
      {
         row.lifecycle_status = "PAPER_BROKER_LIFECYCLE_EXPIRED_BEFORE_ENTRY";
         row.paper_order_state = "PAPER_BROKER_STATE_EXPIRED";
         row.paper_order_event = "PAPER_BROKER_EVENT_EXPIRED_BEFORE_ENTRY";
         row.exit_condition = "EXPIRED_BEFORE_ENTRY";
      }
      return;
   }

   row.best_close = row.entry_close;
   row.worst_close = row.entry_close;

   for(int i=row.entry_index; i<=max_index; i++)
   {
      double c = rates[i].close;

      if(FP_L30IsBullishDirection(row.request_direction))
      {
         if(c > row.best_close) row.best_close = c;
         if(c < row.worst_close) row.worst_close = c;
      }
      else if(FP_L30IsBearishDirection(row.request_direction))
      {
         if(c < row.best_close) row.best_close = c;
         if(c > row.worst_close) row.worst_close = c;
      }

      bool hit_target = FP_L30CloseHitsTarget(row.request_direction, c, row.request_tp);
      bool hit_stop = FP_L30CloseHitsStop(row.request_direction, c, row.request_sl);

      if(hit_target && hit_stop)
      {
         row.exit_index = i;
         row.exit_time = rates[i].time;
         row.exit_close = c;
         row.lifecycle_status = "PAPER_BROKER_LIFECYCLE_AMBIGUOUS_TARGET_AND_STOP_SAME_CLOSE";
         row.paper_order_state = "PAPER_BROKER_STATE_CLOSED_AMBIGUOUS";
         row.paper_order_event = "PAPER_BROKER_EVENT_AMBIGUOUS_SAME_CLOSE";
         row.exit_condition = "AMBIGUOUS_TARGET_AND_STOP_SAME_CLOSE";
         break;
      }

      if(hit_target)
      {
         row.exit_index = i;
         row.exit_time = rates[i].time;
         row.exit_close = c;
         row.lifecycle_status = "PAPER_BROKER_LIFECYCLE_HIT_TARGET_BY_CLOSE";
         row.paper_order_state = "PAPER_BROKER_STATE_CLOSED_TARGET";
         row.paper_order_event = "PAPER_BROKER_EVENT_TARGET_BY_CLOSE";
         row.exit_condition = "TARGET_BY_CLOSE";
         break;
      }

      if(hit_stop)
      {
         row.exit_index = i;
         row.exit_time = rates[i].time;
         row.exit_close = c;
         row.lifecycle_status = "PAPER_BROKER_LIFECYCLE_HIT_STOP_BY_CLOSE";
         row.paper_order_state = "PAPER_BROKER_STATE_CLOSED_STOP";
         row.paper_order_event = "PAPER_BROKER_EVENT_STOP_BY_CLOSE";
         row.exit_condition = "STOP_BY_CLOSE";
         break;
      }
   }

   if(row.exit_index < 0)
   {
      row.bars_in_trade = last_index - row.entry_index;
      row.bars_elapsed_total = last_index - seed_index;

      if(row.bars_elapsed_total >= row.expiry_bars)
      {
         row.exit_index = max_index;
         row.exit_time = rates[max_index].time;
         row.exit_close = rates[max_index].close;
         row.lifecycle_status = "PAPER_BROKER_LIFECYCLE_EXPIRED_AFTER_ENTRY";
         row.paper_order_state = "PAPER_BROKER_STATE_EXPIRED";
         row.paper_order_event = "PAPER_BROKER_EVENT_EXPIRED_AFTER_ENTRY";
         row.exit_condition = "EXPIRED_AFTER_ENTRY";
      }
      else
      {
         row.exit_close = rates[last_index].close;
         row.lifecycle_status = "PAPER_BROKER_LIFECYCLE_ACTIVE_OPEN_CLOSE_ONLY";
         row.paper_order_state = "PAPER_BROKER_STATE_ACTIVE";
         row.paper_order_event = "PAPER_BROKER_EVENT_OPEN";
         row.exit_condition = "OPEN_WAITING_FOR_TARGET_OR_STOP";
      }
   }
   else
   {
      row.bars_in_trade = row.exit_index - row.entry_index;
      row.bars_elapsed_total = row.exit_index - seed_index;
   }

   if(FP_L30IsBullishDirection(row.request_direction))
   {
      row.mfe_close_distance = row.best_close - row.request_price;
      row.mae_close_distance = row.request_price - row.worst_close;
   }
   else if(FP_L30IsBearishDirection(row.request_direction))
   {
      row.mfe_close_distance = row.request_price - row.best_close;
      row.mae_close_distance = row.worst_close - row.request_price;
   }

   FP_L30FinalizeR(row);
}

void FP_L30FinalizeKey(const FP_Level30PaperBrokerLifecycleConfig &cfg,
                       FP_Level30PaperBrokerLifecycleRow &row)
{
   string dedupe_key = row.virtual_ticket;
   dedupe_key += "|STATUS=" + row.lifecycle_status;
   dedupe_key += "|ENTRY=" + FP_L30Time(row.entry_time);
   dedupe_key += "|EXIT=" + FP_L30Time(row.exit_time);
   dedupe_key += "|R=" + DoubleToString(row.realized_r_like, 4);

   if(cfg.skip_duplicate_lifecycle_key && dedupe_key == g_fp_l30_last_lifecycle_key)
   {
      row.duplicate_skipped = true;
      row.lifecycle_sequence = g_fp_l30_lifecycle_sequence;
   }
   else
   {
      g_fp_l30_last_lifecycle_key = dedupe_key;
      g_fp_l30_lifecycle_sequence++;
      row.duplicate_skipped = false;
      row.lifecycle_sequence = g_fp_l30_lifecycle_sequence;
   }

   row.lifecycle_key = row.symbol;
   row.lifecycle_key += "|TF=" + row.period_label;
   row.lifecycle_key += "|SEQ=" + IntegerToString(row.lifecycle_sequence);
   row.lifecycle_key += "|VT=" + row.virtual_ticket;
   row.lifecycle_key += "|STATUS=" + row.lifecycle_status;
   row.lifecycle_key += "|DUP=" + FP_L30Bool(row.duplicate_skipped);
   row.lifecycle_key += "|NO_SEND=true";
   row.lifecycle_key += "|EXEC=NO";
}

#endif // __FP_PAPER_BROKER_LIFECYCLE_RULES_MQH__
