#ifndef __EXP0018_DAYE_RENDER_CHART_RESOLVER_MQH__
#define __EXP0018_DAYE_RENDER_CHART_RESOLVER_MQH__

#include <DayeTrader/EXP0018/DAYE_RenderProjection.mqh>

bool DAYE_RenderChartMatches(const long chart_id,const string hunter_broker_symbol,
                             const ENUM_TIMEFRAMES host_timeframe,const bool require_host_timeframe)
{
   if(chart_id<0) return false;
   if(ChartSymbol(chart_id)!=hunter_broker_symbol) return false;
   if(require_host_timeframe && ChartPeriod(chart_id)!=host_timeframe) return false;
   return true;
}

int DAYE_ResolveHunterTargetCharts(const DAYE_ReferenceUseRecord &use,
                                   const DAYE_RenderConfig &config,
                                   const ENUM_TIMEFRAMES host_timeframe,
                                   long &chart_ids[])
{
   ArrayResize(chart_ids,0);
   long current=ChartID();
   if(config.target_policy==DAYE_RENDER_TARGET_CURRENT_CHART_IF_HUNTER)
   {
      if(DAYE_RenderChartMatches(current,use.hunter_broker_symbol,host_timeframe,config.require_target_chart_host_timeframe))
      {
         ArrayResize(chart_ids,1);
         chart_ids[0]=current;
      }
      return ArraySize(chart_ids);
   }

   long chart=ChartFirst();
   while(chart>=0 && ArraySize(chart_ids)<config.maximum_target_charts_per_use)
   {
      if(DAYE_RenderChartMatches(chart,use.hunter_broker_symbol,host_timeframe,config.require_target_chart_host_timeframe))
      {
         int n=ArraySize(chart_ids);
         ArrayResize(chart_ids,n+1);
         chart_ids[n]=chart;
         if(config.target_policy==DAYE_RENDER_TARGET_FIRST_OPEN_HUNTER_CHART) break;
      }
      chart=ChartNext(chart);
   }

   if(ArraySize(chart_ids)==0 && config.open_missing_hunter_chart)
   {
      ENUM_TIMEFRAMES tf=config.opened_chart_timeframe;
      if(tf==PERIOD_CURRENT) tf=host_timeframe;
      long opened=ChartOpen(use.hunter_broker_symbol,tf);
      if(opened>0)
      {
         ArrayResize(chart_ids,1);
         chart_ids[0]=opened;
      }
   }
   return ArraySize(chart_ids);
}

int DAYE_CountOpenHunterCharts(const string symbol)
{
   int count=0;
   long chart=ChartFirst();
   while(chart>=0)
   {
      if(ChartSymbol(chart)==symbol) count++;
      chart=ChartNext(chart);
   }
   return count;
}

#endif
