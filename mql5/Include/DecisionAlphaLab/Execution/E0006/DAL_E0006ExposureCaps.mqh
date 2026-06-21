#ifndef __DAL_E0006_EXPOSURE_CAPS_MQH__
#define __DAL_E0006_EXPOSURE_CAPS_MQH__

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Execution/E0006/DAL_E0006Types.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>

int DAL_E0006_OrderDirectionFromType(const ENUM_ORDER_TYPE type)
{
   if(type == ORDER_TYPE_BUY_LIMIT || type == ORDER_TYPE_BUY_STOP || type == ORDER_TYPE_BUY_STOP_LIMIT)
      return +1;
   if(type == ORDER_TYPE_SELL_LIMIT || type == ORDER_TYPE_SELL_STOP || type == ORDER_TYPE_SELL_STOP_LIMIT)
      return -1;
   return 0;
}

int DAL_E0006_CountOpenPositionsByDirection(const string symbol, const long magic, const int direction)
{
   int count = 0;
   for(int i = 0; i < PositionsTotal(); i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;

      ENUM_POSITION_TYPE type = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      if(direction > 0 && type == POSITION_TYPE_BUY)
         count++;
      else if(direction < 0 && type == POSITION_TYPE_SELL)
         count++;
   }
   return count;
}

bool DAL_E0006_SideBlockedByOpenCap(
   const DALE0006ExposurePolicy &policy,
   const int direction,
   const int open_buy_positions,
   const int open_sell_positions
)
{
   if(direction > 0)
      return (policy.max_buy_open_before_block > 0 && open_buy_positions >= policy.max_buy_open_before_block);
   if(direction < 0)
      return (policy.max_sell_open_before_block > 0 && open_sell_positions >= policy.max_sell_open_before_block);
   return false;
}

void DAL_E0006_DeletePendingOrdersByDirection(
   const string symbol,
   const long magic,
   const string managed_prefix,
   const int direction,
   CTrade &trade,
   int &deleted,
   int &kept,
   int &failed
)
{
   deleted = 0;
   kept = 0;
   failed = 0;

   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol)
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != magic)
         continue;

      ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(!DAL_ExecOrderIsPendingLimit(type))
         continue;
      if(DAL_E0006_OrderDirectionFromType(type) != direction)
         continue;

      string comment = OrderGetString(ORDER_COMMENT);
      if(StringFind(comment, managed_prefix, 0) != 0)
      {
         kept++;
         continue;
      }

      trade.SetExpertMagicNumber(magic);
      if(trade.OrderDelete(ticket))
         deleted++;
      else
         failed++;
   }
}

#endif
