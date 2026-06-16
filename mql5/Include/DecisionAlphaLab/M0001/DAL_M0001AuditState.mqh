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

   int first_touch_index;
   int touch_confirmed_index;
   int hunt_index;

   ENUM_DALM0001ConsumeReason consume_reason;

   datetime node_time;
   datetime active_from_time;
   datetime current_time;
   datetime extreme_time;
   datetime invalidated_time;
   datetime consumed_time;

   datetime first_touch_time;
   datetime touch_confirmed_time;
   datetime hunt_time;

   ENUM_DALNodeType node_type;
   double node_price;
   double expansion_extreme;
   double territory_lower;
   double territory_upper;

   bool invalidated;
   bool consumed;
   bool active;

   bool touch_started;
   bool touch_confirmed;
   bool hunted;
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

      // Node-level outcome memory.
      // These are stored regardless of the selected consumption model.
      bool touch_started = false;
      bool touch_confirmed = false;
      bool hunted = false;
      int first_touch_index = -1;
      int touch_confirmed_index = -1;
      int hunt_index = -1;

      bool pending_touch = false;
      int pending_touch_outside_count = 0;
      double pending_touch_extreme = extreme;
      int pending_touch_extreme_index = extreme_index;
      double pending_touch_lower = node.price;
      double pending_touch_upper = node.price;

      for(int i = start; i < bars_count; i++)
      {
         if(consumed)
            break;

         if(!pending_touch)
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

            if(hunted_node)
            {
               hunted = true;
               hunt_index = i;

               consumed = true;
               invalidated = true;
               consumed_index = i;
               invalidated_index = i;
               consume_reason = DAL_M0001_CONSUMED_HUNT;
               last_active_index = i;
               break;
            }

            if(touched_zone)
            {
               // A touch is first only a candidate / active event.
               // It is stored for the node in every consume mode.
               if(!touch_started)
               {
                  touch_started = true;
                  first_touch_index = i;
               }

               pending_touch = true;
               pending_touch_outside_count = 0;
               pending_touch_extreme = extreme;
               pending_touch_extreme_index = extreme_index;
               pending_touch_lower = live_lower;
               pending_touch_upper = live_upper;
               last_active_index = i;
               continue;
            }

            continue;
         }

         // Pending touch / active event.
         // The touch is still not confirmed. If the node breaks here, this
         // outcome is HUNT, even in touch consumption mode.
         last_active_index = i;

         bool hunted_node = DAL_M0001Hunted(node.type, node.price, bars[i]);
         if(hunted_node)
         {
            hunted = true;
            hunt_index = i;

            consumed = true;
            invalidated = true;
            consumed_index = i;
            invalidated_index = i;
            consume_reason = DAL_M0001_CONSUMED_HUNT;
            last_active_index = i;
            break;
         }

         bool inside_pending_zone = DAL_CandleIntersectsZone(
            bars[i].low,
            bars[i].high,
            pending_touch_lower,
            pending_touch_upper
         );

         if(inside_pending_zone)
            pending_touch_outside_count = 0;
         else
            pending_touch_outside_count++;

         if(pending_touch_outside_count >= config.exit_gap)
         {
            // Touch becomes confirmed only after exit confirmation.
            if(!touch_confirmed)
            {
               touch_confirmed = true;
               touch_confirmed_index = i;
            }

            if(DAL_M0001ConsumesOnTouch(config))
            {
               consumed = true;
               consumed_index = i;
               consume_reason = DAL_M0001_CONSUMED_TOUCH;
               last_active_index = i;

               // In touch consume mode the node ends at the confirmed touch
               // event, so final geometry is the frozen event geometry.
               extreme = pending_touch_extreme;
               extreme_index = pending_touch_extreme_index;
               break;
            }

            // In hunt consume mode, touch confirmation is recorded but it does
            // not consume the node. The node keeps being checked until HUNT.
            pending_touch = false;
            pending_touch_outside_count = 0;
            continue;
         }
      }

      double lower = node.price;
      double upper = node.price;

      if(consumed && consume_reason == DAL_M0001_CONSUMED_TOUCH)
      {
         lower = pending_touch_lower;
         upper = pending_touch_upper;
         extreme = pending_touch_extreme;
         extreme_index = pending_touch_extreme_index;
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

      state.first_touch_index = first_touch_index;
      state.touch_confirmed_index = touch_confirmed_index;
      state.hunt_index = hunt_index;

      state.consume_reason = consume_reason;

      state.node_time = node.time;
      state.active_from_time = node.active_from_time;
      state.current_time = bars[last_active_index].time;
      state.extreme_time = bars[extreme_index].time;
      state.invalidated_time = invalidated_index >= 0 ? bars[invalidated_index].time : 0;
      state.consumed_time = consumed_index >= 0 ? bars[consumed_index].time : 0;

      state.first_touch_time = first_touch_index >= 0 ? bars[first_touch_index].time : 0;
      state.touch_confirmed_time = touch_confirmed_index >= 0 ? bars[touch_confirmed_index].time : 0;
      state.hunt_time = hunt_index >= 0 ? bars[hunt_index].time : 0;

      state.node_type = node.type;
      state.node_price = node.price;
      state.expansion_extreme = extreme;
      state.territory_lower = lower;
      state.territory_upper = upper;

      state.invalidated = invalidated;
      state.consumed = consumed;
      state.active = !consumed;

      state.touch_started = touch_started;
      state.touch_confirmed = touch_confirmed;
      state.hunted = hunted;

      DAL_M0001AppendNodeAuditState(states, state);
      state_id++;
   }

   return ArraySize(states);
}


#endif
