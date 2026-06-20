//+------------------------------------------------------------------+
//| Decision Alpha Lab — D0006 H5 Live Touch Replay Audit             |
//| Live-valid H0005 reversal touch-entry replay, prefix-only decision |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "D0006: H0005 live-valid walk-forward touch-entry audit. Prefix-only decisions, zone-touch fills, post-fill measurement only."

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0002/DAL_M0002Engine.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecReversalOneToOne.mqh>

#define DAL_D0006_BUILD "1.00"

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpReplayClosedBars = 2000;
input int InpWarmupClosedBars = 300;

// Shared H5/M0001 structure.
input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

// M0002 regime settings.
input int InpRegimeLookbackBars = 100;
input int InpOutcomeCandleOffsetAfterExit = 0;
input int InpBrokerUtcOffsetHours = 0;

// Live touch replay contract.
input int InpBuySlots = 3;
input int InpSellSlots = 3;
input int InpMaxBarsToWaitForTouch = 300;
input int InpMaxBarsToMeasureAfterTouch = 300;
input double InpRewardRForFirstHit = 1.0;
input int InpAuditSpreadPoints = 0;
input bool InpOneActivationPerNode = true;
input bool InpSkipConsumedNodes = true;
input bool InpPrintOnlySummary = false;
input int InpPrintEveryNSteps = 100;
input bool InpWriteCsv = true;
input string InpCsvFileName = "D0006_H5_Live_Touch_Replay.csv";

struct D0006Candidate
{
   bool valid;
   string key;
   DALLRuleNode node;
   int direction;
   double zone_lower;
   double zone_upper;
   double entry_price;
   double stop_price;
   double risk_price;
   double distance_to_market;
};

struct D0006TradeResult
{
   bool filled;
   bool measured;
   bool hit_reward_before_stop;
   bool hit_stop_before_reward;
   bool same_bar_reward_stop;
   datetime activated_time;
   datetime fill_time;
   datetime exit_time;
   int bars_to_touch;
   int bars_measured;
   double mfe_r;
   double mae_r;
   double realized_r;
   string outcome;
   string reason;
};

struct D0006Summary
{
   int steps;
   int load_failures;
   int decision_steps;
   int no_branch_steps;
   int reversal_steps;
   int continuation_steps;
   int future_node_violations;
   int active_from_violations;
   int candidate_activations;
   int buy_activations;
   int sell_activations;
   int touch_entries;
   int unfilled_entries;
   int measured_entries;
   int reward_hits;
   int stop_hits;
   int same_bar_reward_stop;
   int still_open_after_measure;
   double sum_mfe_r;
   double sum_mae_r;
   double sum_realized_r;
   double gross_win_r;
   double gross_loss_r;
};

datetime g_last_open_bar_time = 0;
int g_csv_handle = INVALID_HANDLE;
string g_activated_keys[];
D0006Summary g_summary;

string D0006_Symbol()
{
   if(InpSymbol == "")
      return _Symbol;
   return InpSymbol;
}

ENUM_TIMEFRAMES D0006_Timeframe()
{
   if(InpTimeframe == PERIOD_CURRENT)
      return (ENUM_TIMEFRAMES)_Period;
   return InpTimeframe;
}

string D0006_FormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

string D0006_BoolToString(const bool value)
{
   return (value ? "true" : "false");
}

string D0006_RegimeOutcomeToString(const ENUM_DALM0002Outcome outcome)
{
   if(outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
      return "REVERSAL";
   if(outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      return "CONTINUATION";
   return EnumToString(outcome);
}

string D0006_DirectionToString(const int direction)
{
   if(direction > 0)
      return "BUY";
   if(direction < 0)
      return "SELL";
   return "NONE";
}

void D0006_ResetSummary(D0006Summary &s)
{
   s.steps = 0;
   s.load_failures = 0;
   s.decision_steps = 0;
   s.no_branch_steps = 0;
   s.reversal_steps = 0;
   s.continuation_steps = 0;
   s.future_node_violations = 0;
   s.active_from_violations = 0;
   s.candidate_activations = 0;
   s.buy_activations = 0;
   s.sell_activations = 0;
   s.touch_entries = 0;
   s.unfilled_entries = 0;
   s.measured_entries = 0;
   s.reward_hits = 0;
   s.stop_hits = 0;
   s.same_bar_reward_stop = 0;
   s.still_open_after_measure = 0;
   s.sum_mfe_r = 0.0;
   s.sum_mae_r = 0.0;
   s.sum_realized_r = 0.0;
   s.gross_win_r = 0.0;
   s.gross_loss_r = 0.0;
}

void D0006_ResetCandidate(D0006Candidate &c)
{
   c.valid = false;
   c.key = "";
   ZeroMemory(c.node);
   c.direction = 0;
   c.zone_lower = 0.0;
   c.zone_upper = 0.0;
   c.entry_price = 0.0;
   c.stop_price = 0.0;
   c.risk_price = 0.0;
   c.distance_to_market = 0.0;
}

void D0006_ResetTradeResult(D0006TradeResult &r)
{
   r.filled = false;
   r.measured = false;
   r.hit_reward_before_stop = false;
   r.hit_stop_before_reward = false;
   r.same_bar_reward_stop = false;
   r.activated_time = 0;
   r.fill_time = 0;
   r.exit_time = 0;
   r.bars_to_touch = 0;
   r.bars_measured = 0;
   r.mfe_r = 0.0;
   r.mae_r = 0.0;
   r.realized_r = 0.0;
   r.outcome = "none";
   r.reason = "not_measured";
}

void D0006_BuildM0001Config(DALM0001Config &config)
{
   DAL_M0001DefaultConfig(config);
   config.L = InpL;
   config.zone_ratio = InpZoneRatio;
   config.exit_gap = InpExitGap;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = (InpConsumeMode == DAL_M0001_CONSUME_BY_TOUCH);
   config.max_events = 0;
   config.min_rtv = 0.0;
}

void D0006_BuildM0002Config(DALM0002Config &config)
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
   config.hard_random_candidates = 1;
   config.placebo_shift_bars = 1;
   config.nonoverlap_gap_bars = 0;
   config.block_bootstrap_iterations = 0;
   config.block_bootstrap_block_pairs = 1;
   config.consume_mode = InpConsumeMode;
   config.consume_on_touch = (InpConsumeMode == DAL_M0001_CONSUME_BY_TOUCH);
}

bool D0006_HasNewOpenCandle()
{
   datetime current_open = iTime(D0006_Symbol(), D0006_Timeframe(), 0);
   if(current_open <= 0)
      return false;

   if(g_last_open_bar_time <= 0)
   {
      g_last_open_bar_time = current_open;
      return true;
   }

   if(current_open == g_last_open_bar_time)
      return false;

   g_last_open_bar_time = current_open;
   return true;
}

void D0006_ReverseRates(MqlRates &rates[], const int count)
{
   int left = 0;
   int right = count - 1;
   while(left < right)
   {
      MqlRates tmp = rates[left];
      rates[left] = rates[right];
      rates[right] = tmp;
      left++;
      right--;
   }
}

bool D0006_LoadPrefixBarsByClosedShift(
   const int oldest_closed_shift,
   const int simulated_cursor_closed_shift,
   DALBar &bars[],
   int &bars_count,
   string &reason
)
{
   ArrayResize(bars, 0);
   bars_count = 0;
   reason = "not_loaded";

   if(oldest_closed_shift < simulated_cursor_closed_shift)
   {
      reason = "bad_shift_order";
      return false;
   }

   datetime start_time = iTime(D0006_Symbol(), D0006_Timeframe(), oldest_closed_shift);
   datetime stop_time = iTime(D0006_Symbol(), D0006_Timeframe(), simulated_cursor_closed_shift);
   if(start_time <= 0 || stop_time <= 0)
   {
      reason = "bad_iTime";
      return false;
   }

   if(start_time > stop_time)
   {
      datetime tmp_time = start_time;
      start_time = stop_time;
      stop_time = tmp_time;
   }

   MqlRates raw[];
   ArrayResize(raw, 0);
   int copied = CopyRates(D0006_Symbol(), D0006_Timeframe(), start_time, stop_time, raw);
   if(copied <= 0)
   {
      reason = "copy_rates_prefix_failed*err=" + IntegerToString(GetLastError());
      return false;
   }

   if(copied > 1 && raw[0].time > raw[copied - 1].time)
      D0006_ReverseRates(raw, copied);

   ArrayResize(bars, copied);
   for(int i = 0; i < copied; i++)
   {
      ZeroMemory(bars[i]);
      bars[i].time = raw[i].time;
      bars[i].open = raw[i].open;
      bars[i].high = raw[i].high;
      bars[i].low = raw[i].low;
      bars[i].close = raw[i].close;
   }

   bars_count = copied;
   reason = "loaded_prefix_only";
   return true;
}

bool D0006_LoadForwardBarsAfterCursor(
   const int cursor_closed_shift,
   const int max_forward_closed_bars,
   DALBar &bars[],
   int &bars_count,
   string &reason
)
{
   ArrayResize(bars, 0);
   bars_count = 0;
   reason = "not_loaded";

   if(cursor_closed_shift <= 1)
   {
      reason = "no_future_closed_bars_available";
      return false;
   }

   int first_future_shift = cursor_closed_shift - 1;
   int latest_shift = MathMax(1, cursor_closed_shift - MathMax(1, max_forward_closed_bars));

   datetime start_time = iTime(D0006_Symbol(), D0006_Timeframe(), first_future_shift);
   datetime stop_time = iTime(D0006_Symbol(), D0006_Timeframe(), latest_shift);
   if(start_time <= 0 || stop_time <= 0)
   {
      reason = "bad_future_iTime";
      return false;
   }

   if(start_time > stop_time)
   {
      datetime tmp_time = start_time;
      start_time = stop_time;
      stop_time = tmp_time;
   }

   MqlRates raw[];
   ArrayResize(raw, 0);
   int copied = CopyRates(D0006_Symbol(), D0006_Timeframe(), start_time, stop_time, raw);
   if(copied <= 0)
   {
      reason = "copy_rates_forward_failed*err=" + IntegerToString(GetLastError());
      return false;
   }

   if(copied > 1 && raw[0].time > raw[copied - 1].time)
      D0006_ReverseRates(raw, copied);

   ArrayResize(bars, copied);
   for(int i = 0; i < copied; i++)
   {
      ZeroMemory(bars[i]);
      bars[i].time = raw[i].time;
      bars[i].open = raw[i].open;
      bars[i].high = raw[i].high;
      bars[i].low = raw[i].low;
      bars[i].close = raw[i].close;
   }

   bars_count = copied;
   reason = "loaded_forward_outcome_only";
   return true;
}

string D0006_NodeKey(const DALLRuleNode &node)
{
   return IntegerToString((int)node.type) + "_" + IntegerToString((long)node.time) + "_" + DoubleToString(node.price, 10);
}

bool D0006_KeyExists(const string key)
{
   for(int i = 0; i < ArraySize(g_activated_keys); i++)
   {
      if(g_activated_keys[i] == key)
         return true;
   }
   return false;
}

void D0006_AddKey(const string key)
{
   if(key == "" || D0006_KeyExists(key))
      return;
   int n = ArraySize(g_activated_keys);
   ArrayResize(g_activated_keys, n + 1);
   g_activated_keys[n] = key;
}

bool D0006_AddCandidate(D0006Candidate &slots[], int &slot_count, const int max_slots, const D0006Candidate &candidate)
{
   if(!candidate.valid || max_slots <= 0)
      return false;

   if(slot_count < max_slots)
   {
      ArrayResize(slots, slot_count + 1);
      slots[slot_count] = candidate;
      slot_count++;
      return true;
   }

   int worst_index = -1;
   double worst_dist = -1.0;
   for(int i = 0; i < slot_count; i++)
   {
      if(worst_index < 0 || slots[i].distance_to_market > worst_dist)
      {
         worst_index = i;
         worst_dist = slots[i].distance_to_market;
      }
   }

   if(worst_index >= 0 && candidate.distance_to_market < worst_dist)
   {
      slots[worst_index] = candidate;
      return true;
   }

   return false;
}

bool D0006_BuildCandidateFromNode(
   const DALBar &bars[],
   const int bars_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALLRuleNode &node,
   const double market_close,
   const double spread_price,
   D0006Candidate &candidate,
   string &reason
)
{
   D0006_ResetCandidate(candidate);
   reason = "not_candidate";

   if(!node.confirmed)
   {
      reason = "node_not_confirmed";
      return false;
   }

   int last_index = bars_count - 1;
   if(node.active_from_index < 0 || node.active_from_index > last_index)
   {
      reason = "node_not_active_yet";
      return false;
   }

   if(InpSkipConsumedNodes && DAL_ExecNodeHasEvent(events, events_count, node.id))
   {
      reason = "node_has_m0001_event";
      return false;
   }

   string key = D0006_NodeKey(node);
   if(InpOneActivationPerNode && D0006_KeyExists(key))
   {
      reason = "node_already_activated";
      return false;
   }

   double live_extreme = 0.0;
   double zone_lower = node.price;
   double zone_upper = node.price;
   bool hunted = false;
   if(!DAL_ExecBuildLiveNodeTerritory(bars, bars_count, node, InpZoneRatio, live_extreme, zone_lower, zone_upper, hunted))
   {
      reason = "territory_failed";
      return false;
   }

   double before_extreme = 0.0;
   double before_lower = 0.0;
   double before_upper = 0.0;
   if(DAL_ExecNodeTouchedOrConsumedBeforeNow(bars, bars_count, node, InpZoneRatio, before_extreme, before_lower, before_upper))
   {
      reason = "node_or_zone_already_touched_before_activation";
      return false;
   }

   int direction = 0;
   double entry = 0.0;
   double stop = 0.0;
   double distance = 0.0;

   if(node.type == DAL_NODE_LOW)
   {
      if(!(zone_upper < market_close))
      {
         reason = "buy_zone_not_below_market";
         return false;
      }
      direction = +1;
      entry = zone_upper + spread_price;
      stop = zone_lower;
      distance = market_close - zone_upper;
   }
   else if(node.type == DAL_NODE_HIGH)
   {
      if(!(zone_lower > market_close))
      {
         reason = "sell_zone_not_above_market";
         return false;
      }
      direction = -1;
      entry = zone_lower;
      stop = zone_upper + spread_price;
      distance = zone_lower - market_close;
   }
   else
   {
      reason = "unknown_node_type";
      return false;
   }

   double risk = MathAbs(entry - stop);
   if(risk <= 0.0)
   {
      reason = "invalid_risk";
      return false;
   }

   candidate.valid = true;
   candidate.key = key;
   candidate.node = node;
   candidate.direction = direction;
   candidate.zone_lower = zone_lower;
   candidate.zone_upper = zone_upper;
   candidate.entry_price = entry;
   candidate.stop_price = stop;
   candidate.risk_price = risk;
   candidate.distance_to_market = MathMax(0.0, distance);
   reason = "ok";
   return true;
}

void D0006_SelectLiveTouchCandidates(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   D0006Candidate &candidates[],
   int &candidates_count,
   int &future_node_violations
)
{
   ArrayResize(candidates, 0);
   candidates_count = 0;
   future_node_violations = 0;

   D0006Candidate buy_slots[];
   D0006Candidate sell_slots[];
   int buy_count = 0;
   int sell_count = 0;
   int last_index = bars_count - 1;
   double market_close = bars[last_index].close;
   double point = SymbolInfoDouble(D0006_Symbol(), SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.0;
   double spread_price = MathMax(0, InpAuditSpreadPoints) * point;

   for(int i = 0; i < nodes_count; i++)
   {
      if(nodes[i].confirmed && nodes[i].active_from_index > last_index)
      {
         future_node_violations++;
         continue;
      }

      D0006Candidate c;
      string reason = "";
      if(!D0006_BuildCandidateFromNode(bars, bars_count, events, events_count, nodes[i], market_close, spread_price, c, reason))
         continue;

      if(c.direction > 0)
         D0006_AddCandidate(buy_slots, buy_count, MathMax(0, InpBuySlots), c);
      else if(c.direction < 0)
         D0006_AddCandidate(sell_slots, sell_count, MathMax(0, InpSellSlots), c);
   }

   int total = buy_count + sell_count;
   ArrayResize(candidates, total);
   int out = 0;
   for(int b = 0; b < buy_count; b++)
   {
      candidates[out] = buy_slots[b];
      out++;
   }
   for(int s = 0; s < sell_count; s++)
   {
      candidates[out] = sell_slots[s];
      out++;
   }
   candidates_count = total;
}

bool D0006_TouchCandidateOnBar(const D0006Candidate &candidate, const DALBar &bar)
{
   if(candidate.direction > 0)
      return (bar.low <= candidate.zone_upper && bar.high >= candidate.zone_lower);
   if(candidate.direction < 0)
      return (bar.high >= candidate.zone_lower && bar.low <= candidate.zone_upper);
   return false;
}

void D0006_MeasureAfterTouch(
   const D0006Candidate &candidate,
   const DALBar &forward_bars[],
   const int forward_count,
   const int touch_index,
   D0006TradeResult &result
)
{
   result.measured = false;
   result.reason = "not_measured";

   if(!result.filled || touch_index < 0 || touch_index >= forward_count || candidate.risk_price <= 0.0)
   {
      result.reason = "invalid_touch_measurement_input";
      return;
   }

   double entry = candidate.entry_price;
   double stop = candidate.stop_price;
   double risk = candidate.risk_price;
   double reward_r = MathMax(0.1, InpRewardRForFirstHit);
   double reward_price = (candidate.direction > 0 ? entry + risk * reward_r : entry - risk * reward_r);
   int max_measure = MathMax(1, InpMaxBarsToMeasureAfterTouch);
   int last_index = MathMin(forward_count - 1, touch_index + max_measure - 1);

   double max_favorable = 0.0;
   double max_adverse = 0.0;
   bool decided = false;

   for(int i = touch_index; i <= last_index; i++)
   {
      DALBar bar = forward_bars[i];
      double favorable = 0.0;
      double adverse = 0.0;
      bool reward_hit = false;
      bool stop_hit = false;

      if(candidate.direction > 0)
      {
         favorable = bar.high - entry;
         adverse = entry - bar.low;
         reward_hit = (bar.high >= reward_price);
         stop_hit = (bar.low <= stop);
      }
      else
      {
         favorable = entry - bar.low;
         adverse = bar.high - entry;
         reward_hit = (bar.low <= reward_price);
         stop_hit = (bar.high >= stop);
      }

      if(favorable > max_favorable)
         max_favorable = favorable;
      if(adverse > max_adverse)
         max_adverse = adverse;

      if(!decided && reward_hit && stop_hit)
      {
         result.same_bar_reward_stop = true;
         result.hit_stop_before_reward = true;
         result.realized_r = -1.0;
         result.exit_time = bar.time;
         result.outcome = "same_bar_stop_first";
         decided = true;
      }
      else if(!decided && stop_hit)
      {
         result.hit_stop_before_reward = true;
         result.realized_r = -1.0;
         result.exit_time = bar.time;
         result.outcome = "stop_before_reward";
         decided = true;
      }
      else if(!decided && reward_hit)
      {
         result.hit_reward_before_stop = true;
         result.realized_r = reward_r;
         result.exit_time = bar.time;
         result.outcome = "reward_before_stop";
         decided = true;
      }
   }

   if(!decided)
   {
      DALBar last_bar = forward_bars[last_index];
      double close_r = 0.0;
      if(candidate.direction > 0)
         close_r = (last_bar.close - entry) / risk;
      else
         close_r = (entry - last_bar.close) / risk;

      result.realized_r = close_r;
      result.exit_time = last_bar.time;
      result.outcome = "open_after_measure_window";
   }

   result.mfe_r = max_favorable / risk;
   result.mae_r = max_adverse / risk;
   result.bars_measured = last_index - touch_index + 1;
   result.measured = true;
   result.reason = "measured_post_fill_only";
}

void D0006_ReplayCandidateOutcome(
   const D0006Candidate &candidate,
   const int cursor_shift,
   const datetime activation_time,
   D0006TradeResult &result
)
{
   D0006_ResetTradeResult(result);
   result.activated_time = activation_time;

   DALBar forward_bars[];
   int forward_count = 0;
   string load_reason = "";
   int max_forward = MathMax(1, InpMaxBarsToWaitForTouch) + MathMax(1, InpMaxBarsToMeasureAfterTouch) + 2;
   if(!D0006_LoadForwardBarsAfterCursor(cursor_shift, max_forward, forward_bars, forward_count, load_reason))
   {
      result.reason = load_reason;
      result.outcome = "no_forward_bars";
      return;
   }

   int max_wait = MathMin(forward_count, MathMax(1, InpMaxBarsToWaitForTouch));
   int touch_index = -1;
   for(int i = 0; i < max_wait; i++)
   {
      if(D0006_TouchCandidateOnBar(candidate, forward_bars[i]))
      {
         touch_index = i;
         break;
      }
   }

   if(touch_index < 0)
   {
      result.filled = false;
      result.bars_to_touch = max_wait;
      result.reason = "zone_not_touched_in_wait_window";
      result.outcome = "unfilled";
      return;
   }

   result.filled = true;
   result.fill_time = forward_bars[touch_index].time;
   result.bars_to_touch = touch_index + 1;
   result.reason = "filled_by_zone_touch";
   result.outcome = "filled";

   D0006_MeasureAfterTouch(candidate, forward_bars, forward_count, touch_index, result);
}

void D0006_OpenCsvIfNeeded()
{
   if(!InpWriteCsv)
      return;
   if(g_csv_handle != INVALID_HANDLE)
      return;

   g_csv_handle = FileOpen(InpCsvFileName, FILE_WRITE | FILE_CSV | FILE_ANSI);
   if(g_csv_handle == INVALID_HANDLE)
   {
      Print("DAL_D0006_CSV_OPEN_FAILED *** build=", DAL_D0006_BUILD,
         "*file=", InpCsvFileName,
         "*err=", GetLastError());
      return;
   }

   FileWrite(g_csv_handle,
      "activation_time",
      "node_key",
      "node_id",
      "node_type",
      "direction",
      "zone_lower",
      "zone_upper",
      "entry_price",
      "stop_price",
      "risk_price",
      "distance_to_market",
      "filled",
      "fill_time",
      "bars_to_touch",
      "measured",
      "bars_measured",
      "mfe_r",
      "mae_r",
      "realized_r",
      "reward_hit",
      "stop_hit",
      "same_bar_reward_stop",
      "outcome",
      "reason");
}

void D0006_WriteCsvTrade(const D0006Candidate &candidate, const D0006TradeResult &result)
{
   if(!InpWriteCsv)
      return;
   D0006_OpenCsvIfNeeded();
   if(g_csv_handle == INVALID_HANDLE)
      return;

   FileWrite(g_csv_handle,
      D0006_FormatDateTime(result.activated_time),
      candidate.key,
      candidate.node.id,
      EnumToString(candidate.node.type),
      D0006_DirectionToString(candidate.direction),
      DoubleToString(candidate.zone_lower, 10),
      DoubleToString(candidate.zone_upper, 10),
      DoubleToString(candidate.entry_price, 10),
      DoubleToString(candidate.stop_price, 10),
      DoubleToString(candidate.risk_price, 10),
      DoubleToString(candidate.distance_to_market, 10),
      D0006_BoolToString(result.filled),
      D0006_FormatDateTime(result.fill_time),
      result.bars_to_touch,
      D0006_BoolToString(result.measured),
      result.bars_measured,
      DoubleToString(result.mfe_r, 6),
      DoubleToString(result.mae_r, 6),
      DoubleToString(result.realized_r, 6),
      D0006_BoolToString(result.hit_reward_before_stop),
      D0006_BoolToString(result.hit_stop_before_reward),
      D0006_BoolToString(result.same_bar_reward_stop),
      result.outcome,
      result.reason);
}

void D0006_AccumulateTrade(const D0006Candidate &candidate, const D0006TradeResult &result)
{
   g_summary.candidate_activations++;
   if(candidate.direction > 0)
      g_summary.buy_activations++;
   else if(candidate.direction < 0)
      g_summary.sell_activations++;

   if(result.filled)
      g_summary.touch_entries++;
   else
      g_summary.unfilled_entries++;

   if(result.measured)
   {
      g_summary.measured_entries++;
      g_summary.sum_mfe_r += result.mfe_r;
      g_summary.sum_mae_r += result.mae_r;
      g_summary.sum_realized_r += result.realized_r;
      if(result.realized_r > 0.0)
         g_summary.gross_win_r += result.realized_r;
      else if(result.realized_r < 0.0)
         g_summary.gross_loss_r += MathAbs(result.realized_r);
   }

   if(result.hit_reward_before_stop)
      g_summary.reward_hits++;
   if(result.hit_stop_before_reward)
      g_summary.stop_hits++;
   if(result.same_bar_reward_stop)
      g_summary.same_bar_reward_stop++;
   if(result.outcome == "open_after_measure_window")
      g_summary.still_open_after_measure++;
}

void D0006_PrintTrade(const int step, const D0006Candidate &candidate, const D0006TradeResult &result)
{
   Print("DAL_D0006_TOUCH_TRADE *** build=", DAL_D0006_BUILD,
      "*step=", step,
      "*activation=", D0006_FormatDateTime(result.activated_time),
      "*nodeId=", candidate.node.id,
      "*nodeType=", EnumToString(candidate.node.type),
      "*dir=", D0006_DirectionToString(candidate.direction),
      "*zoneLower=", DoubleToString(candidate.zone_lower, 10),
      "*zoneUpper=", DoubleToString(candidate.zone_upper, 10),
      "*entry=", DoubleToString(candidate.entry_price, 10),
      "*stop=", DoubleToString(candidate.stop_price, 10),
      "*filled=", D0006_BoolToString(result.filled),
      "*fillTime=", D0006_FormatDateTime(result.fill_time),
      "*barsToTouch=", result.bars_to_touch,
      "*mfeR=", DoubleToString(result.mfe_r, 4),
      "*maeR=", DoubleToString(result.mae_r, 4),
      "*realizedR=", DoubleToString(result.realized_r, 4),
      "*outcome=", result.outcome,
      "*reason=", result.reason);
}

bool D0006_RunLiveTouchReplayAudit()
{
   D0006_ResetSummary(g_summary);
   ArrayResize(g_activated_keys, 0);
   D0006_OpenCsvIfNeeded();

   int total_bars = Bars(D0006_Symbol(), D0006_Timeframe());
   if(total_bars <= 0)
   {
      Print("DAL_D0006_AUDIT_FAILED *** build=", DAL_D0006_BUILD,
         "*reason=no_bars*symbol=", D0006_Symbol(),
         "*tf=", EnumToString(D0006_Timeframe()));
      return false;
   }

   int replay_closed = MathMax(100, InpReplayClosedBars);
   int max_oldest_shift = MathMin(total_bars - 1, replay_closed);
   int warmup = MathMax(InpWarmupClosedBars, InpL * 2 + InpRegimeLookbackBars + 30);
   if(max_oldest_shift <= warmup + 2)
   {
      Print("DAL_D0006_AUDIT_FAILED *** build=", DAL_D0006_BUILD,
         "*reason=not_enough_replay_bars",
         "*totalBars=", total_bars,
         "*maxOldestShift=", max_oldest_shift,
         "*warmup=", warmup);
      return false;
   }

   Print("DAL_D0006_AUDIT_START *** build=", DAL_D0006_BUILD,
      "*mode=live_valid_walk_forward_touch_entry",
      "*symbol=", D0006_Symbol(),
      "*tf=", EnumToString(D0006_Timeframe()),
      "*oldestClosedShift=", max_oldest_shift,
      "*warmupClosedBars=", warmup,
      "*decisionContract=prefix_only_nodes_events_regime",
      "*entryContract=zone_touch_after_activation_not_close",
      "*measurementContract=post_fill_only");

   for(int cursor_shift = max_oldest_shift - warmup; cursor_shift >= 2; cursor_shift--)
   {
      g_summary.steps++;
      int step = g_summary.steps;

      DALBar bars[];
      int bars_count = 0;
      string load_reason = "";
      if(!D0006_LoadPrefixBarsByClosedShift(max_oldest_shift, cursor_shift, bars, bars_count, load_reason))
      {
         g_summary.load_failures++;
         continue;
      }

      if(bars_count <= InpL * 2 + 10)
         continue;

      g_summary.decision_steps++;

      DALM0001Config m1;
      D0006_BuildM0001Config(m1);

      DALLRuleNode nodes[];
      int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, m1.L, nodes);

      DALM0001Event events[];
      int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);

      DALM0002Config m2;
      D0006_BuildM0002Config(m2);

      DALM0002BranchSample last_sample;
      int last_event_index = -1;
      bool has_last_sample = DAL_ExecFindLatestBranchSampleFast(events, events_count, bars, bars_count, 0, m2, last_sample, last_event_index);
      if(!has_last_sample)
      {
         g_summary.no_branch_steps++;
         continue;
      }

      if(last_sample.outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      {
         g_summary.continuation_steps++;
         continue;
      }

      if(last_sample.outcome != DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
         continue;

      g_summary.reversal_steps++;

      D0006Candidate candidates[];
      int candidates_count = 0;
      int future_node_violations = 0;
      D0006_SelectLiveTouchCandidates(bars, bars_count, nodes, nodes_count, events, events_count, candidates, candidates_count, future_node_violations);
      if(future_node_violations > 0)
         g_summary.future_node_violations += future_node_violations;

      if(candidates_count <= 0)
         continue;

      datetime activation_time = bars[bars_count - 1].time;
      for(int c = 0; c < candidates_count; c++)
      {
         if(!candidates[c].valid)
            continue;

         if(InpOneActivationPerNode)
            D0006_AddKey(candidates[c].key);

         D0006TradeResult result;
         D0006_ReplayCandidateOutcome(candidates[c], cursor_shift, activation_time, result);
         D0006_AccumulateTrade(candidates[c], result);
         D0006_WriteCsvTrade(candidates[c], result);

         if(!InpPrintOnlySummary && (step % MathMax(1, InpPrintEveryNSteps) == 0 || !result.filled || result.same_bar_reward_stop))
            D0006_PrintTrade(step, candidates[c], result);
      }
   }

   if(g_csv_handle != INVALID_HANDLE)
      FileFlush(g_csv_handle);

   double fill_rate = (g_summary.candidate_activations > 0 ? 100.0 * g_summary.touch_entries / g_summary.candidate_activations : 0.0);
   double reward_rate = (g_summary.measured_entries > 0 ? 100.0 * g_summary.reward_hits / g_summary.measured_entries : 0.0);
   double stop_rate = (g_summary.measured_entries > 0 ? 100.0 * g_summary.stop_hits / g_summary.measured_entries : 0.0);
   double avg_mfe = (g_summary.measured_entries > 0 ? g_summary.sum_mfe_r / g_summary.measured_entries : 0.0);
   double avg_mae = (g_summary.measured_entries > 0 ? g_summary.sum_mae_r / g_summary.measured_entries : 0.0);
   double expectancy = (g_summary.measured_entries > 0 ? g_summary.sum_realized_r / g_summary.measured_entries : 0.0);
   double pf = (g_summary.gross_loss_r > 0.0 ? g_summary.gross_win_r / g_summary.gross_loss_r : 0.0);
   bool pass_contract = (g_summary.future_node_violations == 0 && g_summary.active_from_violations == 0 && g_summary.decision_steps > 0);

   Print("DAL_D0006_AUDIT_SUMMARY *** build=", DAL_D0006_BUILD,
      "*passLiveDecisionContract=", D0006_BoolToString(pass_contract),
      "*steps=", g_summary.steps,
      "*decisionSteps=", g_summary.decision_steps,
      "*loadFailures=", g_summary.load_failures,
      "*noBranchSteps=", g_summary.no_branch_steps,
      "*reversalSteps=", g_summary.reversal_steps,
      "*continuationSteps=", g_summary.continuation_steps,
      "*futureNodeViolations=", g_summary.future_node_violations,
      "*candidateActivations=", g_summary.candidate_activations,
      "*buyActivations=", g_summary.buy_activations,
      "*sellActivations=", g_summary.sell_activations,
      "*touchEntries=", g_summary.touch_entries,
      "*unfilled=", g_summary.unfilled_entries,
      "*fillRatePct=", DoubleToString(fill_rate, 2),
      "*measuredEntries=", g_summary.measured_entries,
      "*rewardHitPct=", DoubleToString(reward_rate, 2),
      "*stopHitPct=", DoubleToString(stop_rate, 2),
      "*sameBarRewardStop=", g_summary.same_bar_reward_stop,
      "*avgMfeR=", DoubleToString(avg_mfe, 4),
      "*avgMaeR=", DoubleToString(avg_mae, 4),
      "*expectancyR=", DoubleToString(expectancy, 4),
      "*profitFactor=", DoubleToString(pf, 4),
      "*csv=", (InpWriteCsv ? InpCsvFileName : "OFF"));

   return pass_contract;
}

int OnInit()
{
   Print("DAL_D0006_INIT *** build=", DAL_D0006_BUILD,
      "*purpose=H0005_live_valid_touch_entry_replay_audit",
      "*symbol=", D0006_Symbol(),
      "*tf=", EnumToString(D0006_Timeframe()),
      "*entry=zone_touch_after_prefix_only_activation",
      "*rewardRForFirstHit=", DoubleToString(InpRewardRForFirstHit, 2));

   D0006_RunLiveTouchReplayAudit();
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   if(g_csv_handle != INVALID_HANDLE)
   {
      FileClose(g_csv_handle);
      g_csv_handle = INVALID_HANDLE;
   }

   Print("DAL_D0006_DEINIT *** build=", DAL_D0006_BUILD,
      "*reason=", reason);
}

void OnTick()
{
   // D0006 is a deterministic historical audit. It intentionally does not trade.
   // Re-run by restarting the tester/expert after changing inputs.
}
