#ifndef __DAL_E0006_REVISIT_CYCLES_MQH__
#define __DAL_E0006_REVISIT_CYCLES_MQH__

#include <Execution/E0006/DAL_E0006Types.mqh>
#include <Execution/E0006/DAL_E0006InternalHunts.mqh>
#include <M0001/DAL_M0001Engine.mqh>

bool DAL_E0006_FirstAndRevisitCyclesQualified(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const double zone_ratio,
   const DALE0006InternalHuntPolicy &hunt_policy,
   const DALE0006RevisitPolicy &revisit_policy,
   int &first_cycle_hunts,
   int &revisit_cycle_hunts,
   int &first_touch_event_id,
   int &revisit_event_id,
   string &reason
)
{
   first_cycle_hunts = 0;
   revisit_cycle_hunts = 0;
   first_touch_event_id = -1;
   revisit_event_id = -1;
   reason = "not_checked";

   if(revisit_policy.entry_phase != DAL_E0006_ENTRY_REVISIT_ONLY)
   {
      reason = "revisit_filter_off";
      return true;
   }

   DALLRuleNode single_node[];
   ArrayResize(single_node, 1);
   single_node[0] = origin;

   DALM0001Config config;
   DAL_M0001DefaultConfig(config);
   config.L = 1;
   config.zone_ratio = zone_ratio;
   config.max_events = 0;
   config.min_rtv = 0.0;

   DALM0001Event events[];
   int events_count = DAL_M0001ComputeEvents(bars, bars_count, single_node, 1, config, events);
   if(events_count < 2)
   {
      reason = "not_enough_m0001_revisits";
      return false;
   }

   int required = MathMax(0, revisit_policy.revisit_required_hunts);
   if(required <= 0)
      required = MathMax(0, hunt_policy.required_hunts);

   int first_index = -1;
   int second_index = -1;
   for(int i = 0; i < events_count; i++)
   {
      if(!events[i].touch_confirmed)
         continue;
      if(events[i].hunted)
         continue;

      if(first_index < 0)
      {
         first_index = i;
         continue;
      }

      second_index = i;
      break;
   }

   if(first_index < 0)
   {
      reason = "no_clean_first_touch_cycle";
      return false;
   }
   if(second_index < 0)
   {
      reason = "no_clean_revisit_cycle";
      return false;
   }

   first_touch_event_id = events[first_index].id;
   revisit_event_id = events[second_index].id;

   int origin_start = origin.index;
   if(origin_start < 0)
      origin_start = origin.active_from_index;

   first_cycle_hunts = DAL_E0006_CountInternalHuntedNodesBetween(
      bars,
      bars_count,
      origin,
      internal_nodes,
      internal_nodes_count,
      origin_start,
      events[first_index].entry_index,
      hunt_policy.same_side_only
   );

   revisit_cycle_hunts = DAL_E0006_CountInternalHuntedNodesBetween(
      bars,
      bars_count,
      origin,
      internal_nodes,
      internal_nodes_count,
      events[first_index].entry_index,
      events[second_index].entry_index,
      hunt_policy.same_side_only
   );

   if(revisit_policy.first_cycle_must_qualify && first_cycle_hunts < required)
   {
      reason = "first_cycle_hunts_below_required_" + IntegerToString(first_cycle_hunts) + "_of_" + IntegerToString(required);
      return false;
   }

   if(revisit_cycle_hunts < required)
   {
      reason = "revisit_cycle_hunts_below_required_" + IntegerToString(revisit_cycle_hunts) + "_of_" + IntegerToString(required);
      return false;
   }

   reason = "revisit_cycles_ok_first_" + IntegerToString(first_cycle_hunts) + "_revisit_" + IntegerToString(revisit_cycle_hunts);
   return true;
}

#endif
