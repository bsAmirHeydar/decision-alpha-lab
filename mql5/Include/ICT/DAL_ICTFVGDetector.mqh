#ifndef __DAL_ICT_FVG_DETECTOR_MQH__
#define __DAL_ICT_FVG_DETECTOR_MQH__

#include <ICT/DAL_ICTTypes.mqh>

int DAL_ICT_DetectFVGs(
   const DALBar &bars[],
   const int bars_count,
   const double point,
   const double min_gap_points,
   DAL_ICTFVG &fvgs[]
)
{
   ArrayResize(fvgs, 0);
   if(bars_count < 3)
      return 0;

   double min_gap = min_gap_points * point;
   int next_id = 0;

   for(int i=2; i<bars_count; i++)
   {
      // Three-candle ICT-style imbalance, chronological bars.
      // Bullish FVG: candle[i-2].high < candle[i].low.
      if(bars[i-2].high + min_gap < bars[i].low)
      {
         int size = ArraySize(fvgs);
         ArrayResize(fvgs, size + 1);
         fvgs[size].id = next_id++;
         fvgs[size].index = i;
         fvgs[size].time = bars[i].time;
         fvgs[size].kind = ICT_FVG_BULLISH;
         fvgs[size].zone_low = bars[i-2].high;
         fvgs[size].zone_high = bars[i].low;
         fvgs[size].width = fvgs[size].zone_high - fvgs[size].zone_low;
         fvgs[size].left_index = i - 2;
         fvgs[size].middle_index = i - 1;
         fvgs[size].right_index = i;
      }

      // Bearish FVG: candle[i-2].low > candle[i].high.
      if(bars[i-2].low - min_gap > bars[i].high)
      {
         int size2 = ArraySize(fvgs);
         ArrayResize(fvgs, size2 + 1);
         fvgs[size2].id = next_id++;
         fvgs[size2].index = i;
         fvgs[size2].time = bars[i].time;
         fvgs[size2].kind = ICT_FVG_BEARISH;
         fvgs[size2].zone_low = bars[i].high;
         fvgs[size2].zone_high = bars[i-2].low;
         fvgs[size2].width = fvgs[size2].zone_high - fvgs[size2].zone_low;
         fvgs[size2].left_index = i - 2;
         fvgs[size2].middle_index = i - 1;
         fvgs[size2].right_index = i;
      }
   }

   return ArraySize(fvgs);
}

int DAL_ICT_FindPathFVG(
   const DAL_ICTFVG &fvgs[],
   const int fvgs_count,
   const DAL_ICTDirection setup_direction,
   const int from_index,
   const int to_index,
   const bool nearest_to_sweep
)
{
   int best = -1;
   for(int i=0; i<fvgs_count; i++)
   {
      if(fvgs[i].index < from_index || fvgs[i].index > to_index)
         continue;

      // High sweep -> bearish reversal: we want the bullish displacement gap that can invert bearish.
      // Low sweep -> bullish reversal: we want the bearish displacement gap that can invert bullish.
      if(setup_direction == ICT_DIR_SELL && fvgs[i].kind != ICT_FVG_BULLISH)
         continue;
      if(setup_direction == ICT_DIR_BUY && fvgs[i].kind != ICT_FVG_BEARISH)
         continue;

      if(best < 0)
      {
         best = i;
         continue;
      }

      if(nearest_to_sweep)
      {
         if(fvgs[i].index > fvgs[best].index)
            best = i;
      }
      else
      {
         if(fvgs[i].width > fvgs[best].width)
            best = i;
      }
   }
   return best;
}

bool DAL_ICT_BarTouchesFVG(
   const DALBar &bar,
   const DAL_ICTFVG &fvg,
   const DAL_ICTDirection setup_direction,
   const double min_touch_pct
)
{
   double pct = DAL_ClampDouble(min_touch_pct, 0.0, 100.0) / 100.0;
   double width = MathMax(fvg.zone_high - fvg.zone_low, 0.0);
   if(width <= 0.0)
      return false;

   if(setup_direction == ICT_DIR_SELL)
   {
      // Price should re-enter enough of a bullish FVG before it closes through the lower edge.
      double required = fvg.zone_high - width * pct;
      return (bar.low <= required && bar.high >= fvg.zone_low);
   }

   if(setup_direction == ICT_DIR_BUY)
   {
      // Price should re-enter enough of a bearish FVG before it closes through the upper edge.
      double required_buy = fvg.zone_low + width * pct;
      return (bar.high >= required_buy && bar.low <= fvg.zone_high);
   }

   return false;
}

int DAL_ICT_FindIFVGConfirmation(
   const DALBar &bars[],
   const int bars_count,
   const DAL_ICTFVG &fvg,
   const DAL_ICTDirection setup_direction,
   const int start_index,
   const int stop_exclusive_index,
   const double fvg_touch_pct,
   const double point,
   const double eps_points,
   DAL_ICTIFVGEvent &ifvg
)
{
   ifvg.id = -1;
   ifvg.index = -1;
   ifvg.time = 0;
   ifvg.fvg_id = fvg.id;
   ifvg.setup_direction = setup_direction;
   ifvg.zone_low = fvg.zone_low;
   ifvg.zone_high = fvg.zone_high;
   ifvg.inversion_close = 0.0;
   ifvg.touch_depth_pct = 0.0;

   int end = stop_exclusive_index;
   if(end <= 0 || end > bars_count)
      end = bars_count;

   double eps = eps_points * point;

   for(int i=MathMax(start_index, fvg.index + 1); i<end; i++)
   {
      if(!DAL_ICT_BarTouchesFVG(bars[i], fvg, setup_direction, fvg_touch_pct))
         continue;

      if(setup_direction == ICT_DIR_SELL)
      {
         if(bars[i].close < fvg.zone_low - eps)
         {
            double width = MathMax(fvg.zone_high - fvg.zone_low, eps);
            double depth = DAL_ClampDouble((fvg.zone_high - bars[i].low) / width * 100.0, 0.0, 100.0);
            ifvg.id = 0;
            ifvg.index = i;
            ifvg.time = bars[i].time;
            ifvg.inversion_close = bars[i].close;
            ifvg.touch_depth_pct = depth;
            return i;
         }
      }
      else if(setup_direction == ICT_DIR_BUY)
      {
         if(bars[i].close > fvg.zone_high + eps)
         {
            double width2 = MathMax(fvg.zone_high - fvg.zone_low, eps);
            double depth2 = DAL_ClampDouble((bars[i].high - fvg.zone_low) / width2 * 100.0, 0.0, 100.0);
            ifvg.id = 0;
            ifvg.index = i;
            ifvg.time = bars[i].time;
            ifvg.inversion_close = bars[i].close;
            ifvg.touch_depth_pct = depth2;
            return i;
         }
      }
   }

   return -1;
}

#endif
