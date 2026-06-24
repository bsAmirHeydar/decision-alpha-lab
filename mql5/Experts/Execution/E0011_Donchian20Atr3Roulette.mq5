//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0011 Donchian20 ATR3 Roulette              |
//| Fresh Donchian breakout, 3 ATR stop, 2R target, Roulette risk    |
//+------------------------------------------------------------------+
#property strict
#property version   "1.10"
#property description "Execution E0011: Donchian 20 breakout with ATR(14)*3 stop, 2R target, Roulette risk, and optional hypothetical profit gate."

#include <Trade/Trade.mqh>
#include <Execution/DAL_ExecRouletteRisk.mqh>
#include <Execution/DAL_ExecDonchianAtr.mqh>
#include <Execution/DAL_ExecHypotheticalProfitGate.mqh>

input string InpSymbol = "";
input ENUM_TIMEFRAMES InpSignalTimeframe = PERIOD_M1;

input int InpDonchianPeriod = 20;
input int InpATRPeriod = 14;
input double InpATRStopMultiplier = 3.0;
input double InpRewardR = 2.0;

input long InpMagicNumber = 5011000;
input int InpMaxOpenTrades = 1;
input int InpSlippagePoints = 30;
input double InpCommissionPerLotRoundTurn = 0.0;
input bool InpAllowMinLotIfRiskTooSmall = false;

input double InpRouletteInitialRiskPercent = 10.0;
input double InpRouletteSaveProfitFactor = 0.50;
input bool InpRoulettePersistState = true;

input bool InpHypoGateEnabled = true;
input bool InpHypoGateStartOpen = false;
input bool InpHypoGatePersistState = true;

input bool InpTradingEnabled = true;
input bool InpPrintLogs = true;

#define DAL_E0011_BUILD "1.10"
string InpOrderCommentPrefix = "E0011DON";

CTrade g_trade;
DALExecRouletteRiskConfig g_roulette_cfg;
DALExecRouletteRiskState g_roulette_state;
DALExecHypotheticalProfitGateConfig g_hypo_gate_cfg;
DALExecHypotheticalProfitGateState g_hypo_gate_state;
datetime g_last_signal_bar_open_time = 0;

struct E0011RiskSizing
{
   bool ok;
   string reason;
   double entry_price;
   double stop_price;
   double risk_cash_requested;
   double tick_size;
   double tick_value_loss;
   double volume_min;
   double volume_max;
   double volume_step;
   double stop_loss_cash_per_lot;
   double total_risk_cash_per_lot;
   double raw_volume;
   double volume;
   double estimated_total_risk_cash;
};

string E0011_Symbol()
{
   if(InpSymbol == "")
      return _Symbol;
   return InpSymbol;
}

string E0011_FormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

void E0011_ResetRiskSizing(E0011RiskSizing &r)
{
   r.ok = false;
   r.reason = "not_calculated";
   r.entry_price = 0.0;
   r.stop_price = 0.0;
   r.risk_cash_requested = 0.0;
   r.tick_size = 0.0;
   r.tick_value_loss = 0.0;
   r.volume_min = 0.0;
   r.volume_max = 0.0;
   r.volume_step = 0.0;
   r.stop_loss_cash_per_lot = 0.0;
   r.total_risk_cash_per_lot = 0.0;
   r.raw_volume = 0.0;
   r.volume = 0.0;
   r.estimated_total_risk_cash = 0.0;
}

int E0011_VolumeDigitsFromStep(const double step)
{
   if(step <= 0.0)
      return 2;
   for(int d = 0; d <= 8; d++)
   {
      double scaled = step * MathPow(10.0, d);
      if(MathAbs(scaled - MathRound(scaled)) < 1e-8)
         return d;
   }
   return 8;
}

double E0011_FloorToStep(const double value, const double step)
{
   if(step <= 0.0)
      return value;
   return MathFloor((value / step) + 1e-12) * step;
}

bool E0011_CalculateRiskVolume(
   const string symbol,
   const double entry_price,
   const double stop_price,
   const double risk_cash,
   const double commission_per_lot_round_turn,
   const bool allow_min_lot_if_risk_too_small,
   E0011RiskSizing &out
)
{
   E0011_ResetRiskSizing(out);
   out.entry_price = entry_price;
   out.stop_price = stop_price;
   out.risk_cash_requested = risk_cash;

   if(symbol == "")
   {
      out.reason = "empty_symbol";
      return false;
   }
   if(risk_cash <= 0.0)
   {
      out.reason = "risk_cash_must_be_positive";
      return false;
   }

   double stop_distance_price = MathAbs(entry_price - stop_price);
   if(stop_distance_price <= 0.0)
   {
      out.reason = "zero_stop_distance";
      return false;
   }

   out.tick_size = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
   if(out.tick_size <= 0.0)
      out.tick_size = SymbolInfoDouble(symbol, SYMBOL_POINT);

   out.tick_value_loss = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE_LOSS);
   if(out.tick_value_loss <= 0.0)
      out.tick_value_loss = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE);

   out.volume_min = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
   out.volume_max = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
   out.volume_step = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);

   if(out.tick_size <= 0.0 || out.tick_value_loss <= 0.0)
   {
      out.reason = "invalid_tick_size_or_value";
      return false;
   }
   if(out.volume_min <= 0.0 || out.volume_max <= 0.0 || out.volume_step <= 0.0)
   {
      out.reason = "invalid_volume_specs";
      return false;
   }

   out.stop_loss_cash_per_lot = (stop_distance_price / out.tick_size) * out.tick_value_loss;
   out.total_risk_cash_per_lot = out.stop_loss_cash_per_lot + MathMax(0.0, commission_per_lot_round_turn);
   if(out.total_risk_cash_per_lot <= 0.0)
   {
      out.reason = "invalid_risk_per_lot";
      return false;
   }

   out.raw_volume = risk_cash / out.total_risk_cash_per_lot;
   out.volume = E0011_FloorToStep(out.raw_volume, out.volume_step);

   if(out.volume > out.volume_max)
      out.volume = out.volume_max;

   if(out.volume < out.volume_min)
   {
      if(!allow_min_lot_if_risk_too_small)
      {
         out.reason = "volume_below_min_for_risk_budget";
         return false;
      }
      out.volume = out.volume_min;
   }

   int digits = E0011_VolumeDigitsFromStep(out.volume_step);
   out.volume = NormalizeDouble(out.volume, digits);
   if(out.volume <= 0.0)
   {
      out.reason = "normalized_volume_zero";
      return false;
   }

   out.estimated_total_risk_cash = out.total_risk_cash_per_lot * out.volume;
   if(!allow_min_lot_if_risk_too_small && out.estimated_total_risk_cash - risk_cash > MathMax(0.01, risk_cash * 0.0001))
   {
      out.reason = "estimated_risk_exceeds_budget";
      return false;
   }

   out.ok = true;
   out.reason = "ok";
   return true;
}

string E0011_RiskSizingToLog(const E0011RiskSizing &r)
{
   return "riskOk=" + (r.ok ? "true" : "false")
      + "*riskReason=" + r.reason
      + "*riskCash=" + DoubleToString(r.risk_cash_requested, 2)
      + "*entry=" + DoubleToString(r.entry_price, 8)
      + "*stop=" + DoubleToString(r.stop_price, 8)
      + "*rawVolume=" + DoubleToString(r.raw_volume, 8)
      + "*volume=" + DoubleToString(r.volume, 8)
      + "*estimatedRisk=" + DoubleToString(r.estimated_total_risk_cash, 2);
}

bool E0011_HasNewSignalCandle()
{
   string symbol = E0011_Symbol();
   datetime current_open = iTime(symbol, InpSignalTimeframe, 0);
   if(current_open <= 0)
      return false;

   if(g_last_signal_bar_open_time <= 0)
   {
      g_last_signal_bar_open_time = current_open;
      return false;
   }

   if(current_open == g_last_signal_bar_open_time)
      return false;

   g_last_signal_bar_open_time = current_open;
   return true;
}

bool E0011_OrderCommentExists(const string symbol, const long magic, const string comment)
{
   int order_total = OrdersTotal();
   for(int i = 0; i < order_total; i++)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol)
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != magic)
         continue;
      if(OrderGetString(ORDER_COMMENT) == comment)
         return true;
   }

   int pos_total = PositionsTotal();
   for(int j = 0; j < pos_total; j++)
   {
      ulong pt = PositionGetTicket(j);
      if(pt == 0 || !PositionSelectByTicket(pt))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;
      if(PositionGetString(POSITION_COMMENT) == comment)
         return true;
   }

   return false;
}

int E0011_CountManagedOpenTrades()
{
   string symbol = E0011_Symbol();
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

string E0011_BarComment(const datetime signal_time, const int direction)
{
   string side = (direction > 0 ? "B" : "S");
   return InpOrderCommentPrefix + side + "T" + IntegerToString((int)signal_time);
}

bool E0011_BuildTradePricePlan(
   const DALExecDonchianBreakoutSignal &signal,
   double &entry_price,
   double &stop_price,
   double &take_profit,
   string &reason
)
{
   reason = "not_built";
   entry_price = 0.0;
   stop_price = 0.0;
   take_profit = 0.0;

   string symbol = E0011_Symbol();
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = _Point;

   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   if(ask <= 0.0 || bid <= 0.0)
   {
      reason = "invalid_bid_ask";
      return false;
   }

   if(signal.direction > 0)
      entry_price = ask;
   else if(signal.direction < 0)
      entry_price = bid;
   else
   {
      reason = "zero_direction";
      return false;
   }

   double atr = 0.0;
   string atr_reason = "";
   if(!DAL_ExecATRClosedValue(symbol, InpSignalTimeframe, InpATRPeriod, 1, atr, atr_reason))
   {
      reason = "atr_failed_" + atr_reason;
      return false;
   }

   double stop_distance = MathMax(0.0, InpATRStopMultiplier) * atr;
   if(stop_distance <= 0.0)
   {
      reason = "invalid_atr_stop_distance";
      return false;
   }

   if(signal.direction > 0)
      stop_price = entry_price - stop_distance;
   else
      stop_price = entry_price + stop_distance;

   long stops_level_points = SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double broker_min_distance = MathMax(0.0, (double)stops_level_points * point);
   double actual_distance = MathAbs(entry_price - stop_price);
   if(broker_min_distance > 0.0 && actual_distance < broker_min_distance)
   {
      reason = "atr_stop_inside_broker_min_distance"
         + "*actualDistance=" + DoubleToString(actual_distance, digits)
         + "*brokerMinDistance=" + DoubleToString(broker_min_distance, digits)
         + "*atr=" + DoubleToString(atr, digits)
         + "*atrMultiplier=" + DoubleToString(InpATRStopMultiplier, 2);
      return false;
   }

   double r = MathAbs(entry_price - stop_price);
   double reward_r = MathMax(0.01, InpRewardR);
   if(signal.direction > 0)
      take_profit = entry_price + reward_r * r;
   else
      take_profit = entry_price - reward_r * r;

   entry_price = NormalizeDouble(entry_price, digits);
   stop_price = NormalizeDouble(stop_price, digits);
   take_profit = NormalizeDouble(take_profit, digits);

   reason = "ok"
      + "*atrReason=" + atr_reason
      + "*atrStopDistance=" + DoubleToString(stop_distance, digits)
      + "*rewardR=" + DoubleToString(reward_r, 2);
   return true;
}

bool E0011_BuildTradePlan(
   const DALExecDonchianBreakoutSignal &signal,
   double &entry_price,
   double &stop_price,
   double &take_profit,
   double &risk_money,
   E0011RiskSizing &sizing,
   string &reason
)
{
   reason = "not_built";
   entry_price = 0.0;
   stop_price = 0.0;
   take_profit = 0.0;
   risk_money = 0.0;
   E0011_ResetRiskSizing(sizing);

   string price_reason = "";
   if(!E0011_BuildTradePricePlan(signal, entry_price, stop_price, take_profit, price_reason))
   {
      reason = "price_plan_failed_" + price_reason;
      return false;
   }

   risk_money = DAL_ExecRouletteRiskMoney(g_roulette_cfg, g_roulette_state);
   if(risk_money <= 0.0)
   {
      reason = "roulette_risk_not_positive";
      return false;
   }

   if(!E0011_CalculateRiskVolume(
      E0011_Symbol(),
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

   reason = "ok"
      + "*" + price_reason
      + "*" + E0011_RiskSizingToLog(sizing)
      + "*" + DAL_ExecRouletteStateToLog(g_roulette_cfg, g_roulette_state)
      + "*" + DAL_ExecHypoGateStateToLog(g_hypo_gate_cfg, g_hypo_gate_state)
      + "*" + DAL_ExecDonchianSignalToLog(signal);
   return true;
}

bool E0011_SendMarketOrder(
   const int direction,
   const double volume,
   const double stop_price,
   const double take_profit,
   const string comment,
   string &reason
)
{
   reason = "not_sent";
   string symbol = E0011_Symbol();

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
   string symbol = E0011_Symbol();
   if(!SymbolSelect(symbol, true))
   {
      Print("DAL_E0011_INIT_FAILED *** reason=symbol_select_failed*symbol=", symbol);
      return INIT_FAILED;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);
   g_trade.SetDeviationInPoints(MathMax(0, InpSlippagePoints));

   DAL_ExecRouletteRiskDefaults(g_roulette_cfg);
   g_roulette_cfg.initial_risk_percent = InpRouletteInitialRiskPercent;
   g_roulette_cfg.save_profit_factor = InpRouletteSaveProfitFactor;
   g_roulette_cfg.persist_state = InpRoulettePersistState;
   g_roulette_cfg.state_key = "E0011_" + symbol + "_" + IntegerToString((int)InpMagicNumber);
   g_roulette_cfg.print_logs = InpPrintLogs;

   DAL_ExecRouletteInit(g_roulette_cfg, g_roulette_state);

   DAL_ExecHypoGateDefaults(g_hypo_gate_cfg);
   g_hypo_gate_cfg.enabled = InpHypoGateEnabled;
   g_hypo_gate_cfg.start_open = InpHypoGateStartOpen;
   g_hypo_gate_cfg.persist_state = InpHypoGatePersistState;
   g_hypo_gate_cfg.state_key = "E0011_" + symbol + "_" + IntegerToString((int)InpMagicNumber);
   g_hypo_gate_cfg.print_logs = InpPrintLogs;
   DAL_ExecHypoGateInit(g_hypo_gate_cfg, g_hypo_gate_state);

   g_last_signal_bar_open_time = iTime(symbol, InpSignalTimeframe, 0);

   Print("DAL_E0011_BUILD_SANITY *** build=", DAL_E0011_BUILD,
      "*symbol=", symbol,
      "*signalTf=", EnumToString(InpSignalTimeframe),
      "*donchianPeriod=", InpDonchianPeriod,
      "*atrPeriod=", InpATRPeriod,
      "*atrStopMultiplier=", DoubleToString(InpATRStopMultiplier, 2),
      "*rewardR=", DoubleToString(InpRewardR, 2),
      "*maxOpenTrades=", InpMaxOpenTrades,
      "*rouletteRiskPct=", DoubleToString(InpRouletteInitialRiskPercent, 2),
      "*rouletteSaveFactor=", DoubleToString(InpRouletteSaveProfitFactor, 4),
      "*hypoGateEnabled=", (InpHypoGateEnabled ? "true" : "false"),
      "*hypoGateStartOpen=", (InpHypoGateStartOpen ? "true" : "false"));

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   DAL_ExecRouletteSave(g_roulette_cfg, g_roulette_state);
   DAL_ExecHypoGateSave(g_hypo_gate_cfg, g_hypo_gate_state);
}

void OnTick()
{
   string symbol = E0011_Symbol();
   if(!SymbolSelect(symbol, true))
   {
      if(InpPrintLogs)
         Print("DAL_E0011_SKIP *** reason=symbol_select_failed*symbol=", symbol);
      return;
   }

   // The hypothetical layer is updated on every tick so a virtual TP/SL can be
   // resolved by price, while actual signal evaluation still runs only once per
   // closed signal-timeframe candle.
   DAL_ExecHypoGateUpdateVirtual(g_hypo_gate_cfg, g_hypo_gate_state, symbol);

   // Execution clock: evaluate once when a new signal-timeframe candle opens.
   // Therefore the signal candle is closed shift 1.
   if(!E0011_HasNewSignalCandle())
      return;

   DAL_ExecRouletteUpdate(g_roulette_cfg, g_roulette_state);

   int managed = E0011_CountManagedOpenTrades();
   if(managed >= MathMax(1, InpMaxOpenTrades))
   {
      if(InpPrintLogs)
         Print("DAL_E0011_SKIP *** reason=max_open_trades*managed=", managed,
            "*max=", MathMax(1, InpMaxOpenTrades),
            "*", DAL_ExecRouletteStateToLog(g_roulette_cfg, g_roulette_state),
            "*", DAL_ExecHypoGateStateToLog(g_hypo_gate_cfg, g_hypo_gate_state));
      return;
   }

   DALExecDonchianBreakoutSignal signal;
   string signal_reason = "";
   if(!DAL_ExecDonchianFreshBreakout(symbol, InpSignalTimeframe, InpDonchianPeriod, signal, signal_reason))
   {
      if(InpPrintLogs)
         Print("DAL_E0011_NO_SIGNAL *** ", signal_reason,
            "*", DAL_ExecRouletteStateToLog(g_roulette_cfg, g_roulette_state),
            "*", DAL_ExecHypoGateStateToLog(g_hypo_gate_cfg, g_hypo_gate_state));
      return;
   }

   double entry_price = 0.0;
   double stop_price = 0.0;
   double take_profit = 0.0;
   string price_plan_reason = "";
   if(!E0011_BuildTradePricePlan(signal, entry_price, stop_price, take_profit, price_plan_reason))
   {
      Print("DAL_E0011_PRICE_PLAN_REJECT *** direction=", DAL_ExecDonchianDirectionToString(signal.direction),
         "*signal=", DAL_ExecDonchianSignalToLog(signal),
         "*pricePlanReason=", price_plan_reason,
         "*", DAL_ExecHypoGateStateToLog(g_hypo_gate_cfg, g_hypo_gate_state));
      return;
   }

   if(!DAL_ExecHypoGateShouldTrade(g_hypo_gate_cfg, g_hypo_gate_state))
   {
      if(!DAL_ExecHypoGateHasActiveVirtual(g_hypo_gate_state))
      {
         bool opened_virtual = DAL_ExecHypoGateOpenVirtualTrade(
            g_hypo_gate_cfg,
            g_hypo_gate_state,
            signal.direction,
            entry_price,
            stop_price,
            take_profit,
            signal.signal_time,
            "blocked_signal_shadowed"
         );

         Print("DAL_E0011_HYPO_GATE_BLOCK *** action=", (opened_virtual ? "virtual_opened" : "virtual_open_failed"),
            "*direction=", DAL_ExecDonchianDirectionToString(signal.direction),
            "*entry=", DoubleToString(entry_price, 8),
            "*sl=", DoubleToString(stop_price, 8),
            "*tp=", DoubleToString(take_profit, 8),
            "*pricePlan=", price_plan_reason,
            "*signal=", DAL_ExecDonchianSignalToLog(signal),
            "*", DAL_ExecHypoGateStateToLog(g_hypo_gate_cfg, g_hypo_gate_state));
      }
      else
      {
         Print("DAL_E0011_HYPO_GATE_BLOCK *** action=waiting_existing_virtual",
            "*direction=", DAL_ExecDonchianDirectionToString(signal.direction),
            "*signal=", DAL_ExecDonchianSignalToLog(signal),
            "*", DAL_ExecHypoGateStateToLog(g_hypo_gate_cfg, g_hypo_gate_state));
      }
      return;
   }

   string comment = E0011_BarComment(signal.signal_time, signal.direction);
   if(E0011_OrderCommentExists(symbol, InpMagicNumber, comment))
   {
      if(InpPrintLogs)
         Print("DAL_E0011_SKIP *** reason=comment_already_exists*comment=", comment,
            "*", DAL_ExecHypoGateStateToLog(g_hypo_gate_cfg, g_hypo_gate_state));
      return;
   }

   if(!InpTradingEnabled)
   {
      Print("DAL_E0011_SIGNAL_DRY_RUN *** direction=", DAL_ExecDonchianDirectionToString(signal.direction),
         "*entry=", DoubleToString(entry_price, 8),
         "*sl=", DoubleToString(stop_price, 8),
         "*tp=", DoubleToString(take_profit, 8),
         "*", DAL_ExecDonchianSignalToLog(signal),
         "*", DAL_ExecRouletteStateToLog(g_roulette_cfg, g_roulette_state),
         "*", DAL_ExecHypoGateStateToLog(g_hypo_gate_cfg, g_hypo_gate_state));
      return;
   }

   double risk_money = 0.0;
   E0011RiskSizing sizing;
   string plan_reason = "";

   if(!E0011_BuildTradePlan(signal, entry_price, stop_price, take_profit, risk_money, sizing, plan_reason))
   {
      Print("DAL_E0011_PLAN_REJECT *** direction=", DAL_ExecDonchianDirectionToString(signal.direction),
         "*signal=", DAL_ExecDonchianSignalToLog(signal),
         "*planReason=", plan_reason,
         "*", DAL_ExecHypoGateStateToLog(g_hypo_gate_cfg, g_hypo_gate_state));
      return;
   }

   string send_reason = "";
   if(E0011_SendMarketOrder(signal.direction, sizing.volume, stop_price, take_profit, comment, send_reason))
   {
      Print("DAL_E0011_ORDER_SENT *** direction=", DAL_ExecDonchianDirectionToString(signal.direction),
         "*volume=", DoubleToString(sizing.volume, 8),
         "*entry=", DoubleToString(entry_price, 8),
         "*sl=", DoubleToString(stop_price, 8),
         "*tp=", DoubleToString(take_profit, 8),
         "*riskMoney=", DoubleToString(risk_money, 2),
         "*comment=", comment,
         "*plan=", plan_reason,
         "*send=", send_reason);
   }
   else
   {
      Print("DAL_E0011_ORDER_FAILED *** direction=", DAL_ExecDonchianDirectionToString(signal.direction),
         "*volume=", DoubleToString(sizing.volume, 8),
         "*sl=", DoubleToString(stop_price, 8),
         "*tp=", DoubleToString(take_profit, 8),
         "*riskMoney=", DoubleToString(risk_money, 2),
         "*comment=", comment,
         "*plan=", plan_reason,
         "*send=", send_reason);
   }
}

void OnTradeTransaction(
   const MqlTradeTransaction &trans,
   const MqlTradeRequest &request,
   const MqlTradeResult &result
)
{
   if(trans.type != TRADE_TRANSACTION_DEAL_ADD)
      return;
   if(trans.deal == 0)
      return;
   if(!HistoryDealSelect(trans.deal))
      return;

   string symbol = E0011_Symbol();
   string deal_symbol = HistoryDealGetString(trans.deal, DEAL_SYMBOL);
   if(deal_symbol != symbol)
      return;

   long magic = (long)HistoryDealGetInteger(trans.deal, DEAL_MAGIC);
   if(magic != InpMagicNumber)
      return;

   ENUM_DEAL_TYPE deal_type = (ENUM_DEAL_TYPE)HistoryDealGetInteger(trans.deal, DEAL_TYPE);
   if(deal_type != DEAL_TYPE_BUY && deal_type != DEAL_TYPE_SELL)
      return;

   ENUM_DEAL_ENTRY deal_entry = (ENUM_DEAL_ENTRY)HistoryDealGetInteger(trans.deal, DEAL_ENTRY);
   if(deal_entry != DEAL_ENTRY_OUT && deal_entry != DEAL_ENTRY_INOUT && deal_entry != DEAL_ENTRY_OUT_BY)
      return;

   double net_profit = HistoryDealGetDouble(trans.deal, DEAL_PROFIT)
      + HistoryDealGetDouble(trans.deal, DEAL_SWAP)
      + HistoryDealGetDouble(trans.deal, DEAL_COMMISSION);

   DAL_ExecHypoGateOnRealClosedDeal(g_hypo_gate_cfg, g_hypo_gate_state, net_profit, trans.deal);
}
