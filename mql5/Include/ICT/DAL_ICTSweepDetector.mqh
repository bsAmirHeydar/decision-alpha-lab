#ifndef __DAL_ICT_SWEEP_DETECTOR_MQH__
#define __DAL_ICT_SWEEP_DETECTOR_MQH__

#include <ICT/DAL_ICTTypes.mqh>
#include <StructuralNodes/DAL_StructuralNodeEngine.mqh>

double DAL_ICT_ZoneHalfWidth(const double point, const double zone_half_width_points)
{
   double half = zone_half_width_points * point;
   if(half <= 0.0)
      half = point * 0.5;
   return half;
}

void DAL_ICT_NodeZone(
   const double node_price,
   const double point,
   const double zone_half_width_points,
   double &zone_low,
   double &zone_high
)
{
   double half = DAL_ICT_ZoneHalfWidth(point, zone_half_width_points);
   zone_low = node_price - half;
   zone_high = node_price + half;
}

double DAL_ICT_HighTouchLevel(const double zone_low, const double zone_high, const double touch_pct)
{
   double pct = DAL_ClampDouble(touch_pct, 0.0, 100.0) / 100.0;
   return zone_low + (zone_high - zone_low) * pct;
}

double DAL_ICT_LowTouchLevel(const double zone_low, const double zone_high, const double touch_pct)
{
   double pct = DAL_ClampDouble(touch_pct, 0.0, 100.0) / 100.0;
   return zone_high - (zone_high - zone_low) * pct;
}

bool DAL_ICT_BarSweepsNode(
   const DALBar &bar,
   const ENUM_DALNodeType node_type,
   const double node_price,
   const double zone_low,
   const double zone_high,
   const DAL_ICTSweepMode mode,
   const double touch_pct,
   const double eps,
   bool &is_hunt,
   double &trigger_level
)
{
   is_hunt = false;
   trigger_level = node_price;

   if(node_type == DAL_NODE_HIGH)
   {
      double touch_level = DAL_ICT_HighTouchLevel(zone_low, zone_high, touch_pct);
      trigger_level = (mode == ICT_SWEEP_HUNT ? zone_high : touch_level);

      bool touched = (bar.high + eps >= touch_level);
      bool hunted = (bar.high + eps >= zone_high && bar.close < node_price - eps);
      is_hunt = hunted;
      return (mode == ICT_SWEEP_HUNT ? hunted : touched);
   }

   double low_touch_level = DAL_ICT_LowTouchLevel(zone_low, zone_high, touch_pct);
   trigger_level = (mode == ICT_SWEEP_HUNT ? zone_low : low_touch_level);

   bool low_touched = (bar.low - eps <= low_touch_level);
   bool low_hunted = (bar.low - eps <= zone_low && bar.close > node_price + eps);
   is_hunt = low_hunted;
   return (mode == ICT_SWEEP_HUNT ? low_hunted : low_touched);
}

int DAL_ICT_DetectSweepEvents(
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DAL_ICTSweepMode mode,
   const double touch_pct,
   const double zone_half_width_points,
   const double point,
   const double eps_points,
   DAL_ICTSweepEvent &sweeps[]
)
{
   ArrayResize(sweeps, 0);
   if(bars_count <= 0 || nodes_count <= 0)
      return 0;

   bool node_used[];
   ArrayResize(node_used, nodes_count);
   for(int u=0; u<nodes_count; u++) node_used[u] = false;

   double eps = eps_points * point;
   int next_id = 0;

   for(int i=0; i<bars_count; i++)
   {
      for(int n=0; n<nodes_count; n++)
      {
         if(node_used[n])
            continue;
         if(nodes[n].active_from_index >= i)
            continue;
         if(nodes[n].index >= i)
            continue;

         double zl = 0.0, zh = 0.0;
         DAL_ICT_NodeZone(nodes[n].price, point, zone_half_width_points, zl, zh);

         bool is_hunt = false;
         double trigger_level = nodes[n].price;
         if(!DAL_ICT_BarSweepsNode(bars[i], nodes[n].type, nodes[n].price, zl, zh, mode, touch_pct, eps, is_hunt, trigger_level))
            continue;

         int size = ArraySize(sweeps);
         ArrayResize(sweeps, size + 1);
         sweeps[size].id = next_id++;
         sweeps[size].index = i;
         sweeps[size].time = bars[i].time;
         sweeps[size].setup_direction = (nodes[n].type == DAL_NODE_HIGH ? ICT_DIR_SELL : ICT_DIR_BUY);
         sweeps[size].node_type = nodes[n].type;
         sweeps[size].node_array_index = n;
         sweeps[size].node_id = nodes[n].id;
         sweeps[size].node_index = nodes[n].index;
         sweeps[size].node_time = nodes[n].time;
         sweeps[size].node_active_from_time = nodes[n].active_from_time;
         sweeps[size].node_price = nodes[n].price;
         sweeps[size].zone_low = zl;
         sweeps[size].zone_high = zh;
         sweeps[size].trigger_level = trigger_level;
         sweeps[size].bar_open = bars[i].open;
         sweeps[size].bar_high = bars[i].high;
         sweeps[size].bar_low = bars[i].low;
         sweeps[size].bar_close = bars[i].close;
         sweeps[size].sweep_extreme = (nodes[n].type == DAL_NODE_HIGH ? bars[i].high : bars[i].low);
         sweeps[size].is_hunt = is_hunt;

         node_used[n] = true;
      }
   }

   return ArraySize(sweeps);
}

int DAL_ICT_FindNextSweepIndex(const DAL_ICTSweepEvent &sweeps[], const int sweeps_count, const int after_bar_index)
{
   int next_index = -1;
   for(int i=0; i<sweeps_count; i++)
   {
      if(sweeps[i].index <= after_bar_index)
         continue;
      if(next_index < 0 || sweeps[i].index < next_index)
         next_index = sweeps[i].index;
   }
   return next_index;
}

datetime DAL_ICT_FindNextSweepTime(const DAL_ICTSweepEvent &sweeps[], const int sweeps_count, const int after_bar_index)
{
   int idx = DAL_ICT_FindNextSweepIndex(sweeps, sweeps_count, after_bar_index);
   if(idx < 0) return 0;
   for(int i=0; i<sweeps_count; i++)
      if(sweeps[i].index == idx)
         return sweeps[i].time;
   return 0;
}

#endif
