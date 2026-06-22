#ifndef __DAL_E0009_ORDER_ENGINE_MQH__
#define __DAL_E0009_ORDER_ENGINE_MQH__

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Execution/E0009/DAL_E0009Types.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecRisk.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>

int DAL_E0009DirectionFromOrderType(const ENUM_ORDER_TYPE t)
{
   if(t == ORDER_TYPE_BUY_LIMIT || t == ORDER_TYPE_BUY_STOP)
      return +1;
   if(t == ORDER_TYPE_SELL_LIMIT || t == ORDER_TYPE_SELL_STOP)
      return -1;
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
      if(!DAL_ExecOrderIsPendingLimit(t) && t != ORDER_TYPE_BUY_STOP && t != ORDER_TYPE_SELL_STOP)
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

bool DAL_E0009CheckOrderGeometry(
   const string symbol,
   const DALE0009HookSignal &signal,
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

   int direction = signal.direction;
   double entry = signal.entry;
   double sl = signal.sl;
   double tp = signal.tp;

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

      if(signal.order_kind == DAL_E0009_KIND_LIMIT && !(entry < ask - min_dist))
      {
         reason = "buy_limit_not_below_ask";
         return false;
      }
      if(signal.order_kind == DAL_E0009_KIND_STOP && !(entry > ask + min_dist))
      {
         reason = "buy_stop_not_above_ask";
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

      if(signal.order_kind == DAL_E0009_KIND_LIMIT && !(entry > bid + min_dist))
      {
         reason = "sell_limit_not_above_bid";
         return false;
      }
      if(signal.order_kind == DAL_E0009_KIND_STOP && !(entry < bid - min_dist))
      {
         reason = "sell_stop_not_below_bid";
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

bool DAL_E0009SendHookOrder(
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
   string &reason,
   DALE0009Diagnostics &diag
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
      diag.duplicate_skip++;
      return true;
   }

   bool is_market = (signal.order_kind == DAL_E0009_KIND_MARKET);

   if(!is_market && max_pending_per_side > 0 && DAL_E0009CountPendingByDirection(symbol, magic, signal.direction, prefix) >= max_pending_per_side)
   {
      reason = "pending_cap";
      diag.cap_reject++;
      return false;
   }

   if(max_positions_per_side > 0 && DAL_E0009CountPositionsByDirection(symbol, magic, signal.direction, prefix) >= max_positions_per_side)
   {
      reason = "position_cap";
      diag.cap_reject++;
      return false;
   }

   string geom = "";
   if(!DAL_E0009CheckOrderGeometry(symbol, signal, geom))
   {
      reason = "geometry_" + geom;
      diag.geometry_reject++;
      return false;
   }

   DALExecRiskSizing risk;
   if(!DAL_ExecCalculateRiskVolume(symbol, signal.entry, signal.sl, risk_cash, commission_per_lot, allow_min_lot, risk))
   {
      reason = "risk_" + risk.reason;
      diag.risk_reject++;
      return false;
   }

   trade.SetExpertMagicNumber(magic);

   bool ok = false;
   if(signal.order_kind == DAL_E0009_KIND_MARKET)
   {
      if(signal.direction > 0)
         ok = trade.Buy(risk.volume, symbol, 0.0, signal.sl, signal.tp, signal.comment);
      else
         ok = trade.Sell(risk.volume, symbol, 0.0, signal.sl, signal.tp, signal.comment);
   }
   else if(signal.order_kind == DAL_E0009_KIND_STOP)
   {
      if(signal.direction > 0)
         ok = trade.BuyStop(risk.volume, signal.entry, symbol, signal.sl, signal.tp, ORDER_TIME_GTC, 0, signal.comment);
      else
         ok = trade.SellStop(risk.volume, signal.entry, symbol, signal.sl, signal.tp, ORDER_TIME_GTC, 0, signal.comment);
   }
   else if(signal.order_kind == DAL_E0009_KIND_LIMIT)
   {
      if(signal.direction > 0)
         ok = trade.BuyLimit(risk.volume, signal.entry, symbol, signal.sl, signal.tp, ORDER_TIME_GTC, 0, signal.comment);
      else
         ok = trade.SellLimit(risk.volume, signal.entry, symbol, signal.sl, signal.tp, ORDER_TIME_GTC, 0, signal.comment);
   }

   if(!ok)
   {
      reason = "send_failed_" + IntegerToString((int)trade.ResultRetcode()) + "_" + trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_ticket_" + IntegerToString((int)(is_market ? trade.ResultDeal() : trade.ResultOrder()));
   return true;
}

bool DAL_E0009PricesCloseEnough(const string symbol, const double a, const double b)
{
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;
   return (MathAbs(a - b) <= point * 0.5);
}

bool DAL_E0009CheckPositionTPGeometry(
   const string symbol,
   const int direction,
   const double tp,
   string &reason
)
{
   if(tp <= 0.0)
   {
      reason = "tp_zero";
      return false;
   }

   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int stops_level = (int)SymbolInfoInteger(symbol, SYMBOL_TRADE_STOPS_LEVEL);
   double min_dist = MathMax(0.0, stops_level * point);

   if(direction > 0)
   {
      if(!(tp > bid + min_dist))
      {
         reason = "buy_tp_too_close";
         return false;
      }
   }
   else if(direction < 0)
   {
      if(!(tp < ask - min_dist))
      {
         reason = "sell_tp_too_close";
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

bool DAL_E0009FindNthHTFOppositeSwingAfterEntry(
   const DALLRuleNode &htf_nodes[],
   const int htf_nodes_count,
   const int position_direction,
   const datetime entry_time,
   const double entry_price,
   const int required_count,
   DALLRuleNode &target,
   int &found_count
)
{
   found_count = 0;
   int required = MathMax(1, required_count);

   // BUY target: confirmed HTF HIGH nodes after entry.
   // SELL target: confirmed HTF LOW nodes after entry.
   ENUM_DALNodeType wanted = (position_direction > 0 ? DAL_NODE_HIGH : DAL_NODE_LOW);

   for(int i = 0; i < htf_nodes_count; i++)
   {
      DALLRuleNode n = htf_nodes[i];
      if(!n.confirmed)
         continue;
      if(n.type != wanted)
         continue;
      if(n.active_from_time <= entry_time)
         continue;

      // Avoid placing TP on the wrong side of the entry.
      if(position_direction > 0 && n.price <= entry_price)
         continue;
      if(position_direction < 0 && n.price >= entry_price)
         continue;

      found_count++;
      if(found_count >= required)
      {
         target = n;
         return true;
      }
   }

   return false;
}

void DAL_E0009SyncHTFThirdSwingTP(
   const string symbol,
   const long magic,
   const string prefix,
   const DALLRuleNode &htf_nodes[],
   const int htf_nodes_count,
   const int required_swing_count,
   CTrade &trade,
   int &checked,
   int &modified,
   int &waiting,
   int &rejected
)
{
   checked = 0;
   modified = 0;
   waiting = 0;
   rejected = 0;

   int required = MathMax(1, required_swing_count);

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;

      string comment = PositionGetString(POSITION_COMMENT);
      if(prefix != "" && StringFind(comment, prefix, 0) != 0)
         continue;

      ENUM_POSITION_TYPE pos_type = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      int direction = (pos_type == POSITION_TYPE_BUY ? +1 : (pos_type == POSITION_TYPE_SELL ? -1 : 0));
      if(direction == 0)
         continue;

      checked++;

      datetime entry_time = (datetime)PositionGetInteger(POSITION_TIME);
      double entry = PositionGetDouble(POSITION_PRICE_OPEN);
      double sl = PositionGetDouble(POSITION_SL);
      double old_tp = PositionGetDouble(POSITION_TP);

      DALLRuleNode target;
      int found = 0;
      if(!DAL_E0009FindNthHTFOppositeSwingAfterEntry(htf_nodes, htf_nodes_count, direction, entry_time, entry, required, target, found))
      {
         waiting++;
         continue;
      }

      int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
      double new_tp = NormalizeDouble(target.price, digits);

      if(DAL_E0009PricesCloseEnough(symbol, old_tp, new_tp))
         continue;

      string geom = "";
      if(!DAL_E0009CheckPositionTPGeometry(symbol, direction, new_tp, geom))
      {
         rejected++;
         continue;
      }

      trade.SetExpertMagicNumber(magic);
      if(trade.PositionModify(ticket, sl, new_tp))
         modified++;
      else
         rejected++;
   }
}

#endif
