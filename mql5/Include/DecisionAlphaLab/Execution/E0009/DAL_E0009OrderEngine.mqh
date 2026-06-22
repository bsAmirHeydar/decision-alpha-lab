#ifndef __DAL_E0009_ORDER_ENGINE_MQH__
#define __DAL_E0009_ORDER_ENGINE_MQH__

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Execution/E0009/DAL_E0009Types.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecRisk.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>

int DAL_E0009DirectionFromOrderType(const ENUM_ORDER_TYPE t)
{
   if(t == ORDER_TYPE_BUY_LIMIT) return +1;
   if(t == ORDER_TYPE_SELL_LIMIT) return -1;
   return 0;
}

bool DAL_E0009PendingExistsByComment(const string symbol, const long magic, const string comment)
{
   for(int i = OrdersTotal() - 1; i >= 0; i--)
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
   return false;
}

int DAL_E0009CountPendingByDirection(const string symbol, const long magic, const int direction, const string prefix)
{
   int count = 0;

   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol)
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != magic)
         continue;

      ENUM_ORDER_TYPE t = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(!DAL_ExecOrderIsPendingLimit(t))
         continue;
      if(DAL_E0009DirectionFromOrderType(t) != direction)
         continue;

      string c = OrderGetString(ORDER_COMMENT);
      if(prefix != "" && StringFind(c, prefix, 0) != 0)
         continue;

      count++;
   }

   return count;
}

int DAL_E0009CountPositionsByDirection(const string symbol, const long magic, const int direction, const string prefix)
{
   int count = 0;

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;

      ENUM_POSITION_TYPE t = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      int d = (t == POSITION_TYPE_BUY ? +1 : (t == POSITION_TYPE_SELL ? -1 : 0));
      if(d != direction)
         continue;

      string c = PositionGetString(POSITION_COMMENT);
      if(prefix != "" && StringFind(c, prefix, 0) != 0)
         continue;

      count++;
   }

   return count;
}

bool DAL_E0009CheckLimitGeometry(
   const string symbol,
   const int direction,
   const double entry,
   const double sl,
   const double tp,
   string &reason
)
{
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int stops_level = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_dist = MathMax(0.0, stops_level * point);

   if(point <= 0.0 || bid <= 0.0 || ask <= 0.0)
   {
      reason = "invalid_quote";
      return false;
   }

   if(direction > 0)
   {
      if(!(sl < entry))
      {
         reason = "bad_buy_sl";
         return false;
      }
      if(tp > 0.0 && !(tp > entry))
      {
         reason = "bad_buy_tp";
         return false;
      }
      if(!(entry < ask - min_dist))
      {
         reason = "buy_limit_not_below_ask";
         return false;
      }
   }
   else if(direction < 0)
   {
      if(!(sl > entry))
      {
         reason = "bad_sell_sl";
         return false;
      }
      if(tp > 0.0 && !(tp < entry))
      {
         reason = "bad_sell_tp";
         return false;
      }
      if(!(entry > bid + min_dist))
      {
         reason = "sell_limit_not_above_bid";
         return false;
      }
   }
   else
   {
      reason = "zero_direction";
      return false;
   }

   reason = "ok";
   return true;
}

bool DAL_E0009SendHookLimit(
   const string symbol,
   const long magic,
   const string prefix,
   const double risk_cash,
   const double commission_per_lot,
   const bool allow_min_lot,
   const int max_pending_per_side,
   const int max_positions_per_side,
   const DALE0009HookSignal &signal,
   CTrade &trade,
   string &reason
)
{
   if(!signal.valid)
   {
      reason = signal.reason;
      return false;
   }

   if(DAL_E0009PendingExistsByComment(symbol, magic, signal.comment))
   {
      reason = "existing_pending_same_hook";
      return true;
   }

   if(max_pending_per_side > 0 && DAL_E0009CountPendingByDirection(symbol, magic, signal.direction, prefix) >= max_pending_per_side)
   {
      reason = "pending_cap";
      return false;
   }

   if(max_positions_per_side > 0 && DAL_E0009CountPositionsByDirection(symbol, magic, signal.direction, prefix) >= max_positions_per_side)
   {
      reason = "position_cap";
      return false;
   }

   string geom = "";
   if(!DAL_E0009CheckLimitGeometry(symbol, signal.direction, signal.entry, signal.sl, signal.tp, geom))
   {
      reason = "geometry_" + geom;
      return false;
   }

   DALExecRiskSizing risk;
   if(!DAL_ExecCalculateRiskVolume(symbol, signal.entry, signal.sl, risk_cash, commission_per_lot, allow_min_lot, risk))
   {
      reason = "risk_" + risk.reason;
      return false;
   }

   trade.SetExpertMagicNumber(magic);

   bool ok = false;
   if(signal.direction > 0)
      ok = trade.BuyLimit(risk.volume, signal.entry, symbol, signal.sl, signal.tp, ORDER_TIME_GTC, 0, signal.comment);
   else
      ok = trade.SellLimit(risk.volume, signal.entry, symbol, signal.sl, signal.tp, ORDER_TIME_GTC, 0, signal.comment);

   if(!ok)
   {
      reason = "send_failed_" + IntegerToString((int)trade.ResultRetcode()) + "_" + trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_ticket_" + IntegerToString((int)trade.ResultOrder());
   return true;
}

#endif
