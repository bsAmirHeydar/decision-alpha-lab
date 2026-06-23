#ifndef __DAL_E0006_INTERNAL_HUNTS_MQH__
#define __DAL_E0006_INTERNAL_HUNTS_MQH__

#include <Execution/E0006/DAL_E0006Types.mqh>
#include <M0001/DAL_M0001Engine.mqh>

bool DAL_E0006_InternalNodeSameSideAllowed(
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_node,
   const bool same_side_only
)
{
   if(!same_side_only)
      return true;
   return (origin.type == internal_node.type);
}

bool DAL_E0006_InternalNodeHuntedByIndex(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &internal_node,
   const int until_index
)
{
   if(!internal_node.confirmed)
      return false;

   int start = internal_node.active_from_index + 1;
   if(start < 0)
      start = internal_node.index + 1;
   if(start < 0)
      start = 0;

   int end = MathMin(until_index, bars_count - 1);
   if(end < start)
      return false;

   for(int i = start; i <= end; i++)
   {
      if(DAL_M0001Hunted(internal_node.type, internal_node.price, bars[i]))
         return true;
   }
   return false;
}

int DAL_E0006_CountInternalHuntedNodesBetween(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const int from_index_exclusive,
   const int until_index_inclusive,
   const bool same_side_only
)
{
   int count = 0;
   int end = MathMin(until_index_inclusive, bars_count - 1);

   for(int k = 0; k < internal_nodes_count; k++)
   {
      DALLRuleNode inner = internal_nodes[k];
      if(!inner.confirmed)
         continue;
      if(inner.index <= from_index_exclusive)
         continue;
      if(inner.index >= end)
         continue;
      if(!DAL_E0006_InternalNodeSameSideAllowed(origin, inner, same_side_only))
         continue;
      if(DAL_E0006_InternalNodeHuntedByIndex(bars, bars_count, inner, end))
         count++;
   }

   return count;
}

int DAL_E0006_CountInternalHuntedNodesForOrigin(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const int until_index,
   const bool same_side_only
)
{
   int start_after_origin = origin.index;
   if(start_after_origin < 0)
      start_after_origin = origin.active_from_index;

   return DAL_E0006_CountInternalHuntedNodesBetween(
      bars,
      bars_count,
      origin,
      internal_nodes,
      internal_nodes_count,
      start_after_origin,
      until_index,
      same_side_only
   );
}

bool DAL_E0006_InternalHuntQualificationPassed(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &origin,
   const DALLRuleNode &internal_nodes[],
   const int internal_nodes_count,
   const DALE0006InternalHuntPolicy &policy,
   int &hunt_count,
   int &required,
   string &reason
)
{
   hunt_count = 0;
   required = MathMax(0, policy.required_hunts);

   if(!policy.enabled || required <= 0)
   {
      reason = "internal_hunt_filter_off";
      return true;
   }

   int until_index = bars_count - 1;
   hunt_count = DAL_E0006_CountInternalHuntedNodesForOrigin(
      bars,
      bars_count,
      origin,
      internal_nodes,
      internal_nodes_count,
      until_index,
      policy.same_side_only
   );

   if(hunt_count < required)
   {
      reason = "internal_hunts_below_required_" + IntegerToString(hunt_count) + "_of_" + IntegerToString(required);
      return false;
   }

   reason = "internal_hunts_ok_" + IntegerToString(hunt_count) + "_of_" + IntegerToString(required);
   return true;
}

#endif
