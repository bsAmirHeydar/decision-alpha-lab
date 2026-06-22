#ifndef __DAL_E0008_ORDER_ENGINE_MQH__
#define __DAL_E0008_ORDER_ENGINE_MQH__

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Execution/E0008/DAL_E0008Types.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecRisk.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>

int DAL_E0008DirectionFromOrderType(const ENUM_ORDER_TYPE t)
{
   if(t == ORDER_TYPE_BUY_LIMIT) return +1;
   if(t == ORDER_TYPE_SELL_LIMIT) return -1;
   return 0;
}

bool DAL_E0008PricesCloseEnough(const string symbol, const double a, const double b)
{
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;
   return (MathAbs(a - b) <= point * 0.5);
}

bool DAL_E0008CheckLimitGeometryOptionalTP(
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
      reason = "invalid_market_quote";
      return false;
   }

   if(direction > 0)
   {
      if(!(sl < entry))
      {
         reason = "invalid_buy_sl";
         return false;
      }
      if(tp > 0.0 && !(tp > entry))
      {
         reason = "invalid_buy_tp";
         return false;
      }
      if(!(entry < ask - min_dist))
      {
         reason = "buy_limit_not_below_ask_or_too_close";
         return false;
      }
   }
   else if(direction < 0)
   {
      if(!(sl > entry))
      {
         reason = "invalid_sell_sl";
         return false;
      }
      if(tp > 0.0 && !(tp < entry))
      {
         reason = "invalid_sell_tp";
         return false;
      }
      if(!(entry > bid + min_dist))
      {
         reason = "sell_limit_not_above_bid_or_too_close";
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

int DAL_E0008CountPendingByDirection(const string symbol, const long magic, const int direction, const string prefix)
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
      if(DAL_E0008DirectionFromOrderType(t) != direction)
         continue;

      string c = OrderGetString(ORDER_COMMENT);
      if(prefix != "" && StringFind(c, prefix, 0) != 0)
         continue;

      count++;
   }

   return count;
}

int DAL_E0008CountPositionsByDirection(const string symbol, const long magic, const int direction, const string prefix)
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

bool DAL_E0008PendingExistsByComment(const string symbol, const long magic, const string comment)
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

bool DAL_E0008SendPlanLimit(
   const string symbol,
   const long magic,
   const string prefix,
   const double risk_cash,
   const double commission_per_lot,
   const bool allow_min_lot,
   const DALE0008ExposurePolicy &exposure,
   const DALE0008TradePlan &plan,
   CTrade &trade,
   string &reason
)
{
   if(!plan.valid)
   {
      reason = plan.reason;
      return false;
   }

   if(DAL_E0008PendingExistsByComment(symbol, magic, plan.comment))
   {
      reason = "existing_pending_same_comment";
      return true;
   }

   int max_pending = (plan.direction > 0 ? exposure.max_buy_pending : exposure.max_sell_pending);
   if(max_pending > 0 && DAL_E0008CountPendingByDirection(symbol, magic, plan.direction, prefix) >= max_pending)
   {
      reason = "side_pending_cap";
      return false;
   }

   int max_pos = (plan.direction > 0 ? exposure.max_buy_positions : exposure.max_sell_positions);
   if(max_pos > 0 && DAL_E0008CountPositionsByDirection(symbol, magic, plan.direction, prefix) >= max_pos)
   {
      reason = "side_position_cap";
      return false;
   }

   string geom = "";
   if(!DAL_E0008CheckLimitGeometryOptionalTP(symbol, plan.direction, plan.entry, plan.sl, plan.tp, geom))
   {
      reason = "geometry_" + geom;
      return false;
   }

   DALExecRiskSizing risk;
   if(!DAL_ExecCalculateRiskVolume(symbol, plan.entry, plan.sl, risk_cash, commission_per_lot, allow_min_lot, risk))
   {
      reason = "risk_" + risk.reason;
      return false;
   }

   trade.SetExpertMagicNumber(magic);

   bool ok = false;
   if(plan.direction > 0)
      ok = trade.BuyLimit(risk.volume, plan.entry, symbol, plan.sl, plan.tp, ORDER_TIME_GTC, 0, plan.comment);
   else
      ok = trade.SellLimit(risk.volume, plan.entry, symbol, plan.sl, plan.tp, ORDER_TIME_GTC, 0, plan.comment);

   if(!ok)
   {
      reason = "send_failed_" + IntegerToString((int)trade.ResultRetcode()) + "_" + trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_ticket_" + IntegerToString((int)trade.ResultOrder());
   return true;
}

bool DAL_E0008CheckPositionTPGeometry(const string symbol, const int direction, const double tp, string &reason)
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

bool DAL_E0008FindNthOppositeNodeAfterTime(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int direction,
   const datetime entry_time,
   const double entry_price,
   const int required_count,
   DALLRuleNode &target
)
{
   ENUM_DALNodeType wanted = (direction > 0 ? DAL_NODE_HIGH : DAL_NODE_LOW);
   int found = 0;
   int required = MathMax(1, required_count);

   for(int i = 0; i < nodes_count; i++)
   {
      DALLRuleNode n = nodes[i];
      if(!n.confirmed)
         continue;
      if(n.type != wanted)
         continue;
      if(n.active_from_time <= entry_time)
         continue;
      if(direction > 0 && n.price <= entry_price)
         continue;
      if(direction < 0 && n.price >= entry_price)
         continue;

      found++;
      if(found >= required)
      {
         target = n;
         return true;
      }
   }

   return false;
}

void DAL_E0008SyncOppositeNodeTP(
   const string symbol,
   const long magic,
   const string prefix,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int required_count,
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

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;

      string c = PositionGetString(POSITION_COMMENT);
      if(prefix != "" && StringFind(c, prefix, 0) != 0)
         continue;

      ENUM_POSITION_TYPE t = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      int direction = (t == POSITION_TYPE_BUY ? +1 : (t == POSITION_TYPE_SELL ? -1 : 0));
      if(direction == 0)
         continue;

      checked++;

      datetime entry_time = (datetime)PositionGetInteger(POSITION_TIME);
      double entry = PositionGetDouble(POSITION_PRICE_OPEN);
      double sl = PositionGetDouble(POSITION_SL);
      double old_tp = PositionGetDouble(POSITION_TP);

      DALLRuleNode target;
      if(!DAL_E0008FindNthOppositeNodeAfterTime(nodes, nodes_count, direction, entry_time, entry, required_count, target))
      {
         waiting++;
         continue;
      }

      int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
      double new_tp = NormalizeDouble(target.price, digits);

      if(DAL_E0008PricesCloseEnough(symbol, old_tp, new_tp))
         continue;

      string geom = "";
      if(!DAL_E0008CheckPositionTPGeometry(symbol, direction, new_tp, geom))
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
