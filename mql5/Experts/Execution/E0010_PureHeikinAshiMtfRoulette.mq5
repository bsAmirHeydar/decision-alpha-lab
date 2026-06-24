//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0010 Pure Heikin Ashi MTF Roulette          |
//| Closed M1 HA body flip aligned with current-forming M10 HA body |
//+------------------------------------------------------------------+
#property strict
#property version   "1.04"
#property description "Execution E0010: pure Heikin Ashi MTF entry with reusable Roulette risk."

#include <Trade/Trade.mqh>
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
input double InpCommissionPerLotRoundTurn = 0.0;
input bool InpAllowMinLotIfRiskTooSmall = false;

input bool InpTradingEnabled = true;
input bool InpPrintLogs = true;

#define DAL_E0010_BUILD "1.04"
string InpOrderCommentPrefix = "E0010HA";

CTrade g_trade;
DALExecRouletteRiskConfig g_roulette_cfg;
DALExecRouletteRiskState g_roulette_state;
datetime g_last_entry_bar_open_time = 0;

struct E0010RiskSizing
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

void E0010_ResetRiskSizing(E0010RiskSizing &r)
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

int E0010_VolumeDigitsFromStep(const double step)
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

double E0010_FloorToStep(const double value, const double step)
{
   if(step <= 0.0)
      return value;
   return MathFloor((value / step) + 1e-12) * step;
}

bool E0010_CalculateRiskVolume(
   const string symbol,
   const double entry_price,
   const double stop_price,
   const double risk_cash,
   const double commission_per_lot_round_turn,
   const bool allow_min_lot_if_risk_too_small,
   E0010RiskSizing &out
)
{
   E0010_ResetRiskSizing(out);
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
   out.volume = E0010_FloorToStep(out.raw_volume, out.volume_step);

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

   int digits = E0010_VolumeDigitsFromStep(out.volume_step);
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

string E0010_RiskSizingToLog(const E0010RiskSizing &r)
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

bool E0010_HasNewEntryCandle()
{
   string symbol = E0010_Symbol();
   datetime current_open = iTime(symbol, InpEntryTimeframe, 0);
   if(current_open <= 0)
      return false;

   if(g_last_entry_bar_open_time <= 0)
   {
      g_last_entry_bar_open_time = current_open;
      return false;
   }

   if(current_open == g_last_entry_bar_open_time)
      return false;

   g_last_entry_bar_open_time = current_open;
   return true;
}

bool E0010_OrderCommentExists(const string symbol, const long magic, const string comment)
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

   // Higher timeframe is deliberately shift 0: current-forming HA candle.
   // Direction is ha_close > ha_open for buy-bias and ha_close < ha_open for sell-bias.
   if(htf_current.ha_dir == 0)
   {
      reason = "htf_current_ha_equal_body";
      return false;
   }

   int flip_direction = 0;
   string flip_reason = "";
   if(!DAL_ExecHAClosedBodyFlip(E0010_Symbol(), InpEntryTimeframe, flip_direction, ltf_previous_closed, ltf_signal_closed, flip_reason))
   {
      reason = "ltf_flip_failed_" + flip_reason
         + "*htfDir=" + DAL_ExecHABodyDirectionToString(htf_current.ha_dir);
      return false;
   }

   // Exact entry rule:
   // Buy: HTF current HA close > HA open, and LTF closed body flips from close < open to close > open.
   // Sell: HTF current HA close < HA open, and LTF closed body flips from close > open to close < open.
   if(flip_direction != htf_current.ha_dir)
   {
      reason = "direction_mismatch*htf=" + DAL_ExecHABodyDirectionToString(htf_current.ha_dir)
         + "*ltfFlip=" + DAL_ExecHABodyDirectionToString(flip_direction);
      return false;
   }

   direction = flip_direction;
   reason = "ok*htfCurrent=" + DAL_ExecHABodyDirectionToString(htf_current.ha_dir)
      + "*ltfPrevClosed=" + DAL_ExecHABodyDirectionToString(ltf_previous_closed.ha_dir)
      + "*ltfSignalClosed=" + DAL_ExecHABodyDirectionToString(ltf_signal_closed.ha_dir)
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
   E0010RiskSizing &sizing,
   string &reason
)
{
   reason = "not_built";
   entry_price = 0.0;
   stop_price = 0.0;
   take_profit = 0.0;
   risk_money = 0.0;
   E0010_ResetRiskSizing(sizing);

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

   risk_money = DAL_ExecRouletteRiskMoney(g_roulette_cfg, g_roulette_state);
   if(risk_money <= 0.0)
   {
      reason = "roulette_risk_not_positive";
      return false;
   }

   if(!E0010_CalculateRiskVolume(
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

   reason = "ok*" + E0010_RiskSizingToLog(sizing)
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
   string symbol = E0010_Symbol();
   if(!SymbolSelect(symbol, true))
   {
      Print("DAL_E0010_INIT_FAILED *** reason=symbol_select_failed*symbol=", symbol);
      return INIT_FAILED;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);
   g_trade.SetDeviationInPoints(MathMax(0, InpSlippagePoints));

   DAL_ExecRouletteRiskDefaults(g_roulette_cfg);
   g_roulette_cfg.initial_risk_percent = InpRouletteInitialRiskPercent;
   g_roulette_cfg.save_profit_factor = InpRouletteSaveProfitFactor;
   g_roulette_cfg.persist_state = InpRoulettePersistState;
   g_roulette_cfg.state_key = "E0010_" + symbol + "_" + IntegerToString((int)InpMagicNumber);
   g_roulette_cfg.print_logs = InpPrintLogs;

   DAL_ExecRouletteInit(g_roulette_cfg, g_roulette_state);

   g_last_entry_bar_open_time = iTime(symbol, InpEntryTimeframe, 0);

   Print("DAL_E0010_BUILD_SANITY *** build=", DAL_E0010_BUILD,
      "*symbol=", symbol,
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
   string symbol = E0010_Symbol();
   if(!SymbolSelect(symbol, true))
   {
      if(InpPrintLogs)
         Print("DAL_E0010_SKIP *** reason=symbol_select_failed*symbol=", symbol);
      return;
   }

   // Important execution clock:
   // E0010 evaluates only once when a new lower-timeframe bar opens.
   // That means the previous lower-timeframe candle has just closed.
   if(!E0010_HasNewEntryCandle())
      return;

   // Roulette is also updated on the lower-timeframe close clock, not every tick.
   DAL_ExecRouletteUpdate(g_roulette_cfg, g_roulette_state);

   int managed = E0010_CountManagedOpenTrades();
   if(managed >= MathMax(1, InpMaxOpenTrades))
   {
      if(InpPrintLogs)
         Print("DAL_E0010_SKIP *** reason=max_open_trades*managed=", managed,
            "*max=", MathMax(1, InpMaxOpenTrades),
            "*", DAL_ExecRouletteStateToLog(g_roulette_cfg, g_roulette_state));
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
   if(E0010_OrderCommentExists(symbol, InpMagicNumber, comment))
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
   E0010RiskSizing sizing;
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
