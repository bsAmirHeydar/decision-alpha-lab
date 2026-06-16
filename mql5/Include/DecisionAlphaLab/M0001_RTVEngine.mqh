//+------------------------------------------------------------------+
//| Decision Alpha Lab — M0001 Live RTV Engine                       |
//| Computes nodes/events from only currently available chart bars.   |
//+------------------------------------------------------------------+

void DAL_AddEvent(DAL_Event &events[], DAL_Event &event)
{
   const int n = ArraySize(events);
   ArrayResize(events, n + 1);
   events[n] = event;
}

bool DAL_FinalizeEvent(
   MqlRates &rates[],
   DAL_Node &node,
   int revisit_id,
   int entry_index,
   int exit_index,
   double lower,
   double upper,
   double frozen_extreme,
   double &inside_logs[],
   double &before_snapshot[],
   bool hunted,
   int hunt_index,
   datetime hunt_time,
   double hunt_price,
   bool is_open,
   DAL_Event &event
)
{
   const int inside_n = ArraySize(inside_logs);
   if(inside_n <= 0)
      return false;

   if(ArraySize(before_snapshot) < inside_n)
      return false;

   double inside_copy[];
   DAL_CopyLogs(inside_logs, inside_copy);

   double before_tail[];
   ArrayResize(before_tail, inside_n);
   const int before_size = ArraySize(before_snapshot);
   for(int i = 0; i < inside_n; i++)
      before_tail[i] = before_snapshot[before_size - inside_n + i];

   const double mean_inside = DAL_MeanAll(inside_copy);
   const double mean_before = DAL_MeanAll(before_tail);
   if(mean_inside == EMPTY_VALUE || mean_before == EMPTY_VALUE || mean_before == 0.0)
      return false;

   event.node_id = node.id;
   event.node_index = node.index;
   event.node_type = node.type;
   event.node_price = node.price;
   event.revisit_id = revisit_id;

   event.entry_index = entry_index;
   event.exit_index = exit_index;
   event.entry_time = rates[entry_index].time;
   event.exit_time = rates[exit_index].time;

   event.event_length = inside_n;
   event.territory_lower = lower;
   event.territory_upper = upper;
   event.expansion_extreme = frozen_extreme;

   event.mean_inside = mean_inside;
   event.mean_before = mean_before;
   event.median_inside = DAL_MedianAll(inside_copy);
   event.median_before = DAL_MedianAll(before_tail);
   event.rtv = mean_inside / mean_before;

   event.hunted = hunted;
   event.hunt_index = hunt_index;
   event.hunt_time = hunt_time;
   event.hunt_price = hunt_price;
   event.is_open = is_open;

   return true;
}

int DAL_ComputeEventsForNode(
   MqlRates &rates[],
   int bars,
   DAL_Node &node,
   DAL_Config &cfg,
   bool include_open_event,
   DAL_Event &events[]
)
{
   if(node.active_from >= bars)
      return 0;

   int before_count = ArraySize(events);

   double extreme = node.price;
   double lower = node.price;
   double upper = node.price;
   bool has_territory = false;

   bool consumed = false;
   bool in_event = false;
   bool hunted = false;

   int revisit_id = 0;
   int outside_count = 0;
   int entry_index = -1;
   int hunt_index = -1;
   datetime hunt_time = 0;
   double hunt_price = 0.0;
   double frozen_extreme = node.price;

   double before_logs[];
   double inside_logs[];
   double before_snapshot[];

   for(int i = node.active_from; i < bars; i++)
   {
      if(consumed)
         break;

      double high = rates[i].high;
      double low = rates[i].low;
      const double move = DAL_LogMove(high, low);

      if(!in_event)
      {
         if(node.type == DAL_NODE_LOW && high > extreme)
            extreme = high;
         else if(node.type == DAL_NODE_HIGH && low < extreme)
            extreme = low;

         DAL_BuildTerritory(node.price, extreme, cfg.zone_ratio, lower, upper);
         has_territory = (MathAbs(extreme - node.price) > (_Point * 0.1));

         if(!has_territory)
         {
            DAL_PushLog(before_logs, move, cfg.max_before_logs);
            continue;
         }

         if(DAL_InZone(high, low, lower, upper))
         {
            in_event = true;
            revisit_id++;
            outside_count = 0;
            entry_index = i;
            hunted = false;
            hunt_index = -1;
            hunt_time = 0;
            hunt_price = 0.0;
            frozen_extreme = extreme;

            DAL_ClearLogs(inside_logs);
            DAL_CopyLogs(before_logs, before_snapshot);
            DAL_PushLog(inside_logs, move);

            if(DAL_HuntBreached(node.type, node.price, high, low))
            {
               hunted = true;
               hunt_index = i;
               hunt_time = rates[i].time;
               hunt_price = DAL_HuntPrice(node.type, node.price, high, low);
            }
         }
         else
         {
            DAL_PushLog(before_logs, move, cfg.max_before_logs);
         }

         continue;
      }

      bool inside = DAL_InZone(high, low, lower, upper);
      if(inside)
      {
         outside_count = 0;
         DAL_PushLog(inside_logs, move);
      }
      else
      {
         outside_count++;
      }

      if(!hunted && DAL_HuntBreached(node.type, node.price, high, low))
      {
         hunted = true;
         hunt_index = i;
         hunt_time = rates[i].time;
         hunt_price = DAL_HuntPrice(node.type, node.price, high, low);
      }

      if(outside_count >= cfg.exit_gap)
      {
         DAL_Event event;
         if(DAL_FinalizeEvent(
               rates,
               node,
               revisit_id,
               entry_index,
               i,
               lower,
               upper,
               frozen_extreme,
               inside_logs,
               before_snapshot,
               hunted,
               hunt_index,
               hunt_time,
               hunt_price,
               false,
               event
            ))
         {
            DAL_AddEvent(events, event);
         }

         if(cfg.consume_on_touch || hunted)
         {
            consumed = true;
            break;
         }

         in_event = false;
         outside_count = 0;
         entry_index = -1;
         hunted = false;
         hunt_index = -1;
         hunt_time = 0;
         hunt_price = 0.0;

         DAL_ClearLogs(inside_logs);
         DAL_ClearLogs(before_snapshot);
         DAL_ClearLogs(before_logs);
         DAL_PushLog(before_logs, move, cfg.max_before_logs);
         extreme = node.price;
      }
   }

   if(include_open_event && in_event && entry_index >= 0)
   {
      DAL_Event open_event;
      if(DAL_FinalizeEvent(
            rates,
            node,
            revisit_id,
            entry_index,
            bars - 1,
            lower,
            upper,
            frozen_extreme,
            inside_logs,
            before_snapshot,
            hunted,
            hunt_index,
            hunt_time,
            hunt_price,
            true,
            open_event
         ))
      {
         DAL_AddEvent(events, open_event);
      }
   }

   return ArraySize(events) - before_count;
}

int DAL_ComputeRTVEvents(
   MqlRates &rates[],
   int bars,
   DAL_Node &nodes[],
   DAL_Config &cfg,
   bool include_open_event,
   DAL_Event &events[]
)
{
   ArrayResize(events, 0);

   const int nodes_total = ArraySize(nodes);
   for(int i = 0; i < nodes_total; i++)
      DAL_ComputeEventsForNode(rates, bars, nodes[i], cfg, include_open_event, events);

   return ArraySize(events);
}
