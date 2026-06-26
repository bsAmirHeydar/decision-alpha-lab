#ifndef __DAL_IMD_ENGINE_MQH__
#define __DAL_IMD_ENGINE_MQH__
#property strict
#include <IntermarketDivergence/DAL_IMDTypes.mqh>
#include <IntermarketDivergence/DAL_IMDLevels.mqh>

void IMD_AppendEvent(IMD_Event &events[], const IMD_Event &e)
{
   int n = ArraySize(events);
   ArrayResize(events, n+1);
   events[n] = e;
}

void IMD_EvaluateOutcome(const IMD_Bar &bars[],
                         const int start_index,
                         const int horizon_bars,
                         const IMD_Bias bias,
                         IMD_Event &e)
{
   int n = ArraySize(bars);
   if(start_index < 0 || start_index >= n) return;
   int to = MathMin(n-1, start_index + MathMax(1, horizon_bars));
   double entry = bars[start_index].close;
   e.entry_close = entry;
   e.mfe_points = 0.0;
   e.mae_points = 0.0;
   e.return_points = 0.0;
   e.bars_to_mfe = 0;
   e.bars_to_mae = 0;

   for(int k=start_index; k<=to; k++)
   {
      double mfe=0.0, mae=0.0;
      if(bias == IMD_BIAS_BUY)
      {
         mfe = bars[k].high - entry;
         mae = entry - bars[k].low;
      }
      else if(bias == IMD_BIAS_SELL)
      {
         mfe = entry - bars[k].low;
         mae = bars[k].high - entry;
      }
      if(mfe > e.mfe_points) { e.mfe_points = mfe; e.bars_to_mfe = k - start_index; }
      if(mae > e.mae_points) { e.mae_points = mae; e.bars_to_mae = k - start_index; }
   }
   if(bias == IMD_BIAS_BUY)
      e.return_points = bars[to].close - entry;
   else if(bias == IMD_BIAS_SELL)
      e.return_points = entry - bars[to].close;
}

int IMD_DetectOriginDestination(const string pair_label,
                                const string origin_symbol,
                                const string destination_symbol,
                                const IMD_Bar &origin[],
                                const IMD_Bar &destination[],
                                const IMD_LevelFamily level_family,
                                const IMD_TriggerMode trigger_mode,
                                const int rolling_lookback,
                                const int session_start_minute,
                                const int session_end_minute,
                                const int step_every_bars,
                                const int step_offset_bars,
                                const int destination_lag_bars,
                                const int signal_valid_bars,
                                const int start_after_bars,
                                const int outcome_horizon_bars,
                                IMD_Event &events[])
{
   int added = 0;
   int n = MathMin(ArraySize(origin), ArraySize(destination));
   int first = MathMax(1, start_after_bars);
   int event_base = ArraySize(events);
   int step = MathMax(1, step_every_bars);
   int lag = MathMax(0, destination_lag_bars);

   for(int i=first; i<n-lag; i++)
   {
      if(((i - step_offset_bars) % step) != 0)
         continue;
      if(origin[i].time != destination[i].time)
         continue;

      IMD_LevelPair ol, dl;
      if(!IMD_GetLevels(origin, i, level_family, rolling_lookback, session_start_minute, session_end_minute, ol)) continue;
      if(!IMD_GetLevels(destination, i, level_family, rolling_lookback, session_start_minute, session_end_minute, dl)) continue;

      for(int side_i=0; side_i<2; side_i++)
      {
         IMD_DivergenceSide side = (side_i == 0 ? IMD_DIV_HIGH : IMD_DIV_LOW);
         double origin_level = (side == IMD_DIV_HIGH ? ol.high : ol.low);
         double dest_level = (side == IMD_DIV_HIGH ? dl.high : dl.low);
         double obp=0.0, dbp=0.0;
         if(!IMD_Triggered(origin[i], side, trigger_mode, origin_level, obp))
            continue;

         bool dest_confirmed = false;
         datetime dest_confirm_time = 0;
         double best_dest_bp = 0.0;
         for(int j=i; j<=MathMin(n-1, i+lag); j++)
         {
            double tmp=0.0;
            if(IMD_Triggered(destination[j], side, trigger_mode, dest_level, tmp))
            {
               dest_confirmed = true;
               dest_confirm_time = destination[j].time;
               best_dest_bp = tmp;
               break;
            }
         }
         if(dest_confirmed)
            continue;

         IMD_Event e;
         IMD_InitEvent(e);
         e.id = event_base + added + 1;
         e.pair_label = pair_label;
         e.origin_symbol = origin_symbol;
         e.destination_symbol = destination_symbol;
         e.bar_index = i;
         e.evaluation_time = origin[i].time;
         int valid_from_index = MathMin(n-1, i+lag);
         int valid_to_index = MathMin(n-1, valid_from_index + MathMax(1, signal_valid_bars));
         e.valid_from_time = origin[valid_from_index].time;
         e.valid_until_time = origin[valid_to_index].time;
         e.side = side;
         e.suggested_bias = IMD_DefaultBiasForSide(side);
         e.level_family = level_family;
         e.trigger_mode = trigger_mode;
         e.step_every_bars = step_every_bars;
         e.step_offset_bars = step_offset_bars;
         e.destination_lag_bars = destination_lag_bars;
         e.signal_valid_bars = signal_valid_bars;
         e.origin_ref_price = origin_level;
         e.destination_ref_price = dest_level;
         e.origin_ref_time = (side == IMD_DIV_HIGH ? ol.high_time : ol.low_time);
         e.destination_ref_time = (side == IMD_DIV_HIGH ? dl.high_time : dl.low_time);
         e.origin_ref_index = (side == IMD_DIV_HIGH ? ol.high_index : ol.low_index);
         e.destination_ref_index = (side == IMD_DIV_HIGH ? dl.high_index : dl.low_index);
         e.origin_break_points = obp;
         e.destination_break_points = best_dest_bp;
         e.divergence_gap_points = MathAbs(origin_level - dest_level);
         e.destination_late_confirmed = false;
         e.destination_confirm_time = dest_confirm_time;
         e.note = "origin took reference; destination failed inside lag";

         // Late confirmation inside validity window.
         for(int j=valid_from_index+1; j<=valid_to_index; j++)
         {
            double late_bp=0.0;
            if(IMD_Triggered(destination[j], side, trigger_mode, dest_level, late_bp))
            {
               e.destination_late_confirmed = true;
               e.destination_confirm_time = destination[j].time;
               break;
            }
         }
         IMD_EvaluateOutcome(origin, valid_from_index, outcome_horizon_bars, e.suggested_bias, e);
         IMD_AppendEvent(events, e);
         added++;
      }
   }
   return added;
}

#endif
