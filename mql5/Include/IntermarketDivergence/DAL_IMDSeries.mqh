#ifndef __DAL_IMD_SERIES_MQH__
#define __DAL_IMD_SERIES_MQH__

#include <IntermarketDivergence/DAL_IMDTypes.mqh>

int DAL_IMD_AlignBarsByTime(
   const DALBar &a_bars[],
   const int a_count,
   const DALBar &b_bars[],
   const int b_count,
   DAL_IMDBarPair &pairs[]
)
{
   ArrayResize(pairs, 0);
   int i = 0;
   int j = 0;
   while(i < a_count && j < b_count)
   {
      if(a_bars[i].time == b_bars[j].time)
      {
         int n = ArraySize(pairs);
         ArrayResize(pairs, n + 1);
         pairs[n].time = a_bars[i].time;
         pairs[n].a = a_bars[i];
         pairs[n].b = b_bars[j];
         i++;
         j++;
      }
      else if(a_bars[i].time < b_bars[j].time)
         i++;
      else
         j++;
   }
   return ArraySize(pairs);
}

int DAL_IMD_LoadAlignedPair(
   const string symbol_a,
   const string symbol_b,
   const ENUM_TIMEFRAMES timeframe,
   const int requested_bars,
   const bool closed_bars_only,
   DAL_IMDBarPair &pairs[]
)
{
   ArrayResize(pairs, 0);
   SymbolSelect(symbol_a, true);
   SymbolSelect(symbol_b, true);

   DALBar a_bars[];
   DALBar b_bars[];
   int a_count = DAL_LoadBarsChronological(symbol_a, timeframe, requested_bars, closed_bars_only, a_bars);
   int b_count = DAL_LoadBarsChronological(symbol_b, timeframe, requested_bars, closed_bars_only, b_bars);
   if(a_count <= 0 || b_count <= 0)
      return 0;

   return DAL_IMD_AlignBarsByTime(a_bars, a_count, b_bars, b_count, pairs);
}

void DAL_IMD_ExtractSymbolBars(const DAL_IMDBarPair &pairs[], const int pairs_count, const bool use_a, DALBar &bars[])
{
   ArrayResize(bars, pairs_count);
   for(int i=0; i<pairs_count; i++)
      bars[i] = (use_a ? pairs[i].a : pairs[i].b);
}

#endif
