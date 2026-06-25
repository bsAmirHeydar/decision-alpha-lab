#ifndef __DAL_ICT_CISD_DETECTOR_MQH__
#define __DAL_ICT_CISD_DETECTOR_MQH__

#include <ICT/DAL_ICTTypes.mqh>

int DAL_ICT_FindLastLegStartIndex(
   const DALBar &bars[],
   const int bars_count,
   const int pivot_index,
   const DAL_ICTDirection setup_direction,
   const int max_lookback_bars
)
{
   if(pivot_index < 0 || pivot_index >= bars_count)
      return -1;

   int max_back = MathMax(max_lookback_bars, 1);
   int start = pivot_index;

   if(setup_direction == ICT_DIR_SELL)
   {
      // The swept high was produced by the final bullish leg. Walk back through bullish/up-close candles.
      for(int i=pivot_index; i>=0 && pivot_index - i <= max_back; i--)
      {
         bool bullish = (bars[i].close >= bars[i].open);
         bool up_close = (i <= 0 || bars[i].close >= bars[i-1].close);
         if(bullish || up_close)
            start = i;
         else
            break;
      }
      return start;
   }

   if(setup_direction == ICT_DIR_BUY)
   {
      // The swept low was produced by the final bearish leg. Walk back through bearish/down-close candles.
      for(int j=pivot_index; j>=0 && pivot_index - j <= max_back; j--)
      {
         bool bearish = (bars[j].close <= bars[j].open);
         bool down_close = (j <= 0 || bars[j].close <= bars[j-1].close);
         if(bearish || down_close)
            start = j;
         else
            break;
      }
      return start;
   }

   return -1;
}

int DAL_ICT_FindCISDConfirmation(
   const DALBar &bars[],
   const int bars_count,
   const DAL_ICTDirection setup_direction,
   const int leg_start_index,
   const int start_index,
   const int stop_exclusive_index,
   const double point,
   const double eps_points,
   DAL_ICTCISDEvent &cisd
)
{
   cisd.id = -1;
   cisd.index = -1;
   cisd.time = 0;
   cisd.setup_direction = setup_direction;
   cisd.leg_start_index = leg_start_index;
   cisd.leg_start_time = 0;
   cisd.leg_start_open = 0.0;
   cisd.confirm_close = 0.0;

   if(leg_start_index < 0 || leg_start_index >= bars_count)
      return -1;

   cisd.leg_start_time = bars[leg_start_index].time;
   cisd.leg_start_open = bars[leg_start_index].open;

   int end = stop_exclusive_index;
   if(end <= 0 || end > bars_count)
      end = bars_count;

   double eps = eps_points * point;

   for(int i=MathMax(start_index, leg_start_index + 1); i<end; i++)
   {
      if(setup_direction == ICT_DIR_SELL && bars[i].close < cisd.leg_start_open - eps)
      {
         cisd.id = 0;
         cisd.index = i;
         cisd.time = bars[i].time;
         cisd.confirm_close = bars[i].close;
         return i;
      }

      if(setup_direction == ICT_DIR_BUY && bars[i].close > cisd.leg_start_open + eps)
      {
         cisd.id = 0;
         cisd.index = i;
         cisd.time = bars[i].time;
         cisd.confirm_close = bars[i].close;
         return i;
      }
   }

   return -1;
}

#endif
