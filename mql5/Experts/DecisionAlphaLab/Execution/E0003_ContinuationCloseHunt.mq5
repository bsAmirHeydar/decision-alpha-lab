//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0003 H0005 Continuation Close-Hunt Executor |
//| Continuation entry after close-hunted node, ATR risk, regime exit  |
//+------------------------------------------------------------------+
#property strict
#property version   "1.03"
#property description "Execution module E0003: continuation close-hunt or Donchian breakout entries, 3ATR risk stop, ATR trailing, optional regime exit."

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/M0002/DAL_M0002Engine.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecRisk.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecReversalOneToOne.mqh>

// Minimal public inputs for the third H5 execution path.
input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 1500;

// Shared H5/M0001 structure.
input int InpL = 5;
input double InpZoneRatio = 0.90;
input int InpExitGap = 6;
input ENUM_DALM0001ConsumeMode InpConsumeMode = DAL_M0001_CONSUME_BY_HUNT;

// Regime source.
enum ENUM_E0003RegimeBasis
{
   E0003_REGIME_LAST_COMPLETED_BRANCH = 0,
   E0003_REGIME_HUMAN_CONTEXT_COMBINED = 1
};

enum ENUM_E0003HumanContextSignal
{
   E0003_HUMAN_CONTEXT_NEUTRAL = 0,
   E0003_HUMAN_CONTEXT_REVERSAL = 1,
   E0003_HUMAN_CONTEXT_CONTINUATION = 2
};

input ENUM_E0003RegimeBasis InpRegimeBasis = E0003_REGIME_LAST_COMPLETED_BRANCH;
input ENUM_E0003HumanContextSignal InpHumanContextSignal = E0003_HUMAN_CONTEXT_NEUTRAL;

// Optional higher-timeframe regime filter. Off by default to keep current tests unchanged.
input bool InpUseHigherTimeframeRegimeFilter = false;
input ENUM_TIMEFRAMES InpHigherRegimeTimeframe = PERIOD_H1;

// Trading session. Broker time, strict: start <= time < end.
input bool InpUseTradingSessionFilter = true;
input int InpTradingStartHour = 0;
input int InpTradingStartMinute = 0;
input int InpTradingEndHour = 23;
input int InpTradingEndMinute = 59;

// Local regime and entry trigger.
input bool InpUseLowerTimeframeRegimeFilter = true;

enum ENUM_E0003EntryMode
{
   E0003_ENTRY_CLOSE_HUNTED_NODE = 0,
   E0003_ENTRY_DONCHIAN_BREAKOUT = 1
};

input ENUM_E0003EntryMode InpEntryMode = E0003_ENTRY_DONCHIAN_BREAKOUT;
input int InpDonchianPeriod = 20;

// Risk model: volume is calculated from entry to ATR stop distance.
input long InpMagicNumber = 5003003;
input double InpRiskCash = 100.0;
input int InpAtrPeriod = 14;
input double InpAtrMultiplier = 3.0;
input bool InpUseAtrTrailingStop = true;
input bool InpExitOnRegimeChange = true;
input int InpCloseHuntBufferPoints = 0;
input int InpMaxEntriesPerBar = 3;

// Internal fixed policy. These are not tester inputs.
#define DAL_E0003_BUILD "1.03"
string InpOrderCommentPrefix = "DALC3";
int InpRegimeLookbackBars = 100;
int InpOutcomeCandleOffsetAfterExit = 0;
int InpBrokerUtcOffsetHours = 0;
bool InpUseClosedBarsOnly = true;
bool InpTradingEnabled = true;
bool InpAllowMinLotIfRiskTooSmall = false;
double InpCommissionPerLotRoundTurn = 0.0;
int InpMaxSimultaneousTrades = -1;
bool InpAllowOppositeTrades = true;
bool InpPrintOrderLogs = true;

CTrade g_trade;
datetime g_last_open_bar_time = 0;
int g_traded_node_ids[];

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

int E0003_ClampInt(const int value, const int lo, const int hi)
{
   if(value < lo)
      return lo;
   if(value > hi)
      return hi;
   return value;
}

string E0003_TwoDigits(const int value)
{
   if(value < 10)
      return "0" + IntegerToString(value);
   return IntegerToString(value);
}

string E0003_FormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

bool E0003_IsTradingSessionOpen(string &reason)
{
   if(!InpUseTradingSessionFilter)
   {
      reason = "timeFilter=OFF";
      return true;
   }

   int start_hour = E0003_ClampInt(InpTradingStartHour, 0, 23);
   int start_minute = E0003_ClampInt(InpTradingStartMinute, 0, 59);
   int end_hour = E0003_ClampInt(InpTradingEndHour, 0, 23);
   int end_minute = E0003_ClampInt(InpTradingEndMinute, 0, 59);
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

   reason = "timeFilter=ON*now=" + E0003_FormatDateTime(now_time)
      + "*window=" + E0003_TwoDigits(start_hour) + ":" + E0003_TwoDigits(start_minute)
      + "-" + E0003_TwoDigits(end_hour) + ":" + E0003_TwoDigits(end_minute)
      + "*open=" + DAL_BoolToString(open);
   return open;
}

string E0003_ManagedCommentPrefix()
{
   return InpOrderCommentPrefix;
}

string E0003_NodeComment(const int node_id, const int direction)
{
   string side = (direction > 0 ? "B" : "S");
   return E0003_ManagedCommentPrefix() + side + "N" + IntegerToString(node_id);
}

string E0003_DonchianComment(const int direction, const datetime signal_time)
{
   string side = (direction > 0 ? "B" : "S");
   return E0003_ManagedCommentPrefix() + side + "D" + IntegerToString((long)signal_time);
}

string E0003_EntryModeToString()
{
   if(InpEntryMode == E0003_ENTRY_DONCHIAN_BREAKOUT)
      return "DONCHIAN_BREAKOUT";
   return "CLOSE_HUNTED_NODE";
}

bool E0003_NodeAlreadyTraded(const int node_id)
{
   for(int i = 0; i < ArraySize(g_traded_node_ids); i++)
   {
      if(g_traded_node_ids[i] == node_id)
         return true;
   }
   return false;
}

void E0003_MarkNodeTraded(const int node_id)
{
   if(E0003_NodeAlreadyTraded(node_id))
      return;
   int n = ArraySize(g_traded_node_ids);
   ArrayResize(g_traded_node_ids, n + 1);
   g_traded_node_ids[n] = node_id;
}

bool E0003_ManagedCommentExists(const string comment)
{
   return DAL_ExecOrderCommentExists(LabSymbol(), InpMagicNumber, comment);
}

void E0003_BuildM0001Config(DALM0001Config &config)
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

void E0003_BuildM0002Config(DALM0002Config &config)
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

bool E0003_HasNewOpenCandle()
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

string E0003_RegimeOutcomeToString(const ENUM_DALM0002Outcome outcome)
{
   if(outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT)
      return "REVERSAL";
   if(outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      return "CONTINUATION";
   return "UNKNOWN";
}

bool E0003_ResolveEffectiveContinuation(DALM0002BranchSample &last_sample, const bool has_last_sample, string &reason)
{
   if(!has_last_sample)
   {
      reason = "no_last_branch";
      return false;
   }

   bool last_reversal = (last_sample.outcome == DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT);
   bool last_continuation = (last_sample.outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT);

   if(InpRegimeBasis == E0003_REGIME_LAST_COMPLETED_BRANCH)
   {
      reason = "regimeBasis=LAST_COMPLETED_BRANCH*last=" + E0003_RegimeOutcomeToString(last_sample.outcome);
      return last_continuation;
   }

   if(InpHumanContextSignal == E0003_HUMAN_CONTEXT_REVERSAL)
   {
      last_sample.outcome = DAL_M0002_OUTCOME_REVERSAL_AFTER_EXIT;
      reason = "regimeBasis=HUMAN_CONTEXT_COMBINED*human=REVERSAL*last=" + (last_reversal ? "REVERSAL" : (last_continuation ? "CONTINUATION" : "UNKNOWN"));
      return false;
   }

   if(InpHumanContextSignal == E0003_HUMAN_CONTEXT_CONTINUATION)
   {
      last_sample.outcome = DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT;
      reason = "regimeBasis=HUMAN_CONTEXT_COMBINED*human=CONTINUATION*last=" + (last_reversal ? "REVERSAL" : (last_continuation ? "CONTINUATION" : "UNKNOWN"));
      return true;
   }

   reason = "regimeBasis=HUMAN_CONTEXT_COMBINED*human=NEUTRAL*last=" + E0003_RegimeOutcomeToString(last_sample.outcome);
   return last_continuation;
}

bool E0003_GetAtrValue(double &atr_value, string &reason)
{
   atr_value = 0.0;
   int period = MathMax(1, InpAtrPeriod);
   int handle = iATR(LabSymbol(), LabTimeframe(), period);
   if(handle == INVALID_HANDLE)
   {
      reason = "atr_invalid_handle";
      return false;
   }

   double buffer[];
   ArraySetAsSeries(buffer, true);
   int copied = CopyBuffer(handle, 0, 1, 1, buffer);
   IndicatorRelease(handle);

   if(copied < 1 || ArraySize(buffer) < 1 || buffer[0] <= 0.0)
   {
      reason = "atr_copy_failed_or_zero";
      return false;
   }

   atr_value = buffer[0];
   reason = "ok";
   return true;
}


bool E0003_GetLastClosedBarClose(double &closed_close, datetime &closed_time, string &reason)
{
   closed_close = 0.0;
   closed_time = 0;
   string symbol = LabSymbol();
   ENUM_TIMEFRAMES tf = LabTimeframe();

   closed_close = iClose(symbol, tf, 1);
   closed_time = iTime(symbol, tf, 1);
   if(closed_close <= 0.0 || closed_time <= 0)
   {
      reason = "last_closed_bar_not_ready";
      return false;
   }

   reason = "ok";
   return true;
}

int E0003_ApplyAtrTrailingStops(const double atr_value, const double closed_close, const datetime closed_time, const string context)
{
   if(!InpUseAtrTrailingStop)
      return 0;

   string symbol = LabSymbol();
   double multiplier = MathMax(0.1, InpAtrMultiplier);
   double stop_distance = atr_value * multiplier;
   if(stop_distance <= 0.0 || closed_close <= 0.0)
      return 0;

   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   int stops_level = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_dist = MathMax(0.0, stops_level * point);
   if(point <= 0.0 || bid <= 0.0 || ask <= 0.0)
      return 0;

   int modified = 0;
   g_trade.SetExpertMagicNumber(InpMagicNumber);

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
      if(!DAL_ExecOrderCommentMatchesPrefix(comment, E0003_ManagedCommentPrefix()))
         continue;

      long pos_type = (long)PositionGetInteger(POSITION_TYPE);
      double old_sl = PositionGetDouble(POSITION_SL);
      double old_tp = PositionGetDouble(POSITION_TP);
      double new_sl = old_sl;
      bool should_modify = false;

      if(pos_type == POSITION_TYPE_BUY)
      {
         double candidate = closed_close - stop_distance;
         double max_allowed = bid - min_dist;
         if(candidate > max_allowed)
            candidate = max_allowed;
         candidate = NormalizeDouble(candidate, digits);

         if(candidate > 0.0 && candidate < bid && (old_sl <= 0.0 || candidate > old_sl + point * 0.5))
         {
            new_sl = candidate;
            should_modify = true;
         }
      }
      else if(pos_type == POSITION_TYPE_SELL)
      {
         double candidate = closed_close + stop_distance;
         double min_allowed = ask + min_dist;
         if(candidate < min_allowed)
            candidate = min_allowed;
         candidate = NormalizeDouble(candidate, digits);

         if(candidate > ask && (old_sl <= 0.0 || candidate < old_sl - point * 0.5))
         {
            new_sl = candidate;
            should_modify = true;
         }
      }

      if(!should_modify)
         continue;

      if(g_trade.PositionModify(ticket, new_sl, old_tp))
      {
         modified++;
         if(InpPrintOrderLogs)
            Print("DAL_E0003_ATR_TRAIL *** build=", DAL_E0003_BUILD,
               "*ticket=", (long)ticket,
               "*time=", E0003_FormatDateTime(closed_time),
               "*context=", context,
               "*close=", DoubleToString(closed_close, digits),
               "*atr=", DoubleToString(atr_value, digits),
               "*atrMultiplier=", DoubleToString(multiplier, 2),
               "*oldSl=", DoubleToString(old_sl, digits),
               "*newSl=", DoubleToString(new_sl, digits),
               "*comment=", comment);
      }
      else
      {
         Print("DAL_E0003_ATR_TRAIL_FAILED *** build=", DAL_E0003_BUILD,
            "*ticket=", (long)ticket,
            "*context=", context,
            "*newSl=", DoubleToString(new_sl, digits),
            "*retcode=", (int)g_trade.ResultRetcode(),
            "*desc=", g_trade.ResultRetcodeDescription());
      }
   }

   return modified;
}

bool E0003_CloseHuntedBeforeSignal(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const int signal_index,
   const double close_buffer
)
{
   int start = node.active_from_index;
   if(start < 0)
      start = 0;
   if(start >= bars_count)
      return true;

   for(int i = start; i < signal_index; i++)
   {
      if(node.type == DAL_NODE_HIGH && bars[i].close > node.price + close_buffer)
         return true;
      if(node.type == DAL_NODE_LOW && bars[i].close < node.price - close_buffer)
         return true;
   }
   return false;
}

bool E0003_NodeCloseHuntedOnSignal(
   const DALBar &bar,
   const DALLRuleNode &node,
   const double close_buffer,
   int &direction
)
{
   direction = 0;
   if(node.type == DAL_NODE_HIGH && bar.close > node.price + close_buffer)
   {
      direction = +1;
      return true;
   }
   if(node.type == DAL_NODE_LOW && bar.close < node.price - close_buffer)
   {
      direction = -1;
      return true;
   }
   return false;
}

bool E0003_GetDonchianBreakoutSignal(
   const DALBar &bars[],
   const int bars_count,
   const int signal_index,
   const int period,
   const double close_buffer,
   int &direction,
   double &breakout_level,
   string &reason
)
{
   direction = 0;
   breakout_level = 0.0;
   reason = "no_signal";

   int lookback = MathMax(1, period);
   if(signal_index < lookback || signal_index >= bars_count)
   {
      reason = "not_enough_donchian_bars";
      return false;
   }

   int start = signal_index - lookback;
   double upper = bars[start].high;
   double lower = bars[start].low;

   for(int i = start + 1; i < signal_index; i++)
   {
      if(bars[i].high > upper)
         upper = bars[i].high;
      if(bars[i].low < lower)
         lower = bars[i].low;
   }

   double close_price = bars[signal_index].close;
   if(close_price > upper + close_buffer)
   {
      direction = +1;
      breakout_level = upper;
      reason = "donchian_upper_breakout";
      return true;
   }

   if(close_price < lower - close_buffer)
   {
      direction = -1;
      breakout_level = lower;
      reason = "donchian_lower_breakout";
      return true;
   }

   reason = "inside_donchian_channel";
   return false;
}

bool E0003_CheckMarketSlGeometry(const int direction, const double sl, string &reason)
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
      if((ask - sl) < min_dist)
      {
         reason = "buy_sl_too_close";
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
      if((sl - bid) < min_dist)
      {
         reason = "sell_sl_too_close";
         return false;
      }
      reason = "ok";
      return true;
   }

   reason = "zero_direction";
   return false;
}

bool E0003_PlaceContinuationMarketRaw(
   const int source_id,
   const string source_label,
   const double source_price,
   const int direction,
   const double atr_value,
   const datetime signal_time,
   const string comment,
   string &reason
)
{
   reason = "not_sent";
   string symbol = LabSymbol();
   double multiplier = MathMax(0.1, InpAtrMultiplier);
   double stop_distance = atr_value * multiplier;
   if(stop_distance <= 0.0)
   {
      reason = "invalid_atr_stop_distance";
      return false;
   }

   double entry = (direction > 0 ? SymbolInfoDouble(symbol, SYMBOL_ASK) : SymbolInfoDouble(symbol, SYMBOL_BID));
   if(entry <= 0.0)
   {
      reason = "invalid_entry_quote";
      return false;
   }

   double sl = (direction > 0 ? entry - stop_distance : entry + stop_distance);
   double tp = 0.0;
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   entry = NormalizeDouble(entry, digits);
   sl = NormalizeDouble(sl, digits);

   string geometry_reason = "";
   if(!E0003_CheckMarketSlGeometry(direction, sl, geometry_reason))
   {
      reason = geometry_reason;
      return false;
   }

   string exposure_reason = "";
   if(!DAL_ExecCanOpenDirection(symbol, InpMagicNumber, direction, InpMaxSimultaneousTrades, InpAllowOppositeTrades, exposure_reason))
   {
      reason = exposure_reason;
      return false;
   }

   DALExecRiskSizing risk;
   if(!DAL_ExecCalculateRiskVolume(symbol, entry, sl, InpRiskCash, InpCommissionPerLotRoundTurn, InpAllowMinLotIfRiskTooSmall, risk))
   {
      reason = "risk_" + risk.reason;
      return false;
   }

   if(comment == "" || E0003_ManagedCommentExists(comment))
   {
      reason = "comment_empty_or_exists";
      return false;
   }

   if(source_id >= 0 && E0003_NodeAlreadyTraded(source_id))
   {
      reason = "node_already_traded";
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
      ok = g_trade.Buy(risk.volume, symbol, 0.0, sl, tp, comment);
   else
      ok = g_trade.Sell(risk.volume, symbol, 0.0, sl, tp, comment);

   if(!ok)
   {
      reason = "market_send_failed_retcode_" + IntegerToString((int)g_trade.ResultRetcode()) + "_" + g_trade.ResultRetcodeDescription();
      return false;
   }

   if(source_id >= 0)
      E0003_MarkNodeTraded(source_id);
   reason = "ok_ticket_" + IntegerToString((int)g_trade.ResultOrder());

   if(InpPrintOrderLogs)
   {
      Print("DAL_E0003_CONTINUATION_ENTRY *** build=", DAL_E0003_BUILD,
         "*entryMode=", E0003_EntryModeToString(),
         "*source=", source_label,
         "*sourceId=", source_id,
         "*dir=", direction,
         "*signalTime=", E0003_FormatDateTime(signal_time),
         "*sourcePrice=", DoubleToString(source_price, digits),
         "*entry=", DoubleToString(entry, digits),
         "*sl=", DoubleToString(sl, digits),
         "*tp=NONE",
         "*atr=", DoubleToString(atr_value, digits),
         "*atrMultiplier=", DoubleToString(multiplier, 2),
         "*riskCash=", DoubleToString(InpRiskCash, 2),
         "*volume=", DoubleToString(risk.volume, 8),
         "*comment=", comment,
         "*reason=", reason);
   }

   return true;
}

bool E0003_PlaceContinuationMarket(
   const DALLRuleNode &node,
   const int direction,
   const double atr_value,
   const datetime signal_time,
   string &reason
)
{
   string comment = E0003_NodeComment(node.id, direction);
   string source_label = (node.type == DAL_NODE_HIGH ? "HIGH_NODE_CLOSE_HUNT" : "LOW_NODE_CLOSE_HUNT");
   return E0003_PlaceContinuationMarketRaw(node.id, source_label, node.price, direction, atr_value, signal_time, comment, reason);
}

bool E0003_PlaceDonchianMarket(
   const int direction,
   const double breakout_level,
   const double atr_value,
   const datetime signal_time,
   string &reason
)
{
   string comment = E0003_DonchianComment(direction, signal_time);
   return E0003_PlaceContinuationMarketRaw(-1, "DONCHIAN_BREAKOUT", breakout_level, direction, atr_value, signal_time, comment, reason);
}

int E0003_CloseManagedPositions(const string context)
{
   int closed = 0;
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
      if(!DAL_ExecOrderCommentMatchesPrefix(comment, E0003_ManagedCommentPrefix()))
         continue;

      if(g_trade.PositionClose(ticket))
      {
         closed++;
         if(InpPrintOrderLogs)
            Print("DAL_E0003_REGIME_EXIT_CLOSE *** build=", DAL_E0003_BUILD, "*ticket=", (long)ticket, "*context=", context, "*comment=", comment);
      }
      else
      {
         Print("DAL_E0003_CLOSE_FAILED *** build=", DAL_E0003_BUILD,
            "*ticket=", (long)ticket,
            "*context=", context,
            "*retcode=", (int)g_trade.ResultRetcode(),
            "*desc=", g_trade.ResultRetcodeDescription());
      }
   }
   return closed;
}

bool E0003_PassesHigherTimeframeRegimeFilter(const ENUM_DALM0002Outcome required_outcome, string &reason)
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
   E0003_BuildM0001Config(htf_m1);

   DALLRuleNode htf_nodes[];
   int htf_nodes_count = DAL_DetectConfirmedStructuralNodes(htf_bars, htf_bars_count, htf_m1.L, htf_nodes);

   DALM0001Event htf_events[];
   int htf_events_count = DAL_M0001ComputeEvents(htf_bars, htf_bars_count, htf_nodes, htf_nodes_count, htf_m1, htf_events);

   DALM0002Config htf_m2;
   E0003_BuildM0002Config(htf_m2);

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
      + "*last=" + E0003_RegimeOutcomeToString(htf_last_sample.outcome)
      + "*required=" + E0003_RegimeOutcomeToString(required_outcome)
      + "*pass=" + DAL_BoolToString(pass);
   return pass;
}


bool E0003_LoadClosedContext(
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

   int min_required = 2;
   if(InpEntryMode == E0003_ENTRY_DONCHIAN_BREAKOUT)
      min_required = MathMax(min_required, MathMax(1, InpDonchianPeriod) + 2);
   if(InpEntryMode == E0003_ENTRY_CLOSE_HUNTED_NODE || InpUseLowerTimeframeRegimeFilter)
      min_required = MathMax(min_required, InpL * 2 + 20);

   if(bars_count <= min_required)
   {
      reason = "not_enough_bars";
      return false;
   }

   bool need_node_engine = (InpEntryMode == E0003_ENTRY_CLOSE_HUNTED_NODE || InpUseLowerTimeframeRegimeFilter);
   bool local_pass = true;
   string local_reason = "ltfRegimeFilter=OFF";

   if(need_node_engine)
   {
      DALM0001Config m1;
      E0003_BuildM0001Config(m1);
      nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, m1.L, nodes);
      events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, m1, events);
   }
   else
   {
      local_reason = "ltfRegimeFilter=OFF*nodeEngine=SKIPPED_FOR_DONCHIAN";
   }

   if(InpUseLowerTimeframeRegimeFilter)
   {
      DALM0002Config m2;
      E0003_BuildM0002Config(m2);

      int last_event_index = -1;
      bool has_last_sample = DAL_ExecFindLatestBranchSampleFast(events, events_count, bars, bars_count, 0, m2, last_sample, last_event_index);
      if(!has_last_sample)
      {
         reason = "ltfRegimeFilter=ON*reason=no_last_branch";
         return false;
      }

      local_pass = E0003_ResolveEffectiveContinuation(last_sample, has_last_sample, local_reason);
      local_reason = "ltfRegimeFilter=ON*" + local_reason;
   }

   is_continuation = local_pass;
   reason = local_reason;

   if(is_continuation)
   {
      string htf_regime_reason = "";
      if(!E0003_PassesHigherTimeframeRegimeFilter(DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT, htf_regime_reason))
      {
         is_continuation = false;
         reason = local_reason + "*" + htf_regime_reason;
      }
      else
      {
         reason = local_reason + "*" + htf_regime_reason;
      }
   }

   return true;
}

void E0003_ProcessNewBar()
{
   double atr_value = 0.0;
   string atr_reason = "";
   bool atr_ok = E0003_GetAtrValue(atr_value, atr_reason);

   double closed_close = 0.0;
   datetime closed_time = 0;
   string closed_reason = "";
   bool closed_ok = E0003_GetLastClosedBarClose(closed_close, closed_time, closed_reason);

   if(atr_ok && closed_ok)
      E0003_ApplyAtrTrailingStops(atr_value, closed_close, closed_time, "new_closed_bar");

   DALBar bars[];
   int bars_count = 0;
   DALLRuleNode nodes[];
   int nodes_count = 0;
   DALM0001Event events[];
   int events_count = 0;
   DALM0002BranchSample last_sample;
   bool is_continuation = false;
   string context_reason = "";

   bool context_ok = E0003_LoadClosedContext(bars, bars_count, nodes, nodes_count, events, events_count, last_sample, is_continuation, context_reason);
   if(!context_ok)
   {
      if(InpExitOnRegimeChange)
         E0003_CloseManagedPositions("context_not_ready_" + context_reason);
      return;
   }

   if(!is_continuation)
   {
      if(InpExitOnRegimeChange)
         E0003_CloseManagedPositions("regime_changed_" + context_reason);
      return;
   }

   string session_reason = "";
   if(!E0003_IsTradingSessionOpen(session_reason))
      return;

   if(bars_count < 2)
      return;

   int signal_index = bars_count - 1;
   DALBar signal_bar = bars[signal_index];

   if(!atr_ok)
   {
      Print("DAL_E0003_SKIP *** build=", DAL_E0003_BUILD, "*reason=", atr_reason);
      return;
   }

   double point = SymbolInfoDouble(LabSymbol(), SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.0;
   double close_buffer = MathMax(0, InpCloseHuntBufferPoints) * point;

   if(InpEntryMode == E0003_ENTRY_DONCHIAN_BREAKOUT)
   {
      int donchian_direction = 0;
      double breakout_level = 0.0;
      string donchian_reason = "";
      if(E0003_GetDonchianBreakoutSignal(bars, bars_count, signal_index, InpDonchianPeriod, close_buffer, donchian_direction, breakout_level, donchian_reason))
      {
         string order_reason = "";
         if(!E0003_PlaceDonchianMarket(donchian_direction, breakout_level, atr_value, signal_bar.time, order_reason) && InpPrintOrderLogs)
         {
            Print("DAL_E0003_SIGNAL_SKIP *** build=", DAL_E0003_BUILD,
               "*entryMode=DONCHIAN_BREAKOUT",
               "*dir=", donchian_direction,
               "*signalTime=", E0003_FormatDateTime(signal_bar.time),
               "*reason=", order_reason);
         }
      }
      return;
   }

   int sent = 0;
   int max_entries = MathMax(1, InpMaxEntriesPerBar);

   for(int i = nodes_count - 1; i >= 0; i--)
   {
      if(sent >= max_entries)
         break;

      DALLRuleNode node = nodes[i];
      if(!node.confirmed)
         continue;
      if(node.active_from_index < 0 || node.active_from_index >= signal_index)
         continue;
      if(E0003_NodeAlreadyTraded(node.id))
         continue;
      if(DAL_ExecNodeHasEvent(events, events_count, node.id))
         continue;

      int direction = 0;
      if(!E0003_NodeCloseHuntedOnSignal(signal_bar, node, close_buffer, direction))
         continue;

      if(E0003_CloseHuntedBeforeSignal(bars, bars_count, node, signal_index, close_buffer))
         continue;

      string comment = E0003_NodeComment(node.id, direction);
      if(E0003_ManagedCommentExists(comment))
         continue;

      string order_reason = "";
      if(E0003_PlaceContinuationMarket(node, direction, atr_value, signal_bar.time, order_reason))
         sent++;
      else if(InpPrintOrderLogs)
         Print("DAL_E0003_SIGNAL_SKIP *** build=", DAL_E0003_BUILD,
            "*nodeId=", node.id,
            "*dir=", direction,
            "*signalTime=", E0003_FormatDateTime(signal_bar.time),
            "*reason=", order_reason);
   }
}

int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagicNumber);
   ArrayResize(g_traded_node_ids, 0);

   Print("DAL_E0003_BUILD_SANITY *** build=", DAL_E0003_BUILD,
      "*symbol=", LabSymbol(),
      "*tf=", EnumToString(LabTimeframe()),
      "*ltfRegimeFilter=", DAL_BoolToString(InpUseLowerTimeframeRegimeFilter),
      "*htfRegimeFilter=", DAL_BoolToString(InpUseHigherTimeframeRegimeFilter),
      "*htfTf=", EnumToString(InpHigherRegimeTimeframe),
      "*module=EXECUTION_H0005_CONTINUATION",
      "*entryMode=", E0003_EntryModeToString(),
      "*donchianPeriod=", InpDonchianPeriod,
      "*riskStop=ATR_MULTIPLE",
      "*atrPeriod=", InpAtrPeriod,
      "*atrMultiplier=", DoubleToString(InpAtrMultiplier, 2),
      "*atrTrail=", DAL_BoolToString(InpUseAtrTrailingStop),
      "*exitOnRegimeChange=", DAL_BoolToString(InpExitOnRegimeChange),
      "*tp=NONE");

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   Comment("");
}

void OnTick()
{
   if(!E0003_HasNewOpenCandle())
      return;

   E0003_ProcessNewBar();
}
