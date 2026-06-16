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
   int consumed_index;
   ENUM_DALM0001ConsumeReason consume_reason;

   datetime node_time;
   datetime active_from_time;
   datetime current_time;
   datetime extreme_time;
   datetime invalidated_time;
   datetime consumed_time;

   ENUM_DALNodeType node_type;
   double node_price;
   double expansion_extreme;
   double territory_lower;
   double territory_upper;

   bool invalidated;
   bool consumed;
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

// README touch semantics: touch starts first event; consumption happens after event completion.
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

      bool consumed = false;
      bool invalidated = false;
      int consumed_index = -1;
      int invalidated_index = -1;
      int last_active_index = bars_count - 1;
      ENUM_DALM0001ConsumeReason consume_reason = DAL_M0001_CONSUMED_NONE;

      bool touch_event_active = false;
      int touch_outside_count = 0;
      int touch_event_entry_index = -1;
      double frozen_extreme = extreme;
      int frozen_extreme_index = extreme_index;
      double frozen_lower = node.price;
      double frozen_upper = node.price;

      for(int i = start; i < bars_count; i++)
      {
         if(!touch_event_active)
         {
            double old_extreme = extreme;
            extreme = DAL_M0001UpdateExtreme(node.type, extreme, bars[i]);

            if(extreme != old_extreme)
               extreme_index = i;

            double live_lower = node.price;
            double live_upper = node.price;
            DAL_M0001Territory(node.type, node.price, extreme, config.zone_ratio, live_lower, live_upper);

            bool touched_zone = DAL_CandleIntersectsZone(bars[i].low, bars[i].high, live_lower, live_upper);
            bool hunted_node = DAL_M0001Hunted(node.type, node.price, bars[i]);

            // Node break always has priority over a touch candidate.
            // If a candle both touches the zone and breaks the node, this is
            // not a confirmed touch consume; it is a HUNT consume.
            if(hunted_node)
            {
               consumed = true;
               invalidated = true;
               consumed_index = i;
               invalidated_index = i;
               consume_reason = DAL_M0001_CONSUMED_HUNT;
               last_active_index = i;
               break;
            }

            if(DAL_M0001ConsumesOnTouch(config) && touched_zone)
            {
               // Touch is provisional first. It becomes a confirmed TOUCH
               // consume only after exit_gap consecutive candles outside the
               // frozen event territory. Until then, it can still become HUNT.
               touch_event_active = true;
               touch_event_entry_index = i;
               touch_outside_count = 0;
               frozen_extreme = extreme;
               frozen_extreme_index = extreme_index;
               frozen_lower = live_lower;
               frozen_upper = live_upper;
               last_active_index = i;
               continue;
            }

            continue;
         }

         // Pending touch / active event.
         // The event geometry is frozen, but a node break before confirmation
         // converts the pending touch into HUNT.
         last_active_index = i;

         bool hunted_node = DAL_M0001Hunted(node.type, node.price, bars[i]);
         if(hunted_node)
         {
            consumed = true;
            invalidated = true;
            consumed_index = i;
            invalidated_index = i;
            consume_reason = DAL_M0001_CONSUMED_HUNT;
            last_active_index = i;
            break;
         }

         bool inside_frozen_zone = DAL_CandleIntersectsZone(
            bars[i].low,
            bars[i].high,
            frozen_lower,
            frozen_upper
         );

         if(inside_frozen_zone)
            touch_outside_count = 0;
         else
            touch_outside_count++;

         if(touch_outside_count >= config.exit_gap)
         {
            consumed = true;
            consumed_index = i;
            consume_reason = DAL_M0001_CONSUMED_TOUCH;
            last_active_index = i;

            // TOUCH is confirmed only now. Freeze final audit state at the
            // first-event geometry, not at a later moving extreme.
            extreme = frozen_extreme;
            extreme_index = frozen_extreme_index;
            break;
         }
      }

      double lower = node.price;
      double upper = node.price;
      if(touch_event_active)
      {
         lower = frozen_lower;
         upper = frozen_upper;
         extreme = frozen_extreme;
         extreme_index = frozen_extreme_index;
      }
      else
      {
         DAL_M0001Territory(node.type, node.price, extreme, config.zone_ratio, lower, upper);
      }

      DALM0001NodeAuditState state;
      state.id = state_id;
      state.node_id = node.id;
      state.node_index = node.index;
      state.active_from_index = node.active_from_index;
      state.current_index = last_active_index;
      state.extreme_index = extreme_index;
      state.invalidated_index = invalidated_index;
      state.consumed_index = consumed_index;
      state.consume_reason = consume_reason;

      state.node_time = node.time;
      state.active_from_time = node.active_from_time;
      state.current_time = bars[last_active_index].time;
      state.extreme_time = bars[extreme_index].time;
      state.invalidated_time = invalidated_index >= 0 ? bars[invalidated_index].time : 0;
      state.consumed_time = consumed_index >= 0 ? bars[consumed_index].time : 0;

      state.node_type = node.type;
      state.node_price = node.price;
      state.expansion_extreme = extreme;
      state.territory_lower = lower;
      state.territory_upper = upper;

      state.invalidated = invalidated;
      state.consumed = consumed;
      state.active = !consumed;

      DAL_M0001AppendNodeAuditState(states, state);
      state_id++;
   }

   return ArraySize(states);
}


#endif
