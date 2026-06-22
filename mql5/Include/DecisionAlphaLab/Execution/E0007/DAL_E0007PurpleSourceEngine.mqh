#ifndef __DAL_E0007_PURPLE_SOURCE_ENGINE_MQH__
#define __DAL_E0007_PURPLE_SOURCE_ENGINE_MQH__

#include <DecisionAlphaLab/Execution/E0007/DAL_E0007Types.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>

double DAL_E0007SpreadPrice(const string symbol)
{
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   if(ask > 0.0 && bid > 0.0 && ask >= bid)
      return ask - bid;

   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   int spread_points = (int)SymbolInfoInteger(symbol, SYMBOL_SPREAD);
   return MathMax(0.0, spread_points * point);
}

bool DAL_E0007SameSideNode(const ENUM_DALNodeType origin_type, const DALLRuleNode &node)
{
   return (node.type == origin_type);
}

bool DAL_E0007FindSourceEventByNode(
   const DALM0001Event &events[],
   const int events_count,
   const int node_id,
   DALM0001Event &first_event,
   bool &has_first,
   DALM0001Event &second_event,
   bool &has_second
)
{
   has_first = false;
   has_second = false;

   for(int i = 0; i < events_count; i++)
   {
      if(events[i].node_id != node_id)
         continue;

      if(!has_first || events[i].revisit_id < first_event.revisit_id)
      {
         if(has_first)
         {
            second_event = first_event;
            has_second = true;
         }
         first_event = events[i];
         has_first = true;
      }
      else if(events[i].revisit_id > first_event.revisit_id)
      {
         if(!has_second || events[i].revisit_id < second_event.revisit_id)
         {
            second_event = events[i];
            has_second = true;
         }
      }
   }

   return has_first;
}

double DAL_E0007ZoneHeight(const DALM0001Event &event)
{
   return MathAbs(event.territory_upper - event.territory_lower);
}

double DAL_E0007FirstReactionR(
   const DALBar &bars[],
   const int bars_count,
   const DALM0001Event &event,
   const int max_bars_after_exit
)
{
   double h = DAL_E0007ZoneHeight(event);
   if(h <= 0.0)
      return 0.0;

   int start = event.exit_index + 1;
   if(start < 0 || start >= bars_count)
      return 0.0;

   int end = bars_count - 1;
   if(max_bars_after_exit > 0)
      end = MathMin(end, start + max_bars_after_exit - 1);

   double best = 0.0;
   for(int i = start; i <= end; i++)
   {
      if(event.node_type == DAL_NODE_LOW)
         best = MathMax(best, bars[i].high - event.territory_upper);
      else
         best = MathMax(best, event.territory_lower - bars[i].low);
   }

   return best / h;
}

bool DAL_E0007FindSecondaryNodeInFirstTouch(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &event,
   DALLRuleNode &secondary
)
{
   bool found = false;

   for(int i = 0; i < nodes_count; i++)
   {
      DALLRuleNode n = nodes[i];
      if(!n.confirmed)
         continue;
      if(!DAL_E0007SameSideNode(event.node_type, n))
         continue;
      if(n.id == event.node_id)
         continue;

      // Secondary node must be born inside the first touch/base window.
      if(n.index < event.entry_index || n.index > event.exit_index)
         continue;

      if(!found)
      {
         secondary = n;
         found = true;
         continue;
      }

      // For BUY from LOW, prefer the lowest internal LOW.
      // For SELL from HIGH, prefer the highest internal HIGH.
      if(event.node_type == DAL_NODE_LOW && n.price < secondary.price)
         secondary = n;
      if(event.node_type == DAL_NODE_HIGH && n.price > secondary.price)
         secondary = n;
   }

   return found;
}

bool DAL_E0007BuildLiveTerritoryForNode(
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

bool DAL_E0007FindDestinationFromRecentExtremes(
   const DALBar &bars[],
   const int bars_count,
   const int direction,
   const double entry,
   const int lookback,
   double &destination
)
{
   destination = 0.0;
   if(bars_count <= 0 || direction == 0)
      return false;

   int start = 0;
   if(lookback > 0)
      start = MathMax(0, bars_count - lookback);

   bool found = false;
   if(direction > 0)
   {
      double best = entry;
      for(int i = start; i < bars_count; i++)
      {
         if(bars[i].high > best)
         {
            best = bars[i].high;
            found = true;
         }
      }
      destination = best;
   }
   else
   {
      double best = entry;
      for(int i = start; i < bars_count; i++)
      {
         if(bars[i].low < best)
         {
            best = bars[i].low;
            found = true;
         }
      }
      destination = best;
   }

   return found;
}

bool DAL_E0007BuildCandidateFromEvent(
   const string symbol,
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &first_event,
   const bool has_second_event,
   const DALM0001Event &second_event,
   const DALE0007SourcePolicy &source,
   const DALE0007PricingPolicy &pricing,
   const ENUM_DAL_E0007_ENTRY_MODE selected_mode,
   DALE0007Candidate &out
)
{
   DAL_E0007_ResetCandidate(out);

   if(!first_event.touch_confirmed)
   {
      out.reason = "first_touch_not_confirmed";
      return false;
   }

   if(source.require_first_touch_not_hunted && first_event.hunted)
   {
      out.reason = "first_touch_hunted";
      return false;
   }

   int survival_bars = bars_count - 1 - first_event.entry_index;
   out.survival_bars = survival_bars;
   if(source.min_source_survival_bars > 0 && survival_bars < source.min_source_survival_bars)
   {
      out.reason = "source_survival_bars_below_required";
      return false;
   }

   int age = bars_count - 1 - first_event.entry_index;
   if(source.max_touch_age_bars > 0 && age > source.max_touch_age_bars)
   {
      out.reason = "source_touch_too_old";
      return false;
   }

   double first_reaction_r = DAL_E0007FirstReactionR(bars, bars_count, first_event, source.max_touch_age_bars);
   out.first_reaction_r = first_reaction_r;
   if(first_reaction_r < MathMax(0.0, source.min_first_reaction_r))
   {
      out.reason = "first_reaction_r_below_required";
      return false;
   }

   ENUM_DAL_E0007_ENTRY_MODE mode = selected_mode;
   if(mode == DAL_E0007_ENTRY_ALL_MODES)
      mode = DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT;

   if(mode == DAL_E0007_ENTRY_FIRST_TOUCH_CONTEXT && !source.allow_first_touch_research_entry)
   {
      out.reason = "first_touch_entry_disabled";
      return false;
   }

   if((mode == DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT || mode == DAL_E0007_ENTRY_SECONDARY_NODE_ZONE)
      && source.require_second_revisit_for_entry
      && has_second_event)
   {
      // If the second event is already confirmed in the available live history,
      // the pending revisit opportunity is usually gone. Keep it as research only.
      out.reason = "second_revisit_already_confirmed";
      return false;
   }

   DALLRuleNode secondary;
   bool has_secondary = DAL_E0007FindSecondaryNodeInFirstTouch(nodes, nodes_count, first_event, secondary);

   if(mode == DAL_E0007_ENTRY_SECONDARY_NODE_ZONE && !has_secondary)
   {
      out.reason = "secondary_node_missing";
      return false;
   }

   double sec_lower = 0.0, sec_upper = 0.0;
   bool sec_hunted = false;
   if(has_secondary)
   {
      if(!DAL_E0007BuildLiveTerritoryForNode(bars, bars_count, secondary, source.zone_ratio, sec_lower, sec_upper, sec_hunted))
         has_secondary = false;
      if(sec_hunted && mode == DAL_E0007_ENTRY_SECONDARY_NODE_ZONE)
      {
         out.reason = "secondary_node_already_hunted";
         return false;
      }
   }

   out.entry_mode = mode;
   out.role = (mode == DAL_E0007_ENTRY_EARLY_LADDER_STEP ? DAL_E0007_ROLE_EARLY_LADDER_STEP : DAL_E0007_ROLE_SOURCE_REVISIT);

   out.direction = (first_event.node_type == DAL_NODE_LOW ? +1 : -1);
   out.source_event_id = first_event.id;
   out.source_revisit_id = first_event.revisit_id;
   out.origin_node_id = first_event.node_id;
   out.origin_type = first_event.node_type;

   out.origin_time = first_event.node_time;
   out.source_touch_time = first_event.entry_time;
   out.source_confirm_time = first_event.touch_confirmed_time;
   out.source_entry_index = first_event.entry_index;
   out.source_exit_index = first_event.exit_index;

   out.origin_node_price = first_event.node_price;
   out.origin_zone_lower = first_event.territory_lower;
   out.origin_zone_upper = first_event.territory_upper;
   out.zone_height = DAL_E0007ZoneHeight(first_event);

   out.first_touch_hunted = first_event.hunted;
   out.second_revisit_exists = has_second_event;

   out.has_secondary_node = has_secondary;
   if(has_secondary)
   {
      out.secondary_node = secondary;
      out.secondary_zone_lower = sec_lower;
      out.secondary_zone_upper = sec_upper;
   }

   double spread = DAL_E0007SpreadPrice(symbol);
   double entry_lower = first_event.territory_lower;
   double entry_upper = first_event.territory_upper;
   double stop_node = first_event.node_price;

   if(mode == DAL_E0007_ENTRY_SECONDARY_NODE_ZONE && has_secondary)
   {
      entry_lower = sec_lower;
      entry_upper = sec_upper;
      stop_node = secondary.price;
   }

   if(first_event.node_type == DAL_NODE_LOW)
   {
      out.entry = entry_upper + spread * MathMax(0.0, pricing.buy_entry_spread_mult);

      if(pricing.stop_mode == DAL_E0007_STOP_ORIGIN_ZONE_BACK)
         out.sl = first_event.territory_lower;
      else if(pricing.stop_mode == DAL_E0007_STOP_ORIGIN_NODE)
         out.sl = first_event.node_price;
      else
         out.sl = (has_secondary ? secondary.price : first_event.node_price);
   }
   else
   {
      out.entry = entry_lower;

      double raw_stop = first_event.territory_upper;
      if(pricing.stop_mode == DAL_E0007_STOP_ORIGIN_NODE)
         raw_stop = first_event.node_price;
      else if(pricing.stop_mode == DAL_E0007_STOP_SECONDARY_NODE || pricing.stop_mode == DAL_E0007_STOP_MICRO_EXTREME)
         raw_stop = (has_secondary ? secondary.price : first_event.node_price);

      // SELL stops must include spread.
      out.sl = raw_stop + spread * MathMax(0.0, pricing.sell_stop_spread_mult);
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

   out.tp = 0.0;
   if(pricing.target_mode == DAL_E0007_TARGET_FIXED_R && pricing.fixed_reward_r > 0.0)
   {
      if(out.direction > 0)
         out.tp = out.entry + out.risk_distance * pricing.fixed_reward_r;
      else
         out.tp = out.entry - out.risk_distance * pricing.fixed_reward_r;
      out.tp = NormalizeDouble(out.tp, digits);
   }

   out.destination_price = 0.0;
   out.potential_r = 0.0;
   if(source.use_destination_r_filter)
   {
      if(!DAL_E0007FindDestinationFromRecentExtremes(bars, bars_count, out.direction, out.entry, source.destination_lookback_bars, out.destination_price))
      {
         out.reason = "destination_missing";
         return false;
      }
      out.potential_r = MathAbs(out.destination_price - out.entry) / out.risk_distance;
      if(out.potential_r < MathMax(0.0, source.min_potential_r))
      {
         out.reason = "potential_r_below_required";
         return false;
      }
   }

   out.valid = true;
   out.reason = "ok";
   return true;
}

int DAL_E0007BuildCandidates(
   const string symbol,
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALE0007SourcePolicy &source,
   const DALE0007PricingPolicy &pricing,
   DALE0007Candidate &candidates[]
)
{
   ArrayResize(candidates, 0);
   if(events_count <= 0 || nodes_count <= 0)
      return 0;

   for(int e = events_count - 1; e >= 0; e--)
   {
      DALM0001Event first = events[e];

      // We only use first touch events as source-proving events.
      if(first.revisit_id != 0)
         continue;

      DALM0001Event first_check, second;
      bool has_first = false, has_second = false;
      if(!DAL_E0007FindSourceEventByNode(events, events_count, first.node_id, first_check, has_first, second, has_second))
         continue;
      if(!has_first || first_check.id != first.id)
         continue;

      ENUM_DAL_E0007_ENTRY_MODE modes[4];
      int modes_count = 1;
      modes[0] = pricing.entry_mode;
      if(pricing.entry_mode == DAL_E0007_ENTRY_ALL_MODES)
      {
         modes_count = 3;
         modes[0] = DAL_E0007_ENTRY_SOURCE_SECOND_REVISIT;
         modes[1] = DAL_E0007_ENTRY_SECONDARY_NODE_ZONE;
         modes[2] = DAL_E0007_ENTRY_EARLY_LADDER_STEP;
      }

      for(int m = 0; m < modes_count; m++)
      {
         DALE0007Candidate c;
         if(DAL_E0007BuildCandidateFromEvent(symbol, bars, bars_count, nodes, nodes_count, first, has_second, second, source, pricing, modes[m], c))
         {
            int n = ArraySize(candidates);
            ArrayResize(candidates, n + 1);
            c.comment = "DALE7_N" + IntegerToString(c.origin_node_id) + "_E" + IntegerToString(c.source_event_id) + "_" + DAL_E0007EntryModeName(c.entry_mode);
            candidates[n] = c;
         }
      }
   }

   return ArraySize(candidates);
}

#endif
