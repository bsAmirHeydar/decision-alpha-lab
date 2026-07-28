#ifndef __AL_UC04_MARKET_STREAM_MQH__
#define __AL_UC04_MARKET_STREAM_MQH__

#include <Market/DAL_Bars.mqh>
#include <Market/DAL_LiveBarStream.mqh>

bool AL_UC04UpdateLiveBarStream(
   const string symbol,
   const ENUM_TIMEFRAMES timeframe,
   const int requested_bars,
   DALBar &live_bars[],
   int &live_bars_count,
   datetime &last_closed_stream_bar_time,
   datetime &analysis_start_time
)
{
   int before_count = live_bars_count;

   bool appended = DAL_AppendLatestClosedBarIfNew(
      symbol,
      timeframe,
      requested_bars,
      live_bars,
      live_bars_count,
      last_closed_stream_bar_time
   );

   if(appended && analysis_start_time <= 0 && live_bars_count > before_count)
      analysis_start_time = live_bars[live_bars_count - 1].time;

   return appended;
}

#endif
