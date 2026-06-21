#ifndef __DAL_E0006_EXIT_TARGETS_MQH__
#define __DAL_E0006_EXIT_TARGETS_MQH__

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Execution/E0006/DAL_E0006Types.mqh>

bool DAL_E0006_FindNthOppositeInternalNodeAfterEntry(
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const int position_direction,
   const datetime entry_time,
   const double entry_price,
   const int required_count,
   DALLRuleNode &target_node,
   int &found_count,
   string &reason
)
{
   found_count = 0;
   reason = "not_found";

   int required = MathMax(1, required_count);
   ENUM_DALNodeType target_type = (position_direction > 0 ? DAL_NODE_HIGH : DAL_NODE_LOW);

   for(int i = 0; i < internal_nodes_count; i++)
   {
      DALLRuleNode node = internal_nodes[i];
      if(!node.confirmed)
         continue;
      if(node.type != target_type)
         continue;
      if(node.active_from_time <= entry_time)
         continue;
      if(position_direction > 0 && node.price <= entry_price)
         continue;
      if(position_direction < 0 && node.price >= entry_price)
         continue;

      found_count++;
      if(found_count >= required)
      {
         target_node = node;
         reason = "ok";
         return true;
      }
   }

   reason = "opposite_internal_nodes_" + IntegerToString(found_count) + "_of_" + IntegerToString(required);
   return false;
}

bool DAL_E0006_CheckPositionTPGeometry(
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

   if(point <= 0.0 || bid <= 0.0 || ask <= 0.0)
   {
      reason = "invalid_market_quote";
      return false;
   }

   if(direction > 0 && !(tp > bid + min_dist))
   {
      reason = "buy_tp_not_above_bid_or_too_close";
      return false;
   }
   if(direction < 0 && !(tp < ask - min_dist))
   {
      reason = "sell_tp_not_below_ask_or_too_close";
      return false;
   }

   reason = "ok";
   return true;
}

#endif
