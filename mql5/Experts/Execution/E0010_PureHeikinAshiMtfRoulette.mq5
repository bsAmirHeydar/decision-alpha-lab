//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0010 Pure Heikin Ashi MTF Roulette          |
//| M1 closed HA flip entry aligned with current-forming M10 HA color |
//+------------------------------------------------------------------+
#property strict
#property version   "1.00"
#property description "Execution E0010: pure Heikin Ashi MTF entry with reusable Roulette risk."

#include <Trade/Trade.mqh>
#include <Execution/DAL_ExecRisk.mqh>
#include <Execution/DAL_ExecOrders.mqh>
#include <Execution/DAL_ExecHeikinAshi.mqh>
#include <Execution/DAL_ExecRouletteRisk.mqh>

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpEntryTimeframe = PERIOD_M1;
input ENUM_TIMEFRAMES InpDirectionTimeframe = PERIOD_M10;

input long InpMagicNumber = 5010000;
input int InpMaxOpenTrades = 1;
input double InpRewardR = 2.0;

input double InpRouletteInitialRiskPercent = 10.0;
input double InpRouletteSaveProfitFactor = 0.50;
input bool InpRoulettePersistState = true;

input int InpStopLookbackClosedBars = 1;
input int InpStopBufferPoints = 0;
input int InpSlippagePoints = 30;

input bool InpTradingEnabled = true;
input bool InpAllowMinLotIfRiskTooSmall = false;
input double InpCommissionPerLotRoundTurn = 0.0;
input bool InpPrintLogs = true;

#define DAL_E0010_BUILD "1.00"
string InpOrderCommentPrefix = "E0010HA";

CTrade g_trade;
DALExecRouletteRiskConfig g_roulette_cfg;
DALExecRouletteRiskState g_roulette_state;
datetime g_last_entry_open_time = 0;

string E0010_Symbol()
{
   if(InpSymbol == "")
      return _Symbol;
   return InpSymbol;
}

string E0010_FormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

bool E0010_HasNewEntryCandle()
{
   datetime current_open = iTime(E0010_Symbol(), InpEntryTimeframe, 0);
   if(current_open <= 0)
      return false;

   if(g_last_entry_open_time <= 0)
   {
      g_last_entry_open_time = current_open;
      return false;
   }

   if(current_open == g_last_entry_open_time)
      return false;

   g_last_entry_open_time = current_open;
   return true;
}

int E0010_CountManagedOpenTrades()
{
   string symbol = E0010_Symbol();
   int count = 0;

   int total = PositionsTotal();
   for(int i = 0; i < total; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != InpMagicNumber)
         continue;

      string comment = PositionGetString(POSITION_COMMENT);
      if(StringFind(comment, InpOrderCommentPrefix, 0) == 0)
         count++;
   }

   return count;
}

string E0010_BarComment(const datetime signal_time, const int direction)
{
   string side = (direction > 0 ? "B" : "S");
   return InpOrderCommentPrefix + side + "T" + IntegerToString((int)signal_time);
}

bool E0010_ResolveSignal(
   int &direction,
   DALExecHeikinAshiBar &htf_current,
   DALExecHeikinAshiBar &ltf_previous_closed,
   DALExecHeikinAshiBar &ltf_signal_closed,
   string &reason
)
{
   direction = 0;
   reason = "not_checked";

   string htf_reason = "";
   if(!DAL_ExecHAComputeAtShift(E0010_Symbol(), InpDirectionTimeframe, 0, 200, htf_current, htf_reason))
   {
      reason = "htf_current_ha_failed_" + htf_reason;
      return false;
   }

   if(htf_current.color == 0)
   {
      reason = "htf_current_ha_doji";
      return false;
   }

   int flip_direction = 0;
   string flip_reason = "";
   if(!DAL_ExecHAClosedColorFlip(E0010_Symbol(), InpEntryTimeframe, flip_direction, ltf_previous_closed, ltf_signal_closed, flip_reason))
   {
      reason = "ltf_flip_failed_" + flip_reason
         + "*htfColor=" + DAL_ExecHAColorToString(htf_current.color);
      return false;
   }

   if(flip_direction != htf_current.color)
   {
      reason = "direction_mismatch*htf=" + DAL_ExecHAColorToString(htf_current.color)
         + "*ltfFlip=" + DAL_ExecHAColorToString(flip_direction);
      return false;
   }

   direction = flip_direction;
   reason = "ok*htfCurrent=" + DAL_ExecHAColorToString(htf_current.color)
      + "*ltfPrevClosed=" + DAL_ExecHAColorToString(ltf_previous_closed.color)
      + "*ltfSignalClosed=" + DAL_ExecHAColorToString(ltf_signal_closed.color)
      + "*signalTime=" + E0010_FormatDateTime(ltf_signal_closed.time);
   return true;
}

bool E0010_BuildTradePlan(
   const int direction,
   const DALExecHeikinAshiBar &signal_closed,
   double &entry_price,
   double &stop_price,
   double &take_profit,
   double &risk_money,
   DALExecRiskSizing &sizing,
   string &reason
)
{
   reason = "not_built";
   entry_price = 0.0;
   stop_price = 0.0;
   take_profit = 0.0;
   risk_money = 0.0;
   DAL_ExecResetRiskSizing(sizing);

   string symbol = E0010_Symbol();
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);

   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   if(ask <= 0.0 || bid <= 0.0)
   {
      reason = "invalid_bid_ask";
      return false;
   }

   if(direction > 0)
      entry_price = ask;
   else if(direction < 0)
      entry_price = bid;
   else
   {
      reason = "zero_direction";
      return false;
   }

   string stop_reason = "";
   if(!DAL_ExecHAStopFromClosedBars(
      symbol,
      InpEntryTimeframe,
      direction,
      InpStopLookbackClosedBars,
      InpStopBufferPoints,
      stop_price,
      stop_reason
   ))
   {
      reason = "stop_failed_" + stop_reason;
      return false;
   }

   if(direction > 0 && stop_price >= entry_price)
   {
      reason = "buy_stop_not_below_entry";
      return false;
   }
   if(direction < 0 && stop_price <= entry_price)
   {
      reason = "sell_stop_not_above_entry";
      return false;
   }

   double r = MathAbs(entry_price - stop_price);
   double reward_r = MathMax(0.01, InpRewardR);
   if(direction > 0)
      take_profit = NormalizeDouble(entry_price + reward_r * r, digits);
   else
      take_profit = NormalizeDouble(entry_price - reward_r * r, digits);

   entry_price = NormalizeDouble(entry_price, digits);
   stop_price = NormalizeDouble(stop_price, digits);

   DAL_ExecRouletteUpdate(g_roulette_cfg, g_roulette_state);
   risk_money = DAL_ExecRouletteRiskMoney(g_roulette_cfg, g_roulette_state);
   if(risk_money <= 0.0)
   {
      reason = "roulette_risk_not_positive";
      return false;
   }

   if(!DAL_ExecCalculateRiskVolume(
      symbol,
      entry_price,
      stop_price,
      risk_money,
      InpCommissionPerLotRoundTurn,
      InpAllowMinLotIfRiskTooSmall,
      sizing
   ))
   {
      reason = "risk_sizing_failed_" + sizing.reason;
      return false;
   }

   reason = "ok*" + DAL_ExecRiskSizingToLog(sizing)
      + "*" + DAL_ExecRouletteStateToLog(g_roulette_cfg, g_roulette_state)
      + "*signalTime=" + E0010_FormatDateTime(signal_closed.time);
   return true;
}

bool E0010_SendMarketOrder(
   const int direction,
   const double volume,
   const double stop_price,
   const double take_profit,
   const string comment,
   string &reason
)
{
   reason = "not_sent";
   string symbol = E0010_Symbol();

   g_trade.SetExpertMagicNumber(InpMagicNumber);
   g_trade.SetDeviationInPoints(MathMax(0, InpSlippagePoints));

   bool ok = false;
   if(direction > 0)
      ok = g_trade.Buy(volume, symbol, 0.0, stop_price, take_profit, comment);
   else if(direction < 0)
      ok = g_trade.Sell(volume, symbol, 0.0, stop_price, take_profit, comment);
   else
   {
      reason = "zero_direction";
      return false;
   }

   if(!ok)
   {
      reason = "trade_failed_retcode_" + IntegerToString((int)g_trade.ResultRetcode())
         + "_" + g_trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_retcode_" + IntegerToString((int)g_trade.ResultRetcode())
      + "_" + g_trade.ResultRetcodeDescription();
   return true;
}

int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagicNumber);
   g_trade.SetDeviationInPoints(MathMax(0, InpSlippagePoints));

   DAL_ExecRouletteRiskDefaults(g_roulette_cfg);
   g_roulette_cfg.initial_risk_percent = InpRouletteInitialRiskPercent;
   g_roulette_cfg.save_profit_factor = InpRouletteSaveProfitFactor;
   g_roulette_cfg.persist_state = InpRoulettePersistState;
   g_roulette_cfg.state_key = "E0010_" + E0010_Symbol() + "_" + IntegerToString((int)InpMagicNumber);
   g_roulette_cfg.print_logs = InpPrintLogs;

   DAL_ExecRouletteInit(g_roulette_cfg, g_roulette_state);

   Print("DAL_E0010_BUILD_SANITY *** build=", DAL_E0010_BUILD,
      "*symbol=", E0010_Symbol(),
      "*entryTf=", EnumToString(InpEntryTimeframe),
      "*directionTf=", EnumToString(InpDirectionTimeframe),
      "*maxOpenTrades=", InpMaxOpenTrades,
      "*rewardR=", DoubleToString(InpRewardR, 2),
      "*rouletteRiskPct=", DoubleToString(InpRouletteInitialRiskPercent, 2),
      "*rouletteSaveFactor=", DoubleToString(InpRouletteSaveProfitFactor, 4));

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   DAL_ExecRouletteSave(g_roulette_cfg, g_roulette_state);
}

void OnTick()
{
   DAL_ExecRouletteUpdate(g_roulette_cfg, g_roulette_state);

   if(!E0010_HasNewEntryCandle())
      return;

   string symbol = E0010_Symbol();
   if(!SymbolSelect(symbol, true))
   {
      if(InpPrintLogs)
         Print("DAL_E0010_SKIP *** reason=symbol_select_failed*symbol=", symbol);
      return;
   }

   int managed = E0010_CountManagedOpenTrades();
   if(managed >= MathMax(1, InpMaxOpenTrades))
   {
      if(InpPrintLogs)
         Print("DAL_E0010_SKIP *** reason=max_open_trades*managed=", managed,
            "*max=", MathMax(1, InpMaxOpenTrades));
      return;
   }

   int direction = 0;
   DALExecHeikinAshiBar htf_current;
   DALExecHeikinAshiBar ltf_previous_closed;
   DALExecHeikinAshiBar ltf_signal_closed;
   string signal_reason = "";

   if(!E0010_ResolveSignal(direction, htf_current, ltf_previous_closed, ltf_signal_closed, signal_reason))
   {
      if(InpPrintLogs)
         Print("DAL_E0010_NO_SIGNAL *** ", signal_reason,
            "*", DAL_ExecRouletteStateToLog(g_roulette_cfg, g_roulette_state));
      return;
   }

   string comment = E0010_BarComment(ltf_signal_closed.time, direction);
   if(DAL_ExecOrderCommentExists(symbol, InpMagicNumber, comment))
   {
      if(InpPrintLogs)
         Print("DAL_E0010_SKIP *** reason=comment_already_exists*comment=", comment);
      return;
   }

   if(!InpTradingEnabled)
   {
      Print("DAL_E0010_SIGNAL_DRY_RUN *** direction=", (direction > 0 ? "BUY" : "SELL"),
         "*", signal_reason,
         "*", DAL_ExecRouletteStateToLog(g_roulette_cfg, g_roulette_state));
      return;
   }

   double entry_price = 0.0;
   double stop_price = 0.0;
   double take_profit = 0.0;
   double risk_money = 0.0;
   DALExecRiskSizing sizing;
   string plan_reason = "";

   if(!E0010_BuildTradePlan(direction, ltf_signal_closed, entry_price, stop_price, take_profit, risk_money, sizing, plan_reason))
   {
      Print("DAL_E0010_PLAN_REJECT *** direction=", (direction > 0 ? "BUY" : "SELL"),
         "*signal=", signal_reason,
         "*planReason=", plan_reason);
      return;
   }

   string send_reason = "";
   if(E0010_SendMarketOrder(direction, sizing.volume, stop_price, take_profit, comment, send_reason))
   {
      Print("DAL_E0010_ORDER_SENT *** direction=", (direction > 0 ? "BUY" : "SELL"),
         "*volume=", DoubleToString(sizing.volume, 8),
         "*entry=", DoubleToString(entry_price, 8),
         "*sl=", DoubleToString(stop_price, 8),
         "*tp=", DoubleToString(take_profit, 8),
         "*riskMoney=", DoubleToString(risk_money, 2),
         "*comment=", comment,
         "*signal=", signal_reason,
         "*send=", send_reason);
   }
   else
   {
      Print("DAL_E0010_ORDER_FAILED *** direction=", (direction > 0 ? "BUY" : "SELL"),
         "*volume=", DoubleToString(sizing.volume, 8),
         "*sl=", DoubleToString(stop_price, 8),
         "*tp=", DoubleToString(take_profit, 8),
         "*riskMoney=", DoubleToString(risk_money, 2),
         "*comment=", comment,
         "*signal=", signal_reason,
         "*send=", send_reason);
   }
}
