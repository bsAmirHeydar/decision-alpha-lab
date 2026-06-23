#ifndef __DAL_E0008_MICRO_TRIGGER_MQH__
#define __DAL_E0008_MICRO_TRIGGER_MQH__

#include <Execution/E0008/DAL_E0008Types.mqh>
#include <Execution/E0008/DAL_E0008MTFContext.mqh>

double DAL_E0008_SpreadPrice(const string symbol)
{
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   if(ask > 0.0 && bid > 0.0 && ask >= bid)
      return ask - bid;

   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int spread_points = (int)SymbolInfoInteger(symbol, SYMBOL_SPREAD);
   return MathMax(0.0, spread_points * point);
}

bool DAL_E0008_BuildLiveTerritoryForNode(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const double zone_ratio,
   double &lower,
   double &upper,
   bool &hunted
)
{
   lower = node.price;
   upper = node.price;
   hunted = false;

   if(node.active_from_index < 0 || node.active_from_index >= bars_count)
      return false;

   double extreme = DAL_M0001InitialExtreme(node.type, bars[node.active_from_index]);

   for(int i = node.active_from_index; i < bars_count; i++)
   {
      extreme = DAL_M0001UpdateExtreme(node.type, extreme, bars[i]);
      DAL_M0001Territory(node.type, node.price, extreme, zone_ratio, lower, upper);
      if(DAL_M0001Hunted(node.type, node.price, bars[i]))
         hunted = true;
   }

   return (upper > lower);
}

bool DAL_E0008_FindLatestSameSideNode(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int direction,
   const datetime after_time,
   const int max_age_bars,
   const int current_index,
   DALLRuleNode &node
)
{
   ENUM_DALNodeType wanted = (direction > 0 ? DAL_NODE_LOW : DAL_NODE_HIGH);
   bool found = false;

   for(int i = nodes_count - 1; i >= 0; i--)
   {
      DALLRuleNode n = nodes[i];
      if(!n.confirmed)
         continue;
      if(n.type != wanted)
         continue;
      if(after_time > 0 && n.active_from_time <= after_time)
         continue;
      if(max_age_bars > 0 && current_index - n.index > max_age_bars)
         continue;

      node = n;
      found = true;
      break;
   }

   return found;
}

bool DAL_E0008_FindSecondaryNodeInsideSource(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const int direction,
   const datetime source_entry_time,
   const datetime source_exit_time,
   DALLRuleNode &secondary
)
{
   ENUM_DALNodeType wanted = (direction > 0 ? DAL_NODE_LOW : DAL_NODE_HIGH);
   bool found = false;

   for(int i = 0; i < nodes_count; i++)
   {
      DALLRuleNode n = nodes[i];
      if(!n.confirmed)
         continue;
      if(n.type != wanted)
         continue;
      if(source_entry_time > 0 && n.time < source_entry_time)
         continue;
      if(source_exit_time > 0 && n.time > source_exit_time)
         continue;

      if(!found)
      {
         secondary = n;
         found = true;
         continue;
      }

      if(direction > 0 && n.price < secondary.price)
         secondary = n;
      if(direction < 0 && n.price > secondary.price)
         secondary = n;
   }

   return found;
}

bool DAL_E0008_BuildMicroTrigger(
   const string symbol,
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALE0008ContextState &local,
   const DALE0008ExecutionPolicy &exec,
   const DALE0008SourcePolicy &source,
   const ENUM_DAL_E0008_ENTRY_MODE selected_mode,
   DALE0008MicroTrigger &out
)
{
   DAL_E0008_ResetMicroTrigger(out);
   out.direction = local.direction;
   out.entry_mode = selected_mode;

   if(!local.valid)
   {
      out.reason = "local_context_invalid";
      return false;
   }

   ENUM_DAL_E0008_ENTRY_MODE mode = selected_mode;
   if(mode == DAL_E0008_ENTRY_ALL_MODES)
      mode = DAL_E0008_ENTRY_MICRO_NODE_REVISIT;

   DALLRuleNode anchor;
   bool has_anchor = false;
   double lower = local.zone_lower;
   double upper = local.zone_upper;
   bool hunted = false;

   if(mode == DAL_E0008_ENTRY_LOCAL_SOURCE_REVISIT)
   {
      anchor.id = local.node_id;
      anchor.type = local.node_type;
      anchor.price = local.node_price;
      anchor.time = local.node_time;
      anchor.index = local.entry_index;
      anchor.active_from_index = local.entry_index;
      anchor.active_from_time = local.touch_time;
      anchor.confirmed = true;
      has_anchor = true;
      lower = local.zone_lower;
      upper = local.zone_upper;
   }
   else if(mode == DAL_E0008_ENTRY_LOCAL_SECONDARY_NODE)
   {
      DALLRuleNode secondary;
      if(!DAL_E0008_FindSecondaryNodeInsideSource(nodes, nodes_count, local.direction, local.touch_time, local.exit_time, secondary))
      {
         out.reason = "secondary_node_missing";
         return false;
      }

      if(!DAL_E0008_BuildLiveTerritoryForNode(bars, bars_count, secondary, source.zone_ratio, lower, upper, hunted))
      {
         out.reason = "secondary_territory_failed";
         return false;
      }

      if(hunted)
      {
         out.reason = "secondary_already_hunted";
         return false;
      }

      anchor = secondary;
      has_anchor = true;

      out.has_secondary_node = true;
      out.secondary_node = secondary;
      out.secondary_zone_lower = lower;
      out.secondary_zone_upper = upper;
   }
   else
   {
      // MICRO_NODE_REVISIT and EARLY_LADDER_STEP both use latest same-side micro node.
      DALLRuleNode micro;
      datetime after_time = (local.exit_time > 0 ? local.exit_time : local.touch_time);
      if(!DAL_E0008_FindLatestSameSideNode(nodes, nodes_count, local.direction, after_time, exec.max_micro_node_age_bars, bars_count - 1, micro))
      {
         out.reason = "micro_node_missing";
         return false;
      }

      if(!DAL_E0008_BuildLiveTerritoryForNode(bars, bars_count, micro, source.zone_ratio, lower, upper, hunted))
      {
         out.reason = "micro_territory_failed";
         return false;
      }

      if(hunted)
      {
         out.reason = "micro_node_already_hunted";
         return false;
      }

      anchor = micro;
      has_anchor = true;
   }

   if(!has_anchor || upper <= lower)
   {
      out.reason = "anchor_missing_or_bad_zone";
      return false;
   }

   double spread = DAL_E0008_SpreadPrice(symbol);

   out.node_id = anchor.id;
   out.node_type = anchor.type;
   out.node_time = anchor.time;
   out.node_price = anchor.price;
   out.zone_lower = lower;
   out.zone_upper = upper;

   if(local.direction > 0)
   {
      out.entry = upper + spread * MathMax(0.0, exec.buy_entry_spread_mult);

      if(exec.stop_mode == DAL_E0008_STOP_LOCAL_SOURCE_ZONE_BACK)
         out.sl = local.zone_lower;
      else if(exec.stop_mode == DAL_E0008_STOP_LOCAL_SOURCE_NODE)
         out.sl = local.node_price;
      else if(exec.stop_mode == DAL_E0008_STOP_SECONDARY_NODE && out.has_secondary_node)
         out.sl = out.secondary_node.price;
      else
         out.sl = anchor.price;
   }
   else
   {
      out.entry = lower;

      double raw_stop = anchor.price;
      if(exec.stop_mode == DAL_E0008_STOP_LOCAL_SOURCE_ZONE_BACK)
         raw_stop = local.zone_upper;
      else if(exec.stop_mode == DAL_E0008_STOP_LOCAL_SOURCE_NODE)
         raw_stop = local.node_price;
      else if(exec.stop_mode == DAL_E0008_STOP_SECONDARY_NODE && out.has_secondary_node)
         raw_stop = out.secondary_node.price;

      // SELL stops must include spread.
      out.sl = raw_stop + spread * MathMax(0.0, exec.sell_stop_spread_mult);
   }

   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   out.entry = NormalizeDouble(out.entry, digits);
   out.sl = NormalizeDouble(out.sl, digits);

   out.risk_distance = MathAbs(out.entry - out.sl);
   if(out.risk_distance <= 0.0)
   {
      out.reason = "zero_risk_distance";
      return false;
   }

   out.valid = true;
   out.reason = "ok";
   return true;
}

bool DAL_E0008_BuildTradePlan(
   const string symbol,
   const DALE0008ContextState &primary_context,
   const DALE0008ContextState &local_context,
   const DALE0008MicroTrigger &trigger,
   const DALE0008ExecutionPolicy &exec,
   DALE0008TradePlan &plan
)
{
   DAL_E0008_ResetTradePlan(plan);

   if(!primary_context.valid)
   {
      plan.reason = "primary_context_invalid";
      return false;
   }
   if(!local_context.valid)
   {
      plan.reason = "local_context_invalid";
      return false;
   }
   if(!trigger.valid)
   {
      plan.reason = "trigger_invalid_" + trigger.reason;
      return false;
   }
   if(primary_context.direction != trigger.direction)
   {
      plan.reason = "context_trigger_direction_mismatch";
      return false;
   }

   plan.direction = trigger.direction;
   plan.entry_mode = trigger.entry_mode;
   plan.stop_mode = exec.stop_mode;
   plan.target_mode = exec.target_mode;

   plan.context_tf = primary_context.tf;
   plan.local_tf = local_context.tf;

   plan.context_node_id = primary_context.node_id;
   plan.local_node_id = local_context.node_id;
   plan.micro_node_id = trigger.node_id;

   plan.entry = trigger.entry;
   plan.sl = trigger.sl;
   plan.risk_distance = trigger.risk_distance;
   plan.destination_price = primary_context.destination_price;

   if(plan.risk_distance <= 0.0)
   {
      plan.reason = "zero_risk";
      return false;
   }

   plan.potential_r = MathAbs(plan.destination_price - plan.entry) / plan.risk_distance;
   if(plan.potential_r < MathMax(0.0, exec.min_potential_r))
   {
      plan.reason = "potential_r_below_required";
      return false;
   }

   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   plan.tp = 0.0;

   if(exec.target_mode == DAL_E0008_TARGET_CONTEXT_DESTINATION)
      plan.tp = NormalizeDouble(plan.destination_price, digits);
   else if(exec.target_mode == DAL_E0008_TARGET_FIXED_R && exec.fixed_reward_r > 0.0)
   {
      if(plan.direction > 0)
         plan.tp = NormalizeDouble(plan.entry + plan.risk_distance * exec.fixed_reward_r, digits);
      else
         plan.tp = NormalizeDouble(plan.entry - plan.risk_distance * exec.fixed_reward_r, digits);
   }

   plan.comment = "DALE8_C" + IntegerToString(plan.context_node_id)
      + "_L" + IntegerToString(plan.local_node_id)
      + "_M" + IntegerToString(plan.micro_node_id)
      + "_" + DAL_E0008EntryModeName(plan.entry_mode);

   plan.valid = true;
   plan.reason = "ok";
   return true;
}

#endif
