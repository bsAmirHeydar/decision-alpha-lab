#ifndef __DAL_EXEC_ORDERS_MQH__
#define __DAL_EXEC_ORDERS_MQH__

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Common/DAL_Common.mqh>

struct DALExecOrderCounts
{
   int positions_total;
   int pending_total;
   int long_total;
   int short_total;
   int long_positions;
   int short_positions;
   int buy_limit_pending;
   int sell_limit_pending;
};

void DAL_ExecResetOrderCounts(DALExecOrderCounts &c)
{
   c.positions_total = 0;
   c.pending_total = 0;
   c.long_total = 0;
   c.short_total = 0;
   c.long_positions = 0;
   c.short_positions = 0;
   c.buy_limit_pending = 0;
   c.sell_limit_pending = 0;
}

bool DAL_ExecOrderIsPendingLimit(const ENUM_ORDER_TYPE t)
{
   return (t == ORDER_TYPE_BUY_LIMIT || t == ORDER_TYPE_SELL_LIMIT);
}

bool DAL_ExecOrderCommentExists(const string symbol, const long magic, const string comment)
{
   int total = OrdersTotal();
   for(int i = 0; i < total; i++)
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

void DAL_ExecCountExposure(const string symbol, const long magic, DALExecOrderCounts &counts)
{
   DAL_ExecResetOrderCounts(counts);

   int pos_total = PositionsTotal();
   for(int i = 0; i < pos_total; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;

      long type = PositionGetInteger(POSITION_TYPE);
      counts.positions_total++;
      if(type == POSITION_TYPE_BUY)
      {
         counts.long_total++;
         counts.long_positions++;
      }
      else if(type == POSITION_TYPE_SELL)
      {
         counts.short_total++;
         counts.short_positions++;
      }
   }

   int ord_total = OrdersTotal();
   for(int j = 0; j < ord_total; j++)
   {
      ulong ticket = OrderGetTicket(j);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol)
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != magic)
         continue;

      ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(!DAL_ExecOrderIsPendingLimit(type))
         continue;

      counts.pending_total++;
      if(type == ORDER_TYPE_BUY_LIMIT)
      {
         counts.long_total++;
         counts.buy_limit_pending++;
      }
      else if(type == ORDER_TYPE_SELL_LIMIT)
      {
         counts.short_total++;
         counts.sell_limit_pending++;
      }
   }
}

bool DAL_ExecCanOpenDirection(
   const string symbol,
   const long magic,
   const int direction,
   const int max_simultaneous_trades,
   const bool allow_opposite_trades,
   string &reason
)
{
   DALExecOrderCounts counts;
   DAL_ExecCountExposure(symbol, magic, counts);

   int total = counts.positions_total + counts.pending_total;
   if(max_simultaneous_trades >= 0 && total >= max_simultaneous_trades)
   {
      reason = "max_simultaneous_reached";
      return false;
   }

   if(!allow_opposite_trades)
   {
      if(direction > 0 && counts.short_total > 0)
      {
         reason = "opposite_short_exposure_exists";
         return false;
      }
      if(direction < 0 && counts.long_total > 0)
      {
         reason = "opposite_long_exposure_exists";
         return false;
      }
   }

   reason = "ok";
   return true;
}

void DAL_ExecNormalizePrices(const string symbol, double &entry, double &sl, double &tp)
{
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   entry = NormalizeDouble(entry, digits);
   sl = NormalizeDouble(sl, digits);
   tp = NormalizeDouble(tp, digits);
}

bool DAL_ExecCheckLimitGeometry(
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
      if(!(sl < entry && tp > entry))
      {
         reason = "invalid_buy_sl_tp_geometry";
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
      if(!(sl > entry && tp < entry))
      {
         reason = "invalid_sell_sl_tp_geometry";
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

bool DAL_ExecPlaceLimitOrder(
   const string symbol,
   const long magic,
   const int direction,
   const double volume,
   double entry,
   double sl,
   double tp,
   const string comment,
   const int expiration_minutes,
   CTrade &trade,
   string &reason
)
{
   DAL_ExecNormalizePrices(symbol, entry, sl, tp);

   if(!DAL_ExecCheckLimitGeometry(symbol, direction, entry, sl, tp, reason))
      return false;

   if(volume <= 0.0)
   {
      reason = "volume_zero";
      return false;
   }

   datetime expiration = 0;
   ENUM_ORDER_TYPE_TIME type_time = ORDER_TIME_GTC;
   if(expiration_minutes > 0)
   {
      type_time = ORDER_TIME_SPECIFIED;
      expiration = TimeCurrent() + expiration_minutes * 60;
   }

   trade.SetExpertMagicNumber(magic);

   bool ok = false;
   if(direction > 0)
      ok = trade.BuyLimit(volume, entry, symbol, sl, tp, type_time, expiration, comment);
   else
      ok = trade.SellLimit(volume, entry, symbol, sl, tp, type_time, expiration, comment);

   if(!ok)
   {
      reason = "trade_send_failed_retcode_" + IntegerToString((int)trade.ResultRetcode()) + "_" + trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_ticket_" + IntegerToString((int)trade.ResultOrder());
   return true;
}

#endif
