#ifndef __DAL_IMD_LEVELS_MQH__
#define __DAL_IMD_LEVELS_MQH__
#property strict
#include <IntermarketDivergence/DAL_IMDTypes.mqh>

bool IMD_InSessionMinutes(const datetime t, const int start_minute, const int end_minute)
{
   int m = IMD_MinuteOfDay(t);
   if(start_minute == end_minute) return true;
   if(start_minute < end_minute)
      return (m >= start_minute && m < end_minute);
   return (m >= start_minute || m < end_minute);
}

bool IMD_PreviousCandleLevels(const IMD_Bar &bars[], const int i, IMD_LevelPair &levels)
{
   levels.ok = false;
   if(i <= 0 || i >= ArraySize(bars)) return false;
   levels.high = bars[i-1].high;
   levels.low = bars[i-1].low;
   levels.high_time = bars[i-1].time;
   levels.low_time = bars[i-1].time;
   levels.high_index = i-1;
   levels.low_index = i-1;
   levels.source_name = "PREVIOUS_CANDLE";
   levels.ok = true;
   return true;
}

bool IMD_RollingLookbackLevels(const IMD_Bar &bars[], const int i, const int lookback, IMD_LevelPair &levels)
{
   levels.ok = false;
   if(i <= 0 || i >= ArraySize(bars)) return false;
   int from = MathMax(0, i - MathMax(1, lookback));
   int to = i - 1;
   if(to < from) return false;
   double hi = bars[from].high, lo = bars[from].low;
   int hi_i = from, lo_i = from;
   for(int k=from; k<=to; k++)
   {
      if(bars[k].high > hi) { hi = bars[k].high; hi_i = k; }
      if(bars[k].low < lo) { lo = bars[k].low; lo_i = k; }
   }
   levels.high = hi;
   levels.low = lo;
   levels.high_time = bars[hi_i].time;
   levels.low_time = bars[lo_i].time;
   levels.high_index = hi_i;
   levels.low_index = lo_i;
   levels.source_name = "ROLLING_LOOKBACK";
   levels.ok = true;
   return true;
}

bool IMD_CurrentSessionLevels(const IMD_Bar &bars[],
                              const int i,
                              const int session_start_minute,
                              const int session_end_minute,
                              IMD_LevelPair &levels)
{
   levels.ok = false;
   if(i <= 0 || i >= ArraySize(bars)) return false;
   int date_key = IMD_DateKey(bars[i].time);
   bool found = false;
   double hi = 0.0, lo = 0.0;
   int hi_i = -1, lo_i = -1;
   for(int k=i-1; k>=0; k--)
   {
      if(IMD_DateKey(bars[k].time) != date_key) break;
      if(!IMD_InSessionMinutes(bars[k].time, session_start_minute, session_end_minute)) continue;
      if(!found)
      {
         hi = bars[k].high; lo = bars[k].low; hi_i = k; lo_i = k; found = true;
      }
      else
      {
         if(bars[k].high > hi) { hi = bars[k].high; hi_i = k; }
         if(bars[k].low < lo) { lo = bars[k].low; lo_i = k; }
      }
   }
   if(!found) return false;
   levels.high = hi;
   levels.low = lo;
   levels.high_time = bars[hi_i].time;
   levels.low_time = bars[lo_i].time;
   levels.high_index = hi_i;
   levels.low_index = lo_i;
   levels.source_name = "CURRENT_SESSION";
   levels.ok = true;
   return true;
}

bool IMD_PreviousSessionLevels(const IMD_Bar &bars[],
                               const int i,
                               const int session_start_minute,
                               const int session_end_minute,
                               IMD_LevelPair &levels)
{
   levels.ok = false;
   if(i <= 0 || i >= ArraySize(bars)) return false;
   int current_date = IMD_DateKey(bars[i].time);
   int prev_date = -1;
   for(int k=i-1; k>=0; k--)
   {
      int d = IMD_DateKey(bars[k].time);
      if(d != current_date && IMD_InSessionMinutes(bars[k].time, session_start_minute, session_end_minute))
      {
         prev_date = d;
         break;
      }
   }
   if(prev_date < 0) return false;

   bool found = false;
   double hi = 0.0, lo = 0.0;
   int hi_i = -1, lo_i = -1;
   for(int k=i-1; k>=0; k--)
   {
      int d = IMD_DateKey(bars[k].time);
      if(d != prev_date)
      {
         if(found) break;
         continue;
      }
      if(!IMD_InSessionMinutes(bars[k].time, session_start_minute, session_end_minute)) continue;
      if(!found)
      {
         hi = bars[k].high; lo = bars[k].low; hi_i = k; lo_i = k; found = true;
      }
      else
      {
         if(bars[k].high > hi) { hi = bars[k].high; hi_i = k; }
         if(bars[k].low < lo) { lo = bars[k].low; lo_i = k; }
      }
   }
   if(!found) return false;
   levels.high = hi;
   levels.low = lo;
   levels.high_time = bars[hi_i].time;
   levels.low_time = bars[lo_i].time;
   levels.high_index = hi_i;
   levels.low_index = lo_i;
   levels.source_name = "PREVIOUS_SESSION";
   levels.ok = true;
   return true;
}

bool IMD_GetLevels(const IMD_Bar &bars[],
                   const int i,
                   const IMD_LevelFamily family,
                   const int rolling_lookback,
                   const int session_start_minute,
                   const int session_end_minute,
                   IMD_LevelPair &levels)
{
   if(family == IMD_LEVEL_PREVIOUS_CANDLE)
      return IMD_PreviousCandleLevels(bars, i, levels);
   if(family == IMD_LEVEL_ROLLING_LOOKBACK)
      return IMD_RollingLookbackLevels(bars, i, rolling_lookback, levels);
   if(family == IMD_LEVEL_CURRENT_SESSION)
      return IMD_CurrentSessionLevels(bars, i, session_start_minute, session_end_minute, levels);
   if(family == IMD_LEVEL_PREVIOUS_SESSION)
      return IMD_PreviousSessionLevels(bars, i, session_start_minute, session_end_minute, levels);
   return false;
}

bool IMD_Triggered(const IMD_Bar &bar,
                   const IMD_DivergenceSide side,
                   const IMD_TriggerMode mode,
                   const double level,
                   double &break_points)
{
   break_points = 0.0;
   if(side == IMD_DIV_HIGH)
   {
      if(mode == IMD_TRIGGER_WICK_TOUCH)
      {
         if(bar.high >= level) { break_points = bar.high - level; return true; }
         return false;
      }
      if(mode == IMD_TRIGGER_CLOSE_BREAK)
      {
         if(bar.close > level) { break_points = bar.close - level; return true; }
         return false;
      }
      if(mode == IMD_TRIGGER_HUNT_REJECT_CLOSE)
      {
         if(bar.high >= level && bar.close < level) { break_points = bar.high - level; return true; }
         return false;
      }
   }
   else
   {
      if(mode == IMD_TRIGGER_WICK_TOUCH)
      {
         if(bar.low <= level) { break_points = level - bar.low; return true; }
         return false;
      }
      if(mode == IMD_TRIGGER_CLOSE_BREAK)
      {
         if(bar.close < level) { break_points = level - bar.close; return true; }
         return false;
      }
      if(mode == IMD_TRIGGER_HUNT_REJECT_CLOSE)
      {
         if(bar.low <= level && bar.close > level) { break_points = level - bar.low; return true; }
         return false;
      }
   }
   return false;
}

#endif
