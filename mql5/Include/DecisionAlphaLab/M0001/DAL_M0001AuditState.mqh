#ifndef __DAL_M0001_AUDIT_STATE_MQH__
#define __DAL_M0001_AUDIT_STATE_MQH__

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>

struct DALM0001NodeAuditState
{
   int id;
   int node_id;
   int node_index;
   int active_from_index;
   int current_index;
   int extreme_index;
   int invalidated_index;

   datetime node_time;
   datetime active_from_time;
   datetime current_time;
   datetime extreme_time;
   datetime invalidated_time;

   ENUM_DALNodeType node_type;
   double node_price;
   double expansion_extreme;
   double territory_lower;
   double territory_upper;

   bool invalidated;
   bool active;
};

int DAL_M0001AppendNodeAuditState(
   DALM0001NodeAuditState &states[],
   const DALM0001NodeAuditState &state
)
{
   int size = ArraySize(states);
   ArrayResize(states, size + 1);
   states[size] = state;
   return size;
}

int DAL_M0001ComputeNodeAuditStates(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Config &config,
   DALM0001NodeAuditState &states[]
)
{
   ArrayResize(states, 0);

   if(bars_count <= 0 || nodes_count <= 0)
      return 0;

   int state_id = 0;

   for(int n = 0; n < nodes_count; n++)
   {
      DALLRuleNode node = nodes[n];
      int start = node.active_from_index;

      if(start < 0 || start >= bars_count)
         continue;

      double extreme = DAL_M0001InitialExtreme(node.type, bars[start]);
      int extreme_index = start;

      bool invalidated = false;
      int invalidated_index = -1;

      for(int i = start; i < bars_count; i++)
      {
         double old_extreme = extreme;
         extreme = DAL_M0001UpdateExtreme(node.type, extreme, bars[i]);

         if(extreme != old_extreme)
            extreme_index = i;

         if(!invalidated && DAL_M0001Hunted(node.type, node.price, bars[i]))
         {
            invalidated = true;
            invalidated_index = i;
            // Keep scanning for audit extreme, but mark the live hunt zone as invalidated.
         }
      }

      double lower = node.price;
      double upper = node.price;
      DAL_M0001Territory(node.type, node.price, extreme, config.zone_ratio, lower, upper);

      DALM0001NodeAuditState state;
      state.id = state_id;
      state.node_id = node.id;
      state.node_index = node.index;
      state.active_from_index = node.active_from_index;
      state.current_index = bars_count - 1;
      state.extreme_index = extreme_index;
      state.invalidated_index = invalidated_index;

      state.node_time = node.time;
      state.active_from_time = node.active_from_time;
      state.current_time = bars[bars_count - 1].time;
      state.extreme_time = bars[extreme_index].time;
      state.invalidated_time = invalidated_index >= 0 ? bars[invalidated_index].time : 0;

      state.node_type = node.type;
      state.node_price = node.price;
      state.expansion_extreme = extreme;
      state.territory_lower = lower;
      state.territory_upper = upper;

      state.invalidated = invalidated;
      state.active = !invalidated;

      DAL_M0001AppendNodeAuditState(states, state);
      state_id++;
   }

   return ArraySize(states);
}

#endif
