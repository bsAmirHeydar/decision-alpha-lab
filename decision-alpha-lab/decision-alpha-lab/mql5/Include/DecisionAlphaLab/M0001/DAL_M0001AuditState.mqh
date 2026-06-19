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
   int tracking_cycle_start_index;
   int current_index;
   int extreme_index;
   int invalidated_index;
   int consumed_index;

   int first_touch_index;
   int touch_confirmed_index;
   int hunt_index;
   int last_touch_confirmed_index;
   int pending_touch_entry_index;
   int pending_touch_revisit_id;
   int pending_touch_outside_count;
   int confirmed_touch_count;
   int next_revisit_id;
   int bars_since_last_touch_confirmed;
   int bars_since_first_touch;

   ENUM_DALM0001ConsumeReason consume_reason;

   datetime node_time;
   datetime active_from_time;
   datetime tracking_cycle_start_time;
   datetime current_time;
   datetime extreme_time;
   datetime invalidated_time;
   datetime consumed_time;

   datetime first_touch_time;
   datetime touch_confirmed_time;
   datetime hunt_time;
   datetime last_touch_confirmed_time;
   datetime pending_touch_entry_time;

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
   bool pending_touch;
   bool revisited_live;
   bool fresh_live;
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

      double tracking_extreme = DAL_M0001InitialExtreme(node.type, bars[start]);
      int extreme_index = start;
      int tracking_cycle_start_index = start;

      bool consumed = false;
      bool invalidated = false;
      int consumed_index = -1;
      int invalidated_index = -1;
      int last_active_index = bars_count - 1;
      ENUM_DALM0001ConsumeReason consume_reason = DAL_M0001_CONSUMED_NONE;

      bool touch_started = false;
      bool touch_confirmed = false;
      bool hunted = false;
      bool pending_touch = false;

      int first_touch_index = -1;
      int touch_confirmed_index = -1;
      int last_touch_confirmed_index = -1;
      int hunt_index = -1;

      int pending_touch_entry_index = -1;
      int pending_touch_revisit_id = -1;
      int pending_touch_outside_count = 0;

      int confirmed_touch_count = 0;
      int next_revisit_id = 0;
      int bars_since_last_touch_confirmed = -1;
      int bars_since_first_touch = -1;

      double pending_touch_extreme = tracking_extreme;
      int pending_touch_extreme_index = extreme_index;
      double pending_touch_lower = node.price;
      double pending_touch_upper = node.price;

      for(int i = start; i < bars_count; i++)
      {
         if(consumed)
            break;

         last_active_index = i;

         // Node-level tracking extreme keeps updating while the node is alive.
         double old_extreme = tracking_extreme;
         tracking_extreme = DAL_M0001UpdateExtreme(node.type, tracking_extreme, bars[i]);
         if(tracking_extreme != old_extreme)
            extreme_index = i;

         if(!pending_touch)
         {
            double live_lower = node.price;
            double live_upper = node.price;
            DAL_M0001Territory(node.type, node.price, tracking_extreme, config.zone_ratio, live_lower, live_upper);

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
               break;
            }

            if(touched_zone)
            {
               if(!touch_started)
               {
                  touch_started = true;
                  first_touch_index = i;
               }

               pending_touch = true;
               pending_touch_entry_index = i;
               pending_touch_revisit_id = next_revisit_id;
               pending_touch_outside_count = 0;

               pending_touch_extreme = tracking_extreme;
               pending_touch_extreme_index = extreme_index;
               pending_touch_lower = live_lower;
               pending_touch_upper = live_upper;
            }

            continue;
         }

         // Active pending revisit. It can still convert to HUNT before
         // exit-gap confirmation.
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
            break;
         }

         // Exit confirmation is strict:
         // high/low must not intersect the frozen pending zone for exit_gap
         // consecutive candles. Any re-touch resets the outside counter.
         bool fully_outside_pending_zone = !DAL_CandleIntersectsZone(
            bars[i].low,
            bars[i].high,
            pending_touch_lower,
            pending_touch_upper
         );

         if(fully_outside_pending_zone)
            pending_touch_outside_count++;
         else
            pending_touch_outside_count = 0;

         if(pending_touch_outside_count >= config.exit_gap)
         {
            touch_confirmed = true;

            if(touch_confirmed_index < 0)
               touch_confirmed_index = i;

            last_touch_confirmed_index = i;
            confirmed_touch_count++;
            next_revisit_id++;

            if(DAL_M0001ConsumesOnTouch(config))
            {
               consumed = true;
               consumed_index = i;
               consume_reason = DAL_M0001_CONSUMED_TOUCH;

               // In TOUCH mode final visible geometry is the frozen first event.
               tracking_extreme = pending_touch_extreme;
               extreme_index = pending_touch_extreme_index;
               break;
            }

            // In HUNT mode, confirmed touches are stored and the node returns
            // to TRACKING for the next revisit.
            //
            // Critical revisit semantics:
            // the next revisit is a live node with memory, but its territory
            // cycle is fresh. Expansion extreme resets after the confirmed visit
            // and is no longer measured from the original node candle.
            int next_tracking_index = i + 1;
            if(next_tracking_index < bars_count)
            {
               tracking_cycle_start_index = next_tracking_index;
               tracking_extreme = DAL_M0001InitialExtreme(node.type, bars[next_tracking_index]);
               extreme_index = next_tracking_index;
            }

            pending_touch = false;
            pending_touch_entry_index = -1;
            pending_touch_revisit_id = -1;
            pending_touch_outside_count = 0;
         }
      }

      double lower = node.price;
      double upper = node.price;

      if(consumed && consume_reason == DAL_M0001_CONSUMED_TOUCH)
      {
         // TOUCH consumption finalizes the event geometry that was frozen at
         // entry. This is a historical final state, not a live zone.
         lower = pending_touch_lower;
         upper = pending_touch_upper;
         tracking_extreme = pending_touch_extreme;
         extreme_index = pending_touch_extreme_index;
      }
      else
      {
         // Live zone semantics:
         // while the node is alive, the visual zone must always be rebuilt from
         // the current cycle extreme. Pending-touch/event geometry is frozen for
         // exit confirmation only; it must not freeze the live territory box.
         DAL_M0001Territory(node.type, node.price, tracking_extreme, config.zone_ratio, lower, upper);
      }

      DALM0001NodeAuditState state;
      state.id = state_id;
      state.node_id = node.id;
      state.node_index = node.index;
      state.active_from_index = node.active_from_index;
      state.tracking_cycle_start_index = tracking_cycle_start_index;
      state.current_index = last_active_index;
      state.extreme_index = extreme_index;
      state.invalidated_index = invalidated_index;
      state.consumed_index = consumed_index;

      state.first_touch_index = first_touch_index;
      state.touch_confirmed_index = touch_confirmed_index;
      state.hunt_index = hunt_index;
      state.last_touch_confirmed_index = last_touch_confirmed_index;
      state.pending_touch_entry_index = pending_touch_entry_index;
      state.pending_touch_revisit_id = pending_touch_revisit_id;
      state.pending_touch_outside_count = pending_touch_outside_count;
      state.confirmed_touch_count = confirmed_touch_count;
      state.next_revisit_id = next_revisit_id;

      if(last_touch_confirmed_index >= 0)
         bars_since_last_touch_confirmed = last_active_index - last_touch_confirmed_index;

      if(first_touch_index >= 0)
         bars_since_first_touch = last_active_index - first_touch_index;

      state.bars_since_last_touch_confirmed = bars_since_last_touch_confirmed;
      state.bars_since_first_touch = bars_since_first_touch;

      state.consume_reason = consume_reason;

      state.node_time = node.time;
      state.active_from_time = node.active_from_time;
      state.tracking_cycle_start_time = bars[tracking_cycle_start_index].time;
      state.current_time = bars[last_active_index].time;
      state.extreme_time = bars[extreme_index].time;
      state.invalidated_time = invalidated_index >= 0 ? bars[invalidated_index].time : 0;
      state.consumed_time = consumed_index >= 0 ? bars[consumed_index].time : 0;

      state.first_touch_time = first_touch_index >= 0 ? bars[first_touch_index].time : 0;
      state.touch_confirmed_time = touch_confirmed_index >= 0 ? bars[touch_confirmed_index].time : 0;
      state.hunt_time = hunt_index >= 0 ? bars[hunt_index].time : 0;
      state.last_touch_confirmed_time = last_touch_confirmed_index >= 0 ? bars[last_touch_confirmed_index].time : 0;
      state.pending_touch_entry_time = pending_touch_entry_index >= 0 ? bars[pending_touch_entry_index].time : 0;

      state.node_type = node.type;
      state.node_price = node.price;
      state.expansion_extreme = tracking_extreme;
      state.territory_lower = lower;
      state.territory_upper = upper;

      state.invalidated = invalidated;
      state.consumed = consumed;
      state.active = !consumed;

      state.touch_started = touch_started;
      state.touch_confirmed = touch_confirmed;
      state.hunted = hunted;
      state.pending_touch = pending_touch;
      state.revisited_live = (!state.consumed && !state.pending_touch && state.confirmed_touch_count > 0);
      state.fresh_live = (!state.consumed && !state.pending_touch && state.confirmed_touch_count == 0);

      DAL_M0001AppendNodeAuditState(states, state);
      state_id++;
   }

   return ArraySize(states);
}


#endif
