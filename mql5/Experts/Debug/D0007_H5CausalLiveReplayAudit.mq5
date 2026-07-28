//+------------------------------------------------------------------+
//| Decision Alpha Lab — D0007 H5 Causal Live Replay Audit            |
//| Root live-valid H0005 validator: causal regime batches, no future  |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "D0007: H0005 causal live replay. Same-candle regime batches, prefix-only decisions, touch/break entries, post-fill measurement."

#include <Market/DAL_Bars.mqh>
#include <StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <M0001/DAL_M0001Config.mqh>
#include <M0001/DAL_M0001Engine.mqh>
#include <M0002/DAL_M0002Engine.mqh>
#include <M0005/DAL_M0005LiveCausal.mqh>
#include <AlphaLab/UC04/AL_UC04M0001Config.mqh>

#define DAL_D0007_BUILD "1.00"

enum ENUM_DALD0007Family
{
   DAL_D0007_BOTH = 0,
   DAL_D0007_REVERSAL_ONLY = 1,
   DAL_D0007_CONTINUATION_ONLY = 2
};

enum ENUM_DALD0007ContinuationBreakMode
{
   DAL_D0007_CONT_CLOSE_BREAK = 0,
   DAL_D0007_CONT_INTRABAR_BREAK = 1
};

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpReplayClosedBars = 1500;
input int InpWarmupClosedBars = 300;

input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

input ENUM_DALD0007Family InpFamiliesToAudit = DAL_D0007_BOTH;
input ENUM_DALD0007ContinuationBreakMode InpContinuationBreakMode = DAL_D0007_CONT_CLOSE_BREAK;
input bool InpUseCausalDirectionFilter = false;
input bool InpSkipAmbiguousEnergyBatch = true;
input bool InpSkipConsumedOrTouchedNodes = true;
input bool InpOneActivationPerNodeFamily = true;

input int InpReversalBuySlots = 3;
input int InpReversalSellSlots = 3;
input int InpContinuationBuySlots = 3;
input int InpContinuationSellSlots = 3;
input int InpMaxBarsToWaitForEntry = 300;
input int InpMaxBarsToMeasureAfterEntry = 300;
input double InpRewardR = 1.0;
input int InpAuditSpreadPoints = 0;
input bool InpSameBarStopFirst = true;

input int InpRegimeLookbackBars = 100;
input int InpOutcomeCandleOffsetAfterExit = 0;
input int InpBrokerUtcOffsetHours = 0;
input bool InpPrintOnlySummary = true;
input int InpPrintEveryNSteps = 100;
input bool InpWriteCsv = true;
input string InpCsvFileName = "D0007_H5_Causal_Live_Replay.csv";

struct D0007Candidate
{
   bool valid;
   string family;
   string key;
   DALLRuleNode node;
   int direction;
   double zone_lower;
   double zone_upper;
   double entry_hint_price;
   double stop_price;
   double distance_to_market;
   int regime_energy;
   int regime_direction;
   int regime_known_index;
   datetime regime_known_time;
   int regime_batch_count;
   int regime_rev_count;
   int regime_cont_count;
   bool regime_ambiguous_direction;
};

struct D0007TradeResult
{
   bool entered;
   bool measured;
   bool hit_reward_before_stop;
   bool hit_stop_before_reward;
   bool same_bar_reward_stop;
   datetime activation_time;
   datetime entry_time;
   datetime exit_time;
   int bars_to_entry;
   int bars_measured;
   double entry_price;
   double stop_price;
   double risk_price;
   double mfe_r;
   double mae_r;
   double realized_r;
   string outcome;
   string reason;
};

struct D0007Summary
{
   int steps;
   int load_failures;
   int decision_steps;
   int no_sample_steps;
   int ambiguous_energy_steps;
   int same_bar_batch_steps;
   int mixed_direction_steps;
   int reversal_regime_steps;
   int continuation_regime_steps;
   int candidates;
   int reversal_candidates;
   int continuation_candidates;
   int buy_candidates;
   int sell_candidates;
   int entered;
   int unfilled;
   int measured;
   int reward_hits;
   int stop_hits;
   int same_bar_reward_stop;
   int open_after_window;
   double sum_mfe_r;
   double sum_mae_r;
   double sum_realized_r;
   double gross_win_r;
   double gross_loss_r;
};

int g_csv = INVALID_HANDLE;
string g_keys[];
D0007Summary g_sum;

string D0007_Symbol()
{
   return (InpSymbol == "" ? _Symbol : InpSymbol);
}

ENUM_TIMEFRAMES D0007_Timeframe()
{
   return (InpTimeframe == PERIOD_CURRENT ? (ENUM_TIMEFRAMES)_Period : InpTimeframe);
}

string D0007_TimeText(const datetime t)
{
   if(t <= 0) return "0";
   return TimeToString(t, TIME_DATE | TIME_MINUTES | TIME_SECONDS);
}

string D0007_BoolText(const bool v)
{
   return (v ? "true" : "false");
}

string D0007_DirText(const int d)
{
   if(d > 0) return "BUY";
   if(d < 0) return "SELL";
   return "NONE";
}

void D0007_ResetSummary(D0007Summary &s)
{
   s.steps = 0;
   s.load_failures = 0;
   s.decision_steps = 0;
   s.no_sample_steps = 0;
   s.ambiguous_energy_steps = 0;
   s.same_bar_batch_steps = 0;
   s.mixed_direction_steps = 0;
   s.reversal_regime_steps = 0;
   s.continuation_regime_steps = 0;
   s.candidates = 0;
   s.reversal_candidates = 0;
   s.continuation_candidates = 0;
   s.buy_candidates = 0;
   s.sell_candidates = 0;
   s.entered = 0;
   s.unfilled = 0;
   s.measured = 0;
   s.reward_hits = 0;
   s.stop_hits = 0;
   s.same_bar_reward_stop = 0;
   s.open_after_window = 0;
   s.sum_mfe_r = 0.0;
   s.sum_mae_r = 0.0;
   s.sum_realized_r = 0.0;
   s.gross_win_r = 0.0;
   s.gross_loss_r = 0.0;
}

void D0007_ResetCandidate(D0007Candidate &c)
{
   c.valid = false;
   c.family = "";
   c.key = "";
   ZeroMemory(c.node);
   c.direction = 0;
   c.zone_lower = 0.0;
   c.zone_upper = 0.0;
   c.entry_hint_price = 0.0;
   c.stop_price = 0.0;
   c.distance_to_market = 0.0;
   c.regime_energy = DAL_H5_REGIME_UNKNOWN;
   c.regime_direction = 0;
   c.regime_known_index = -1;
   c.regime_known_time = 0;
   c.regime_batch_count = 0;
   c.regime_rev_count = 0;
   c.regime_cont_count = 0;
   c.regime_ambiguous_direction = false;
}

void D0007_ResetTradeResult(D0007TradeResult &r)
{
   r.entered = false;
   r.measured = false;
   r.hit_reward_before_stop = false;
   r.hit_stop_before_reward = false;
   r.same_bar_reward_stop = false;
   r.activation_time = 0;
   r.entry_time = 0;
   r.exit_time = 0;
   r.bars_to_entry = 0;
   r.bars_measured = 0;
   r.entry_price = 0.0;
   r.stop_price = 0.0;
   r.risk_price = 0.0;
   r.mfe_r = 0.0;
   r.mae_r = 0.0;
   r.realized_r = 0.0;
   r.outcome = "none";
   r.reason = "not_measured";
}

void D0007_BuildM0001Config(DALM0001Config &config)
{
   AL_UC04BuildM0001Config(
      config,
      InpL,
      InpZoneRatio,
      InpExitGap,
      InpConsumeMode
   );
}

void D0007_BuildM0002Config(DALM0002Config &config)
{
   DAL_M0002DefaultConfig(config);
   config.measure_mode = DAL_M0002_MEASURE_EVENT_RTV;
   config.outcome_candle_offset_after_exit = MathMax(0, InpOutcomeCandleOffsetAfterExit);
   config.post_outcome_sample_bars = 0;
   config.use_event_length_for_sample = false;
   config.random_samples_per_event = 1;
   config.bootstrap_iterations = 0;
   config.permutation_iterations = 0;
   config.validation_splits = 1;
   config.broker_utc_offset_hours = InpBrokerUtcOffsetHours;
   config.regime_lookback_bars = MathMax(1, InpRegimeLookbackBars);
   config.print_group_session_regime = false;
   config.run_stress_suite = false;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = (InpConsumeMode == DAL_M0001_CONSUME_BY_TOUCH);
}

void D0007_ReverseRates(MqlRates &rates[], const int count)
{
   int l = 0;
   int r = count - 1;
   while(l < r)
   {
      MqlRates tmp = rates[l];
      rates[l] = rates[r];
      rates[r] = tmp;
      l++;
      r--;
   }
}

bool D0007_RatesToBars(MqlRates &raw[], const int copied, DALBar &bars[])
{
   if(copied <= 0)
      return false;
   if(copied > 1 && raw[0].time > raw[copied - 1].time)
      D0007_ReverseRates(raw, copied);
   ArrayResize(bars, copied);
   for(int i = 0; i < copied; i++)
   {
      bars[i].time = raw[i].time;
      bars[i].open = raw[i].open;
      bars[i].high = raw[i].high;
      bars[i].low = raw[i].low;
      bars[i].close = raw[i].close;
      bars[i].tick_volume = raw[i].tick_volume;
      bars[i].spread = raw[i].spread;
   }
   return true;
}

bool D0007_LoadPrefixBars(const int oldest_closed_shift, const int cursor_closed_shift, DALBar &bars[], int &bars_count, string &reason)
{
   ArrayResize(bars, 0);
   bars_count = 0;
   reason = "not_loaded";
   if(oldest_closed_shift < cursor_closed_shift)
   {
      reason = "bad_shift_order";
      return false;
   }
   datetime start_time = iTime(D0007_Symbol(), D0007_Timeframe(), oldest_closed_shift);
   datetime stop_time = iTime(D0007_Symbol(), D0007_Timeframe(), cursor_closed_shift);
   if(start_time <= 0 || stop_time <= 0)
   {
      reason = "bad_itime";
      return false;
   }
   if(start_time > stop_time)
   {
      datetime t = start_time;
      start_time = stop_time;
      stop_time = t;
   }
   MqlRates raw[];
   int copied = CopyRates(D0007_Symbol(), D0007_Timeframe(), start_time, stop_time, raw);
   if(copied <= 0)
   {
      reason = "copy_prefix_failed*err=" + IntegerToString(GetLastError());
      return false;
   }
   if(!D0007_RatesToBars(raw, copied, bars))
   {
      reason = "rates_to_bars_failed";
      return false;
   }
   bars_count = copied;
   reason = "ok_prefix_only";
   return true;
}

bool D0007_LoadForwardBars(const int cursor_closed_shift, const int max_forward_bars, DALBar &bars[], int &bars_count, string &reason)
{
   ArrayResize(bars, 0);
   bars_count = 0;
   reason = "not_loaded";
   if(cursor_closed_shift <= 1)
   {
      reason = "no_future_closed_bars";
      return false;
   }
   int first_shift = cursor_closed_shift - 1;
   int latest_shift = MathMax(1, cursor_closed_shift - MathMax(1, max_forward_bars));
   datetime start_time = iTime(D0007_Symbol(), D0007_Timeframe(), first_shift);
   datetime stop_time = iTime(D0007_Symbol(), D0007_Timeframe(), latest_shift);
   if(start_time <= 0 || stop_time <= 0)
   {
      reason = "bad_future_itime";
      return false;
   }
   if(start_time > stop_time)
   {
      datetime t = start_time;
      start_time = stop_time;
      stop_time = t;
   }
   MqlRates raw[];
   int copied = CopyRates(D0007_Symbol(), D0007_Timeframe(), start_time, stop_time, raw);
   if(copied <= 0)
   {
      reason = "copy_forward_failed*err=" + IntegerToString(GetLastError());
      return false;
   }
   if(!D0007_RatesToBars(raw, copied, bars))
   {
      reason = "future_rates_to_bars_failed";
      return false;
   }
   bars_count = copied;
   reason = "ok_outcome_only";
   return true;
}

string D0007_NodeFamilyKey(const string family, const DALLRuleNode &node)
{
   return family + "_" + IntegerToString((int)node.type) + "_" + IntegerToString((long)node.time) + "_" + DoubleToString(node.price, 10);
}

bool D0007_KeyExists(const string key)
{
   for(int i = 0; i < ArraySize(g_keys); i++)
      if(g_keys[i] == key)
         return true;
   return false;
}

void D0007_AddKey(const string key)
{
   if(key == "" || D0007_KeyExists(key))
      return;
   int n = ArraySize(g_keys);
   ArrayResize(g_keys, n + 1);
   g_keys[n] = key;
}

bool D0007_BuildLiveTerritory(const DALBar &bars[], const int bars_count, const DALLRuleNode &node, double &extreme, double &lower, double &upper, bool &hunted)
{
   extreme = 0.0;
   lower = node.price;
   upper = node.price;
   hunted = false;
   if(bars_count <= 0 || node.active_from_index < 0 || node.active_from_index >= bars_count)
      return false;
   extreme = DAL_M0001InitialExtreme(node.type, bars[node.active_from_index]);
   for(int i = node.active_from_index; i < bars_count; i++)
   {
      extreme = DAL_M0001UpdateExtreme(node.type, extreme, bars[i]);
      DAL_M0001Territory(node.type, node.price, extreme, InpZoneRatio, lower, upper);
      if(DAL_M0001Hunted(node.type, node.price, bars[i]))
         hunted = true;
   }
   return true;
}

bool D0007_NodeTouchedOrConsumedBeforeDecision(const DALBar &bars[], const int bars_count, const DALLRuleNode &node)
{
   if(bars_count <= 0 || node.active_from_index < 0 || node.active_from_index >= bars_count)
      return true;
   double extreme = DAL_M0001InitialExtreme(node.type, bars[node.active_from_index]);
   for(int i = node.active_from_index; i < bars_count; i++)
   {
      extreme = DAL_M0001UpdateExtreme(node.type, extreme, bars[i]);
      double lower = node.price;
      double upper = node.price;
      DAL_M0001Territory(node.type, node.price, extreme, InpZoneRatio, lower, upper);
      bool touched = DAL_CandleIntersectsZone(bars[i].low, bars[i].high, lower, upper);
      bool hunted = DAL_M0001Hunted(node.type, node.price, bars[i]);
      if(touched || (hunted && !touched))
         return true;
   }
   return false;
}

bool D0007_NodeHasClosedEvent(const DALM0001Event &events[], const int events_count, const int node_id)
{
   for(int i = 0; i < events_count; i++)
      if(events[i].node_id == node_id)
         return true;
   return false;
}

bool D0007_CandidatePassesDirectionFilter(const int candidate_direction, const DALM0005CausalRegimeState &state)
{
   if(!InpUseCausalDirectionFilter)
      return true;
   if(state.direction == 0)
      return false;
   return (candidate_direction == state.direction);
}

bool D0007_AddCandidateToSlots(D0007Candidate &slots[], int &slot_count, const int max_slots, const D0007Candidate &c)
{
   if(!c.valid || max_slots <= 0)
      return false;
   if(slot_count < max_slots)
   {
      ArrayResize(slots, slot_count + 1);
      slots[slot_count] = c;
      slot_count++;
      return true;
   }
   int worst = -1;
   double worst_dist = -1.0;
   for(int i = 0; i < slot_count; i++)
   {
      if(worst < 0 || slots[i].distance_to_market > worst_dist)
      {
         worst = i;
         worst_dist = slots[i].distance_to_market;
      }
   }
   if(worst >= 0 && c.distance_to_market < worst_dist)
   {
      slots[worst] = c;
      return true;
   }
   return false;
}

bool D0007_BuildCandidate(
   const string family,
   const DALBar &bars[],
   const int bars_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALLRuleNode &node,
   const DALM0005CausalRegimeState &state,
   const double spread_price,
   D0007Candidate &c,
   string &reason
)
{
   D0007_ResetCandidate(c);
   reason = "not_candidate";
   int last_index = bars_count - 1;
   if(!node.confirmed || node.active_from_index < 0 || node.active_from_index > last_index)
   {
      reason = "node_not_live_confirmed";
      return false;
   }
   if(InpSkipConsumedOrTouchedNodes)
   {
      if(D0007_NodeHasClosedEvent(events, events_count, node.id))
      {
         reason = "node_has_closed_event";
         return false;
      }
      if(D0007_NodeTouchedOrConsumedBeforeDecision(bars, bars_count, node))
      {
         reason = "node_already_touched_or_consumed_in_prefix";
         return false;
      }
   }

   double extreme = 0.0;
   double lower = node.price;
   double upper = node.price;
   bool hunted = false;
   if(!D0007_BuildLiveTerritory(bars, bars_count, node, extreme, lower, upper, hunted))
   {
      reason = "territory_failed";
      return false;
   }

   double market = bars[last_index].close;
   int dir = 0;
   double entry_hint = 0.0;
   double stop = 0.0;
   double dist = 0.0;

   if(family == "REV")
   {
      if(node.type == DAL_NODE_LOW)
      {
         if(!(upper < market)) { reason = "rev_buy_zone_not_below_market"; return false; }
         dir = +1;
         entry_hint = upper + spread_price;
         stop = lower;
         dist = market - upper;
      }
      else
      {
         if(!(lower > market)) { reason = "rev_sell_zone_not_above_market"; return false; }
         dir = -1;
         entry_hint = lower;
         stop = upper + spread_price;
         dist = lower - market;
      }
   }
   else if(family == "CONT")
   {
      if(node.type == DAL_NODE_HIGH)
      {
         if(!(upper > market)) { reason = "cont_buy_break_zone_not_above_market"; return false; }
         dir = +1;
         entry_hint = 0.0;
         stop = lower;
         dist = upper - market;
      }
      else
      {
         if(!(lower < market)) { reason = "cont_sell_break_zone_not_below_market"; return false; }
         dir = -1;
         entry_hint = 0.0;
         stop = upper + spread_price;
         dist = market - lower;
      }
   }
   else
   {
      reason = "unknown_family";
      return false;
   }

   if(!D0007_CandidatePassesDirectionFilter(dir, state))
   {
      reason = "causal_direction_filter_rejected";
      return false;
   }

   string key = D0007_NodeFamilyKey(family, node);
   if(InpOneActivationPerNodeFamily && D0007_KeyExists(key))
   {
      reason = "already_activated_node_family";
      return false;
   }

   c.valid = true;
   c.family = family;
   c.key = key;
   c.node = node;
   c.direction = dir;
   c.zone_lower = lower;
   c.zone_upper = upper;
   c.entry_hint_price = entry_hint;
   c.stop_price = stop;
   c.distance_to_market = MathMax(0.0, dist);
   c.regime_energy = state.energy;
   c.regime_direction = state.direction;
   c.regime_known_index = state.known_index;
   c.regime_known_time = state.known_time;
   c.regime_batch_count = state.batch_count;
   c.regime_rev_count = state.reversal_count;
   c.regime_cont_count = state.continuation_count;
   c.regime_ambiguous_direction = state.ambiguous_direction;
   reason = "ok";
   return true;
}

void D0007_SelectCandidates(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALM0005CausalRegimeState &state,
   D0007Candidate &out_candidates[],
   int &out_count
)
{
   ArrayResize(out_candidates, 0);
   out_count = 0;

   double point = SymbolInfoDouble(D0007_Symbol(), SYMBOL_POINT);
   if(point <= 0.0) point = 0.0;
   double spread_price = MathMax(0, InpAuditSpreadPoints) * point;

   D0007Candidate rev_buy[];
   D0007Candidate rev_sell[];
   D0007Candidate cont_buy[];
   D0007Candidate cont_sell[];
   int rb = 0, rs = 0, cb = 0, cs = 0;

   for(int i = 0; i < nodes_count; i++)
   {
      if((InpFamiliesToAudit == DAL_D0007_BOTH || InpFamiliesToAudit == DAL_D0007_REVERSAL_ONLY) && state.energy == DAL_H5_REGIME_REVERSAL)
      {
         D0007Candidate c;
         string reason = "";
         if(D0007_BuildCandidate("REV", bars, bars_count, events, events_count, nodes[i], state, spread_price, c, reason))
         {
            if(c.direction > 0)
               D0007_AddCandidateToSlots(rev_buy, rb, MathMax(0, InpReversalBuySlots), c);
            else if(c.direction < 0)
               D0007_AddCandidateToSlots(rev_sell, rs, MathMax(0, InpReversalSellSlots), c);
         }
      }

      if((InpFamiliesToAudit == DAL_D0007_BOTH || InpFamiliesToAudit == DAL_D0007_CONTINUATION_ONLY) && state.energy == DAL_H5_REGIME_CONTINUATION)
      {
         D0007Candidate c2;
         string reason2 = "";
         if(D0007_BuildCandidate("CONT", bars, bars_count, events, events_count, nodes[i], state, spread_price, c2, reason2))
         {
            if(c2.direction > 0)
               D0007_AddCandidateToSlots(cont_buy, cb, MathMax(0, InpContinuationBuySlots), c2);
            else if(c2.direction < 0)
               D0007_AddCandidateToSlots(cont_sell, cs, MathMax(0, InpContinuationSellSlots), c2);
         }
      }
   }

   int total = rb + rs + cb + cs;
   ArrayResize(out_candidates, total);
   int k = 0;
   for(int a = 0; a < rb; a++) { out_candidates[k] = rev_buy[a]; k++; }
   for(int b = 0; b < rs; b++) { out_candidates[k] = rev_sell[b]; k++; }
   for(int c = 0; c < cb; c++) { out_candidates[k] = cont_buy[c]; k++; }
   for(int d = 0; d < cs; d++) { out_candidates[k] = cont_sell[d]; k++; }
   out_count = total;
}

bool D0007_EntryTriggeredOnBar(const D0007Candidate &c, const DALBar &bar)
{
   if(c.family == "REV")
   {
      return DAL_CandleIntersectsZone(bar.low, bar.high, c.zone_lower, c.zone_upper);
   }

   if(c.family == "CONT")
   {
      if(c.direction > 0)
      {
         if(InpContinuationBreakMode == DAL_D0007_CONT_CLOSE_BREAK)
            return bar.close > c.zone_upper;
         return bar.high > c.zone_upper;
      }
      if(c.direction < 0)
      {
         if(InpContinuationBreakMode == DAL_D0007_CONT_CLOSE_BREAK)
            return bar.close < c.zone_lower;
         return bar.low < c.zone_lower;
      }
   }
   return false;
}

double D0007_EntryPriceForTriggeredBar(const D0007Candidate &c, const DALBar &bar, const double spread_price)
{
   if(c.family == "REV")
      return c.entry_hint_price;

   if(c.direction > 0)
   {
      if(InpContinuationBreakMode == DAL_D0007_CONT_CLOSE_BREAK)
         return bar.close + spread_price;
      return c.zone_upper + spread_price;
   }

   if(c.direction < 0)
   {
      if(InpContinuationBreakMode == DAL_D0007_CONT_CLOSE_BREAK)
         return bar.close;
      return c.zone_lower;
   }

   return bar.close;
}

void D0007_MeasureFromEntryIndex(const D0007Candidate &c, const DALBar &bars[], const int bars_count, const int entry_index, const double entry_price, D0007TradeResult &r)
{
   if(entry_index < 0 || entry_index >= bars_count)
   {
      r.reason = "bad_entry_index";
      return;
   }

   double stop = c.stop_price;
   double risk = MathAbs(entry_price - stop);
   if(risk <= 0.0)
   {
      r.reason = "invalid_risk";
      return;
   }

   double reward_r = MathMax(0.1, InpRewardR);
   double target = (c.direction > 0 ? entry_price + reward_r * risk : entry_price - reward_r * risk);
   int max_measure = MathMax(1, InpMaxBarsToMeasureAfterEntry);
   int last = MathMin(bars_count - 1, entry_index + max_measure - 1);
   double mfe = 0.0;
   double mae = 0.0;
   bool decided = false;

   r.entry_price = entry_price;
   r.stop_price = stop;
   r.risk_price = risk;

   for(int i = entry_index; i <= last; i++)
   {
      double favorable = 0.0;
      double adverse = 0.0;
      bool reward = false;
      bool stop_hit = false;
      if(c.direction > 0)
      {
         favorable = bars[i].high - entry_price;
         adverse = entry_price - bars[i].low;
         reward = bars[i].high >= target;
         stop_hit = bars[i].low <= stop;
      }
      else
      {
         favorable = entry_price - bars[i].low;
         adverse = bars[i].high - entry_price;
         reward = bars[i].low <= target;
         stop_hit = bars[i].high >= stop;
      }
      if(favorable > mfe) mfe = favorable;
      if(adverse > mae) mae = adverse;

      if(!decided && reward && stop_hit)
      {
         r.same_bar_reward_stop = true;
         if(InpSameBarStopFirst)
         {
            r.hit_stop_before_reward = true;
            r.realized_r = -1.0;
            r.outcome = "same_bar_stop_first";
         }
         else
         {
            r.hit_reward_before_stop = true;
            r.realized_r = reward_r;
            r.outcome = "same_bar_reward_first";
         }
         r.exit_time = bars[i].time;
         decided = true;
      }
      else if(!decided && stop_hit)
      {
         r.hit_stop_before_reward = true;
         r.realized_r = -1.0;
         r.outcome = "stop_before_reward";
         r.exit_time = bars[i].time;
         decided = true;
      }
      else if(!decided && reward)
      {
         r.hit_reward_before_stop = true;
         r.realized_r = reward_r;
         r.outcome = "reward_before_stop";
         r.exit_time = bars[i].time;
         decided = true;
      }
   }

   if(!decided)
   {
      double close_r = 0.0;
      if(c.direction > 0)
         close_r = (bars[last].close - entry_price) / risk;
      else
         close_r = (entry_price - bars[last].close) / risk;
      r.realized_r = close_r;
      r.outcome = "open_after_measure_window";
      r.exit_time = bars[last].time;
   }

   r.mfe_r = mfe / risk;
   r.mae_r = mae / risk;
   r.bars_measured = last - entry_index + 1;
   r.measured = true;
   r.reason = "measured_post_entry_only";
}

void D0007_ReplayCandidate(const D0007Candidate &c, const int cursor_shift, const datetime activation_time, D0007TradeResult &r)
{
   D0007_ResetTradeResult(r);
   r.activation_time = activation_time;

   int max_forward = MathMax(1, InpMaxBarsToWaitForEntry) + MathMax(1, InpMaxBarsToMeasureAfterEntry) + 2;
   DALBar future[];
   int future_count = 0;
   string load_reason = "";
   if(!D0007_LoadForwardBars(cursor_shift, max_forward, future, future_count, load_reason))
   {
      r.reason = load_reason;
      r.outcome = "no_forward_bars";
      return;
   }

   int max_wait = MathMin(future_count, MathMax(1, InpMaxBarsToWaitForEntry));
   int entry_i = -1;
   for(int i = 0; i < max_wait; i++)
   {
      if(D0007_EntryTriggeredOnBar(c, future[i]))
      {
         entry_i = i;
         break;
      }
   }

   if(entry_i < 0)
   {
      r.entered = false;
      r.bars_to_entry = max_wait;
      r.outcome = "unfilled";
      r.reason = "entry_not_triggered_in_wait_window";
      return;
   }

   double point = SymbolInfoDouble(D0007_Symbol(), SYMBOL_POINT);
   if(point <= 0.0) point = 0.0;
   double spread_price = MathMax(0, InpAuditSpreadPoints) * point;
   double entry_price = D0007_EntryPriceForTriggeredBar(c, future[entry_i], spread_price);

   r.entered = true;
   r.entry_time = future[entry_i].time;
   r.bars_to_entry = entry_i + 1;
   r.outcome = "entered";
   r.reason = "entry_triggered_after_causal_activation";
   D0007_MeasureFromEntryIndex(c, future, future_count, entry_i, entry_price, r);
}

void D0007_OpenCsv()
{
   if(!InpWriteCsv || g_csv != INVALID_HANDLE)
      return;
   g_csv = FileOpen(InpCsvFileName, FILE_WRITE | FILE_CSV | FILE_ANSI);
   if(g_csv == INVALID_HANDLE)
   {
      Print("DAL_D0007_CSV_OPEN_FAILED *** build=", DAL_D0007_BUILD, "*file=", InpCsvFileName, "*err=", GetLastError());
      return;
   }
   FileWrite(g_csv,
      "activation_time", "family", "energy", "regime_direction", "known_time", "known_index", "batch_count", "rev_count", "cont_count", "ambiguous_direction",
      "node_id", "node_type", "direction", "zone_lower", "zone_upper", "entry_price", "stop_price", "risk_price",
      "entered", "entry_time", "bars_to_entry", "measured", "bars_measured", "mfe_r", "mae_r", "realized_r", "reward_hit", "stop_hit", "same_bar", "outcome", "reason");
}

void D0007_WriteCsv(const D0007Candidate &c, const D0007TradeResult &r)
{
   if(!InpWriteCsv)
      return;
   D0007_OpenCsv();
   if(g_csv == INVALID_HANDLE)
      return;
   FileWrite(g_csv,
      D0007_TimeText(r.activation_time), c.family, DAL_M0005CausalEnergyToString(c.regime_energy), D0007_DirText(c.regime_direction), D0007_TimeText(c.regime_known_time), c.regime_known_index, c.regime_batch_count, c.regime_rev_count, c.regime_cont_count, D0007_BoolText(c.regime_ambiguous_direction),
      c.node.id, EnumToString(c.node.type), D0007_DirText(c.direction), DoubleToString(c.zone_lower, 10), DoubleToString(c.zone_upper, 10), DoubleToString(r.entry_price, 10), DoubleToString(r.stop_price, 10), DoubleToString(r.risk_price, 10),
      D0007_BoolText(r.entered), D0007_TimeText(r.entry_time), r.bars_to_entry, D0007_BoolText(r.measured), r.bars_measured, DoubleToString(r.mfe_r, 6), DoubleToString(r.mae_r, 6), DoubleToString(r.realized_r, 6), D0007_BoolText(r.hit_reward_before_stop), D0007_BoolText(r.hit_stop_before_reward), D0007_BoolText(r.same_bar_reward_stop), r.outcome, r.reason);
}

void D0007_Accumulate(const D0007Candidate &c, const D0007TradeResult &r)
{
   g_sum.candidates++;
   if(c.family == "REV") g_sum.reversal_candidates++;
   if(c.family == "CONT") g_sum.continuation_candidates++;
   if(c.direction > 0) g_sum.buy_candidates++;
   if(c.direction < 0) g_sum.sell_candidates++;

   if(r.entered) g_sum.entered++; else g_sum.unfilled++;
   if(r.measured)
   {
      g_sum.measured++;
      g_sum.sum_mfe_r += r.mfe_r;
      g_sum.sum_mae_r += r.mae_r;
      g_sum.sum_realized_r += r.realized_r;
      if(r.realized_r > 0.0) g_sum.gross_win_r += r.realized_r;
      if(r.realized_r < 0.0) g_sum.gross_loss_r += MathAbs(r.realized_r);
   }
   if(r.hit_reward_before_stop) g_sum.reward_hits++;
   if(r.hit_stop_before_reward) g_sum.stop_hits++;
   if(r.same_bar_reward_stop) g_sum.same_bar_reward_stop++;
   if(r.outcome == "open_after_measure_window") g_sum.open_after_window++;
}

void D0007_PrintCandidateResult(const int step, const D0007Candidate &c, const D0007TradeResult &r)
{
   Print("DAL_D0007_TRADE *** build=", DAL_D0007_BUILD,
      "*step=", step,
      "*family=", c.family,
      "*energy=", DAL_M0005CausalEnergyToString(c.regime_energy),
      "*known=", D0007_TimeText(c.regime_known_time),
      "*batch=", c.regime_batch_count,
      "*ambigDir=", D0007_BoolText(c.regime_ambiguous_direction),
      "*nodeId=", c.node.id,
      "*nodeType=", EnumToString(c.node.type),
      "*dir=", D0007_DirText(c.direction),
      "*entered=", D0007_BoolText(r.entered),
      "*entryTime=", D0007_TimeText(r.entry_time),
      "*mfeR=", DoubleToString(r.mfe_r, 4),
      "*maeR=", DoubleToString(r.mae_r, 4),
      "*realizedR=", DoubleToString(r.realized_r, 4),
      "*outcome=", r.outcome,
      "*reason=", r.reason);
}

bool D0007_Run()
{
   D0007_ResetSummary(g_sum);
   ArrayResize(g_keys, 0);
   D0007_OpenCsv();

   int total = Bars(D0007_Symbol(), D0007_Timeframe());
   if(total <= 0)
   {
      Print("DAL_D0007_FAILED *** build=", DAL_D0007_BUILD, "*reason=no_bars");
      return false;
   }

   int replay = MathMax(200, InpReplayClosedBars);
   int oldest_shift = MathMin(total - 1, replay);
   int warmup = MathMax(InpWarmupClosedBars, InpL * 2 + InpRegimeLookbackBars + 50);
   if(oldest_shift <= warmup + 3)
   {
      Print("DAL_D0007_FAILED *** build=", DAL_D0007_BUILD, "*reason=not_enough_bars*oldestShift=", oldest_shift, "*warmup=", warmup);
      return false;
   }

   Print("DAL_D0007_START *** build=", DAL_D0007_BUILD,
      "*mode=root_causal_live_replay",
      "*symbol=", D0007_Symbol(),
      "*tf=", EnumToString(D0007_Timeframe()),
      "*contract=prefix_only_decision_same_candle_batches_no_fake_sequence",
      "*entry=reversal_zone_touch_or_continuation_break_after_regime_known",
      "*families=", EnumToString(InpFamiliesToAudit));

   for(int cursor_shift = oldest_shift - warmup; cursor_shift >= 2; cursor_shift--)
   {
      g_sum.steps++;
      int step = g_sum.steps;
      DALBar bars[];
      int bars_count = 0;
      string load_reason = "";
      if(!D0007_LoadPrefixBars(oldest_shift, cursor_shift, bars, bars_count, load_reason))
      {
         g_sum.load_failures++;
         continue;
      }
      if(bars_count <= InpL * 2 + 20)
         continue;
      g_sum.decision_steps++;
      int decision_index = bars_count - 1;

      DALM0001Config m1;
      D0007_BuildM0001Config(m1);
      DALLRuleNode nodes[];
      int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, m1.L, nodes);
      DALM0001Event events[];
      int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);

      DALM0002Config m2;
      D0007_BuildM0002Config(m2);
      DALM0002BranchSample all_samples[];
      DALM0002BranchSample rev_samples[];
      DALM0002BranchSample cont_samples[];
      DALM0002Audit audit;
      int sample_count = DAL_M0002CollectBranchSamples(events, events_count, bars, bars_count, 0, m2, all_samples, rev_samples, cont_samples, audit);
      if(sample_count <= 0)
      {
         g_sum.no_sample_steps++;
         continue;
      }

      DALM0005CausalRegimeState state;
      bool has_state = DAL_M0005BuildLatestCausalRegimeState(all_samples, sample_count, bars, bars_count, decision_index, state);
      if(state.same_bar_batch_count > 0) g_sum.same_bar_batch_steps++;
      if(state.ambiguous_direction) g_sum.mixed_direction_steps++;
      if(!has_state)
      {
         if(state.ambiguous_energy) g_sum.ambiguous_energy_steps++;
         if(InpSkipAmbiguousEnergyBatch)
            continue;
      }
      if(!state.valid)
         continue;
      if(state.energy == DAL_H5_REGIME_REVERSAL) g_sum.reversal_regime_steps++;
      if(state.energy == DAL_H5_REGIME_CONTINUATION) g_sum.continuation_regime_steps++;

      D0007Candidate candidates[];
      int candidates_count = 0;
      D0007_SelectCandidates(bars, bars_count, nodes, nodes_count, events, events_count, state, candidates, candidates_count);
      if(candidates_count <= 0)
         continue;

      datetime activation_time = bars[decision_index].time;
      for(int c = 0; c < candidates_count; c++)
      {
         if(!candidates[c].valid)
            continue;
         if(InpOneActivationPerNodeFamily)
            D0007_AddKey(candidates[c].key);
         D0007TradeResult r;
         D0007_ReplayCandidate(candidates[c], cursor_shift, activation_time, r);
         D0007_Accumulate(candidates[c], r);
         D0007_WriteCsv(candidates[c], r);
         if(!InpPrintOnlySummary && (step % MathMax(1, InpPrintEveryNSteps) == 0 || r.same_bar_reward_stop || !r.entered))
            D0007_PrintCandidateResult(step, candidates[c], r);
      }
   }

   if(g_csv != INVALID_HANDLE)
      FileFlush(g_csv);

   double entry_rate = (g_sum.candidates > 0 ? 100.0 * g_sum.entered / g_sum.candidates : 0.0);
   double reward_rate = (g_sum.measured > 0 ? 100.0 * g_sum.reward_hits / g_sum.measured : 0.0);
   double stop_rate = (g_sum.measured > 0 ? 100.0 * g_sum.stop_hits / g_sum.measured : 0.0);
   double avg_mfe = (g_sum.measured > 0 ? g_sum.sum_mfe_r / g_sum.measured : 0.0);
   double avg_mae = (g_sum.measured > 0 ? g_sum.sum_mae_r / g_sum.measured : 0.0);
   double expectancy = (g_sum.measured > 0 ? g_sum.sum_realized_r / g_sum.measured : 0.0);
   double pf = (g_sum.gross_loss_r > 0.0 ? g_sum.gross_win_r / g_sum.gross_loss_r : 0.0);
   bool pass_contract = (g_sum.load_failures == 0 && g_sum.decision_steps > 0);

   Print("DAL_D0007_SUMMARY *** build=", DAL_D0007_BUILD,
      "*passCausalReplayContract=", D0007_BoolText(pass_contract),
      "*steps=", g_sum.steps,
      "*decisionSteps=", g_sum.decision_steps,
      "*loadFailures=", g_sum.load_failures,
      "*noSampleSteps=", g_sum.no_sample_steps,
      "*ambiguousEnergySteps=", g_sum.ambiguous_energy_steps,
      "*sameBarBatchSteps=", g_sum.same_bar_batch_steps,
      "*mixedDirectionSteps=", g_sum.mixed_direction_steps,
      "*reversalRegimeSteps=", g_sum.reversal_regime_steps,
      "*continuationRegimeSteps=", g_sum.continuation_regime_steps,
      "*candidates=", g_sum.candidates,
      "*reversalCandidates=", g_sum.reversal_candidates,
      "*continuationCandidates=", g_sum.continuation_candidates,
      "*buyCandidates=", g_sum.buy_candidates,
      "*sellCandidates=", g_sum.sell_candidates,
      "*entered=", g_sum.entered,
      "*unfilled=", g_sum.unfilled,
      "*entryRatePct=", DoubleToString(entry_rate, 2),
      "*measured=", g_sum.measured,
      "*rewardHitPct=", DoubleToString(reward_rate, 2),
      "*stopHitPct=", DoubleToString(stop_rate, 2),
      "*sameBarRewardStop=", g_sum.same_bar_reward_stop,
      "*openAfterWindow=", g_sum.open_after_window,
      "*avgMfeR=", DoubleToString(avg_mfe, 4),
      "*avgMaeR=", DoubleToString(avg_mae, 4),
      "*expectancyR=", DoubleToString(expectancy, 4),
      "*profitFactor=", DoubleToString(pf, 4),
      "*csv=", (InpWriteCsv ? InpCsvFileName : "OFF"));

   return pass_contract;
}

int OnInit()
{
   Print("DAL_D0007_INIT *** build=", DAL_D0007_BUILD,
      "*purpose=H5_root_causal_live_replay_audit",
      "*symbol=", D0007_Symbol(),
      "*tf=", EnumToString(D0007_Timeframe()),
      "*sameCandlePolicy=batch_not_sequence",
      "*directionFilter=", D0007_BoolText(InpUseCausalDirectionFilter));
   D0007_Run();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   if(g_csv != INVALID_HANDLE)
   {
      FileClose(g_csv);
      g_csv = INVALID_HANDLE;
   }
   Print("DAL_D0007_DEINIT *** build=", DAL_D0007_BUILD, "*reason=", reason);
}

void OnTick()
{
   // Historical validator only. Restart tester/expert after changing inputs.
}
