#ifndef __DAL_E0006_ZONE_PRICING_MQH__
#define __DAL_E0006_ZONE_PRICING_MQH__

#include <DecisionAlphaLab/Execution/E0006/DAL_E0006Types.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>

bool DAL_E0006_BuildLiveNodeTerritory(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const double zone_ratio,
   double &last_extreme,
   double &last_lower,
   double &last_upper,
   bool &hunted
)
{
   last_extreme = 0.0;
   last_lower = node.price;
   last_upper = node.price;
   hunted = false;

   if(bars_count <= 0 || node.active_from_index < 0 || node.active_from_index >= bars_count)
      return false;

   last_extreme = DAL_M0001InitialExtreme(node.type, bars[node.active_from_index]);
   for(int i = node.active_from_index; i < bars_count; i++)
   {
      last_extreme = DAL_M0001UpdateExtreme(node.type, last_extreme, bars[i]);
      DAL_M0001Territory(node.type, node.price, last_extreme, zone_ratio, last_lower, last_upper);

      if(DAL_M0001Hunted(node.type, node.price, bars[i]))
         hunted = true;
   }

   return true;
}

bool DAL_E0006_BuildZoneOrderPlan(
   const string symbol,
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const double zone_ratio,
   const double spread,
   const DALE0006PricingPolicy &pricing,
   DALE0006ZoneOrderPlan &plan
)
{
   DAL_E0006_ResetZoneOrderPlan(plan);

   if(!node.confirmed)
   {
      plan.reason = "node_unconfirmed";
      return false;
   }
   if(node.active_from_index < 0 || node.active_from_index >= bars_count)
   {
      plan.reason = "node_not_active_in_window";
      return false;
   }

   double extreme = 0.0, lower = 0.0, upper = 0.0;
   bool hunted = false;
   if(!DAL_E0006_BuildLiveNodeTerritory(bars, bars_count, node, zone_ratio, extreme, lower, upper, hunted))
   {
      plan.reason = "live_territory_build_failed";
      return false;
   }
   if(hunted)
   {
      plan.reason = "node_hunted_invalidated";
      return false;
   }

   double reward_r = (pricing.reward_r > 0.0 ? MathMax(0.01, pricing.reward_r) : 0.0);

   plan.node_id = node.id;
   plan.node_index = node.index;
   plan.node_type = node.type;
   plan.node_time = node.time;
   plan.active_from_time = node.active_from_time;
   plan.node_price = node.price;
   plan.live_extreme = extreme;
   plan.origin_zone_lower = lower;
   plan.origin_zone_upper = upper;
   plan.zone_lower = lower;
   plan.zone_upper = upper;
   plan.entry_anchor_node_id = node.id;
   plan.entry_anchor_node_type = node.type;
   plan.entry_anchor_node_time = node.time;
   plan.entry_anchor_node_price = node.price;
   plan.spread = spread;
   plan.reward_r = reward_r;

   if(node.type == DAL_NODE_LOW)
   {
      plan.direction = +1;
      plan.entry = upper + spread * MathMax(0.0, pricing.buy_entry_spread_mult);
      if(pricing.stop_anchor == DAL_E0006_STOP_REVISIT_SECONDARY_NODE)
      {
         plan.reason = "secondary_stop_requires_revisit_context";
         return false;
      }
      plan.sl = (pricing.stop_anchor == DAL_E0006_STOP_NODE_PRICE ? node.price : lower);
      plan.risk_distance = MathAbs(plan.entry - plan.sl);
      plan.tp = (reward_r > 0.0 ? plan.entry + plan.risk_distance * reward_r : 0.0);
   }
   else
   {
      plan.direction = -1;
      plan.entry = lower;
      if(pricing.stop_anchor == DAL_E0006_STOP_REVISIT_SECONDARY_NODE)
      {
         plan.reason = "secondary_stop_requires_revisit_context";
         return false;
      }
      double raw_stop = (pricing.stop_anchor == DAL_E0006_STOP_NODE_PRICE ? node.price : upper);
      plan.sl = raw_stop + spread * MathMax(0.0, pricing.sell_stop_spread_mult);
      plan.risk_distance = MathAbs(plan.entry - plan.sl);
      plan.tp = (reward_r > 0.0 ? plan.entry - plan.risk_distance * reward_r + spread * MathMax(0.0, pricing.sell_tp_spread_mult) : 0.0);
   }

   if(plan.risk_distance <= 0.0)
   {
      plan.reason = "zero_stop_distance";
      return false;
   }

   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   plan.entry = NormalizeDouble(plan.entry, digits);
   plan.sl = NormalizeDouble(plan.sl, digits);
   plan.tp = NormalizeDouble(plan.tp, digits);

   plan.valid = true;
   plan.reason = "ok";
   return true;
}

#endif
