#ifndef __EXP0018_DAYE_SESSION_BOX_CHART_RESOLVER_MQH__
#define __EXP0018_DAYE_SESSION_BOX_CHART_RESOLVER_MQH__

#include <DayeTrader/EXP0018/DAYE_SessionBoxGeometry.mqh>

int DAYE_ResolveSessionBoxTargetCharts(const string broker_symbol,
                                       const DAYE_SessionBoxConfig &config,
                                       long &chart_ids[])
{
   ArrayResize(chart_ids,0);
   long current=ChartID();
   if(config.target_policy==DAYE_SESSION_BOX_TARGET_CURRENT_CHART_IF_SYMBOL)
   {
      if(ChartSymbol(current)==broker_symbol)
      {
         ArrayResize(chart_ids,1);
         chart_ids[0]=current;
      }
      return ArraySize(chart_ids);
   }

   long chart=ChartFirst();
   while(chart>=0 && ArraySize(chart_ids)<config.maximum_target_charts_per_symbol)
   {
      if(ChartSymbol(chart)==broker_symbol)
      {
         int n=ArraySize(chart_ids);
         ArrayResize(chart_ids,n+1);
         chart_ids[n]=chart;
         if(config.target_policy==DAYE_SESSION_BOX_TARGET_FIRST_OPEN_SYMBOL_CHART) break;
      }
      chart=ChartNext(chart);
   }

   if(ArraySize(chart_ids)==0 && config.open_missing_symbol_chart)
   {
      ENUM_TIMEFRAMES timeframe=config.opened_chart_timeframe;
      if(timeframe==PERIOD_CURRENT) timeframe=PERIOD_M15;
      long opened=ChartOpen(broker_symbol,timeframe);
      if(opened>0)
      {
         ArrayResize(chart_ids,1);
         chart_ids[0]=opened;
      }
   }
   return ArraySize(chart_ids);
}

#endif
