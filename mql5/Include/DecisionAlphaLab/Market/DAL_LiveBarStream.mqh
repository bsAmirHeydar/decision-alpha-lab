#ifndef __DAL_LIVE_BAR_STREAM_MQH__
#define __DAL_LIVE_BAR_STREAM_MQH__

#include <DecisionAlphaLab/Market/DAL_Bars.mqh>

// Read exactly one bar by shift. This is intentionally not a bulk history copy.
// In live-stream mode the Expert appends only the newly closed bar.
bool DAL_ReadBarByShift(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int shift,
   DALBar &bar
)
{
   if(shift < 0)
      return false;

   datetime t = iTime(symbol, timeframe, shift);
   if(t <= 0)
      return false;

   bar.time = t;
   bar.open = iOpen(symbol, timeframe, shift);
   bar.high = iHigh(symbol, timeframe, shift);
   bar.low = iLow(symbol, timeframe, shift);
   bar.close = iClose(symbol, timeframe, shift);
   bar.tick_volume = (long)iVolume(symbol, timeframe, shift);
   bar.spread = 0;

   if(bar.open == 0.0 && bar.high == 0.0 && bar.low == 0.0 && bar.close == 0.0)
      return false;

   return true;
}

bool DAL_AppendBarChronological(
   DALBar &bars[],
   int &bars_count,
   const int max_bars,
   const DALBar &bar
)
{
   if(bar.time <= 0)
      return false;

   if(bars_count > 0 && bars[bars_count - 1].time == bar.time)
      return false;

   // max_bars <= 0 means unbounded stream/history.
   // This is the correct default for Strategy Tester: the test date range
   // controls the sample, not an arbitrary candle count.
   if(max_bars <= 0 || bars_count < max_bars)
   {
      ArrayResize(bars, bars_count + 1);
      bars[bars_count] = bar;
      bars_count++;
      return true;
   }

   // Optional capped rolling stream: keep chronological order and drop oldest.
   for(int i = 1; i < bars_count; i++)
      bars[i - 1] = bars[i];

   bars[bars_count - 1] = bar;
   return true;
}

int DAL_WarmupClosedBarsByShift(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int requested_bars,
   const int max_bars,
   DALBar &bars[],
   int &bars_count
)
{
   ArrayResize(bars, 0);
   bars_count = 0;

   int count = requested_bars;
   if(count <= 0)
      return 0;

   int cap = max_bars;
   if(cap <= 0)
      cap = count;

   count = MathMin(count, cap);

   // Oldest -> newest closed bars.
   for(int shift = count; shift >= 1; shift--)
   {
      DALBar bar;
      if(DAL_ReadBarByShift(symbol, timeframe, shift, bar))
         DAL_AppendBarChronological(bars, bars_count, cap, bar);
   }

   return bars_count;
}

datetime DAL_LastClosedBarTime(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe
)
{
   return iTime(symbol, timeframe, 1);
}

bool DAL_AppendLatestClosedBarIfNew(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int max_bars,
   DALBar &bars[],
   int &bars_count,
   datetime &last_closed_bar_time
)
{
   DALBar bar;
   if(!DAL_ReadBarByShift(symbol, timeframe, 1, bar))
      return false;

   if(bar.time == last_closed_bar_time)
      return false;

   bool appended = DAL_AppendBarChronological(bars, bars_count, max_bars, bar);
   if(appended)
      last_closed_bar_time = bar.time;

   return appended;
}

#endif
