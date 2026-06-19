#ifndef __DAL_BARS_MQH__
#define __DAL_BARS_MQH__

struct DALBar
{
   datetime time;
   double open;
   double high;
   double low;
   double close;
   long tick_volume;
   int spread;
};

int DAL_LoadBarsChronological(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int requested_bars,
   const bool closed_bars_only,
   DALBar &bars[]
)
{
   ArrayResize(bars, 0);

   int start_pos = closed_bars_only ? 1 : 0;
   int count = requested_bars;

   // requested_bars <= 0 means load all bars available to the terminal/tester
   // for the selected symbol/timeframe/date range. No hard 500-bar fallback.
   if(count <= 0)
   {
      int available = Bars(symbol, timeframe);
      count = available - start_pos;
   }

   if(count <= 0)
      return 0;

   MqlRates rates[];
   ArraySetAsSeries(rates, true);

   int copied = CopyRates(symbol, timeframe, start_pos, count, rates);
   if(copied <= 0)
      return 0;

   ArrayResize(bars, copied);

   // CopyRates with series=true is newest at index 0. Convert to oldest -> newest.
   for(int i = 0; i < copied; i++)
   {
      int src = copied - 1 - i;
      bars[i].time = rates[src].time;
      bars[i].open = rates[src].open;
      bars[i].high = rates[src].high;
      bars[i].low = rates[src].low;
      bars[i].close = rates[src].close;
      bars[i].tick_volume = rates[src].tick_volume;
      bars[i].spread = rates[src].spread;
   }

   return copied;
}

int DAL_PeriodSecondsSafe(const ENUM_TIMEFRAMES timeframe)
{
   int seconds = PeriodSeconds(timeframe);
   if(seconds <= 0)
      seconds = 60;
   return seconds;
}

#endif
