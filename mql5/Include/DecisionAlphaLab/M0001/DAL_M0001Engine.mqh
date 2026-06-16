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
   const bool hunted,
   const bool consumed,
   const ENUM_DALM0001ConsumeReason consume_reason,
   const int consumed_index,
   DALM0001Event &event
)
{
   int inside_len = exit_index - entry_index + 1;
   if(inside_len <= 0)
      return false;

   int before_start = entry_index - inside_len;
   if(before_start < 0)
      return false;

   event.id = event_id;
   event.node_id = node.id;
   event.revisit_id = revisit_id;
   event.node_index = node.index;
   event.active_from_index = node.active_from_index;
   event.entry_index = entry_index;
   event.exit_index = exit_index;
   event.consumed_index = consumed_index;

   event.node_time = node.time;
   event.active_from_time = node.active_from_time;
   event.entry_time = bars[entry_index].time;
   event.exit_time = bars[exit_index].time;
   event.consumed_time = consumed_index >= 0 ? bars[consumed_index].time : 0;

   event.node_type = node.type;
   event.node_price = node.price;
   event.expansion_extreme = extreme;
   event.territory_lower = lower;
   event.territory_upper = upper;

   event.mean_before = DAL_MeanRangeLog(log_moves, before_start, inside_len);
   event.mean_inside = DAL_MeanRangeLog(log_moves, entry_index, inside_len);
   event.rtv = DAL_SafeDiv(event.mean_inside, event.mean_before, 0.0);
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

      int i = start;
      while(i < bars_count && !consumed)
      {
         double extreme = DAL_M0001InitialExtreme(node.type, bars[start]);
         double lower = node.price;
         double upper = node.price;

         bool in_event = false;
         int entry_index = -1;
         int outside_count = 0;
         bool hunted = false;
         bool event_consumed = false;
         int event_consumed_index = -1;
         ENUM_DALM0001ConsumeReason consume_reason = DAL_M0001_CONSUMED_NONE;
         double consume_extreme = extreme;
         double consume_lower = lower;
         double consume_upper = upper;

         for(; i < bars_count; i++)
         {
            extreme = DAL_M0001UpdateExtreme(node.type, extreme, bars[i]);
            DAL_M0001Territory(node.type, node.price, extreme, config.zone_ratio, lower, upper);

            bool intersects = DAL_CandleIntersectsZone(bars[i].low, bars[i].high, lower, upper);

            if(!in_event)
            {
               if(intersects)
               {
                  in_event = true;
                  entry_index = i;
                  outside_count = 0;
                  hunted = DAL_M0001Hunted(node.type, node.price, bars[i]);

                  if(hunted)
                  {
                     event_consumed = true;
                     event_consumed_index = i;
                     consume_reason = DAL_M0001_CONSUMED_HUNT;
                     consume_extreme = extreme;
                     consume_lower = lower;
                     consume_upper = upper;
                  }
                  else if(DAL_M0001ConsumesOnTouch(config))
                  {
                     event_consumed = true;
                     event_consumed_index = i;
                     consume_reason = DAL_M0001_CONSUMED_TOUCH;
                     consume_extreme = extreme;
                     consume_lower = lower;
                     consume_upper = upper;
                  }
               }
               continue;
            }

            if(DAL_M0001Hunted(node.type, node.price, bars[i]))
            {
               hunted = true;

               if(!event_consumed)
               {
                  event_consumed = true;
                  event_consumed_index = i;
                  consume_reason = DAL_M0001_CONSUMED_HUNT;
                  consume_extreme = extreme;
                  consume_lower = lower;
                  consume_upper = upper;
               }
            }

            if(intersects)
               outside_count = 0;
            else
               outside_count++;

            if(outside_count >= config.exit_gap)
            {
               int exit_index = i;
               DALM0001Event event;
               double final_extreme = event_consumed ? consume_extreme : extreme;
               double final_lower = event_consumed ? consume_lower : lower;
               double final_upper = event_consumed ? consume_upper : upper;

               if(DAL_M0001FinalizeEvent(
                     bars,
                     log_moves,
                     node,
                     event_id,
                     revisit_id,
                     entry_index,
                     exit_index,
                     final_lower,
                     final_upper,
                     final_extreme,
                     hunted,
                     event_consumed,
                     consume_reason,
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
                  consumed = true;

               i = exit_index + 1;
               break;
            }
         }

         // No further closed event for this node in the available live stream.
         if(i >= bars_count)
            break;

         if(config.max_events > 0 && ArraySize(events) >= config.max_events)
            return ArraySize(events);
      }
   }

   return ArraySize(events);
}

#endif
