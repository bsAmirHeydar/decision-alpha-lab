#ifndef __DAL_IMD_SERIES_MQH__
#define __DAL_IMD_SERIES_MQH__
#property strict
#include <IntermarketDivergence/DAL_IMDTypes.mqh>

bool IMD_LoadBrokerBars(const string symbol,
                        const ENUM_TIMEFRAMES timeframe,
                        const int max_bars,
                        IMD_Bar &out_bars[])
{
   ArrayResize(out_bars, 0);
   if(max_bars <= 10) return false;
   if(!SymbolSelect(symbol, true))
      Print("IMD: SymbolSelect failed for ", symbol);

   MqlRates rates[];
   ArraySetAsSeries(rates, false);
   int copied = CopyRates(symbol, timeframe, 0, max_bars, rates);
   if(copied <= 0)
   {
      Print("IMD: CopyRates failed symbol=", symbol, " err=", GetLastError());
      return false;
   }

   ArrayResize(out_bars, copied);
   for(int i=0; i<copied; i++)
   {
      out_bars[i].time = rates[i].time;
      out_bars[i].open = rates[i].open;
      out_bars[i].high = rates[i].high;
      out_bars[i].low = rates[i].low;
      out_bars[i].close = rates[i].close;
      out_bars[i].volume = (long)rates[i].tick_volume;
   }
   return copied > 0;
}

bool IMD_LoadCsvBarsCommon(const string file_name,
                           const int max_bars,
                           IMD_Bar &out_bars[])
{
   ArrayResize(out_bars, 0);
   int handle = FileOpen(file_name, FILE_READ | FILE_CSV | FILE_COMMON | FILE_ANSI, ',');
   if(handle == INVALID_HANDLE)
   {
      Print("IMD: CSV open failed: ", file_name, " err=", GetLastError());
      return false;
   }

   // Required CSV header: time,open,high,low,close,volume
   if(!FileIsEnding(handle))
   {
      // skip header fields
      for(int h=0; h<6 && !FileIsLineEnding(handle) && !FileIsEnding(handle); h++)
         FileReadString(handle);
      while(!FileIsLineEnding(handle) && !FileIsEnding(handle)) FileReadString(handle);
   }

   int n = 0;
   while(!FileIsEnding(handle) && (max_bars <= 0 || n < max_bars))
   {
      string ts = FileReadString(handle);
      if(ts == "")
      {
         while(!FileIsLineEnding(handle) && !FileIsEnding(handle)) FileReadString(handle);
         continue;
      }
      string so = FileReadString(handle);
      string sh = FileReadString(handle);
      string sl = FileReadString(handle);
      string sc = FileReadString(handle);
      string sv = FileReadString(handle);
      while(!FileIsLineEnding(handle) && !FileIsEnding(handle)) FileReadString(handle);

      datetime t = StringToTime(ts);
      if(t <= 0) continue;

      ArrayResize(out_bars, n+1);
      out_bars[n].time = t;
      out_bars[n].open = StringToDouble(so);
      out_bars[n].high = StringToDouble(sh);
      out_bars[n].low = StringToDouble(sl);
      out_bars[n].close = StringToDouble(sc);
      out_bars[n].volume = (long)StringToInteger(sv);
      n++;
   }
   FileClose(handle);
   return n > 0;
}

int IMD_AlignByTime(const IMD_Bar &a[],
                    const IMD_Bar &b[],
                    IMD_Bar &out_a[],
                    IMD_Bar &out_b[])
{
   ArrayResize(out_a, 0);
   ArrayResize(out_b, 0);
   int ia=0, ib=0, n=0;
   int na=ArraySize(a), nb=ArraySize(b);
   while(ia<na && ib<nb)
   {
      if(a[ia].time == b[ib].time)
      {
         ArrayResize(out_a, n+1);
         ArrayResize(out_b, n+1);
         out_a[n] = a[ia];
         out_b[n] = b[ib];
         n++; ia++; ib++;
      }
      else if(a[ia].time < b[ib].time)
         ia++;
      else
         ib++;
   }
   return n;
}

#endif
