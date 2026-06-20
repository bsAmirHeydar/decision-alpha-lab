//+------------------------------------------------------------------+
//| Decision Alpha Lab — D0009 H5 Atomic No-Sample Replay Audit       |
//| H0005 validator with ZERO M0002 branch samples. Prefix-only state. |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "D0009: H5 live replay without building any M0002 samples. Raw M0001 event batches only; entry/outcome measured after trigger."

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>

#define DAL_D0009_BUILD "1.00"
#define DAL_D0009_REGIME_UNKNOWN -1
#define DAL_D0009_REGIME_REVERSAL 0
#define DAL_D0009_REGIME_CONTINUATION 1
#define DAL_D0009_REGIME_AMBIGUOUS 2

enum ENUM_DALD0009Family
{
   DAL_D0009_BOTH = 0,
   DAL_D0009_REVERSAL_ONLY = 1,
   DAL_D0009_CONTINUATION_ONLY = 2
};

enum ENUM_DALD0009ContinuationBreakMode
{
   DAL_D0009_CONT_CLOSE_BREAK = 0,
   DAL_D0009_CONT_INTRABAR_BREAK = 1
};

enum ENUM_DALD0009ContinuationRiskMode
{
   DAL_D0009_CONT_RISK_ATR = 0,
   DAL_D0009_CONT_RISK_STRUCTURAL_ZONE = 1
};

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpReplayClosedBars = 1500;
input int InpWarmupClosedBars = 300;

// M0001 structure.
input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

// Atomic no-sample regime contract.
input int InpOutcomeCandleOffsetAfterExit = 0;
input bool InpRequireEventRtvReady = false;
input bool InpSkipAmbiguousEnergyBatch = true;
input bool InpUseCausalDirectionFilter = false;

// Families and execution trigger.
input ENUM_DALD0009Family InpFamiliesToAudit = DAL_D0009_BOTH;
input ENUM_DALD0009ContinuationBreakMode InpContinuationBreakMode = DAL_D0009_CONT_CLOSE_BREAK;
input ENUM_DALD0009ContinuationRiskMode InpContinuationRiskMode = DAL_D0009_CONT_RISK_ATR;

// Candidate slots.
input int InpReversalBuySlots = 3;
input int InpReversalSellSlots = 3;
input int InpContinuationBuySlots = 3;
input int InpContinuationSellSlots = 3;
input bool InpSkipTouchedOrClosedNodesBeforeDecision = true;
input bool InpOneActivationPerNodeFamily = true;

// Risk and measurement.
input int InpMaxBarsToWaitForEntry = 300;
input int InpMaxBarsToMeasureAfterEntry = 300;
input double InpRewardR = 1.0;
input int InpAuditSpreadPoints = 0;
input bool InpSameBarStopFirst = true;
input int InpAtrPeriod = 14;
input double InpAtrMultiplier = 4.0;

// Output.
input bool InpPrintOnlySummary = true;
input int InpPrintEveryNSteps = 100;
input bool InpWriteCsv = true;
input string InpCsvFileName = "D0009_H5_Atomic_NoSample_Replay.csv";

struct D0009RegimeState
{
   bool valid;
   bool ambiguous_energy;
   bool ambiguous_direction;
   int energy;
   int direction;
   int known_index;
   datetime known_time;
   int batch_count;
   int reversal_count;
   int continuation_count;
   int buy_direction_count;
   int sell_direction_count;
   int same_bar_batch_count;
   string reason;
};

struct D0009Candidate
{
   bool valid;
   string family;
   string key;
   DALLRuleNode node;
   int direction;
   double zone_lower;
   double zone_upper;
   double entry_hint_price;
   double structural_stop_price;
   double activation_atr;
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

struct D0009TradeResult
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

struct D0009FamilyStats
{
   int candidates;
   int entered;
   int unfilled;
   int measured;
   int wins;
   int losses;
   int flats;
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

struct D0009Summary
{
   int steps;
   int load_failures;
   int decision_steps;
   int no_event_steps;
   int no_regime_steps;
   int ambiguous_energy_steps;
   int same_bar_batch_steps;
   int mixed_direction_steps;
   int reversal_regime_steps;
   int continuation_regime_steps;
   int raw_events_seen;
   int raw_events_used_for_regime;
   D0009FamilyStats all;
   D0009FamilyStats reversal;
   D0009FamilyStats continuation;
};

int g_csv = INVALID_HANDLE;
string g_keys[];
D0009Summary g_sum;

string D0009_Symbol()
{
   return (InpSymbol == "" ? _Symbol : InpSymbol);
}

ENUM_TIMEFRAMES D0009_Timeframe()
{
   return (InpTimeframe == PERIOD_CURRENT ? (ENUM_TIMEFRAMES)_Period : InpTimeframe);
}

string D0009_TimeText(const datetime t)
{
   if(t <= 0) return "0";
   return TimeToString(t, TIME_DATE | TIME_MINUTES | TIME_SECONDS);
}

string D0009_BoolText(const bool v)
{
   return (v ? "true" : "false");
}

string D0009_DirText(const int d)
{
   if(d > 0) return "BUY";
   if(d < 0) return "SELL";
   return "NONE";
}

string D0009_EnergyText(const int e)
{
   if(e == DAL_D0009_REGIME_REVERSAL) return "REVERSAL";
   if(e == DAL_D0009_REGIME_CONTINUATION) return "CONTINUATION";
   if(e == DAL_D0009_REGIME_AMBIGUOUS) return "AMBIGUOUS";
   return "UNKNOWN";
}

void D0009_ResetRegime(D0009RegimeState &s)
{
   s.valid = false;
   s.ambiguous_energy = false;
   s.ambiguous_direction = false;
   s.energy = DAL_D0009_REGIME_UNKNOWN;
   s.direction = 0;
   s.known_index = -1;
   s.known_time = 0;
   s.batch_count = 0;
   s.reversal_count = 0;
   s.continuation_count = 0;
   s.buy_direction_count = 0;
   s.sell_direction_count = 0;
   s.same_bar_batch_count = 0;
   s.reason = "not_built";
}

void D0009_ResetCandidate(D0009Candidate &c)
{
   c.valid = false;
   c.family = "";
   c.key = "";
   ZeroMemory(c.node);
   c.direction = 0;
   c.zone_lower = 0.0;
   c.zone_upper = 0.0;
   c.entry_hint_price = 0.0;
   c.structural_stop_price = 0.0;
   c.activation_atr = 0.0;
   c.distance_to_market = 0.0;
   c.regime_energy = DAL_D0009_REGIME_UNKNOWN;
   c.regime_direction = 0;
   c.regime_known_index = -1;
   c.regime_known_time = 0;
   c.regime_batch_count = 0;
   c.regime_rev_count = 0;
   c.regime_cont_count = 0;
   c.regime_ambiguous_direction = false;
}

void D0009_ResetTrade(D0009TradeResult &r)
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

void D0009_ResetFamilyStats(D0009FamilyStats &s)
{
   s.candidates = 0;
   s.entered = 0;
   s.unfilled = 0;
   s.measured = 0;
   s.wins = 0;
   s.losses = 0;
   s.flats = 0;
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

void D0009_ResetSummary(D0009Summary &s)
{
   s.steps = 0;
   s.load_failures = 0;
   s.decision_steps = 0;
   s.no_event_steps = 0;
   s.no_regime_steps = 0;
   s.ambiguous_energy_steps = 0;
   s.same_bar_batch_steps = 0;
   s.mixed_direction_steps = 0;
   s.reversal_regime_steps = 0;
   s.continuation_regime_steps = 0;
   s.raw_events_seen = 0;
   s.raw_events_used_for_regime = 0;
   D0009_ResetFamilyStats(s.all);
   D0009_ResetFamilyStats(s.reversal);
   D0009_ResetFamilyStats(s.continuation);
}

void D0009_BuildM0001Config(DALM0001Config &config)
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

void D0009_ReverseRates(MqlRates &rates[], const int count)
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

bool D0009_RatesToBars(MqlRates &raw[], const int copied, DALBar &bars[])
{
   if(copied <= 0)
      return false;
   if(copied > 1 && raw[0].time > raw[copied - 1].time)
      D0009_ReverseRates(raw, copied);
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

bool D0009_LoadPrefixBars(const int oldest_closed_shift, const int cursor_closed_shift, DALBar &bars[], int &bars_count, string &reason)
{
   ArrayResize(bars, 0);
   bars_count = 0;
   reason = "not_loaded";
   if(oldest_closed_shift < cursor_closed_shift)
   {
      reason = "bad_shift_order";
      return false;
   }
   datetime start_time = iTime(D0009_Symbol(), D0009_Timeframe(), oldest_closed_shift);
   datetime stop_time = iTime(D0009_Symbol(), D0009_Timeframe(), cursor_closed_shift);
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
   int copied = CopyRates(D0009_Symbol(), D0009_Timeframe(), start_time, stop_time, raw);
   if(copied <= 0)
   {
      reason = "copy_prefix_failed*err=" + IntegerToString(GetLastError());
      return false;
   }
   if(!D0009_RatesToBars(raw, copied, bars))
   {
      reason = "rates_to_bars_failed";
      return false;
   }
   bars_count = copied;
   reason = "ok_prefix_only";
   return true;
}

bool D0009_LoadForwardBars(const int cursor_closed_shift, const int max_forward_bars, DALBar &bars[], int &bars_count, string &reason)
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
   datetime start_time = iTime(D0009_Symbol(), D0009_Timeframe(), first_shift);
   datetime stop_time = iTime(D0009_Symbol(), D0009_Timeframe(), latest_shift);
   if(start_time <= 0 || stop_time <= 0)
   {
      reason = "bad_forward_itime";
      return false;
   }
   if(start_time > stop_time)
   {
      datetime t = start_time;
      start_time = stop_time;
      stop_time = t;
   }
   MqlRates raw[];
   int copied = CopyRates(D0009_Symbol(), D0009_Timeframe(), start_time, stop_time, raw);
   if(copied <= 0)
   {
      reason = "copy_forward_failed*err=" + IntegerToString(GetLastError());
      return false;
   }
   if(!D0009_RatesToBars(raw, copied, bars))
   {
      reason = "forward_rates_to_bars_failed";
      return false;
   }
   bars_count = copied;
   reason = "ok_outcome_only";
   return true;
}

int D0009_EventKnownIndex(const DALM0001Event &event)
{
   int base = event.exit_index;
   if(base < 0)
      base = event.touch_confirmed_index;
   if(base < 0)
      return -1;
   return base + MathMax(0, InpOutcomeCandleOffsetAfterExit);
}

bool D0009_EventEligibleForRegime(const DALM0001Event &event)
{
   if(!event.closed || !event.touch_confirmed)
      return false;
   if(InpRequireEventRtvReady && !event.rtv_ready)
      return false;
   return true;
}

bool D0009_ClassifyRawEvent(
   const DALM0001Event &event,
   const DALBar &bars[],
   const int bars_count,
   int &energy,
   int &direction,
   int &known_index
)
{
   energy = DAL_D0009_REGIME_UNKNOWN;
   direction = 0;
   known_index = D0009_EventKnownIndex(event);
   if(!D0009_EventEligibleForRegime(event))
      return false;
   if(known_index < 0 || known_index >= bars_count)
      return false;
   double close_price = bars[known_index].close;
   if(close_price == event.node_price)
      return false;

   bool low = (event.node_type == DAL_NODE_LOW);
   bool reversal = false;
   if(low)
      reversal = (close_price > event.node_price);
   else
      reversal = (close_price < event.node_price);

   energy = reversal ? DAL_D0009_REGIME_REVERSAL : DAL_D0009_REGIME_CONTINUATION;
   if(energy == DAL_D0009_REGIME_REVERSAL)
      direction = low ? +1 : -1;
   else
      direction = low ? -1 : +1;
   return true;
}

bool D0009_BuildLatestRawEventRegimeState(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const int decision_index,
   D0009RegimeState &state
)
{
   D0009_ResetRegime(state);
   state.reason = "no_raw_event_known";
   if(events_count <= 0 || bars_count <= 0 || decision_index < 0)
      return false;

   int latest_known = -1;
   for(int i = 0; i < events_count; i++)
   {
      int energy = DAL_D0009_REGIME_UNKNOWN;
      int dir = 0;
      int known = -1;
      if(!D0009_ClassifyRawEvent(events[i], bars, bars_count, energy, dir, known))
         continue;
      if(known <= decision_index && known > latest_known)
         latest_known = known;
   }

   if(latest_known < 0)
      return false;

   int batch = 0;
   int rev = 0;
   int cont = 0;
   int buy = 0;
   int sell = 0;
   for(int j = 0; j < events_count; j++)
   {
      int energy_j = DAL_D0009_REGIME_UNKNOWN;
      int dir_j = 0;
      int known_j = -1;
      if(!D0009_ClassifyRawEvent(events[j], bars, bars_count, energy_j, dir_j, known_j))
         continue;
      if(known_j != latest_known)
         continue;
      batch++;
      if(energy_j == DAL_D0009_REGIME_REVERSAL) rev++;
      if(energy_j == DAL_D0009_REGIME_CONTINUATION) cont++;
      if(dir_j > 0) buy++;
      if(dir_j < 0) sell++;
   }

   if(batch <= 0)
      return false;

   state.known_index = latest_known;
   state.known_time = (latest_known >= 0 && latest_known < bars_count ? bars[latest_known].time : 0);
   state.batch_count = batch;
   state.reversal_count = rev;
   state.continuation_count = cont;
   state.buy_direction_count = buy;
   state.sell_direction_count = sell;
   state.same_bar_batch_count = (batch > 1 ? 1 : 0);

   if(rev > 0 && cont > 0)
   {
      state.valid = false;
      state.ambiguous_energy = true;
      state.energy = DAL_D0009_REGIME_AMBIGUOUS;
      state.reason = "same_candle_raw_event_mixed_reversal_continuation";
      return false;
   }

   if(rev > 0)
      state.energy = DAL_D0009_REGIME_REVERSAL;
   else if(cont > 0)
      state.energy = DAL_D0009_REGIME_CONTINUATION;
   else
      state.energy = DAL_D0009_REGIME_UNKNOWN;

   if(buy > 0 && sell > 0)
   {
      state.ambiguous_direction = true;
      state.direction = 0;
   }
   else if(buy > 0)
      state.direction = +1;
   else if(sell > 0)
      state.direction = -1;
   else
      state.direction = 0;

   state.valid = (state.energy == DAL_D0009_REGIME_REVERSAL || state.energy == DAL_D0009_REGIME_CONTINUATION);
   state.reason = (state.valid ? "ok_raw_event_batch_no_samples" : "unknown_energy");
   return state.valid;
}

bool D0009_KeyExists(const string key)
{
   for(int i = 0; i < ArraySize(g_keys); i++)
      if(g_keys[i] == key)
         return true;
   return false;
}

void D0009_AddKey(const string key)
{
   if(key == "" || D0009_KeyExists(key))
      return;
   int n = ArraySize(g_keys);
   ArrayResize(g_keys, n + 1);
   g_keys[n] = key;
}

string D0009_NodeFamilyKey(const string family, const DALLRuleNode &node)
{
   return family + "_" + IntegerToString((int)node.type) + "_" + IntegerToString((long)node.time) + "_" + DoubleToString(node.price, 10);
}

bool D0009_BuildLiveTerritory(const DALBar &bars[], const int bars_count, const DALLRuleNode &node, double &lower, double &upper, bool &hunted)
{
   lower = node.price;
   upper = node.price;
   hunted = false;
   if(bars_count <= 0 || node.active_from_index < 0 || node.active_from_index >= bars_count)
      return false;
   double extreme = DAL_M0001InitialExtreme(node.type, bars[node.active_from_index]);
   for(int i = node.active_from_index; i < bars_count; i++)
   {
      extreme = DAL_M0001UpdateExtreme(node.type, extreme, bars[i]);
      DAL_M0001Territory(node.type, node.price, extreme, InpZoneRatio, lower, upper);
      if(DAL_M0001Hunted(node.type, node.price, bars[i]))
         hunted = true;
   }
   return true;
}

bool D0009_NodeTouchedBeforeDecision(const DALBar &bars[], const int bars_count, const DALLRuleNode &node)
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
      if(DAL_CandleIntersectsZone(bars[i].low, bars[i].high, lower, upper))
         return true;
      if(DAL_M0001Hunted(node.type, node.price, bars[i]))
         return true;
   }
   return false;
}

bool D0009_NodeHasRawEvent(const DALM0001Event &events[], const int events_count, const int node_id)
{
   for(int i = 0; i < events_count; i++)
      if(events[i].node_id == node_id)
         return true;
   return false;
}

bool D0009_PassesDirectionFilter(const int candidate_direction, const D0009RegimeState &state)
{
   if(!InpUseCausalDirectionFilter)
      return true;
   if(state.direction == 0)
      return false;
   return (candidate_direction == state.direction);
}

double D0009_ActivationAtr(const DALBar &bars[], const int bars_count)
{
   int period = MathMax(1, InpAtrPeriod);
   if(bars_count < 2)
      return 0.0;
   int last = bars_count - 1;
   int first = MathMax(1, last - period + 1);
   double sum = 0.0;
   int n = 0;
   for(int i = first; i <= last; i++)
   {
      double prev_close = bars[i - 1].close;
      double tr1 = bars[i].high - bars[i].low;
      double tr2 = MathAbs(bars[i].high - prev_close);
      double tr3 = MathAbs(bars[i].low - prev_close);
      double tr = MathMax(tr1, MathMax(tr2, tr3));
      if(tr > 0.0)
      {
         sum += tr;
         n++;
      }
   }
   return (n > 0 ? sum / n : 0.0);
}

bool D0009_AddCandidateToSlots(D0009Candidate &slots[], int &slot_count, const int max_slots, const D0009Candidate &c)
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

bool D0009_BuildCandidate(
   const string family,
   const DALBar &bars[],
   const int bars_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALLRuleNode &node,
   const D0009RegimeState &state,
   const double spread_price,
   D0009Candidate &c,
   string &reason
)
{
   D0009_ResetCandidate(c);
   reason = "not_candidate";
   int last_index = bars_count - 1;
   if(!node.confirmed || node.active_from_index < 0 || node.active_from_index > last_index)
   {
      reason = "node_not_live_confirmed";
      return false;
   }

   if(InpSkipTouchedOrClosedNodesBeforeDecision)
   {
      if(D0009_NodeHasRawEvent(events, events_count, node.id))
      {
         reason = "node_has_raw_event_in_prefix";
         return false;
      }
      if(D0009_NodeTouchedBeforeDecision(bars, bars_count, node))
      {
         reason = "node_touched_or_hunted_in_prefix";
         return false;
      }
   }

   double lower = node.price;
   double upper = node.price;
   bool hunted = false;
   if(!D0009_BuildLiveTerritory(bars, bars_count, node, lower, upper, hunted))
   {
      reason = "territory_failed";
      return false;
   }

   double market = bars[last_index].close;
   int dir = 0;
   double entry_hint = 0.0;
   double structural_stop = 0.0;
   double dist = 0.0;

   if(family == "REV")
   {
      if(node.type == DAL_NODE_LOW)
      {
         if(!(upper < market)) { reason = "rev_buy_zone_not_below_market"; return false; }
         dir = +1;
         entry_hint = upper + spread_price;
         structural_stop = lower;
         dist = market - upper;
      }
      else
      {
         if(!(lower > market)) { reason = "rev_sell_zone_not_above_market"; return false; }
         dir = -1;
         entry_hint = lower;
         structural_stop = upper + spread_price;
         dist = lower - market;
      }
   }
   else if(family == "CONT")
   {
      if(node.type == DAL_NODE_HIGH)
      {
         if(!(upper > market)) { reason = "cont_buy_break_zone_not_above_market"; return false; }
         dir = +1;
         structural_stop = lower;
         dist = upper - market;
      }
      else
      {
         if(!(lower < market)) { reason = "cont_sell_break_zone_not_below_market"; return false; }
         dir = -1;
         structural_stop = upper + spread_price;
         dist = market - lower;
      }
   }
   else
   {
      reason = "unknown_family";
      return false;
   }

   if(!D0009_PassesDirectionFilter(dir, state))
   {
      reason = "direction_filter_rejected";
      return false;
   }

   string key = D0009_NodeFamilyKey(family, node);
   if(InpOneActivationPerNodeFamily && D0009_KeyExists(key))
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
   c.structural_stop_price = structural_stop;
   c.activation_atr = D0009_ActivationAtr(bars, bars_count);
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

void D0009_SelectCandidates(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   const D0009RegimeState &state,
   D0009Candidate &out_candidates[],
   int &out_count
)
{
   ArrayResize(out_candidates, 0);
   out_count = 0;

   double point = SymbolInfoDouble(D0009_Symbol(), SYMBOL_POINT);
   if(point <= 0.0) point = 0.0;
   double spread_price = MathMax(0, InpAuditSpreadPoints) * point;

   D0009Candidate rev_buy[];
   D0009Candidate rev_sell[];
   D0009Candidate cont_buy[];
   D0009Candidate cont_sell[];
   int rb = 0, rs = 0, cb = 0, cs = 0;

   for(int i = 0; i < nodes_count; i++)
   {
      if((InpFamiliesToAudit == DAL_D0009_BOTH || InpFamiliesToAudit == DAL_D0009_REVERSAL_ONLY) && state.energy == DAL_D0009_REGIME_REVERSAL)
      {
         D0009Candidate c;
         string reason = "";
         if(D0009_BuildCandidate("REV", bars, bars_count, events, events_count, nodes[i], state, spread_price, c, reason))
         {
            if(c.direction > 0)
               D0009_AddCandidateToSlots(rev_buy, rb, MathMax(0, InpReversalBuySlots), c);
            else if(c.direction < 0)
               D0009_AddCandidateToSlots(rev_sell, rs, MathMax(0, InpReversalSellSlots), c);
         }
      }

      if((InpFamiliesToAudit == DAL_D0009_BOTH || InpFamiliesToAudit == DAL_D0009_CONTINUATION_ONLY) && state.energy == DAL_D0009_REGIME_CONTINUATION)
      {
         D0009Candidate c2;
         string reason2 = "";
         if(D0009_BuildCandidate("CONT", bars, bars_count, events, events_count, nodes[i], state, spread_price, c2, reason2))
         {
            if(c2.direction > 0)
               D0009_AddCandidateToSlots(cont_buy, cb, MathMax(0, InpContinuationBuySlots), c2);
            else if(c2.direction < 0)
               D0009_AddCandidateToSlots(cont_sell, cs, MathMax(0, InpContinuationSellSlots), c2);
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

bool D0009_EntryTriggeredOnBar(const D0009Candidate &c, const DALBar &bar)
{
   if(c.family == "REV")
      return DAL_CandleIntersectsZone(bar.low, bar.high, c.zone_lower, c.zone_upper);

   if(c.family == "CONT")
   {
      if(c.direction > 0)
      {
         if(InpContinuationBreakMode == DAL_D0009_CONT_CLOSE_BREAK)
            return bar.close > c.zone_upper;
         return bar.high > c.zone_upper;
      }
      if(c.direction < 0)
      {
         if(InpContinuationBreakMode == DAL_D0009_CONT_CLOSE_BREAK)
            return bar.close < c.zone_lower;
         return bar.low < c.zone_lower;
      }
   }
   return false;
}

double D0009_EntryPriceForTriggeredBar(const D0009Candidate &c, const DALBar &bar, const double spread_price)
{
   if(c.family == "REV")
      return c.entry_hint_price;

   if(c.direction > 0)
   {
      if(InpContinuationBreakMode == DAL_D0009_CONT_CLOSE_BREAK)
         return bar.close + spread_price;
      return c.zone_upper + spread_price;
   }
   if(c.direction < 0)
   {
      if(InpContinuationBreakMode == DAL_D0009_CONT_CLOSE_BREAK)
         return bar.close;
      return c.zone_lower;
   }
   return bar.close;
}

double D0009_StopForEntry(const D0009Candidate &c, const double entry_price)
{
   if(c.family == "CONT" && InpContinuationRiskMode == DAL_D0009_CONT_RISK_ATR)
   {
      double atr_risk = c.activation_atr * MathMax(0.1, InpAtrMultiplier);
      if(atr_risk > 0.0)
         return (c.direction > 0 ? entry_price - atr_risk : entry_price + atr_risk);
   }
   return c.structural_stop_price;
}

void D0009_MeasureFromEntryIndex(const D0009Candidate &c, const DALBar &bars[], const int bars_count, const int entry_index, const double entry_price, D0009TradeResult &r)
{
   if(entry_index < 0 || entry_index >= bars_count)
   {
      r.reason = "bad_entry_index";
      return;
   }

   double stop = D0009_StopForEntry(c, entry_price);
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

void D0009_ReplayCandidate(const D0009Candidate &c, const int cursor_shift, const datetime activation_time, D0009TradeResult &r)
{
   D0009_ResetTrade(r);
   r.activation_time = activation_time;
   int max_forward = MathMax(1, InpMaxBarsToWaitForEntry) + MathMax(1, InpMaxBarsToMeasureAfterEntry) + 2;
   DALBar future[];
   int future_count = 0;
   string load_reason = "";
   if(!D0009_LoadForwardBars(cursor_shift, max_forward, future, future_count, load_reason))
   {
      r.reason = load_reason;
      r.outcome = "no_forward_bars";
      return;
   }

   int max_wait = MathMin(future_count, MathMax(1, InpMaxBarsToWaitForEntry));
   int entry_i = -1;
   for(int i = 0; i < max_wait; i++)
   {
      if(D0009_EntryTriggeredOnBar(c, future[i]))
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

   double point = SymbolInfoDouble(D0009_Symbol(), SYMBOL_POINT);
   if(point <= 0.0) point = 0.0;
   double spread_price = MathMax(0, InpAuditSpreadPoints) * point;
   double entry_price = D0009_EntryPriceForTriggeredBar(c, future[entry_i], spread_price);

   r.entered = true;
   r.entry_time = future[entry_i].time;
   r.bars_to_entry = entry_i + 1;
   r.outcome = "entered";
   r.reason = "entry_triggered_after_raw_event_regime_known";
   D0009_MeasureFromEntryIndex(c, future, future_count, entry_i, entry_price, r);
}

void D0009_AddStats(D0009FamilyStats &s, const D0009TradeResult &r)
{
   s.candidates++;
   if(r.entered) s.entered++; else s.unfilled++;
   if(r.measured)
   {
      s.measured++;
      s.sum_mfe_r += r.mfe_r;
      s.sum_mae_r += r.mae_r;
      s.sum_realized_r += r.realized_r;
      if(r.realized_r > 0.0)
      {
         s.wins++;
         s.gross_win_r += r.realized_r;
      }
      else if(r.realized_r < 0.0)
      {
         s.losses++;
         s.gross_loss_r += MathAbs(r.realized_r);
      }
      else
         s.flats++;
   }
   if(r.hit_reward_before_stop) s.reward_hits++;
   if(r.hit_stop_before_reward) s.stop_hits++;
   if(r.same_bar_reward_stop) s.same_bar_reward_stop++;
   if(r.outcome == "open_after_measure_window") s.open_after_window++;
}

void D0009_Accumulate(const D0009Candidate &c, const D0009TradeResult &r)
{
   D0009_AddStats(g_sum.all, r);
   if(c.family == "REV")
      D0009_AddStats(g_sum.reversal, r);
   else if(c.family == "CONT")
      D0009_AddStats(g_sum.continuation, r);
}

void D0009_OpenCsv()
{
   if(!InpWriteCsv || g_csv != INVALID_HANDLE)
      return;
   g_csv = FileOpen(InpCsvFileName, FILE_WRITE | FILE_CSV | FILE_ANSI);
   if(g_csv == INVALID_HANDLE)
   {
      Print("DAL_D0009_CSV_OPEN_FAILED *** build=", DAL_D0009_BUILD, "*file=", InpCsvFileName, "*err=", GetLastError());
      return;
   }
   FileWrite(g_csv,
      "activation_time", "family", "energy", "regime_direction", "known_time", "known_index", "batch_count", "rev_count", "cont_count", "ambiguous_direction",
      "node_id", "node_type", "direction", "zone_lower", "zone_upper", "entry_price", "stop_price", "risk_price", "activation_atr",
      "entered", "entry_time", "bars_to_entry", "measured", "bars_measured", "mfe_r", "mae_r", "realized_r", "reward_hit", "stop_hit", "same_bar", "outcome", "reason");
}

void D0009_WriteCsv(const D0009Candidate &c, const D0009TradeResult &r)
{
   if(!InpWriteCsv)
      return;
   D0009_OpenCsv();
   if(g_csv == INVALID_HANDLE)
      return;
   FileWrite(g_csv,
      D0009_TimeText(r.activation_time), c.family, D0009_EnergyText(c.regime_energy), D0009_DirText(c.regime_direction), D0009_TimeText(c.regime_known_time), c.regime_known_index, c.regime_batch_count, c.regime_rev_count, c.regime_cont_count, D0009_BoolText(c.regime_ambiguous_direction),
      c.node.id, EnumToString(c.node.type), D0009_DirText(c.direction), DoubleToString(c.zone_lower, 10), DoubleToString(c.zone_upper, 10), DoubleToString(r.entry_price, 10), DoubleToString(r.stop_price, 10), DoubleToString(r.risk_price, 10), DoubleToString(c.activation_atr, 10),
      D0009_BoolText(r.entered), D0009_TimeText(r.entry_time), r.bars_to_entry, D0009_BoolText(r.measured), r.bars_measured, DoubleToString(r.mfe_r, 6), DoubleToString(r.mae_r, 6), DoubleToString(r.realized_r, 6), D0009_BoolText(r.hit_reward_before_stop), D0009_BoolText(r.hit_stop_before_reward), D0009_BoolText(r.same_bar_reward_stop), r.outcome, r.reason);
}

void D0009_PrintTrade(const int step, const D0009Candidate &c, const D0009TradeResult &r)
{
   Print("DAL_D0009_TRADE *** build=", DAL_D0009_BUILD,
      "*step=", step,
      "*family=", c.family,
      "*energy=", D0009_EnergyText(c.regime_energy),
      "*known=", D0009_TimeText(c.regime_known_time),
      "*batch=", c.regime_batch_count,
      "*nodeId=", c.node.id,
      "*dir=", D0009_DirText(c.direction),
      "*entered=", D0009_BoolText(r.entered),
      "*entryTime=", D0009_TimeText(r.entry_time),
      "*risk=", DoubleToString(r.risk_price, 6),
      "*mfeR=", DoubleToString(r.mfe_r, 4),
      "*maeR=", DoubleToString(r.mae_r, 4),
      "*realizedR=", DoubleToString(r.realized_r, 4),
      "*outcome=", r.outcome,
      "*reason=", r.reason);
}

void D0009_PrintFamilyStats(const string name, const D0009FamilyStats &s)
{
   double entry_rate = (s.candidates > 0 ? 100.0 * s.entered / s.candidates : 0.0);
   double win_rate = (s.measured > 0 ? 100.0 * s.wins / s.measured : 0.0);
   double loss_rate = (s.measured > 0 ? 100.0 * s.losses / s.measured : 0.0);
   double flat_rate = (s.measured > 0 ? 100.0 * s.flats / s.measured : 0.0);
   double reward_rate = (s.measured > 0 ? 100.0 * s.reward_hits / s.measured : 0.0);
   double stop_rate = (s.measured > 0 ? 100.0 * s.stop_hits / s.measured : 0.0);
   double avg_mfe = (s.measured > 0 ? s.sum_mfe_r / s.measured : 0.0);
   double avg_mae = (s.measured > 0 ? s.sum_mae_r / s.measured : 0.0);
   double expectancy = (s.measured > 0 ? s.sum_realized_r / s.measured : 0.0);
   double pf = (s.gross_loss_r > 0.0 ? s.gross_win_r / s.gross_loss_r : 0.0);
   double avg_win = (s.wins > 0 ? s.gross_win_r / s.wins : 0.0);
   double avg_loss = (s.losses > 0 ? s.gross_loss_r / s.losses : 0.0);
   Print("DAL_D0009_SUMMARY_", name, " *** build=", DAL_D0009_BUILD,
      "*contract=NO_M0002_SAMPLES_RAW_M0001_EVENT_BATCHES",
      "*candidates=", s.candidates,
      "*entered=", s.entered,
      "*entryRatePct=", DoubleToString(entry_rate, 2),
      "*measured=", s.measured,
      "*winRatePct=", DoubleToString(win_rate, 2),
      "*lossRatePct=", DoubleToString(loss_rate, 2),
      "*flatRatePct=", DoubleToString(flat_rate, 2),
      "*avgWinR=", DoubleToString(avg_win, 4),
      "*avgLossR=", DoubleToString(avg_loss, 4),
      "*profitFactor=", DoubleToString(pf, 4),
      "*expectancyR=", DoubleToString(expectancy, 4),
      "*rewardHitPct=", DoubleToString(reward_rate, 2),
      "*stopHitPct=", DoubleToString(stop_rate, 2),
      "*avgMfeR=", DoubleToString(avg_mfe, 4),
      "*avgMaeR=", DoubleToString(avg_mae, 4),
      "*sameBar=", s.same_bar_reward_stop,
      "*openAfterWindow=", s.open_after_window);
}

bool D0009_Run()
{
   D0009_ResetSummary(g_sum);
   ArrayResize(g_keys, 0);
   D0009_OpenCsv();

   int total = Bars(D0009_Symbol(), D0009_Timeframe());
   if(total <= 0)
   {
      Print("DAL_D0009_FAILED *** build=", DAL_D0009_BUILD, "*reason=no_bars");
      return false;
   }

   int replay = MathMax(200, InpReplayClosedBars);
   int oldest_shift = MathMin(total - 1, replay);
   int warmup = MathMax(InpWarmupClosedBars, InpL * 2 + InpAtrPeriod + InpExitGap + 50);
   if(oldest_shift <= warmup + 3)
   {
      Print("DAL_D0009_FAILED *** build=", DAL_D0009_BUILD, "*reason=not_enough_bars*oldestShift=", oldest_shift, "*warmup=", warmup);
      return false;
   }

   Print("DAL_D0009_START *** build=", DAL_D0009_BUILD,
      "*symbol=", D0009_Symbol(),
      "*tf=", EnumToString(D0009_Timeframe()),
      "*mode=atomic_no_sample_live_replay",
      "*contract=no_branch_samples_raw_M0001_events_only",
      "*continuationRisk=", EnumToString(InpContinuationRiskMode),
      "*continuationBreak=", EnumToString(InpContinuationBreakMode));

   for(int cursor_shift = oldest_shift - warmup; cursor_shift >= 2; cursor_shift--)
   {
      g_sum.steps++;
      int step = g_sum.steps;
      DALBar bars[];
      int bars_count = 0;
      string load_reason = "";
      if(!D0009_LoadPrefixBars(oldest_shift, cursor_shift, bars, bars_count, load_reason))
      {
         g_sum.load_failures++;
         continue;
      }
      if(bars_count <= InpL * 2 + InpAtrPeriod + 20)
         continue;

      g_sum.decision_steps++;
      int decision_index = bars_count - 1;

      DALM0001Config m1;
      D0009_BuildM0001Config(m1);
      DALLRuleNode nodes[];
      int nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, m1.L, nodes);
      DALM0001Event events[];
      int events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);
      g_sum.raw_events_seen += events_count;
      if(events_count <= 0)
      {
         g_sum.no_event_steps++;
         continue;
      }

      D0009RegimeState state;
      bool has_state = D0009_BuildLatestRawEventRegimeState(events, events_count, bars, bars_count, decision_index, state);
      if(state.same_bar_batch_count > 0) g_sum.same_bar_batch_steps++;
      if(state.ambiguous_direction) g_sum.mixed_direction_steps++;
      if(!has_state)
      {
         if(state.ambiguous_energy) g_sum.ambiguous_energy_steps++;
         else g_sum.no_regime_steps++;
         if(InpSkipAmbiguousEnergyBatch)
            continue;
      }
      if(!state.valid)
         continue;

      g_sum.raw_events_used_for_regime += state.batch_count;
      if(state.energy == DAL_D0009_REGIME_REVERSAL) g_sum.reversal_regime_steps++;
      if(state.energy == DAL_D0009_REGIME_CONTINUATION) g_sum.continuation_regime_steps++;

      D0009Candidate candidates[];
      int candidates_count = 0;
      D0009_SelectCandidates(bars, bars_count, nodes, nodes_count, events, events_count, state, candidates, candidates_count);
      if(candidates_count <= 0)
         continue;

      datetime activation_time = bars[decision_index].time;
      for(int c = 0; c < candidates_count; c++)
      {
         if(!candidates[c].valid)
            continue;
         if(InpOneActivationPerNodeFamily)
            D0009_AddKey(candidates[c].key);
         D0009TradeResult r;
         D0009_ReplayCandidate(candidates[c], cursor_shift, activation_time, r);
         D0009_Accumulate(candidates[c], r);
         D0009_WriteCsv(candidates[c], r);
         if(!InpPrintOnlySummary && (step % MathMax(1, InpPrintEveryNSteps) == 0 || r.same_bar_reward_stop || !r.entered))
            D0009_PrintTrade(step, candidates[c], r);
      }
   }

   if(g_csv != INVALID_HANDLE)
      FileFlush(g_csv);

   Print("DAL_D0009_AUDIT *** build=", DAL_D0009_BUILD,
      "*sampleCalls=0",
      "*branchSamplesBuilt=0",
      "*contract=no_samples_raw_events_only",
      "*steps=", g_sum.steps,
      "*decisionSteps=", g_sum.decision_steps,
      "*loadFailures=", g_sum.load_failures,
      "*rawEventsSeen=", g_sum.raw_events_seen,
      "*rawEventsUsedForRegime=", g_sum.raw_events_used_for_regime,
      "*noEventSteps=", g_sum.no_event_steps,
      "*noRegimeSteps=", g_sum.no_regime_steps,
      "*sameBarBatchSteps=", g_sum.same_bar_batch_steps,
      "*ambiguousEnergySteps=", g_sum.ambiguous_energy_steps,
      "*mixedDirectionSteps=", g_sum.mixed_direction_steps,
      "*reversalRegimeSteps=", g_sum.reversal_regime_steps,
      "*continuationRegimeSteps=", g_sum.continuation_regime_steps);

   D0009_PrintFamilyStats("ALL", g_sum.all);
   D0009_PrintFamilyStats("REVERSAL", g_sum.reversal);
   D0009_PrintFamilyStats("CONTINUATION", g_sum.continuation);
   return true;
}

int OnInit()
{
   D0009_Run();
   if(g_csv != INVALID_HANDLE)
   {
      FileClose(g_csv);
      g_csv = INVALID_HANDLE;
   }
   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   if(g_csv != INVALID_HANDLE)
   {
      FileClose(g_csv);
      g_csv = INVALID_HANDLE;
   }
}

void OnTick()
{
}
