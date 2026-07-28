#ifndef __DAL_E0007_ORDER_ENGINE_MQH__
#define __DAL_E0007_ORDER_ENGINE_MQH__

#include <Trade/Trade.mqh>
#include <Execution/E0007/DAL_E0007Types.mqh>
#include <Execution/DAL_ExecRisk.mqh>
#include <Execution/DAL_ExecOrders.mqh>
#include <AlphaLab/UC04/AL_UC04CorePrimitives.mqh>

int DAL_E0007DirectionFromOrderType(const ENUM_ORDER_TYPE t)
{
   if(t == ORDER_TYPE_BUY_LIMIT) return +1;
   if(t == ORDER_TYPE_SELL_LIMIT) return -1;
   return 0;
}

bool DAL_E0007PricesCloseEnough(const string symbol, const double a, const double b)
{
   return AL_UC04PricesCloseEnough(symbol, a, b);
}

bool DAL_E0007CheckLimitGeometryOptionalTP(
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

int DAL_E0007CountPendingByDirection(
   const string symbol,
   const long magic,
   const int direction,
   const string prefix
)
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
      if(DAL_E0007DirectionFromOrderType(t) != direction)
         continue;

      string comment = OrderGetString(ORDER_COMMENT);
      if(prefix != "" && StringFind(comment, prefix, 0) != 0)
         continue;

      count++;
   }
   return count;
}

int DAL_E0007CountPositionsByDirection(
   const string symbol,
   const long magic,
   const int direction,
   const string prefix
)
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

      string comment = PositionGetString(POSITION_COMMENT);
      if(prefix != "" && StringFind(comment, prefix, 0) != 0)
         continue;

      count++;
   }
   return count;
}

bool DAL_E0007PendingCommentExists(
   const string symbol,
   const long magic,
   const string comment
)
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

bool DAL_E0007SendCandidateLimit(
   const string symbol,
   const long magic,
   const double risk_cash,
   const double commission_per_lot,
   const bool allow_min_lot,
   const DALE0007ExposurePolicy &exposure,
   const string comment_prefix,
   const DALE0007Candidate &c,
   CTrade &trade,
   string &reason
)
{
   if(!c.valid)
   {
      reason = c.reason;
      return false;
   }

   if(DAL_E0007PendingCommentExists(symbol, magic, c.comment))
   {
      reason = "existing_pending_same_comment";
      return true;
   }

   int max_pending = (c.direction > 0 ? exposure.max_buy_pending : exposure.max_sell_pending);
   if(max_pending > 0 && DAL_E0007CountPendingByDirection(symbol, magic, c.direction, comment_prefix) >= max_pending)
   {
      reason = "side_pending_cap";
      return false;
   }

   int max_pos = (c.direction > 0 ? exposure.max_buy_positions : exposure.max_sell_positions);
   if(max_pos > 0 && DAL_E0007CountPositionsByDirection(symbol, magic, c.direction, comment_prefix) >= max_pos)
   {
      reason = "side_position_cap";
      return false;
   }

   string geom = "";
   if(!DAL_E0007CheckLimitGeometryOptionalTP(symbol, c.direction, c.entry, c.sl, c.tp, geom))
   {
      reason = "geometry_" + geom;
      return false;
   }

   DALExecRiskSizing risk;
   if(!DAL_ExecCalculateRiskVolume(symbol, c.entry, c.sl, risk_cash, commission_per_lot, allow_min_lot, risk))
   {
      reason = "risk_" + risk.reason;
      return false;
   }

   trade.SetExpertMagicNumber(magic);

   bool ok = false;
   if(c.direction > 0)
      ok = trade.BuyLimit(risk.volume, c.entry, symbol, c.sl, c.tp, ORDER_TIME_GTC, 0, c.comment);
   else
      ok = trade.SellLimit(risk.volume, c.entry, symbol, c.sl, c.tp, ORDER_TIME_GTC, 0, c.comment);

   if(!ok)
   {
      reason = "send_failed_" + IntegerToString((int)trade.ResultRetcode()) + "_" + trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_ticket_" + IntegerToString((int)trade.ResultOrder());
   return true;
}

bool DAL_E0007CheckPositionTPGeometry(const string symbol, const int direction, const double tp, string &reason)
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

bool DAL_E0007FindNthOppositeNodeAfterTime(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int position_direction,
   const datetime entry_time,
   const double entry_price,
   const int required_count,
   DALLRuleNode &target,
   int &found_count
)
{
   found_count = 0;
   ENUM_DALNodeType target_type = (position_direction > 0 ? DAL_NODE_HIGH : DAL_NODE_LOW);
   int required = MathMax(1, required_count);

   for(int i = 0; i < nodes_count; i++)
   {
      DALLRuleNode n = nodes[i];
      if(!n.confirmed)
         continue;
      if(n.type != target_type)
         continue;
      if(n.active_from_time <= entry_time)
         continue;
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

void DAL_E0007SyncOppositeNodeTP(
   const string symbol,
   const long magic,
   const string prefix,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int opposite_node_count,
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

   int required = MathMax(1, opposite_node_count);

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

      ENUM_POSITION_TYPE type = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      int direction = (type == POSITION_TYPE_BUY ? +1 : (type == POSITION_TYPE_SELL ? -1 : 0));
      if(direction == 0)
         continue;

      checked++;

      datetime entry_time = (datetime)PositionGetInteger(POSITION_TIME);
      double entry = PositionGetDouble(POSITION_PRICE_OPEN);
      double sl = PositionGetDouble(POSITION_SL);
      double old_tp = PositionGetDouble(POSITION_TP);

      DALLRuleNode target;
      int found = 0;
      if(!DAL_E0007FindNthOppositeNodeAfterTime(nodes, nodes_count, direction, entry_time, entry, required, target, found))
      {
         waiting++;
         continue;
      }

      int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
      double new_tp = NormalizeDouble(target.price, digits);

      if(DAL_E0007PricesCloseEnough(symbol, old_tp, new_tp))
         continue;

      string geom = "";
      if(!DAL_E0007CheckPositionTPGeometry(symbol, direction, new_tp, geom))
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
