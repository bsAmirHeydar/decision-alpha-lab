#ifndef __DAL_IMD_ENGINE_MQH__
#define __DAL_IMD_ENGINE_MQH__

#include <IntermarketDivergence/DAL_IMDTypes.mqh>
#include <IntermarketDivergence/DAL_IMDReferenceLevels.mqh>

bool DAL_IMD_LevelTriggered(
   const DALBar &bar,
   const DAL_IMDLevelSide side,
   const double level,
   const DAL_IMDTriggerMode mode,
   const double eps,
   double &break_points
)
{
   break_points = 0.0;

   if(side == IMD_LEVEL_HIGH)
   {
      break_points = bar.high - level;
      if(mode == IMD_TRIGGER_CLOSE_BREAK)
         return (bar.close > level + eps);
      if(mode == IMD_TRIGGER_HUNT_REJECT_CLOSE)
         return (bar.high > level + eps && bar.close < level - eps);
      return (bar.high >= level - eps);
   }

   break_points = level - bar.low;
   if(mode == IMD_TRIGGER_CLOSE_BREAK)
      return (bar.close < level - eps);
   if(mode == IMD_TRIGGER_HUNT_REJECT_CLOSE)
      return (bar.low < level - eps && bar.close > level + eps);
   return (bar.low <= level + eps);
}

bool DAL_IMD_DestinationTriggersInLag(
   const DALBar &dest_bars[],
   const int bars_count,
   const int start_index,
   const int lag_bars,
   const DAL_IMDLevelSide side,
   const DAL_IMDLevelSource dest_level_source,
   const int dest_rolling_lookback,
   const bool exclude_current_bar,
   const int session_start_hour,
   const int session_start_minute,
   const int session_end_hour,
   const int session_end_minute,
   const DALLRuleNode &dest_nodes[],
   const int dest_nodes_count,
   const DAL_IMDTriggerMode trigger_mode,
   const double eps,
   datetime &confirm_time,
   int &confirm_index
)
{
   confirm_time = 0;
   confirm_index = -1;

   int end_index = MathMin(bars_count - 1, start_index + MathMax(0, lag_bars));
   for(int i=start_index; i<=end_index; i++)
   {
      DAL_IMDReferenceLevel level;
      if(!DAL_IMD_ResolveReferenceLevel(dest_bars, bars_count, dest_nodes, dest_nodes_count, i, side, dest_level_source, dest_rolling_lookback, exclude_current_bar, session_start_hour, session_start_minute, session_end_hour, session_end_minute, level))
         continue;

      double bp=0.0;
      if(DAL_IMD_LevelTriggered(dest_bars[i], side, level.price, trigger_mode, eps, bp))
      {
         confirm_time = dest_bars[i].time;
         confirm_index = i;
         return true;
      }
   }
   return false;
}

bool DAL_IMD_BuildProbeState(
   const DALBar &origin_bars[],
   const DALBar &dest_bars[],
   const int bars_count,
   const int index,
   const DAL_IMDLevelSide side,
   const DAL_IMDLevelSource origin_level_source,
   const DAL_IMDLevelSource destination_level_source,
   const int origin_rolling_lookback,
   const int destination_rolling_lookback,
   const bool exclude_current_bar,
   const int session_start_hour,
   const int session_start_minute,
   const int session_end_hour,
   const int session_end_minute,
   const DALLRuleNode &origin_nodes[],
   const int origin_nodes_count,
   const DALLRuleNode &dest_nodes[],
   const int dest_nodes_count,
   const DAL_IMDTriggerMode trigger_mode,
   const int destination_lag_bars,
   const double eps,
   DAL_IMDProbeState &state
)
{
   state.origin_triggered = false;
   state.destination_triggered = false;
   state.destination_triggered_in_lag = false;
   state.destination_confirm_time = 0;
   state.destination_confirm_index = -1;
   state.origin_ref_price = 0.0;
   state.destination_ref_price = 0.0;
   state.origin_ref_index = -1;
   state.destination_ref_index = -1;
   state.origin_ref_time = 0;
   state.destination_ref_time = 0;
   state.origin_node_id = -1;
   state.destination_node_id = -1;
   state.origin_probe_high = origin_bars[index].high;
   state.origin_probe_low = origin_bars[index].low;
   state.origin_probe_close = origin_bars[index].close;
   state.destination_probe_high = dest_bars[index].high;
   state.destination_probe_low = dest_bars[index].low;
   state.destination_probe_close = dest_bars[index].close;
   state.origin_break_points = 0.0;
   state.destination_break_points = 0.0;

   DAL_IMDReferenceLevel o_level;
   DAL_IMDReferenceLevel d_level;
   if(!DAL_IMD_ResolveReferenceLevel(origin_bars, bars_count, origin_nodes, origin_nodes_count, index, side, origin_level_source, origin_rolling_lookback, exclude_current_bar, session_start_hour, session_start_minute, session_end_hour, session_end_minute, o_level))
      return false;

   if(!DAL_IMD_ResolveReferenceLevel(dest_bars, bars_count, dest_nodes, dest_nodes_count, index, side, destination_level_source, destination_rolling_lookback, exclude_current_bar, session_start_hour, session_start_minute, session_end_hour, session_end_minute, d_level))
      return false;

   state.origin_ref_price = o_level.price;
   state.destination_ref_price = d_level.price;
   state.origin_ref_index = o_level.source_index;
   state.destination_ref_index = d_level.source_index;
   state.origin_ref_time = o_level.source_time;
   state.destination_ref_time = d_level.source_time;
   state.origin_node_id = o_level.node_id;
   state.destination_node_id = d_level.node_id;

   double obp=0.0, dbp=0.0;
   state.origin_triggered = DAL_IMD_LevelTriggered(origin_bars[index], side, o_level.price, trigger_mode, eps, obp);
   state.destination_triggered = DAL_IMD_LevelTriggered(dest_bars[index], side, d_level.price, trigger_mode, eps, dbp);
   state.origin_break_points = obp;
   state.destination_break_points = dbp;

   if(destination_lag_bars > 0)
   {
      datetime ctime=0;
      int cidx=-1;
      state.destination_triggered_in_lag = DAL_IMD_DestinationTriggersInLag(dest_bars, bars_count, index, destination_lag_bars, side, destination_level_source, destination_rolling_lookback, exclude_current_bar, session_start_hour, session_start_minute, session_end_hour, session_end_minute, dest_nodes, dest_nodes_count, trigger_mode, eps, ctime, cidx);
      state.destination_confirm_time = ctime;
      state.destination_confirm_index = cidx;
   }
   else
   {
      state.destination_triggered_in_lag = state.destination_triggered;
      if(state.destination_triggered)
      {
         state.destination_confirm_time = dest_bars[index].time;
         state.destination_confirm_index = index;
      }
   }

   return true;
}

datetime DAL_IMD_FindLateDestinationConfirm(
   const DALBar &dest_bars[],
   const int bars_count,
   const int start_index,
   const int max_bars,
   const DAL_IMDLevelSide side,
   const DAL_IMDLevelSource dest_level_source,
   const int dest_rolling_lookback,
   const bool exclude_current_bar,
   const int session_start_hour,
   const int session_start_minute,
   const int session_end_hour,
   const int session_end_minute,
   const DALLRuleNode &dest_nodes[],
   const int dest_nodes_count,
   const DAL_IMDTriggerMode trigger_mode,
   const double eps,
   int &confirm_index
)
{
   confirm_index = -1;
   int end_index = MathMin(bars_count - 1, start_index + MathMax(0, max_bars));
   for(int i=start_index; i<=end_index; i++)
   {
      DAL_IMDReferenceLevel level;
      if(!DAL_IMD_ResolveReferenceLevel(dest_bars, bars_count, dest_nodes, dest_nodes_count, i, side, dest_level_source, dest_rolling_lookback, exclude_current_bar, session_start_hour, session_start_minute, session_end_hour, session_end_minute, level))
         continue;
      double bp=0.0;
      if(DAL_IMD_LevelTriggered(dest_bars[i], side, level.price, trigger_mode, eps, bp))
      {
         confirm_index = i;
         return dest_bars[i].time;
      }
   }
   return 0;
}

void DAL_IMD_AddEvaluatedStep(
   DAL_IMDEvaluatedStep &steps[],
   const int index,
   const datetime time,
   const string origin_symbol,
   const string destination_symbol,
   const string side,
   const DAL_IMDProbeState &state
)
{
   int n = ArraySize(steps);
   ArrayResize(steps, n + 1);
   steps[n].index = index;
   steps[n].time = time;
   steps[n].origin_symbol = origin_symbol;
   steps[n].destination_symbol = destination_symbol;
   steps[n].side = side;
   steps[n].origin_triggered = state.origin_triggered;
   steps[n].destination_triggered = state.destination_triggered;
   steps[n].destination_triggered_in_lag = state.destination_triggered_in_lag;
   steps[n].origin_ref = state.origin_ref_price;
   steps[n].destination_ref = state.destination_ref_price;
   steps[n].origin_high = state.origin_probe_high;
   steps[n].origin_low = state.origin_probe_low;
   steps[n].destination_high = state.destination_probe_high;
   steps[n].destination_low = state.destination_probe_low;
}

void DAL_IMD_AddDivergenceEvent(
   DAL_IMDDivergenceEvent &events[],
   const string pair_label,
   const string origin_symbol,
   const string destination_symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int step_every_bars,
   const int step_offset_bars,
   const int index,
   const datetime evaluation_time,
   const DAL_IMDDivergenceSide div_side,
   const DAL_IMDLevelSource origin_level_source,
   const DAL_IMDLevelSource destination_level_source,
   const DAL_IMDTriggerMode trigger_mode,
   const int destination_lag_bars,
   const int signal_valid_bars,
   const int period_seconds,
   const DALBar &origin_bar,
   const DALBar &destination_bar,
   const DAL_IMDProbeState &state,
   const datetime late_confirm_time,
   const int late_confirm_index
)
{
   int n = ArraySize(events);
   ArrayResize(events, n + 1);
   events[n].id = n;
   events[n].pair_label = pair_label;
   events[n].origin_symbol = origin_symbol;
   events[n].destination_symbol = destination_symbol;
   events[n].timeframe = timeframe;
   events[n].step_every_bars = step_every_bars;
   events[n].step_offset_bars = step_offset_bars;
   events[n].index = index;
   events[n].evaluation_time = evaluation_time;
   int vf_index = index + MathMax(0, destination_lag_bars);
   events[n].valid_from_time = evaluation_time + (datetime)(MathMax(0, destination_lag_bars) * period_seconds);
   events[n].divergence_side = div_side;
   events[n].suggested_bias = (div_side == IMD_DIV_HIGH ? IMD_BIAS_SELL : IMD_BIAS_BUY);
   events[n].origin_level_source = origin_level_source;
   events[n].destination_level_source = destination_level_source;
   events[n].trigger_mode = trigger_mode;
   events[n].destination_lag_bars = destination_lag_bars;
   events[n].signal_valid_bars = signal_valid_bars;
   events[n].origin_ref_price = state.origin_ref_price;
   events[n].destination_ref_price = state.destination_ref_price;
   events[n].origin_ref_time = state.origin_ref_time;
   events[n].destination_ref_time = state.destination_ref_time;
   events[n].origin_ref_index = state.origin_ref_index;
   events[n].destination_ref_index = state.destination_ref_index;
   events[n].origin_node_id = state.origin_node_id;
   events[n].destination_node_id = state.destination_node_id;
   events[n].origin_open = origin_bar.open;
   events[n].origin_high = origin_bar.high;
   events[n].origin_low = origin_bar.low;
   events[n].origin_close = origin_bar.close;
   events[n].destination_open = destination_bar.open;
   events[n].destination_high = destination_bar.high;
   events[n].destination_low = destination_bar.low;
   events[n].destination_close = destination_bar.close;
   events[n].origin_break_points = state.origin_break_points;
   events[n].destination_break_points = state.destination_break_points;
   events[n].divergence_gap_points = state.origin_break_points - MathMax(0.0, state.destination_break_points);
   double denom = MathMax(1e-9, MathAbs(state.origin_break_points));
   events[n].normalized_gap_ratio = events[n].divergence_gap_points / denom;
   events[n].destination_confirm_time = late_confirm_time;

   datetime fixed_until = events[n].valid_from_time + (datetime)(MathMax(1, signal_valid_bars) * period_seconds);
   if(late_confirm_time > 0 && late_confirm_time < fixed_until)
   {
      events[n].valid_until_time = late_confirm_time;
      events[n].valid_until_exclusive_time = late_confirm_time + period_seconds;
      events[n].window_end_reason = IMD_WINDOW_DEST_LATE_CONFIRM;
   }
   else
   {
      events[n].valid_until_time = fixed_until;
      events[n].valid_until_exclusive_time = fixed_until + period_seconds;
      events[n].window_end_reason = IMD_WINDOW_FIXED_END;
   }

   events[n].note = "origin_triggered_destination_failed";
}

void DAL_IMD_ApplyNextDivergenceWindowEnd(DAL_IMDDivergenceEvent &events[], const int events_count, const int period_seconds)
{
   for(int i=0; i<events_count; i++)
   {
      datetime next_time = 0;
      for(int j=0; j<events_count; j++)
      {
         if(i == j) continue;
         if(events[j].origin_symbol != events[i].origin_symbol) continue;
         if(events[j].destination_symbol != events[i].destination_symbol) continue;
         if(events[j].divergence_side != events[i].divergence_side) continue;
         if(events[j].valid_from_time <= events[i].valid_from_time) continue;
         if(next_time == 0 || events[j].valid_from_time < next_time)
            next_time = events[j].valid_from_time;
      }
      if(next_time > 0 && next_time < events[i].valid_until_time)
      {
         events[i].valid_until_time = next_time;
         events[i].valid_until_exclusive_time = next_time + period_seconds;
         events[i].window_end_reason = IMD_WINDOW_NEXT_DIVERGENCE;
      }
   }
}

int DAL_IMD_BuildDivergenceEventsOneDirection(
   const string pair_label,
   const string origin_symbol,
   const string destination_symbol,
   const ENUM_TIMEFRAMES timeframe,
   const DALBar &origin_bars[],
   const DALBar &dest_bars[],
   const int bars_count,
   const DALLRuleNode &origin_nodes[],
   const int origin_nodes_count,
   const DALLRuleNode &dest_nodes[],
   const int dest_nodes_count,
   const int start_index,
   const int step_every_bars,
   const int step_offset_bars,
   const DAL_IMDLevelSource origin_level_source,
   const DAL_IMDLevelSource destination_level_source,
   const int origin_rolling_lookback,
   const int destination_rolling_lookback,
   const bool exclude_current_bar_from_reference,
   const int session_start_hour,
   const int session_start_minute,
   const int session_end_hour,
   const int session_end_minute,
   const DAL_IMDTriggerMode trigger_mode,
   const int destination_lag_bars,
   const int signal_valid_bars,
   const double eps_points,
   const double point,
   const bool check_highs,
   const bool check_lows,
   const bool write_all_steps,
   DAL_IMDDivergenceEvent &events[],
   DAL_IMDEvaluatedStep &steps[]
)
{
   int period_seconds = DAL_PeriodSecondsSafe(timeframe);
   double eps = eps_points * point;
   int every = MathMax(1, step_every_bars);
   int offset = MathMax(0, step_offset_bars);
   int min_i = MathMax(1, start_index);
   int max_i = bars_count - 1 - MathMax(0, destination_lag_bars);
   if(max_i <= min_i)
      return 0;

   int before = ArraySize(events);

   for(int i=min_i; i<=max_i; i++)
   {
      if(((i - offset) % every) != 0)
         continue;

      if(check_highs)
      {
         DAL_IMDProbeState state_h;
         if(DAL_IMD_BuildProbeState(origin_bars, dest_bars, bars_count, i, IMD_LEVEL_HIGH, origin_level_source, destination_level_source, origin_rolling_lookback, destination_rolling_lookback, exclude_current_bar_from_reference, session_start_hour, session_start_minute, session_end_hour, session_end_minute, origin_nodes, origin_nodes_count, dest_nodes, dest_nodes_count, trigger_mode, destination_lag_bars, eps, state_h))
         {
            if(write_all_steps)
               DAL_IMD_AddEvaluatedStep(steps, i, origin_bars[i].time, origin_symbol, destination_symbol, "HIGH", state_h);

            if(state_h.origin_triggered && !state_h.destination_triggered_in_lag)
            {
               int late_idx=-1;
               datetime late_confirm = DAL_IMD_FindLateDestinationConfirm(dest_bars, bars_count, i + MathMax(1, destination_lag_bars + 1), MathMax(1, signal_valid_bars), IMD_LEVEL_HIGH, destination_level_source, destination_rolling_lookback, exclude_current_bar_from_reference, session_start_hour, session_start_minute, session_end_hour, session_end_minute, dest_nodes, dest_nodes_count, trigger_mode, eps, late_idx);
               DAL_IMD_AddDivergenceEvent(events, pair_label, origin_symbol, destination_symbol, timeframe, every, offset, i, origin_bars[i].time, IMD_DIV_HIGH, origin_level_source, destination_level_source, trigger_mode, destination_lag_bars, signal_valid_bars, period_seconds, origin_bars[i], dest_bars[i], state_h, late_confirm, late_idx);
            }
         }
      }

      if(check_lows)
      {
         DAL_IMDProbeState state_l;
         if(DAL_IMD_BuildProbeState(origin_bars, dest_bars, bars_count, i, IMD_LEVEL_LOW, origin_level_source, destination_level_source, origin_rolling_lookback, destination_rolling_lookback, exclude_current_bar_from_reference, session_start_hour, session_start_minute, session_end_hour, session_end_minute, origin_nodes, origin_nodes_count, dest_nodes, dest_nodes_count, trigger_mode, destination_lag_bars, eps, state_l))
         {
            if(write_all_steps)
               DAL_IMD_AddEvaluatedStep(steps, i, origin_bars[i].time, origin_symbol, destination_symbol, "LOW", state_l);

            if(state_l.origin_triggered && !state_l.destination_triggered_in_lag)
            {
               int late_idx=-1;
               datetime late_confirm = DAL_IMD_FindLateDestinationConfirm(dest_bars, bars_count, i + MathMax(1, destination_lag_bars + 1), MathMax(1, signal_valid_bars), IMD_LEVEL_LOW, destination_level_source, destination_rolling_lookback, exclude_current_bar_from_reference, session_start_hour, session_start_minute, session_end_hour, session_end_minute, dest_nodes, dest_nodes_count, trigger_mode, eps, late_idx);
               DAL_IMD_AddDivergenceEvent(events, pair_label, origin_symbol, destination_symbol, timeframe, every, offset, i, origin_bars[i].time, IMD_DIV_LOW, origin_level_source, destination_level_source, trigger_mode, destination_lag_bars, signal_valid_bars, period_seconds, origin_bars[i], dest_bars[i], state_l, late_confirm, late_idx);
            }
         }
      }
   }

   return ArraySize(events) - before;
}

#endif
