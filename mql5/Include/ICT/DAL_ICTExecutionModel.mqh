#ifndef __DAL_ICT_EXECUTION_MODEL_MQH__
#define __DAL_ICT_EXECUTION_MODEL_MQH__

#include <ICT/DAL_ICTTypes.mqh>
#include <ICT/DAL_ICTSweepDetector.mqh>
#include <ICT/DAL_ICTFVGDetector.mqh>
#include <ICT/DAL_ICTCISDDetector.mqh>

int DAL_ICT_FindTargetNode(
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DAL_ICTDirection direction,
   const double entry_price,
   const int entry_index,
   int &target_node_array_index
)
{
   target_node_array_index = -1;
   double best_distance = 0.0;

   for(int i=0; i<nodes_count; i++)
   {
      if(nodes[i].active_from_index > entry_index)
         continue;

      if(direction == ICT_DIR_SELL)
      {
         if(nodes[i].type != DAL_NODE_LOW)
            continue;
         if(nodes[i].price >= entry_price)
            continue;
         double d = entry_price - nodes[i].price;
         if(target_node_array_index < 0 || d < best_distance)
         {
            target_node_array_index = i;
            best_distance = d;
         }
      }
      else if(direction == ICT_DIR_BUY)
      {
         if(nodes[i].type != DAL_NODE_HIGH)
            continue;
         if(nodes[i].price <= entry_price)
            continue;
         double d2 = nodes[i].price - entry_price;
         if(target_node_array_index < 0 || d2 < best_distance)
         {
            target_node_array_index = i;
            best_distance = d2;
         }
      }
   }

   return target_node_array_index;
}

double DAL_ICT_TargetPriceFromNode(
   const DALLRuleNode &node,
   const DAL_ICTDirection direction,
   const DAL_ICTTargetMode target_mode,
   const double point,
   const double zone_half_width_points,
   const double target_touch_pct
)
{
   double zl = 0.0, zh = 0.0;
   DAL_ICT_NodeZone(node.price, point, zone_half_width_points, zl, zh);

   if(direction == ICT_DIR_SELL)
   {
      if(target_mode == ICT_TARGET_HUNT)
         return zl;
      return DAL_ICT_LowTouchLevel(zl, zh, target_touch_pct);
   }

   if(direction == ICT_DIR_BUY)
   {
      if(target_mode == ICT_TARGET_HUNT)
         return zh;
      return DAL_ICT_HighTouchLevel(zl, zh, target_touch_pct);
   }

   return node.price;
}

bool DAL_ICT_ResolveExit(
   const DALBar &bars[],
   const int bars_count,
   const DAL_ICTDirection direction,
   const int entry_index,
   const double sl_price,
   const double target_price,
   const int next_sweep_index,
   const bool exit_on_next_sweep,
   datetime &exit_time,
   DAL_ICTExitReason &exit_reason,
   double &exit_price,
   int &bars_to_exit
)
{
   exit_time = 0;
   exit_reason = ICT_EXIT_NONE;
   exit_price = 0.0;
   bars_to_exit = 0;

   int horizon = bars_count;
   if(exit_on_next_sweep && next_sweep_index > entry_index && next_sweep_index < horizon)
      horizon = next_sweep_index + 1;

   for(int i=entry_index + 1; i<horizon; i++)
   {
      if(direction == ICT_DIR_SELL)
      {
         bool hit_sl = (bars[i].high >= sl_price);
         bool hit_tp = (bars[i].low <= target_price);

         // Conservative same-bar ordering: SL first.
         if(hit_sl)
         {
            exit_time = bars[i].time;
            exit_reason = ICT_EXIT_SL;
            exit_price = sl_price;
            bars_to_exit = i - entry_index;
            return true;
         }
         if(hit_tp)
         {
            exit_time = bars[i].time;
            exit_reason = ICT_EXIT_TP;
            exit_price = target_price;
            bars_to_exit = i - entry_index;
            return true;
         }
      }
      else if(direction == ICT_DIR_BUY)
      {
         bool hit_sl2 = (bars[i].low <= sl_price);
         bool hit_tp2 = (bars[i].high >= target_price);

         if(hit_sl2)
         {
            exit_time = bars[i].time;
            exit_reason = ICT_EXIT_SL;
            exit_price = sl_price;
            bars_to_exit = i - entry_index;
            return true;
         }
         if(hit_tp2)
         {
            exit_time = bars[i].time;
            exit_reason = ICT_EXIT_TP;
            exit_price = target_price;
            bars_to_exit = i - entry_index;
            return true;
         }
      }
   }

   if(exit_on_next_sweep && next_sweep_index > entry_index && next_sweep_index < bars_count)
   {
      exit_time = bars[next_sweep_index].time;
      exit_reason = ICT_EXIT_NEXT_SWEEP;
      exit_price = bars[next_sweep_index].close;
      bars_to_exit = next_sweep_index - entry_index;
      return true;
   }

   if(bars_count > entry_index + 1)
   {
      int last = bars_count - 1;
      exit_time = bars[last].time;
      exit_reason = ICT_EXIT_CSV_END;
      exit_price = bars[last].close;
      bars_to_exit = last - entry_index;
      return true;
   }

   return false;
}

int DAL_ICT_BuildSweepIFVGCISDSignals(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const DALBar &bars[],
   const int bars_count,
   const int L,
   const DALLRuleNode &nodes[],
   const int nodes_count,
   const DAL_ICTSweepEvent &sweeps[],
   const int sweeps_count,
   const DAL_ICTFVG &fvgs[],
   const int fvgs_count,
   const double point,
   const int pre_sweep_fvg_lookback_bars,
   const int max_setup_bars_after_sweep,
   const int max_leg_lookback_bars,
   const double fvg_touch_pct,
   const double zone_half_width_points,
   const double target_touch_pct,
   const DAL_ICTTargetMode target_mode,
   const double min_rr,
   const double sl_buffer_points,
   const double eps_points,
   const bool exit_on_next_sweep,
   DAL_ICTEntrySignal &signals[]
)
{
   ArrayResize(signals, 0);

   if(bars_count <= 0 || sweeps_count <= 0 || nodes_count <= 0)
      return 0;

   int next_signal_id = 0;

   for(int s=0; s<sweeps_count; s++)
   {
      DAL_ICTSweepEvent sweep = sweeps[s];
      int next_sweep_index = DAL_ICT_FindNextSweepIndex(sweeps, sweeps_count, sweep.index);
      int stop_exclusive = bars_count;
      if(next_sweep_index > sweep.index)
         stop_exclusive = next_sweep_index;
      if(max_setup_bars_after_sweep > 0)
         stop_exclusive = MathMin(stop_exclusive, sweep.index + max_setup_bars_after_sweep + 1);

      int path_from = MathMax(0, sweep.index - MathMax(pre_sweep_fvg_lookback_bars, 1));
      int fvg_arr_index = DAL_ICT_FindPathFVG(fvgs, fvgs_count, sweep.setup_direction, path_from, sweep.index, true);
      if(fvg_arr_index < 0)
         continue;

      DAL_ICTIFVGEvent ifvg;
      int ifvg_index = DAL_ICT_FindIFVGConfirmation(
         bars,
         bars_count,
         fvgs[fvg_arr_index],
         sweep.setup_direction,
         sweep.index + 1,
         stop_exclusive,
         fvg_touch_pct,
         point,
         eps_points,
         ifvg
      );
      if(ifvg_index < 0)
         continue;

      int leg_start_index = DAL_ICT_FindLastLegStartIndex(bars, bars_count, sweep.index, sweep.setup_direction, max_leg_lookback_bars);
      if(leg_start_index < 0)
         continue;

      DAL_ICTCISDEvent cisd;
      int cisd_index = DAL_ICT_FindCISDConfirmation(
         bars,
         bars_count,
         sweep.setup_direction,
         leg_start_index,
         ifvg_index + 1,
         stop_exclusive,
         point,
         eps_points,
         cisd
      );
      if(cisd_index < 0)
         continue;

      double entry_price = bars[cisd_index].close;
      double sl_buffer = sl_buffer_points * point;
      double sl_price = 0.0;
      if(sweep.setup_direction == ICT_DIR_SELL)
         sl_price = sweep.sweep_extreme + sl_buffer;
      else if(sweep.setup_direction == ICT_DIR_BUY)
         sl_price = sweep.sweep_extreme - sl_buffer;
      else
         continue;

      double risk_points = MathAbs(entry_price - sl_price) / point;
      if(risk_points <= 0.0)
         continue;

      int target_node_arr = -1;
      if(DAL_ICT_FindTargetNode(nodes, nodes_count, sweep.setup_direction, entry_price, cisd_index, target_node_arr) < 0)
         continue;

      double target_price = DAL_ICT_TargetPriceFromNode(nodes[target_node_arr], sweep.setup_direction, target_mode, point, zone_half_width_points, target_touch_pct);
      double reward_points = 0.0;
      if(sweep.setup_direction == ICT_DIR_SELL)
         reward_points = (entry_price - target_price) / point;
      else
         reward_points = (target_price - entry_price) / point;

      if(reward_points <= 0.0)
         continue;

      double rr = reward_points / risk_points;
      if(rr < min_rr)
         continue;

      datetime exit_time = 0;
      DAL_ICTExitReason exit_reason = ICT_EXIT_NONE;
      double exit_price = 0.0;
      int bars_to_exit = 0;
      DAL_ICT_ResolveExit(bars, bars_count, sweep.setup_direction, cisd_index, sl_price, target_price, next_sweep_index, exit_on_next_sweep, exit_time, exit_reason, exit_price, bars_to_exit);

      double pnl_r = 0.0;
      if(exit_reason != ICT_EXIT_NONE)
      {
         if(sweep.setup_direction == ICT_DIR_SELL)
            pnl_r = (entry_price - exit_price) / MathAbs(entry_price - sl_price);
         else
            pnl_r = (exit_price - entry_price) / MathAbs(entry_price - sl_price);
      }

      int size = ArraySize(signals);
      ArrayResize(signals, size + 1);
      signals[size].id = next_signal_id++;
      signals[size].symbol = symbol;
      signals[size].timeframe = timeframe;
      signals[size].L = L;
      signals[size].direction = sweep.setup_direction;
      signals[size].sweep_id = sweep.id;
      signals[size].sweep_time = sweep.time;
      signals[size].valid_from_time = sweep.time;
      signals[size].valid_until_time = (next_sweep_index > sweep.index && next_sweep_index < bars_count ? bars[next_sweep_index].time : bars[bars_count-1].time);
      signals[size].valid_until_exclusive_time = signals[size].valid_until_time;
      signals[size].next_sweep_index = next_sweep_index;
      signals[size].next_sweep_time = (next_sweep_index > sweep.index && next_sweep_index < bars_count ? bars[next_sweep_index].time : 0);
      signals[size].fvg_id = fvgs[fvg_arr_index].id;
      signals[size].fvg_time = fvgs[fvg_arr_index].time;
      signals[size].fvg_low = fvgs[fvg_arr_index].zone_low;
      signals[size].fvg_high = fvgs[fvg_arr_index].zone_high;
      signals[size].ifvg_index = ifvg_index;
      signals[size].ifvg_time = ifvg.time;
      signals[size].cisd_index = cisd_index;
      signals[size].cisd_time = cisd.time;
      signals[size].leg_start_index = cisd.leg_start_index;
      signals[size].leg_start_time = cisd.leg_start_time;
      signals[size].leg_start_open = cisd.leg_start_open;
      signals[size].entry_time = bars[cisd_index].time;
      signals[size].entry_price = entry_price;
      signals[size].sl_price = sl_price;
      signals[size].target_price = target_price;
      signals[size].target_node_id = nodes[target_node_arr].id;
      signals[size].target_node_time = nodes[target_node_arr].time;
      signals[size].target_node_price = nodes[target_node_arr].price;
      signals[size].risk_points = risk_points;
      signals[size].reward_points = reward_points;
      signals[size].rr = rr;
      signals[size].exit_time = exit_time;
      signals[size].exit_reason = exit_reason;
      signals[size].exit_price = exit_price;
      signals[size].pnl_r = pnl_r;
      signals[size].bars_to_exit = bars_to_exit;
   }

   return ArraySize(signals);
}

#endif
