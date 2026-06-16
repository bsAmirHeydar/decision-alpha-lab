#ifndef __DAL_M0001_ENGINE_MQH__
#define __DAL_M0001_ENGINE_MQH__

#include <DecisionAlphaLab/Common/DAL_Math.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/LRule/DAL_LRuleTypes.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Types.mqh>

void DAL_M0001BuildLogMoves(const DALBar &bars[], const int count, double &log_moves[])
{
   ArrayResize(log_moves, count);
   for(int i = 0; i < count; i++)
      log_moves[i] = DAL_LogRange(bars[i].high, bars[i].low);
}

void DAL_M0001Territory(
   const ENUM_DALNodeType type,
   const double node_price,
   const double extreme,
   const double zone_ratio,
   double &lower,
   double &upper
)
{
   double distance = MathAbs(extreme - node_price);
   double half_width = distance * (1.0 - zone_ratio);
   lower = node_price - half_width;
   upper = node_price + half_width;
}

bool DAL_M0001Hunted(const ENUM_DALNodeType type, const double node_price, const DALBar &bar)
{
   if(type == DAL_NODE_LOW)
      return bar.low < node_price;
   return bar.high > node_price;
}

double DAL_M0001InitialExtreme(const ENUM_DALNodeType type, const DALBar &bar)
{
   if(type == DAL_NODE_LOW)
      return bar.high;
   return bar.low;
}

double DAL_M0001UpdateExtreme(const ENUM_DALNodeType type, const double extreme, const DALBar &bar)
{
   if(type == DAL_NODE_LOW)
      return MathMax(extreme, bar.high);
   return MathMin(extreme, bar.low);
}

int DAL_M0001AppendEvent(DALM0001Event &events[], const DALM0001Event &event)
{
   int size = ArraySize(events);
   ArrayResize(events, size + 1);
   events[size] = event;
   return size;
}

bool DAL_M0001FinalizeEvent(
   const DALBar &bars[],
   const double &log_moves[],
   const DALLRuleNode &node,
   const int event_id,
   const int revisit_id,
   const int entry_index,
   const int exit_index,
   const double lower,
   const double upper,
   const double extreme,
   const bool touch_confirmed,
   const int touch_confirmed_index,
   const bool hunted,
   const bool consumed,
   const ENUM_DALM0001ConsumeReason consume_reason,
   const int consumed_index,
   DALM0001Event &event
)
{
   int event_length = exit_index - entry_index + 1;
   if(event_length <= 0)
      return false;

   // For visual/revisit audit we keep the event even when a full same-length
   // baseline is not available. RTV becomes zero until the baseline exists.
   int before_start = entry_index - event_length;
   int before_length = event_length;
   bool has_full_baseline = (before_start >= 0);

   event.id = event_id;
   event.node_id = node.id;
   event.revisit_id = revisit_id;
   event.node_index = node.index;
   event.active_from_index = node.active_from_index;
   event.entry_index = entry_index;
   event.exit_index = exit_index;
   event.consumed_index = consumed_index;
   event.touch_confirmed_index = touch_confirmed_index;
   event.event_length = event_length;

   event.node_time = node.time;
   event.active_from_time = node.active_from_time;
   event.entry_time = bars[entry_index].time;
   event.exit_time = bars[exit_index].time;
   event.consumed_time = consumed_index >= 0 ? bars[consumed_index].time : 0;
   event.touch_confirmed_time = touch_confirmed_index >= 0 ? bars[touch_confirmed_index].time : 0;

   event.node_type = node.type;
   event.node_price = node.price;
   event.expansion_extreme = extreme;
   event.territory_lower = lower;
   event.territory_upper = upper;

   event.mean_before = 0.0;
   event.mean_inside = DAL_MeanRangeLog(log_moves, entry_index, event_length);

   if(has_full_baseline)
      event.mean_before = DAL_MeanRangeLog(log_moves, before_start, before_length);

   event.rtv = DAL_SafeDiv(event.mean_inside, event.mean_before, 0.0);
   event.touch_confirmed = touch_confirmed;
   event.hunted = hunted;
   event.consumed = consumed;
   event.consume_reason = consume_reason;
   event.closed = true;

   return true;
}

int DAL_M0001ComputeEvents(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DALM0001Config &config,
   DALM0001Event &events[]
)
{
   ArrayResize(events, 0);

   if(bars_count <= 0 || nodes_count <= 0)
      return 0;

   double log_moves[];
   DAL_M0001BuildLogMoves(bars, bars_count, log_moves);

   int event_id = 0;

   for(int n = 0; n < nodes_count; n++)
   {
      DALLRuleNode node = nodes[n];
      int start = node.active_from_index;

      if(start < 0 || start >= bars_count)
         continue;

      int revisit_id = 0;
      bool consumed = false;

      // Tracking extreme is node-level and keeps updating while the node is alive.
      // Event geometry freezes separately at each revisit entry.
      double tracking_extreme = DAL_M0001InitialExtreme(node.type, bars[start]);

      int i = start;
      while(i < bars_count && !consumed)
      {
         bool in_event = false;
         int entry_index = -1;
         int outside_count = 0;

         double event_extreme = tracking_extreme;
         double event_lower = node.price;
         double event_upper = node.price;

         // 1) TRACKING: wait for the next zone touch or node hunt.
         for(; i < bars_count; i++)
         {
            tracking_extreme = DAL_M0001UpdateExtreme(node.type, tracking_extreme, bars[i]);

            double live_lower = node.price;
            double live_upper = node.price;
            DAL_M0001Territory(node.type, node.price, tracking_extreme, config.zone_ratio, live_lower, live_upper);

            bool touched_zone = DAL_CandleIntersectsZone(bars[i].low, bars[i].high, live_lower, live_upper);
            bool hunted_now = DAL_M0001Hunted(node.type, node.price, bars[i]);

            // HUNT always has priority over a still-unconfirmed touch candidate.
            if(hunted_now)
            {
               consumed = true;

               if(touched_zone)
               {
                  // A gap/break candle that also intersects the zone is kept as
                  // a one-candle hunted revisit for visual audit.
                  DALM0001Event event;
                  if(DAL_M0001FinalizeEvent(
                        bars,
                        log_moves,
                        node,
                        event_id,
                        revisit_id,
                        i,
                        i,
                        live_lower,
                        live_upper,
                        tracking_extreme,
                        false,
                        -1,
                        true,
                        true,
                        DAL_M0001_CONSUMED_HUNT,
                        i,
                        event
                     ))
                  {
                     if(event.rtv >= config.min_rtv)
                     {
                        DAL_M0001AppendEvent(events, event);
                        event_id++;
                     }
                  }
               }

               i++;
               break;
            }

            if(!touched_zone)
               continue;

            // A revisit starts. Its territory/extreme are frozen here.
            in_event = true;
            entry_index = i;
            outside_count = 0;
            event_extreme = tracking_extreme;
            event_lower = live_lower;
            event_upper = live_upper;
            i++;
            break;
         }

         if(consumed)
            break;

         if(!in_event)
            break;

         // 2) ACTIVE EVENT / PENDING TOUCH:
         // The frozen event zone is used for exit confirmation, while the
         // node-level tracking extreme keeps updating for future revisits.
         for(; i < bars_count; i++)
         {
            tracking_extreme = DAL_M0001UpdateExtreme(node.type, tracking_extreme, bars[i]);

            bool hunted_now = DAL_M0001Hunted(node.type, node.price, bars[i]);
            if(hunted_now)
            {
               DALM0001Event event;
               if(DAL_M0001FinalizeEvent(
                     bars,
                     log_moves,
                     node,
                     event_id,
                     revisit_id,
                     entry_index,
                     i,
                     event_lower,
                     event_upper,
                     event_extreme,
                     false,
                     -1,
                     true,
                     true,
                     DAL_M0001_CONSUMED_HUNT,
                     i,
                     event
                  ))
               {
                  if(event.rtv >= config.min_rtv)
                  {
                     DAL_M0001AppendEvent(events, event);
                     event_id++;
                  }
               }

               consumed = true;
               i++;
               break;
            }

            bool inside_frozen_zone = DAL_CandleIntersectsZone(
               bars[i].low,
               bars[i].high,
               event_lower,
               event_upper
            );

            if(inside_frozen_zone)
               outside_count = 0;
            else
               outside_count++;

            if(outside_count >= config.exit_gap)
            {
               // Touch is confirmed only here.
               bool event_consumed = false;
               int event_consumed_index = -1;
               ENUM_DALM0001ConsumeReason reason = DAL_M0001_CONSUMED_NONE;

               if(DAL_M0001ConsumesOnTouch(config))
               {
                  event_consumed = true;
                  event_consumed_index = i;
                  reason = DAL_M0001_CONSUMED_TOUCH;
               }

               DALM0001Event event;
               if(DAL_M0001FinalizeEvent(
                     bars,
                     log_moves,
                     node,
                     event_id,
                     revisit_id,
                     entry_index,
                     i,
                     event_lower,
                     event_upper,
                     event_extreme,
                     true,
                     i,
                     false,
                     event_consumed,
                     reason,
                     event_consumed_index,
                     event
                  ))
               {
                  if(event.rtv >= config.min_rtv)
                  {
                     DAL_M0001AppendEvent(events, event);
                     event_id++;
                  }
               }

               revisit_id++;

               if(event_consumed)
               {
                  consumed = true;
               }
               else
               {
                  // Revisited-live memory:
                  // after a confirmed revisit in HUNT mode, the node remains alive
                  // but its next territory cycle must start fresh after this visit.
                  // The next revisit extreme is computed from the first bar after
                  // the confirmed event, not from the original node candle.
                  int next_tracking_index = i + 1;
                  if(next_tracking_index < bars_count)
                     tracking_extreme = DAL_M0001InitialExtreme(node.type, bars[next_tracking_index]);
               }

               i++;
               break;
            }
         }

         if(config.max_events > 0 && ArraySize(events) >= config.max_events)
            return ArraySize(events);

         // No closed event yet in available bars.
         if(i >= bars_count)
            break;
      }
   }

   return ArraySize(events);
}


#endif
