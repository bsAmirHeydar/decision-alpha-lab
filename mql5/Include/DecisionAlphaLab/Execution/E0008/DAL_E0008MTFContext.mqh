#ifndef __DAL_E0008_MTF_CONTEXT_MQH__
#define __DAL_E0008_MTF_CONTEXT_MQH__

#include <DecisionAlphaLab/Execution/E0008/DAL_E0008Types.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>

bool DAL_E0008_LoadM0001Map(
   const string symbol,
   const ENUM_TIMEFRAMES tf,
   const int bars_requested,
   const int L,
   const double zone_ratio,
   const int exit_gap,
   const int max_events,
   DALBar &bars[],
   int &bars_count,
   DALLRuleNode &nodes[],
   int &nodes_count,
   DALM0001Event &events[],
   int &events_count,
   string &reason
)
{
   bars_count = DAL_LoadBarsChronological(symbol, tf, bars_requested, true, bars);
   if(bars_count <= 0)
   {
      reason = "bars_load_failed";
      return false;
   }

   nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, MathMax(1, L), nodes);
   if(nodes_count <= 0)
   {
      reason = "no_nodes";
      return false;
   }

   DALM0001Config cfg;
   DAL_M0001DefaultConfig(cfg);
   cfg.L = MathMax(1, L);
   cfg.zone_ratio = MathMax(0.0, MathMin(0.9999, zone_ratio));
   cfg.exit_gap = MathMax(1, exit_gap);
   cfg.consume_mode = DAL_M0001_CONSUME_BY_HUNT;
   cfg.consume_on_touch = false;
   cfg.max_events = MathMax(1, max_events);
   cfg.min_rtv = 0.0;

   events_count = DAL_M0001ComputeEvents(bars, bars_count, nodes, nodes_count, cfg, events);
   if(events_count <= 0)
   {
      reason = "no_m0001_events";
      return false;
   }

   reason = "ok";
   return true;
}

double DAL_E0008_EventZoneHeight(const DALM0001Event &event)
{
   return MathAbs(event.territory_upper - event.territory_lower);
}

bool DAL_E0008_FindFirstAndSecondEventByNode(
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

      if(events[i].revisit_id == 0)
      {
         first_event = events[i];
         has_first = true;
      }
      else if(events[i].revisit_id > 0)
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

double DAL_E0008_FirstReactionR(
   const DALBar &bars[],
   const int bars_count,
   const DALM0001Event &event,
   const int max_bars_after_exit
)
{
   double h = DAL_E0008_EventZoneHeight(event);
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

bool DAL_E0008_FindDestinationFromExtremes(
   const DALBar &bars[],
   const int bars_count,
   const int direction,
   const double from_price,
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
      double best = from_price;
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
      double best = from_price;
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

bool DAL_E0008_BuildBestContextFromMap(
   const ENUM_TIMEFRAMES tf,
   const DALBar &bars[],
   const int bars_count,
   const DALM0001Event &events[],
   const int events_count,
   const DALE0008SourcePolicy &source,
   const int destination_lookback_bars,
   DALE0008ContextState &best
)
{
   DAL_E0008_ResetContext(best);
   best.tf = tf;

   if(events_count <= 0 || bars_count <= 0)
   {
      best.reason = "empty_map";
      return false;
   }

   double best_score = -1.0e100;

   for(int i = events_count - 1; i >= 0; i--)
   {
      DALM0001Event first = events[i];
      if(first.revisit_id != 0)
         continue;
      if(!first.touch_confirmed)
         continue;

      DALM0001Event f, second;
      bool has_first = false, has_second = false;
      if(!DAL_E0008_FindFirstAndSecondEventByNode(events, events_count, first.node_id, f, has_first, second, has_second))
         continue;

      if(!has_first || f.id != first.id)
         continue;

      if(source.require_first_touch_not_hunted && first.hunted)
         continue;

      int survival_bars = bars_count - 1 - first.entry_index;
      if(source.min_source_survival_bars > 0 && survival_bars < source.min_source_survival_bars)
         continue;

      int age = bars_count - 1 - first.entry_index;
      if(source.max_source_age_bars > 0 && age > source.max_source_age_bars)
         continue;

      double reaction_r = DAL_E0008_FirstReactionR(bars, bars_count, first, source.max_source_age_bars);
      if(reaction_r < MathMax(0.0, source.min_first_reaction_r))
         continue;

      int direction = (first.node_type == DAL_NODE_LOW ? +1 : -1);
      double destination = 0.0;
      if(!DAL_E0008_FindDestinationFromExtremes(bars, bars_count, direction, first.node_price, destination_lookback_bars, destination))
         continue;

      double z = DAL_E0008_EventZoneHeight(first);
      if(z <= 0.0)
         continue;

      double dest_r = MathAbs(destination - first.node_price) / z;

      // Score rewards first reaction, open destination distance, and recency.
      double recency_score = 1.0 / (1.0 + MathMax(0, age));
      double score = reaction_r * 10.0 + dest_r + recency_score;

      if(has_second)
         score += 10.0;

      if(score > best_score)
      {
         best_score = score;
         best.valid = true;
         best.reason = "ok";
         best.direction = direction;
         best.role = (has_second ? DAL_E0008_CONTEXT_SOURCE_REVISIT : DAL_E0008_CONTEXT_SOURCE);

         best.node_id = first.node_id;
         best.event_id = first.id;
         best.revisit_id = first.revisit_id;
         best.node_type = first.node_type;

         best.node_time = first.node_time;
         best.touch_time = first.entry_time;
         best.exit_time = first.exit_time;
         best.entry_index = first.entry_index;
         best.exit_index = first.exit_index;

         best.node_price = first.node_price;
         best.zone_lower = first.territory_lower;
         best.zone_upper = first.territory_upper;
         best.zone_height = z;

         best.first_touch_hunted = first.hunted;
         best.has_second_revisit = has_second;
         best.first_reaction_r = reaction_r;
         best.survival_bars = survival_bars;
         best.source_age_bars = age;
         best.destination_price = destination;
         best.context_score = score;
      }
   }

   if(!best.valid)
   {
      best.reason = "no_context_passed_source_gates";
      return false;
   }

   return true;
}

int DAL_E0008_CountAlignedContexts(
   const DALE0008ContextState &c1,
   const bool use1,
   const DALE0008ContextState &c2,
   const bool use2,
   const DALE0008ContextState &c3,
   const bool use3,
   const int direction,
   const bool reject_conflict,
   bool &has_conflict
)
{
   int aligned = 0;
   has_conflict = false;

   if(use1 && c1.valid)
   {
      if(c1.direction == direction) aligned++;
      else has_conflict = true;
   }
   if(use2 && c2.valid)
   {
      if(c2.direction == direction) aligned++;
      else has_conflict = true;
   }
   if(use3 && c3.valid)
   {
      if(c3.direction == direction) aligned++;
      else has_conflict = true;
   }

   if(reject_conflict && has_conflict)
      return -aligned;

   return aligned;
}

bool DAL_E0008_SelectPrimaryContext(
   const DALE0008ContextState &c1,
   const bool use1,
   const DALE0008ContextState &c2,
   const bool use2,
   const DALE0008ContextState &c3,
   const bool use3,
   DALE0008ContextState &primary
)
{
   DAL_E0008_ResetContext(primary);

   double best_score = -1.0e100;

   if(use1 && c1.valid && c1.context_score > best_score)
   {
      primary = c1;
      best_score = c1.context_score;
   }
   if(use2 && c2.valid && c2.context_score > best_score)
   {
      primary = c2;
      best_score = c2.context_score;
   }
   if(use3 && c3.valid && c3.context_score > best_score)
   {
      primary = c3;
      best_score = c3.context_score;
   }

   if(!primary.valid)
   {
      primary.reason = "no_primary_context";
      return false;
   }

   return true;
}

#endif
