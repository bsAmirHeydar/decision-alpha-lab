//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0004 H0005 Continuation Heikin Ashi Flip    |
//| Continuation-direction HA color flip, fixed 1:2 by default         |
//+------------------------------------------------------------------+
#property strict
#property version   "1.02"
#property description "Execution module E0004: continuation-direction Heikin Ashi color flip, fixed-R market entries."

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0002/DAL_M0002Engine.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecRisk.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecReversalOneToOne.mqh>

// Minimal public inputs for the fourth H5 execution path.
input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 1500;

// Shared H5/M0001 structure and regime source.
input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

enum ENUM_E0004RegimeBasis
{
   E0004_REGIME_LAST_COMPLETED_BRANCH = 0,
   E0004_REGIME_HUMAN_CONTEXT_COMBINED = 1
};

enum ENUM_E0004HumanContextSignal
{
   E0004_HUMAN_CONTEXT_NEUTRAL = 0,
   E0004_HUMAN_CONTEXT_REVERSAL = 1,
   E0004_HUMAN_CONTEXT_CONTINUATION = 2
};

input ENUM_E0004RegimeBasis InpRegimeBasis = E0004_REGIME_LAST_COMPLETED_BRANCH;
input ENUM_E0004HumanContextSignal InpHumanContextSignal = E0004_HUMAN_CONTEXT_NEUTRAL;

// Optional higher-timeframe regime filter. Off by default to keep current tests unchanged.
input bool InpUseHigherTimeframeRegimeFilter = false;
input ENUM_TIMEFRAMES InpHigherRegimeTimeframe = PERIOD_H1;

// Trading session. Broker time, strict: start <= time < end.
input bool InpUseTradingSessionFilter = true;
input int InpTradingStartHour = 0;
input int InpTradingStartMinute = 0;
input int InpTradingEndHour = 23;
input int InpTradingEndMinute = 59;

// Risk/entry policy.
input long InpMagicNumber = 5004004;
input double InpRiskCash = 100.0;
input double InpRewardR = 2.0;
input bool InpAllowSimultaneousTrades = true;
input int InpContinuationBreakBufferPoints = 0;

// Internal fixed policy. These are not tester inputs.
#define DAL_E0004_BUILD "1.02"
string InpOrderCommentPrefix = "DALH4";
int InpRegimeLookbackBars = 100;
int InpOutcomeCandleOffsetAfterExit = 0;
int InpBrokerUtcOffsetHours = 0;
bool InpUseClosedBarsOnly = true;
bool InpTradingEnabled = true;
bool InpAllowMinLotIfRiskTooSmall = false;
double InpCommissionPerLotRoundTurn = 0.0;
int InpDirectionLookbackBars = 300;
bool InpPrintOrderLogs = false;

CTrade g_trade;
datetime g_last_open_bar_time = 0;

string LabSymbol()
{
   if(InpSymbol == "")
      return _Symbol;
   return InpSymbol;
}

ENUM_TIMEFRAMES LabTimeframe()
{
   if(InpTimeframe == PERIOD_CURRENT)
      return (ENUM_TIMEFRAMES)_Period;
   return InpTimeframe;
}

int E0004_ClampInt(const int value, const int lo, const int hi)
{
   if(value < lo)
      return lo;
   if(value > hi)
      return hi;
   return value;
}

string E0004_TwoDigits(const int value)
{
   if(value < 10)
      return "0" + IntegerToString(value);
   return IntegerToString(value);
}

string E0004_FormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

bool E0004_IsTradingSessionOpen(string &reason)
{
   if(!InpUseTradingSessionFilter)
   {
      reason = "timeFilter=OFF";
      return true;
   }

   int start_hour = E0004_ClampInt(InpTradingStartHour, 0, 23);
   int start_minute = E0004_ClampInt(InpTradingStartMinute, 0, 59);
   int end_hour = E0004_ClampInt(InpTradingEndHour, 0, 23);
   int end_minute = E0004_ClampInt(InpTradingEndMinute, 0, 59);
   int start = start_hour * 60 + start_minute;
   int finish = end_hour * 60 + end_minute;

   datetime now_time = TimeCurrent();
   MqlDateTime dt;
   TimeToStruct(now_time, dt);
   int now_minute = dt.hour * 60 + dt.min;

   bool open = false;
   if(start == finish)
      open = true;
   else if(start < finish)
      open = (now_minute >= start && now_minute < finish);
   else
      open = (now_minute >= start || now_minute < finish);

   reason = "timeFilter=ON*now=" + E0004_FormatDateTime(now_time)
      + "*window=" + E0004_TwoDigits(start_hour) + ":" + E0004_TwoDigits(start_minute)
      + "-" + E0004_TwoDigits(end_hour) + ":" + E0004_TwoDigits(end_minute)
      + "*open=" + DAL_BoolToString(open);
   return open;
}

string E0004_ManagedCommentPrefix()
{
   return InpOrderCommentPrefix;
}

string E0004_BarComment(const datetime signal_time, const int direction)
{
   string side = (direction > 0 ? "B" : "S");
   return E0004_ManagedCommentPrefix() + side + "T" + IntegerToString((int)signal_time);
}

void E0004_BuildM0001Config(DALM0001Config &config)
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

void E0004_BuildM0002Config(DALM0002Config &config)
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

bool E0004_HasNewOpenCandle()
{
   datetime current_open = iTime(LabSymbol(), LabTimeframe(), 0);
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

string E0004_RegimeOutcomeToString(const ENUM_DALM0002Outcome outcome)
{
   if(outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
      return "REVERSAL";
   if(outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      return "CONTINUATION";
   return "UNKNOWN";
}

bool E0004_ResolveEffectiveContinuation(DALM0002BranchSample &last_sample, const bool has_last_sample, string &reason)
{
   if(!has_last_sample)
   {
      reason = "no_last_branch";
      return false;
   }

   bool last_reversal = (last_sample.outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT);
   bool last_continuation = (last_sample.outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT);

   if(InpRegimeBasis == E0004_REGIME_LAST_COMPLETED_BRANCH)
   {
      reason = "regimeBasis=LAST_COMPLETED_BRANCH*last=" + E0004_RegimeOutcomeToString(last_sample.outcome);
      return last_continuation;
   }

   if(InpHumanContextSignal == E0004_HUMAN_CONTEXT_REVERSAL)
   {
      last_sample.outcome = DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT;
      reason = "regimeBasis=HUMAN_CONTEXT_COMBINED*human=REVERSAL*last=" + (last_reversal ? "REVERSAL" : (last_continuation ? "CONTINUATION" : "UNKNOWN"));
      return false;
   }

   if(InpHumanContextSignal == E0004_HUMAN_CONTEXT_CONTINUATION)
   {
      last_sample.outcome = DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT;
      reason = "regimeBasis=HUMAN_CONTEXT_COMBINED*human=CONTINUATION*last=" + (last_reversal ? "REVERSAL" : (last_continuation ? "CONTINUATION" : "UNKNOWN"));
      return true;
   }

   reason = "regimeBasis=HUMAN_CONTEXT_COMBINED*human=NEUTRAL*last=" + E0004_RegimeOutcomeToString(last_sample.outcome);
   return last_continuation;
}

bool E0004_PassesHigherTimeframeRegimeFilter(const ENUM_DALM0002Outcome required_outcome, string &reason)
{
   if(!InpUseHigherTimeframeRegimeFilter)
   {
      reason = "htfRegimeFilter=OFF";
      return true;
   }

   ENUM_TIMEFRAMES htf = InpHigherRegimeTimeframe;
   if(htf == PERIOD_CURRENT)
      htf = LabTimeframe();

   DALBar htf_bars[];
   int htf_bars_count = DAL_LoadBarsChronological(LabSymbol(), htf, InpBars, true, htf_bars);
   if(InpUseClosedBarsOnly && htf_bars_count > 1)
   {
      htf_bars_count--;
      ArrayResize(htf_bars, htf_bars_count);
   }

   if(htf_bars_count <= InpL * 2 + 10)
   {
      reason = "htfRegimeFilter=ON*tf=" + EnumToString(htf) + "*reason=not_enough_bars";
      return false;
   }

   DALM0001Config htf_m1;
   E0004_BuildM0001Config(htf_m1);

   DALLRuleNode htf_nodes[];
   int htf_nodes_count = DAL_DetectConfirmedStructuralNodes(htf_bars, htf_bars_count, htf_m1.L, htf_nodes);

   DALM0001Event htf_events[];
   int htf_events_count = DAL_M0001ComputeEvents(htf_bars, htf_bars_count, htf_nodes, htf_nodes_count, htf_m1, htf_events);

   DALM0002Config htf_m2;
   E0004_BuildM0002Config(htf_m2);

   DALM0002BranchSample htf_last_sample;
   int htf_last_event_index = -1;
   bool htf_has_last_sample = DAL_ExecFindLatestBranchSampleFast(htf_events, htf_events_count, htf_bars, htf_bars_count, 0, htf_m2, htf_last_sample, htf_last_event_index);
   if(!htf_has_last_sample)
   {
      reason = "htfRegimeFilter=ON*tf=" + EnumToString(htf) + "*reason=no_last_branch";
      return false;
   }

   bool pass = (htf_last_sample.outcome == required_outcome);
   reason = "htfRegimeFilter=ON*tf=" + EnumToString(htf)
      + "*last=" + E0004_RegimeOutcomeToString(htf_last_sample.outcome)
      + "*required=" + E0004_RegimeOutcomeToString(required_outcome)
      + "*pass=" + DAL_BoolToString(pass);
   return pass;
}


bool E0004_LoadClosedContext(
   DALBar &bars[],
   int &bars_count,
   DALLRuleNode &nodes[],
   int &nodes_count,
   DALM0001Event &events[],
   int &events_count,
   DALM0002BranchSample &last_sample,
   bool &is_continuation,
   string &reason
)
{
   ArrayResize(bars, 0);
   ArrayResize(nodes, 0);
   ArrayResize(events, 0);
   bars_count = 0;
   nodes_count = 0;
   events_count = 0;
   is_continuation = false;
   reason = "not_loaded";

   bars_count = DAL_LoadBarsChronological(LabSymbol(), LabTimeframe(), InpBars, true, bars);
   if(InpUseClosedBarsOnly && bars_count > 1)
   {
      bars_count--;
      ArrayResize(bars, bars_count);
   }

   if(bars_count <= InpL * 2 + 20)
   {
      reason = "not_enough_bars";
      return false;
   }

   DALM0001Config m1;
   E0004_BuildM0001Config(m1);
   nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, m1.L, nodes);
   events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);

   DALM0002Config m2;
   E0004_BuildM0002Config(m2);

   int last_event_index = -1;
   bool has_last_sample = DAL_ExecFindLatestBranchSampleFast(events, events_count, bars, bars_count, 0, m2, last_sample, last_event_index);

   string regime_reason = "";
   is_continuation = E0004_ResolveEffectiveContinuation(last_sample, has_last_sample, regime_reason);
   reason = regime_reason;

   if(is_continuation)
   {
      string htf_regime_reason = "";
      if(!E0004_PassesHigherTimeframeRegimeFilter(DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT, htf_regime_reason))
      {
         is_continuation = false;
         reason = regime_reason + "*" + htf_regime_reason;
      }
      else
      {
         reason = regime_reason + "*" + htf_regime_reason;
      }
   }

   return has_last_sample;
}

int E0004_Sign(const double value)
{
   if(value > 0.0)
      return +1;
   if(value < 0.0)
      return -1;
   return 0;
}

bool E0004_ComputeHeikinAshiPair(
   const DALBar &bars[],
   const int bars_count,
   const int signal_index,
   int &prev_color,
   int &signal_color,
   double &signal_ha_low,
   double &signal_ha_high,
   double &recent3_stop_low,
   double &recent3_stop_high,
   string &reason
)
{
   prev_color = 0;
   signal_color = 0;
   signal_ha_low = 0.0;
   signal_ha_high = 0.0;
   recent3_stop_low = 0.0;
   recent3_stop_high = 0.0;
   reason = "not_computed";

   if(signal_index < 1 || signal_index >= bars_count)
   {
      reason = "bad_signal_index";
      return false;
   }

   double ha_open[];
   double ha_close[];
   double ha_high[];
   double ha_low[];
   ArrayResize(ha_open, signal_index + 1);
   ArrayResize(ha_close, signal_index + 1);
   ArrayResize(ha_high, signal_index + 1);
   ArrayResize(ha_low, signal_index + 1);

   for(int i = 0; i <= signal_index; i++)
   {
      ha_close[i] = (bars[i].open + bars[i].high + bars[i].low + bars[i].close) / 4.0;
      if(i == 0)
         ha_open[i] = (bars[i].open + bars[i].close) / 2.0;
      else
         ha_open[i] = (ha_open[i - 1] + ha_close[i - 1]) / 2.0;

      ha_high[i] = MathMax(bars[i].high, MathMax(ha_open[i], ha_close[i]));
      ha_low[i] = MathMin(bars[i].low, MathMin(ha_open[i], ha_close[i]));
   }

   prev_color = E0004_Sign(ha_close[signal_index - 1] - ha_open[signal_index - 1]);
   signal_color = E0004_Sign(ha_close[signal_index] - ha_open[signal_index]);
   signal_ha_low = ha_low[signal_index];
   signal_ha_high = ha_high[signal_index];

   int first_stop_index = MathMax(0, signal_index - 2);
   recent3_stop_low = signal_ha_low;
   recent3_stop_high = signal_ha_high;
   for(int j = first_stop_index; j <= signal_index; j++)
   {
      // Use the farther stop from both the real candle and the Heikin Ashi candle.
      // Buy stop: lowest low behind the last three candles.
      // Sell stop: highest high behind the last three candles, spread is added later.
      recent3_stop_low = MathMin(recent3_stop_low, MathMin(bars[j].low, ha_low[j]));
      recent3_stop_high = MathMax(recent3_stop_high, MathMax(bars[j].high, ha_high[j]));
   }

   if(prev_color == 0 || signal_color == 0)
   {
      reason = "heikin_ashi_doji";
      return false;
   }

   if(prev_color == signal_color)
   {
      reason = "heikin_ashi_no_color_flip";
      return false;
   }

   reason = "ok";
   return true;
}

bool E0004_DetectContinuationDirection(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int signal_index,
   int &direction,
   string &reason
)
{
   direction = 0;
   reason = "no_recent_close_hunt_direction";
   if(signal_index < 0 || signal_index >= bars_count)
      return false;

   double point = SymbolInfoDouble(LabSymbol(), SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.0;
   double close_buffer = MathMax(0, InpContinuationBreakBufferPoints) * point;
   int first_bar = MathMax(0, signal_index - MathMax(1, InpDirectionLookbackBars));

   for(int b = signal_index; b >= first_bar; b--)
   {
      double close_price = bars[b].close;
      for(int n = nodes_count - 1; n >= 0; n--)
      {
         DALLRuleNode node = nodes[n];
         if(!node.confirmed)
            continue;
         if(node.active_from_index < 0 || node.active_from_index > b)
            continue;

         if(node.type == DAL_NODE_HIGH && close_price > node.price + close_buffer)
         {
            direction = +1;
            reason = "latest_high_node_close_hunt_up*bar=" + E0004_FormatDateTime(bars[b].time) + "*nodeId=" + IntegerToString(node.id);
            return true;
         }

         if(node.type == DAL_NODE_LOW && close_price < node.price - close_buffer)
         {
            direction = -1;
            reason = "latest_low_node_close_hunt_down*bar=" + E0004_FormatDateTime(bars[b].time) + "*nodeId=" + IntegerToString(node.id);
            return true;
         }
      }
   }

   return false;
}

bool E0004_HasManagedOpenPosition()
{
   string symbol = LabSymbol();
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;
      string comment = PositionGetString(POSITION_COMMENT);
      if(DAL_ExecOrderCommentMatchesPrefix(comment, E0004_ManagedCommentPrefix()))
         return true;
   }
   return false;
}

bool E0004_ManagedCommentExists(const string comment)
{
   if(DAL_ExecOrderCommentExists(LabSymbol(), InpMagicNumber, comment))
      return true;

   string symbol = LabSymbol();
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;
      if(PositionGetString(POSITION_COMMENT) == comment)
         return true;
   }

   return false;
}

bool E0004_CheckMarketGeometry(const int direction, const double sl, const double tp, string &reason)
{
   string symbol = LabSymbol();
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int stops_level = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_dist = MathMax(0.0, stops_level * point);

   if(point <= 0.0 || bid <= 0.0 || ask <= 0.0)
   {
      reason = "invalid_market_quote";
      return false;
   }

   if(direction > 0)
   {
      if(!(sl < ask))
      {
         reason = "buy_sl_not_below_ask";
         return false;
      }
      if(!(tp > ask))
      {
         reason = "buy_tp_not_above_ask";
         return false;
      }
      if((ask - sl) < min_dist || (tp - ask) < min_dist)
      {
         reason = "buy_sl_or_tp_too_close";
         return false;
      }
      reason = "ok";
      return true;
   }

   if(direction < 0)
   {
      if(!(sl > bid))
      {
         reason = "sell_sl_not_above_bid";
         return false;
      }
      if(!(tp < bid))
      {
         reason = "sell_tp_not_below_bid";
         return false;
      }
      if((sl - bid) < min_dist || (bid - tp) < min_dist)
      {
         reason = "sell_sl_or_tp_too_close";
         return false;
      }
      reason = "ok";
      return true;
   }

   reason = "zero_direction";
   return false;
}

bool E0004_PlaceHeikinAshiMarket(
   const int direction,
   const double signal_ha_low,
   const double signal_ha_high,
   const double recent3_stop_low,
   const double recent3_stop_high,
   const datetime signal_time,
   const string direction_reason,
   string &reason
)
{
   reason = "not_sent";
   string symbol = LabSymbol();

   if(!InpAllowSimultaneousTrades && E0004_HasManagedOpenPosition())
   {
      reason = "simultaneous_trade_blocked";
      return false;
   }

   string comment = E0004_BarComment(signal_time, direction);
   if(E0004_ManagedCommentExists(comment))
   {
      reason = "signal_already_traded";
      return false;
   }

   double entry = (direction > 0 ? SymbolInfoDouble(symbol, SYMBOL_ASK) : SymbolInfoDouble(symbol, SYMBOL_BID));
   if(entry <= 0.0)
   {
      reason = "invalid_entry_quote";
      return false;
   }

   double reward = MathMax(0.1, InpRewardR);
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double spread = 0.0;
   if(bid > 0.0 && ask > 0.0 && ask >= bid)
      spread = ask - bid;

   double sl = 0.0;
   if(direction > 0)
      sl = MathMin(signal_ha_low, recent3_stop_low);
   else
      sl = MathMax(signal_ha_high, recent3_stop_high) + spread;

   double risk = MathAbs(entry - sl);
   if(risk <= 0.0)
   {
      reason = "invalid_recent3_heikin_ashi_stop_risk";
      return false;
   }

   double tp = (direction > 0 ? entry + risk * reward : entry - risk * reward);
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   entry = NormalizeDouble(entry, digits);
   sl = NormalizeDouble(sl, digits);
   tp = NormalizeDouble(tp, digits);

   string geometry_reason = "";
   if(!E0004_CheckMarketGeometry(direction, sl, tp, geometry_reason))
   {
      reason = geometry_reason;
      return false;
   }

   DALExecRiskSizing risk_sizing;
   if(!DAL_ExecCalculateRiskVolume(symbol, entry, sl, InpRiskCash, InpCommissionPerLotRoundTurn, InpAllowMinLotIfRiskTooSmall, risk_sizing))
   {
      reason = "risk_" + risk_sizing.reason;
      return false;
   }

   if(!InpTradingEnabled)
   {
      reason = "trading_disabled";
      return false;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);

   bool ok = false;
   if(direction > 0)
      ok = g_trade.Buy(risk_sizing.volume, symbol, 0.0, sl, tp, comment);
   else
      ok = g_trade.Sell(risk_sizing.volume, symbol, 0.0, sl, tp, comment);

   if(!ok)
   {
      reason = "market_send_failed_retcode_" + IntegerToString((int)g_trade.ResultRetcode()) + "_" + g_trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_ticket_" + IntegerToString((int)g_trade.ResultOrder());

   if(InpPrintOrderLogs)
   {
      Print("DAL_E0004_HA_FLIP_ENTRY *** build=", DAL_E0004_BUILD,
         "*dir=", direction,
         "*signalTime=", E0004_FormatDateTime(signal_time),
         "*entry=", DoubleToString(entry, digits),
         "*sl=", DoubleToString(sl, digits),
         "*tp=", DoubleToString(tp, digits),
         "*signalHaLow=", DoubleToString(signal_ha_low, digits),
         "*signalHaHigh=", DoubleToString(signal_ha_high, digits),
         "*recent3StopLow=", DoubleToString(recent3_stop_low, digits),
         "*recent3StopHigh=", DoubleToString(recent3_stop_high, digits),
         "*rewardR=", DoubleToString(reward, 2),
         "*riskCash=", DoubleToString(InpRiskCash, 2),
         "*volume=", DoubleToString(risk_sizing.volume, 8),
         "*simultaneous=", DAL_BoolToString(InpAllowSimultaneousTrades),
         "*directionReason=", direction_reason,
         "*comment=", comment,
         "*reason=", reason);
   }

   return true;
}

void E0004_ProcessNewBar()
{
   string session_reason = "";
   if(!E0004_IsTradingSessionOpen(session_reason))
      return;

   DALBar bars[];
   int bars_count = 0;
   DALLRuleNode nodes[];
   int nodes_count = 0;
   DALM0001Event events[];
   int events_count = 0;
   DALM0002BranchSample last_sample;
   bool is_continuation = false;
   string context_reason = "";

   bool context_ok = E0004_LoadClosedContext(bars, bars_count, nodes, nodes_count, events, events_count, last_sample, is_continuation, context_reason);
   if(!context_ok || !is_continuation)
      return;

   if(bars_count < 3)
      return;

   int signal_index = bars_count - 1;
   int prev_color = 0;
   int signal_color = 0;
   double signal_ha_low = 0.0;
   double signal_ha_high = 0.0;
   double recent3_stop_low = 0.0;
   double recent3_stop_high = 0.0;
   string ha_reason = "";
   if(!E0004_ComputeHeikinAshiPair(bars, bars_count, signal_index, prev_color, signal_color, signal_ha_low, signal_ha_high, recent3_stop_low, recent3_stop_high, ha_reason))
      return;

   int continuation_direction = 0;
   string direction_reason = "";
   if(!E0004_DetectContinuationDirection(bars, bars_count, nodes, nodes_count, signal_index, continuation_direction, direction_reason))
      return;

   if(signal_color != continuation_direction)
      return;

   string order_reason = "";
   if(!E0004_PlaceHeikinAshiMarket(signal_color, signal_ha_low, signal_ha_high, recent3_stop_low, recent3_stop_high, bars[signal_index].time, direction_reason, order_reason))
   {
      if(InpPrintOrderLogs)
         Print("DAL_E0004_SIGNAL_SKIP *** build=", DAL_E0004_BUILD,
            "*signalTime=", E0004_FormatDateTime(bars[signal_index].time),
            "*haColor=", signal_color,
            "*continuationDir=", continuation_direction,
            "*reason=", order_reason);
   }
}

int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagicNumber);

   Print("DAL_E0004_BUILD_SANITY *** build=", DAL_E0004_BUILD,
      "*symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*htfRegimeFilter=", DAL_BoolToString(InpUseHigherTimeframeRegimeFilter),
      "*htfTf=", EnumToString(InpHigherRegimeTimeframe),
      "*module=EXECUTION_H0005_CONTINUATION_HEIKIN_ASHI_FLIP",
      "*entry=HA_COLOR_FLIP_IN_CONTINUATION_DIRECTION",
      "*stop=FARTHEST_OF_SIGNAL_HA_AND_LAST_3_CANDLE_EXTREMES",
      "*tp=FIXED_R",
      "*rewardR=", DoubleToString(InpRewardR, 2),
      "*allowSimultaneous=", DAL_BoolToString(InpAllowSimultaneousTrades));

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   Comment("");
}

void OnTick()
{
   if(!E0004_HasNewOpenCandle())
      return;

   E0004_ProcessNewBar();
}
